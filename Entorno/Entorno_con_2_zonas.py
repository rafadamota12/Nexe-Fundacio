# -*- coding: utf-8 -*-

# Importacion de picamera2 para caputrar fotogramas desde la Raspberry Pi
# Importacion cv2 para dibujar secciones, mostrar ventanas, etc.
# Importacion MediaPipe para detección y seguimiento de las manos
# Importacion time para poder controlar tiempo que permanece la mano en una zona
# Importacion pygame para reproduccion de audio
from picamera2 import Picamera2
import cv2, mediapipe as mp
import time
import pygame


# ---------------------- Configuración cámara ----------------------

picam2 = Picamera2() # Se crea el objeto picam2
picam2.preview_configuration.main.size = (1080, 920) # Definicion de la resolución
picam2.preview_configuration.main.format = "RGB888" # definición del formato de color
picam2.configure("preview")
picam2.start() # Inicia la cámara

# ---------------------- MediaPipe Hands ----------------------

mp_hands = mp.solutions.hands # seleccionamos el módulo hands de MediaPipe
mp_drawing = mp.solutions.drawing_utils # utilidad para dibujar puntos clave y conexiones


# ---------------------- Pygame para audio ----------------------

pygame.mixer.init() # inicialización mixer de pygame para poder cargar y reproducir audio mp3

# Clasificación de zonas según canción seleccionada
canciones = {
    # Zona A
    "A": "/home/nexe/Desktop/Nexe-Fundacio/Entorno/Audios/bobesponja.mp3",
    # Zona B
    "B": "/home/nexe/Desktop/Nexe-Fundacio/Entorno/Audios/mickey.mp3",
}

# Reproduce la canción según la zona seleccionada
def reproducir_cancion(target):
    
    ruta = canciones.get(target)
    if ruta:
        pygame.mixer.music.load(ruta) # se carga el fichero de la cancion en el reproductor
        pygame.mixer.music.play() # comienza la canción

# Comprobación si el punto se encuentra dentro de la sección del rectangulo
def punto_en_rect(x, y, rect):
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2


# ---------------------- Variables de estado ----------------------

current_target = None
enter_time = None
selected_once = {"A": False, "B": False} # si selecciona zona A, no se volverá a seleccionar hasta que salga y vuelva a entrar.


# ---------------------- Bucle principal con MediaPipe ----------------------

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    
    print("Mitad izquierda = A, mitad derecha = B. Manten la mano 2s. ESC para salir.")

    while True:
        frame_rgb = picam2.capture_array() # capturar un frame de la camara como array (imagen)
        h, w, _ = frame_rgb.shape  # h = height; w = width. Altura y anchura de la imagen, el tercer parametro es el RGB

        mid_x = w // 2

        # Define las zonas como rectángulos: A izquierda, B derecha
        ZONAS = {
            "A": (0,      0,   mid_x, h),   # mitad izquierda
            "B": (mid_x,  0,   w,     h),   # mitad derecha
        }

        results = hands.process(frame_rgb)
        hand_center_px = None # se guardan coordenadas del centro de la mano (muñeca)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame_rgb, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                wrist = hand_landmarks.landmark[0] # se selecciona landmark 0 en este caso la muñeca

                # Convierte coordenadas normalizadas (0..1) a píxeles multiplicando por ancho y alto.
                cx = int(wrist.x * w)
                cy = int(wrist.y * h)

                hand_center_px = (cx, cy)

                cv2.circle(frame_rgb, (cx, cy), 8, (0, 255, 0), -1) # dibujo del punto verde de la muñeca

        for key, rect in ZONAS.items():
            x1, y1, x2, y2 = rect

            color = (255, 0, 0) if key != current_target else (0, 255, 0) # Si la zona se activa se pone verde y sino se queda azul

            cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), color, 10) # dibujo del rectangulo
            cv2.putText(frame_rgb, key, (x1 + 10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3) # texto de la zona (A, B)

        # ---------- Lógica de dwell time ----------

        now = time.time()
        target_actual = None

        # Si se detecta la mano se comprueba en qué zona cae.
        if hand_center_px is not None:
            hx, hy = hand_center_px
            for key, rect in ZONAS.items():
                # Si la mano está dentro de la zona, la marcamos como objetivo actual.
                if punto_en_rect(hx, hy, rect):
                    target_actual = key
                    break

        # Si la mano no está en ninguna zona, reiniciamos estado.
        if target_actual is None:
            if current_target is not None:
                selected_once[current_target] = False

            current_target = None # no hay zona activa
            enter_time = None # no hay tiempo de entrada valido
        else:
            if target_actual != current_target:
                if current_target is not None:
                    selected_once[current_target] = False

                current_target = target_actual # se actualiza la zona activa
                enter_time = now # Guarda instante de entrada a la nueva zona

            # Si la mano sigue en la misma zona (target_actual == current_target).
            else:
                if enter_time is not None and not selected_once[current_target]:
                    dwell = now - enter_time # tiempo que lleva dentro de la zona

                    # Si supera 1 segundo se considera dentro
                    if dwell >= 1.0:
                        print(f"Zona {current_target} seleccionada")
                        reproducir_cancion(current_target)
                        selected_once[current_target] = True

        cv2.imshow("Deteccion de manos - Pantalla dividida", frame_rgb) # visualización

        # Lectura del teclado, si se presiona ESC sale
        if cv2.waitKey(1) & 0xFF == 27: 
            break


cv2.destroyAllWindows() # Cierra todas las ventanas
picam2.stop() # Detiene la camara
pygame.mixer.quit() # Cierra el mixer
