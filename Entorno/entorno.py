# -*- coding: utf-8 -*-
from picamera2 import Picamera2
import cv2, mediapipe as mp
import time
import pygame
from pathlib import Path

def reproducir_cancion(ruta_audio: Path):
    pygame.mixer.music.load(str(ruta_audio))
    pygame.mixer.music.play()

def punto_en_rect(x, y, rect):
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

# definición de numero de imagenes-audio que quieres ver y distribución de cada una
def grid_shape(n: int):
    mapping = {2: (1, 2), 4: (2, 2), 6: (2, 3), 8: (2, 4), 10: (2, 5), 12: (3, 4)}
    if n not in mapping:
        raise ValueError("Numero de favoritos no soportado. Soportados: 2,4,6,8,10,12.")
    return mapping[n]

def generar_zonas(w, h, n):
    rows, cols = grid_shape(n)
    cell_w = w // cols
    cell_h = h // rows

    zonas = {}
    for i in range(n):
        r, c = divmod(i, cols)
        x1 = c * cell_w
        y1 = r * cell_h
        x2 = (c + 1) * cell_w if c < cols - 1 else w
        y2 = (r + 1) * cell_h if r < rows - 1 else h
        zonas[i] = (x1, y1, x2, y2)
    return zonas

def cargar_pares(alumno_dir: Path, stems_filtrados: list[str] | None):
    dir_imagenes = alumno_dir / "Imagenes"
    dir_canciones = alumno_dir / "Audios"

    if not dir_imagenes.exists():
        raise FileNotFoundError(f"No existe la carpeta: {dir_imagenes}")
    if not dir_canciones.exists():
        raise FileNotFoundError(f"No existe la carpeta: {dir_canciones}")

    ext_img = {".jpg", ".jpeg", ".png"}
    ext_aud = {".mp3", ".wav", ".ogg"}

    imgs = {p.stem: p for p in dir_imagenes.iterdir() if p.is_file() and p.suffix.lower() in ext_img}
    auds = {p.stem: p for p in dir_canciones.iterdir() if p.is_file() and p.suffix.lower() in ext_aud}

    ids = sorted(set(imgs.keys()) & set(auds.keys()))
    if not ids:
        raise RuntimeError("No hay pares imagen+audio con el mismo nombre en Imagenes/Audios.")

    if stems_filtrados is None:
        ids_use = ids
    else:
        wanted = set(stems_filtrados)
        ids_use = [s for s in ids if s in wanted]

    if not ids_use:
        raise RuntimeError("No hay favoritos válidos (o no coinciden con nombres de archivos).")

    canciones = {}
    imagenes = {}

    for idx, stem in enumerate(ids_use):
        canciones[idx] = auds[stem]
        img = cv2.imread(str(imgs[stem]))
        if img is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen: {imgs[stem]}")
        imagenes[idx] = img

    return canciones, imagenes, len(ids_use)

def main(alumno_dir: Path, screen_w: int | None = None, screen_h: int | None = None, stems_favoritos: list[str] | None = None):
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1080, 920)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.configure("preview")
    picam2.start()

    mp_hands = mp.solutions.hands
    pygame.mixer.init()

    canciones, imagenes, N = cargar_pares(alumno_dir, stems_favoritos)

    current_target = None
    enter_time = None
    selected_once = {k: False for k in range(N)}

    WINDOW = "UI"
    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(WINDOW, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    try:
        with mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6) as hands:
            while True:
                frame_rgb = picam2.capture_array()
                h, w, _ = frame_rgb.shape

                ZONAS = generar_zonas(w, h, N)

                results = hands.process(frame_rgb)
                hand_center_px = None
                if results.multi_hand_landmarks:
                    wrist = results.multi_hand_landmarks[0].landmark[0]
                    hand_center_px = (int(wrist.x * w), int(wrist.y * h))


                for key, (x1, y1, x2, y2) in ZONAS.items():
                    zone_w, zone_h = (x2 - x1), (y2 - y1)
                    src_rs = cv2.resize(imagenes[key], (zone_w, zone_h), interpolation=cv2.INTER_AREA)
                    frame_rgb[y1:y2, x1:x2] = src_rs

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
                            # no reiniciar música mientras está sonando
                            if (now - enter_time) >= 1.0 and not pygame.mixer.music.get_busy():
                                reproducir_cancion(canciones[current_target])
                                selected_once[current_target] = True

                for key, (x1, y1, x2, y2) in ZONAS.items():
                    color = (0, 0, 0) if key != current_target else (0, 255, 0)
                    cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), color, 20)

                if hand_center_px is not None:
                    cv2.circle(frame_rgb, hand_center_px, 20, (0, 255, 0), -1)

                if screen_w and screen_h:
                    ui_show = cv2.resize(frame_rgb, (screen_w - 50, screen_h - 50), interpolation=cv2.INTER_AREA)
                else:
                    ui_show = frame_rgb

                cv2.imshow(WINDOW, ui_show)

                if cv2.waitKey(1) & 0xFF == 27:
                    break
    finally:
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        if picam2 is not None:
            try:
                picam2.stop()
            except Exception:
                pass
            try:
                picam2.close()
            except Exception:
                pass
        pygame.mixer.quit()
