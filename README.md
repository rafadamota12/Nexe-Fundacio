# Entorno interactivo para Nexe Fundació

**Diseño e implementación de un entorno recreativo interactivo orientado a niños con múltiples discapacidades**

## 📖 Descripción

Este proyecto consiste en una aplicación interactiva que facilita actividades recreativas para niños con discapacidades múltiples, fomentando su desarrollo mediante tecnología accesible.

## 🔧 Estrucutra del proyecto
├── Nexe Entorno.desktop        # Acceso directo
├── Entorno/                    # Código fuente
├── Tests/                      # Modelos de prueba
└── README.md

## 🚀 Instalación y Uso

Requisitos previos:

  - Raspberry Pi 5
  - Cámara AI
  - Conexión a Internet

**1- Verificación/Instalación de Git:**

  Abrir un terminal y ejecutar:
  
  sudo apt update
  sudo apt install git -y
  git --version

  Una vez se ve la versión de Git se puede seguir.

**2- Clonar repositorio:**

  git clone https://github.com/rafadamota12/Nexe-Fundacio.git
  cd Nexe-Fundacio

**3- Instalación dependencias:**

  En el terminal, ejecutar:
  
  sudo apt install python3-opencv -y
  python3 -m pip install --break-system-packages mediapipe

**4- Ejecutar la aplicación**

    1. Ve a la carpeta Nexe-Fundacio/
    2. Haz doble clic en Nexe Entorno.desktop
    3. ¡La aplicación se iniciará automáticamente!


## 💻 Tecnologías

- OpenCV para procesamiento de imágenes
- Raspberry Pi y librerías específicas para hardware
- MediaPipe Hands

**Proyecto Final de Grado (TFG) - Rafael Da Mota**




