from picamera2 import Picamera2
import cv2, mediapipe as mp
import time
import pygame

# ---------- Configurar camara ----------
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1080, 920)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

# ---------- MediaPipe Hands ----------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# ---------- Pygame para audio ----------
pygame.mixer.init()

canciones = {
    "A": "/home/nexe/Desktop/GestureControl/Canciones/ytmp3.gg - Bob Esponja Intro (Español de España) - Javier Salinas.mp3",
    "B": "/home/nexe/Desktop/GestureControl/Canciones/ytmp3.gg - Canta la canción de Calliou - Pitiflutv.mp3",
}

def reproducir_cancion(target):
    ruta = canciones.get(target)
    if ruta:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play()

def punto_en_rect(x, y, rect):
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

# ---------- Estado para dwell time ----------
current_target = None
enter_time = None
selected_once = {"A": False, "B": False}

with mp_hands.Hands(min_detection_confidence=0.7,
                    min_tracking_confidence=0.7) as hands:
    print("Mitad izquierda = A, mitad derecha = B. Manten la mano 2s. ESC para salir.")
    while True:
        frame_rgb = picam2.capture_array()
        h, w, _ = frame_rgb.shape  # aqui w=720, h=480

        # --------- definir las dos mitades ----------
        mid_x = w // 2
        ZONAS = {
            "A": (0,      0,   mid_x, h),   # mitad izquierda
            "B": (mid_x,  0,   w,     h),   # mitad derecha
        }

        # Procesar con MediaPipe
        results = hands.process(frame_rgb)
        hand_center_px = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame_rgb, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                wrist = hand_landmarks.landmark[0]
                cx = int(wrist.x * w)
                cy = int(wrist.y * h)
                hand_center_px = (cx, cy)
                cv2.circle(frame_rgb, (cx, cy), 8, (0, 255, 0), -1)

        # Dibujar las dos secciones
        for key, rect in ZONAS.items():
            x1, y1, x2, y2 = rect
            color = (255, 0, 0) if key != current_target else (0, 255, 255)
            cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame_rgb, key, (x1 + 10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)

        # ---------- Logica de dwell time ----------
        now = time.time()
        target_actual = None

        if hand_center_px is not None:
            hx, hy = hand_center_px
            for key, rect in ZONAS.items():
                if punto_en_rect(hx, hy, rect):
                    target_actual = key
                    break

        if target_actual is None:
            if current_target is not None:
                selected_once[current_target] = False
            current_target = None
            enter_time = None
        else:
            if target_actual != current_target:
                if current_target is not None:
                    selected_once[current_target] = False
                current_target = target_actual
                enter_time = now
            else:
                if enter_time is not None and not selected_once[current_target]:
                    dwell = now - enter_time
                    if dwell >= 1.0:
                        print(f"Zona {current_target} seleccionada")
                        reproducir_cancion(current_target)
                        selected_once[current_target] = True

        cv2.imshow("Deteccion de manos - Pantalla dividida", frame_rgb)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cv2.destroyAllWindows()
picam2.stop()
pygame.mixer.quit()
