# -*- coding: utf-8 -*-

# Importacion de picamera2 para caputrar fotogramas desde la Raspberry Pi
# Importacion cv2 para dibujar secciones, mostrar ventanas, etc.
# Importacion MediaPipe para detección y seguimiento de las manos
# Importacion time para poder controlar tiempo que permanece la mano en una zona
# Importacion pygame para reproduccion de audio
# Importacion path para poder recorrer rutas de forma segura
# Importacion random para la asignación aleatoria de multimedia
from picamera2 import Picamera2
import cv2, mediapipe as mp
import time
import pygame
from pathlib import Path
import random

# Carpetas
DIR_CANCIONES = Path("/home/nexe/Desktop/Nexe-Fundacio/Entorno/Audios") 
DIR_IMAGENES = Path("/home/nexe/Desktop/Nexe-Fundacio/Entorno/Imagenes")

# Configuración de la camara
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1080, 920)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

# MediaPipe Hands
mp_hands = mp.solutions.hands

# Pygame para audio
pygame.mixer.init()

def reproducir_cancion(ruta_audio: Path):
    pygame.mixer.music.load(str(ruta_audio))
    pygame.mixer.music.play()

def punto_en_rect(x, y, rect):
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

# Cargar imagen+audio por nombre base
ext_img = {".jpg", ".jpeg", ".png"}
ext_aud = {".mp3", ".wav", ".ogg"}

imgs = {p.stem: p for p in DIR_IMAGENES.iterdir() if p.is_file() and p.suffix.lower() in ext_img}
auds = {p.stem: p for p in DIR_CANCIONES.iterdir() if p.is_file() and p.suffix.lower() in ext_aud}

ids = sorted(set(imgs.keys()) & set(auds.keys()))
# Control de numero de pares que hay 
if len(ids) < 6:
    faltan_imgs = sorted(set(auds.keys()) - set(imgs.keys()))
    faltan_auds = sorted(set(imgs.keys()) - set(auds.keys()))
    raise RuntimeError(
        f"Necesitas al menos 6 pares imagen+audio con el mismo nombre.\n"
        f"Pares encontrados: {len(ids)}\n"
        f"Sin imagen (hay audio pero no imagen): {faltan_imgs[:10]}\n"
        f"Sin audio (hay imagen pero no audio): {faltan_auds[:10]}"
    )

elegidos = random.sample(ids, 6)  # 6 distintos

zonas = ["A", "B", "C", "D", "E", "F"]
canciones = {}   # zona -> Path audio
imagenes = {}    # zona -> imagen BGR (cv2)

for zona, stem in zip(zonas, elegidos):
    canciones[zona] = auds[stem]
    img = cv2.imread(str(imgs[stem]))
    if img is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {imgs[stem]}")
    imagenes[zona] = img

print("Asignación aleatoria (zona -> nombre):")
for zona, stem in zip(zonas, elegidos):
    print(f"  {zona} -> {stem}")

# ---------- Estado dwell time ----------
current_target = None
enter_time = None
selected_once = {k: False for k in zonas}

WINDOW = "UI (sin camara)"
cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW, 1080, 920)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    print("Rejilla 2x3: A B C arriba / D E F abajo. Mantén 1s. ESC para salir.")
    while True:
        frame_rgb = picam2.capture_array()
        h, w, _ = frame_rgb.shape

        # definicion rejilla 2x3
        cell_w = w // 3
        cell_h = h // 2

        ZONAS = {
            "A": (0 * cell_w, 0 * cell_h, 1 * cell_w, 1 * cell_h),
            "B": (1 * cell_w, 0 * cell_h, 2 * cell_w, 1 * cell_h),
            "C": (2 * cell_w, 0 * cell_h, 3 * cell_w, 1 * cell_h),
            "D": (0 * cell_w, 1 * cell_h, 1 * cell_w, 2 * cell_h),
            "E": (1 * cell_w, 1 * cell_h, 2 * cell_w, 2 * cell_h),
            "F": (2 * cell_w, 1 * cell_h, 3 * cell_w, 2 * cell_h),
        }

        results = hands.process(frame_rgb)
        hand_center_px = None

        if results.multi_hand_landmarks:
            wrist = results.multi_hand_landmarks[0].landmark[0]
            cx = int(wrist.x * w)
            cy = int(wrist.y * h)
            hand_center_px = (cx, cy)

        # Pegar imagen en cada zona usando ROI
        for key, (x1, y1, x2, y2) in ZONAS.items():
            zone_w, zone_h = (x2 - x1), (y2 - y1)
            src = imagenes[key]
            src_rs = cv2.resize(src, (zone_w, zone_h), interpolation=cv2.INTER_AREA)
            frame_rgb[y1:y2, x1:x2] = src_rs

        # --- Logica dwell time ---
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
                        reproducir_cancion(canciones[current_target])
                        selected_once[current_target] = True

        # Dibujar líneas de secciones 
        for key, (x1, y1, x2, y2) in ZONAS.items():
            color = (0, 0, 0) if key != current_target else (0, 255, 0)
            cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), color, 3)

        # Cursor donde está la mano
        if hand_center_px is not None:
            cv2.circle(frame_rgb, hand_center_px, 10, (0, 255, 0), -1)

        cv2.imshow(WINDOW, frame_rgb)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cv2.destroyAllWindows()
picam2.stop()
pygame.mixer.quit()
