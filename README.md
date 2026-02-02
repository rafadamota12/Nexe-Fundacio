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
  ```bash
  sudo apt update
  sudo apt install git -y
  git --version
  ```
  Una vez se ve la versión de Git se puede seguir.

**2- Clonar repositorio:**
```bash
git clone https://github.com/rafadamota12/Nexe-Fundacio.git
cd Nexe-Fundacio
```
**3- Instalación dependencias:**

  En el terminal, ejecutar:
  ```bash
  sudo apt install python3 python3-pip
  sudo apt install python3-opencv -y
  python3 -m pip install --break-system-packages mediapipe
  ```
## ▶️ Uso de la aplicación

    1. Ve a la carpeta Nexe-Fundacio/
    2. Haz doble clic en Nexe Entorno.desktop
    3. ¡La aplicación se iniciará automáticamente!

Una vez iniciado:
  -  La cámara detectará las manos.
  -  Los gestos permitirán interactuar con el entorno.
  -  Se mostrarán los elementos visuales en pantalla.

## 📂 Estructura del proyecto
```bash
Nexe-Fundacio/
│
├── Entorno/        # Código principal del entorno
├── Tests/          # Pruebas
├── main.py         # Archivo principal
└── README.md
```

## 💻 Tecnologías utilizadas

-  Python
-  OpenCV
-  MediaPipe Hands
-  Raspberry Pi OS

## 📷 Capturas
![Interfaz principal](Screenshots/demoentorno.png)
![Interfaz principal](Screenshots/demoentorno1.png)

## 🧑‍🎓 AUTOR
**Proyecto Final de Grado (TFG) - Rafael Da Mota**

---
# 🎮 Interactive Environment for Nexe Foundation

Final Degree Project (TFG) focused on the design and development of an **accessible interactive recreational environment for children with multiple disabilities**, using computer vision and low-cost hardware.

The system allows interaction through camera-based gesture recognition, offering adapted playful activities that promote stimulation and learning.

---

## 📌 Index

- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Screenshots](#screenshots)
- [Author](#author)

---

## 📖 Description

This project develops an interactive environment that allows children with multiple disabilities to interact with different activities through gestures, without the need for complex physical devices.

It is designed to run on a **Raspberry Pi 5** with a camera, making the system accessible, portable, and low-cost.

---

## ✨ Features

- Hand detection using computer vision.
- Real-time interaction.
- Simple and visual interface.
- Designed to be extendable with new games or activities.
- Compatible with Raspberry Pi.

---

## ⚙️ Requirements

### Hardware
- Raspberry Pi 5  
- Raspberry-compatible camera  

### Software
- Python 3.9 or higher  
- OpenCV  
- MediaPipe  
- Git  

---

## 🛠️ Installation

**1- Verify/Install Git:**

Open a terminal and run:

```bash
sudo apt update
sudo apt install git -y
git --version
```

**2- Clone repository:**
```bash
git clone https://github.com/rafadamota12/Nexe-Fundacio.git
cd Nexe-Fundacio
```

**3- Install dependencies:**
In the terminal, run:
```bash
sudo apt install python3 python3-pip
sudo apt install python3-opencv -y
python3 -m pip install --break-system-packages mediapipe
```

## ▶️ Application Usage
    1. Go to the Nexe-Fundacio/ folder
    2. Double-click on Nexe Entorno.desktop
    3. The application will start automatically!
Once started:
  -  The camera will detect hands.
  -  Gestures will allow interaction with the environment.
  -  Visual elements will be displayed on screen.

## 📂 Project Structure
```bash
Nexe-Fundacio/
│
├── Entorno/        # Main environment code
├── Tests/          # Tests
├── main.py         # Main file
└── README.md
```

## 💻 Technologies Used

-  Python
-  OpenCV
-  MediaPipe Hands
-  Raspberry Pi OS

## 📷 Screenshots

(Add screenshots or GIFs of the application running)

## 🧑‍🎓 AUTHOR

**Final Degree Project (TFG) – Rafael Da Mota**
