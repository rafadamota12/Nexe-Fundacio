# Nexe-Fundació

**Diseño e implementación de un entorno recreativo interactivo orientado a niños con múltiples discapacidades**

---
## 🐍 Instalación de Python 3.11 y entorno virtual

Este proyecto requiere Python 3.11 para asegurar compatibilidad con TensorFlow y otras librerías.

### Pasos para instalar Python 3.11 en Linux:

- sudo apt update
- sudo apt install wget build-essential libssl-dev zlib1g-dev libncurses-dev libreadline-dev libffi-dev libsqlite3-dev
- wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
- tar -xf Python-3.11.0.tgz
- cd Python-3.11.0
- ./configure --enable-optimizations
- make -j$(nproc)
- sudo make altinstall


### Crear entorno virtual con Python 3.11

- python3 -m venv --system-site-packages .NexeEnv311
- source .NexeEnv311/bin/activate
- pip install -r requirements.txt


Esto garantiza que las dependencias se instalen en un ambiente controlado con la versión apropiada de Python.


---

## 📖 Descripción

Este proyecto consiste en una aplicación interactiva que facilita actividades recreativas para niños con discapacidades múltiples, fomentando su desarrollo mediante tecnología accesible.

---

## 🚀 Uso

Explica aquí brevemente cómo ejecutar o iniciar el proyecto tras la instalación.

---

## 💻 Tecnologías

- TensorFlow y Keras para Machine Learning
- OpenCV para procesamiento de imágenes
- Raspberry Pi y librerías específicas para hardware




