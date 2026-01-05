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

def punto_en_rect(x, y, rect):
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

# ---------- Videos (solo imagen) ----------
pathA = "/home/nexe/Desktop/Nexe-Fundacio/Entorno/Videos/ytmp3.gg - Bob Esponja Intro (Español de España) - Javier Salinas (720p, h264).mp4"
pathB = "/home/nexe/Desktop/Nexe-Fundacio/Entorno/Videos/ytmp3.gg - Disney Junior España ｜ La Casa de Mickey Mouse ｜ Cabecera oficial de La casa de Mickey Mouse - Disney Junior España (720p, h264).mp4"

capA = cv2.VideoCapture(pathA)
capB = cv2.VideoCapture(pathB)

if not capA.isOpened() or not capB.isOpened():
    raise OSError("OpenCV no pudo abrir uno de los MP4. Prueba a re-encodear con ffmpeg o usa GStreamer.")

# ---------- Audios (extraídos del mp4) ----------
pygame.mixer.init()
audio_files = {
    "A": "/home/nexe/Desktop/Nexe-Fundacio/Entorno/Canciones/ytmp3.gg-Bob-Esponja-Intro-_Español-de-España_-Javier-Salinas-_720p_-h264_.mp3",
    "B": "/home/nexe/Desktop/Nexe-Fundacio/Entorno/Canciones/ytmp3.mp3",
}

audio_current = None      # "A" / "B" / None
audio_loaded = None       # cuál está cargado ahora en pygame
audio_paused = False

def audio_switch_to(target):
    """Cambia el audio al target y lo pone a sonar desde el principio."""
    global audio_current, audio_loaded, audio_paused
    if target is None:
        return
    if audio_current == target and pygame.mixer.music.get_busy():
        return
    pygame.mixer.music.stop()  # para el que haya [web:101]
    pygame.mixer.music.load(audio_files[target])  # carga audio [web:101]
    pygame.mixer.music.play(-1)  # loop mientras estés en la zona
    audio_current = target
    audio_loaded = target
    audio_paused = False

def audio_pause_if_playing():
    global audio_paused
    if pygame.mixer.music.get_busy() and not audio_paused:
        pygame.mixer.music.pause()  # pausa [web:101]
        audio_paused = True

def audio_unpause_if_needed():
    global audio_paused
    if audio_paused:
        pygame.mixer.music.unpause()  # reanuda [web:101]
        audio_paused = False

# ---------- UI ----------
WINDOW = "UI (sin camara)"
cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW, 1080, 920)

# ---------- Último frame mostrado (para pausar/congelar) ----------
lastA = None
lastB = None

# Precargar 1 frame
retA, tmpA = capA.read()
if retA and tmpA is not None:
    lastA = tmpA
else:
    capA.set(cv2.CAP_PROP_POS_FRAMES, 0)

retB, tmpB = capB.read()
if retB and tmpB is not None:
    lastB = tmpB
else:
    capB.set(cv2.CAP_PROP_POS_FRAMES, 0)

# ---------- Estado dwell time (lo dejo por si lo quieres usar después) ----------
current_target = None
enter_time = None
selected_once = {"A": False, "B": False}

with mp_hands.Hands(min_detection_confidence=0.7,
                    min_tracking_confidence=0.7) as hands:
    print("Mitad izquierda = A, mitad derecha = B. ESC para salir.")
    while True:
        frame_rgb = picam2.capture_array()
        h, w, _ = frame_rgb.shape

        mid_x = w // 2
        ZONAS = {
            "A": (0,     0, mid_x, h),
            "B": (mid_x, 0, w,     h),
        }

        # --- Detección ---
        results = hands.process(frame_rgb)
        hand_center_px = None

        if results.multi_hand_landmarks:
            wrist = results.multi_hand_landmarks[0].landmark[0]
            cx = int(wrist.x * w)
            cy = int(wrist.y * h)
            hand_center_px = (cx, cy)

        # --- Zona actual ---
        target_actual = None
        if hand_center_px is not None:
            hx, hy = hand_center_px
            for key, rect in ZONAS.items():
                if punto_en_rect(hx, hy, rect):
                    target_actual = key
                    break

        # --- Video: solo avanza el de la zona activa ---
        if target_actual == "A":
            retA, frameA = capA.read()
            if not retA or frameA is None:
                capA.set(cv2.CAP_PROP_POS_FRAMES, 0)
                retA, frameA = capA.read()
            if retA and frameA is not None:
                lastA = frameA

        elif target_actual == "B":
            retB, frameB = capB.read()
            if not retB or frameB is None:
                capB.set(cv2.CAP_PROP_POS_FRAMES, 0)
                retB, frameB = capB.read()
            if retB and frameB is not None:
                lastB = frameB

        # --- Audio: suena solo en la zona activa ---
        if target_actual in ("A", "B"):
            if audio_current != target_actual:
                audio_switch_to(target_actual)
            else:
                audio_unpause_if_needed()
        else:
            audio_pause_if_playing()

        # --- UI frame ---
        ui_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        ui_frame[:] = (15, 15, 15)

        for key, (x1, y1, x2, y2) in ZONAS.items():
            zone_w, zone_h = (x2 - x1), (y2 - y1)
            src = lastA if key == "A" else lastB
            if src is None:
                continue
            src_rs = cv2.resize(src, (zone_w, zone_h), interpolation=cv2.INTER_AREA)
            ui_frame[y1:y2, x1:x2] = src_rs

        # --- Líneas de secciones ---
        for key, (x1, y1, x2, y2) in ZONAS.items():
            color = (0, 255, 0) if key == target_actual else (0, 0, 0)
            cv2.rectangle(ui_frame, (x1, y1), (x2, y2), color, 3)

        if hand_center_px is not None:
            cv2.circle(ui_frame, hand_center_px, 10, (0, 255, 0), -1)

        cv2.imshow(WINDOW, ui_frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cv2.destroyAllWindows()
picam2.stop()
capA.release()
capB.release()
pygame.mixer.music.stop()
pygame.mixer.quit()
