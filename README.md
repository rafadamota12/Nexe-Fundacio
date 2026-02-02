# 🎮 Entorno Interactivo para Nexe Fundació

Proyecto Final de Grado (TFG) orientado al diseño y desarrollo de un **entorno interactivo recreativo accesible para niños con múltiples discapacidades**, utilizando visión por computador y hardware de bajo coste.

El sistema permite la interacción a través de gestos captados por cámara, ofreciendo actividades lúdicas adaptadas que fomentan la estimulación y el aprendizaje.

---
## 📌 Índice

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Capturas](#capturas)
- [Autor](#autor)

---


## 📖 Descripción

Este proyecto desarrolla un entorno interactivo que permite a niños con múltiples discapacidades interactuar con diferentes actividades mediante gestos, sin necesidad de dispositivos físicos complejos.

Está diseñado para ejecutarse en una **Raspberry Pi 5** con cámara, haciendo el sistema accesible, portátil y de bajo coste.

---

## Características

- Detección de manos mediante visión artificial.
- Interacción en tiempo real.
- Interfaz sencilla y visual.
- Pensado para ser ampliable con nuevos juegos o actividades.
- Compatible con Raspberry Pi.

---

## ⚙️ Requisitos

### Hardware
- Raspberry Pi 5  
- Cámara compatible con Raspberry  

### Software
- Python 3.9 o superior  
- OpenCV  
- MediaPipe  
- Git  

---

## 🛠️ Instalación

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
    
    sudo apt install python3 python3-pip
    sudo apt install python3-opencv -y
    python3 -m pip install --break-system-packages mediapipe

## ▶️ Uso de la aplicación

    1. Ve a la carpeta Nexe-Fundacio/
    2. Haz doble clic en Nexe Entorno.desktop
    3. ¡La aplicación se iniciará automáticamente!

Una vez iniciado:
  -  La cámara detectará las manos.
  -  Los gestos permitirán interactuar con el entorno.
  -  Se mostrarán los elementos visuales en pantalla.

## 📂 Estructura del proyecto
Nexe-Fundacio/
│
├── Entorno/        # Código principal del entorno
├── Tests/          # Pruebas
├── main.py         # Archivo principal
└── README.md


## 💻 Tecnologías utilizadas

Python

OpenCV

MediaPipe

Raspberry Pi OS

## 📷 Capturas

## 🧑‍🎓 AUTOR
**Proyecto Final de Grado (TFG) - Rafael Da Mota**




