from picamera2 import Picamera2
import cv2, mediapipe as mp

picam2 = Picamera2()
picam2.preview_configuration.main.size = (720,480) #Configurar el tamaño de la preview de la camara 
picam2.preview_configuration.main.format = "RGB888" #Configurar el formato de color de la preview
picam2.configure("preview") #Aplica las configraciones de preview a la camara
picam2.start() #Inicia la camara

mp_hands = mp.solutions.hands #Modulo de manos de mediapipe
mp_drawing = mp.solutions.drawing_utils #Utilidades de dibujo de MediaPipe, que se utiliza para dibujar los landmarks (puntos de ref.) de las manos.
 
# Inicializa el modelo de manos de MediaPipe con un umbral de confianza para la deteccion y el seguimiento de 0.7 (70%). El bloque with asegura que los recursos se liberen al salir.
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands: 
    while True:
        # Capturar frame en RGB
        frame_rgb = picam2.capture_array()
        
        # Procesar con MediaPipe (RGB)c
        results = hands.process(frame_rgb)
        
        # Dibujar landmarks (puntos de ref.) en el frame RGB
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame_rgb, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Convertir a BGR solo para mostrar
        # frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR) [NO ES MUY IMPORTANTE PONER ESTA LINEA YA QUE EN LA LINEA 6 YA ELIGES QUE FORMATO DE COLOR QUIERES]
        cv2.imshow("Deteccion de manos", frame_rgb)
        
        if cv2.waitKey(1) & 0xFF == 27: # Si se hace click de ESC o Ctrl+C sale del bucle
            break

cv2.destroyAllWindows() # Cierra todas las ventanas de OpenCV
picam2.stop() # Para la camarasss
