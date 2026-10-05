# AccessAI — detección urbana

AccessAI es un prototipo de Streamlit que utiliza YOLO26s para detectar elementos relacionados con la accesibilidad urbana en imágenes y vídeos. Está diseñado para ejecutar inferencias en una GPU NVIDIA compatible con CUDA.

Clases del modelo:

- `Obstaculo_Dinamico`
- `Obstaculo_Fijo`
- `Barrera_Arquitectonica`
- `Infraestructura_Peatonal`

## Requisitos e instalación

- Python 3.10 o posterior.
- GPU NVIDIA y PyTorch instalado con soporte CUDA compatible con el equipo.
- Un checkpoint entrenado de AccessAI (`best.pt`).

En el entorno virtual del proyecto, instala las dependencias de la aplicación:

```bash
pip install streamlit ultralytics opencv-python
```

Instala PyTorch siguiendo las instrucciones oficiales correspondientes a la versión de CUDA del equipo. La aplicación se detiene si PyTorch no detecta CUDA; no utiliza CPU automáticamente.

## Modelo

La aplicación busca automáticamente el checkpoint más reciente que coincida con esta ruta, relativa a la raíz del proyecto:

```text
*/weights/best.pt
```

Si no encuentra un modelo, se puede seleccionar manualmente un archivo `best.pt` en la interfaz. La aplicación lo guarda como `best_uploaded.pt` en la raíz del proyecto.

## Ejecución

Desde la raíz del proyecto, activa el entorno virtual y ejecuta:

```bash
streamlit run app/streamlit_app.py
```

Abre la URL local que muestre Streamlit. Usa la barra lateral para ajustar la confianza mínima y el tamaño de imagen. Las pestañas permiten procesar imágenes y vídeos y consultar información del proyecto. Las salidas de vídeo se guardan en `runs/detect/AccessAI_Streamlit_video/`.

## Plan de trabajo

1. **Preparar el entorno:** instalar dependencias y comprobar que `torch.cuda.is_available()` devuelve `True`.
2. **Validar el modelo:** colocar el checkpoint en la ruta esperada o seleccionarlo en la interfaz.
3. **Verificar imágenes:** probar distintas imágenes, umbrales y tamaños; revisar anotaciones y recuentos por clase.
4. **Verificar vídeos:** comprobar los frames procesados, el resumen de detecciones y la reproducción/descarga del vídeo resultante.
5. **Evaluar y mejorar:** documentar errores y tiempos, priorizar mejoras y volver a probar ambos flujos tras cada cambio.

## Guía para agentes

- Conserva el idioma principal en español y la coherencia con las cuatro clases del modelo.
- Respeta el requisito de GPU: comunica claramente la falta de CUDA y no añadas un fallback silencioso a CPU.
- Al cambiar rutas, checkpoint o inferencia, considera tanto la carga manual como la automática y prueba los flujos de imagen y vídeo.
- No añadas checkpoints, vídeos ni otros archivos de gran tamaño al repositorio; documenta dónde deben colocarse.
- Mantén este README actualizado cuando cambien los requisitos o los comandos de ejecución.

## Estructura relevante

```text
proyecto2/
├── app/
│   ├── README.md
│   └── streamlit_app.py
└── runs/
	└── detect/<entrenamiento>/weights/best.pt
```
****


---
## app multiplataforma
Para convertir el proyecto actual de **Streamlit** en una **app multiplataforma**, la arquitectura recomendada es separar la interfaz Flutter de la IA en Python:

```text
Flutter
   │
   │ HTTP / REST
   ▼
Python + FastAPI
   │
   ▼
YOLO26s + PyTorch CUDA
   │
   ▼
NVIDIA RTX 4060
```

La parte **Flutter** será la aplicación para **Web, Android/iOS y escritorio**, mientras que **Python** seguirá encargándose de YOLO26s, OpenCV, PyTorch y el procesamiento de imágenes/vídeos.

### README actualizado

# AccessAI — Detección urbana multiplataforma

AccessAI es un prototipo de inteligencia artificial para detectar elementos relacionados con la accesibilidad urbana en imágenes y vídeos.

La aplicación utiliza:

* **Flutter** para la interfaz multiplataforma.
* **Python + FastAPI** para el backend.
* **YOLO26s** para detección de objetos.
* **PyTorch** para ejecución de la inferencia.
* **CUDA + NVIDIA GPU** para acelerar la inferencia.
* **OpenCV** para procesamiento de imágenes y vídeos.

La aplicación está diseñada para funcionar desde una misma base de código Flutter en:

* Web
* Android
* iOS
* Windows
* Linux
* macOS

El backend Python se ejecuta localmente o en un servidor y proporciona una API REST que recibe imágenes y vídeos y devuelve los resultados de YOLO26s.

---

## Clases del modelo

El modelo AccessAI utiliza exactamente cuatro clases:

| ID | Clase                      |
| -: | -------------------------- |
|  0 | `Obstaculo_Dinamico`       |
|  1 | `Obstaculo_Fijo`           |
|  2 | `Barrera_Arquitectonica`   |
|  3 | `Infraestructura_Peatonal` |

---

# Arquitectura de la aplicación

```text
                 ACCESSAI
                    │
                    ▼
        ┌───────────────────────┐
        │        FLUTTER        │
        │                       │
        │  Web                  │
        │  Android              │
        │  iOS                  │
        │  Windows              │
        │  Linux                │
        │  macOS                │
        └───────────┬───────────┘
                    │
                    │ HTTP / REST API
                    ▼
        ┌───────────────────────┐
        │    PYTHON + FASTAPI   │
        │                       │
        │  Recepción archivos   │
        │  Inferencia YOLO26s   │
        │  OpenCV               │
        │  PyTorch              │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │      NVIDIA CUDA      │
        │                       │
        │ RTX 4060 Laptop GPU   │
        │        8 GB VRAM      │
        └───────────────────────┘
```

---

# Requisitos

## Backend

Se necesita:

* Python 3.10 o posterior.
* PyTorch con soporte CUDA compatible con el equipo.
* GPU NVIDIA compatible con CUDA.
* Ultralytics.
* YOLO26s.
* OpenCV.
* FastAPI.
* Uvicorn.

El backend **no utiliza CPU automáticamente**.

Cuando PyTorch no detecta CUDA, la aplicación debe mostrar claramente el error y detener la inferencia.

Comprobación:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Debe devolver:

```text
True
```

También se puede comprobar la GPU:

```bash
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

---

# Flutter

Instalar Flutter y comprobar:

```bash
flutter --version
flutter doctor
```

El proyecto Flutter debe permitir ejecutar:

```bash
flutter run -d chrome
```

para Web,

```bash
flutter run -d windows
```

para Windows,

y el dispositivo correspondiente para Android, iOS, Linux o macOS.

---

# Modelo YOLO26s

AccessAI utiliza un checkpoint entrenado:

```text
best.pt
```

El modelo debe colocarse en el backend.

Ejemplo:

```text
backend/
└── models/
    └── best.pt
```

También puede configurarse mediante una variable de entorno:

```text
BEST_MODEL_PATH=./models/best.pt
```

No se deben añadir checkpoints grandes al repositorio Git.

El archivo `best.pt` debe mantenerse localmente o almacenarse mediante el mecanismo de distribución elegido para el proyecto.

---

# Instalación del backend

Desde la carpeta `backend`:

```bash
python -m venv .venv
```

Activar el entorno en Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejemplo de dependencias:

```text
fastapi
uvicorn
python-multipart
ultralytics
opencv-python
torch
torchvision
```

PyTorch debe instalarse con la versión CUDA apropiada para el equipo.

---

# Ejecución del backend

Desde:

```text
backend/
```

ejecutar:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API quedará disponible en:

```text
http://127.0.0.1:8000
```

Documentación automática:

```text
http://127.0.0.1:8000/docs
```

Comprobación:

```text
http://127.0.0.1:8000/api/health
```

---

# API

El backend proporciona endpoints REST para que Flutter pueda comunicarse con Python.

Ejemplo conceptual:

```text
GET  /api/health
GET  /api/model
POST /api/predict/image
POST /api/predict/video
```

## Health

Respuesta esperada:

```json
{
  "status": "ok",
  "cuda": true,
  "device": "cuda:0",
  "gpu": "NVIDIA RTX 4060 Laptop GPU"
}
```

## Imagen

Flutter envía una imagen mediante `multipart/form-data`.

Python ejecuta:

```python
model.predict(
    source=image,
    conf=confidence,
    imgsz=imgsz,
    device=0
)
```

La API devuelve información como:

```json
{
  "detections": 3,
  "classes": {
    "Obstaculo_Dinamico": 1,
    "Obstaculo_Fijo": 1,
    "Infraestructura_Peatonal": 1
  },
  "image_url": "/results/image_result.jpg"
}
```

---

# Aplicación Flutter

La aplicación Flutter reemplaza la interfaz Streamlit.

La interfaz tendrá como mínimo:

```text
AccessAI
│
├── Inicio
│
├── Imagen
│   ├── Seleccionar imagen
│   ├── Confianza
│   ├── Tamaño de imagen
│   ├── Ejecutar detección
│   ├── Imagen original
│   ├── Imagen anotada
│   └── Detecciones por clase
│
├── Vídeo
│   ├── Seleccionar vídeo
│   ├── Confianza
│   ├── Tamaño de imagen
│   ├── Ejecutar detección
│   ├── Vídeo original
│   ├── Vídeo procesado
│   └── Resumen de detecciones
│
└── Proyecto
    ├── Modelo
    ├── Clases
    ├── GPU
    ├── CUDA
    └── Información de AccessAI
```

---

# Configuración de la API en Flutter

La URL del backend puede configurarse mediante:

```bash
--dart-define=API_URL=http://127.0.0.1:8000
```

Windows:

```powershell
flutter run -d windows `
  --dart-define=API_URL=http://127.0.0.1:8000
```

Web:

```powershell
flutter run -d chrome `
  --dart-define=API_URL=http://127.0.0.1:8000
```

Android Emulator:

```powershell
flutter run -d emulator-5554 `
  --dart-define=API_URL=http://10.0.2.2:8000
```

---

# Flujo de imagen

```text
Usuario
   │
   ▼
Flutter
   │
   │ selecciona imagen
   ▼
POST /api/predict/image
   │
   ▼
FastAPI
   │
   ▼
YOLO26s
   │
   ▼
CUDA : GPU NVIDIA
   │
   ▼
Detecciones
   │
   ├── clase
   ├── confianza
   └── bounding box
   │
   ▼
FastAPI
   │
   ▼
Flutter
   │
   ├── imagen anotada
   ├── número de detecciones
   └── detecciones por clase
```

---

# Flujo de vídeo

```text
Usuario
   │
   ▼
Flutter
   │
   ▼
Subida del vídeo
   │
   ▼
FastAPI
   │
   ▼
OpenCV + YOLO26s
   │
   ▼
Procesamiento de frames
   │
   ▼
Vídeo anotado
   │
   ▼
Flutter
```

La aplicación debe mostrar:

* vídeo original;
* vídeo procesado;
* número de frames procesados;
* detecciones totales;
* detecciones por clase;
* descarga del vídeo resultante.

---

# GPU y CUDA

AccessAI mantiene el requisito de GPU del prototipo original.

La inferencia utiliza:

```python
device = 0
```

cuando CUDA está disponible.

La aplicación debe comprobar:

```python
torch.cuda.is_available()
```

Antes de ejecutar YOLO26s.

Cuando devuelve `False`:

```text
CUDA no disponible.

AccessAI no ejecutará la inferencia en CPU.

Comprueba el controlador NVIDIA y la instalación de PyTorch CUDA.
```

No debe existir un fallback silencioso:

```python
device = "cpu"
```

---

# Estructura del proyecto

```text
AccessAI/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── model.py
│   │   ├── inference.py
│   │   └── schemas.py
│   │
│   ├── models/
│   │   └── best.pt
│   │
│   ├── storage/
│   │   ├── uploads/
│   │   └── results/
│   │
│   ├── requirements.txt
│   └── .env
│
├── flutter_app/
│   ├── lib/
│   │   ├── main.dart
│   │   ├── models/
│   │   ├── services/
│   │   ├── screens/
│   │   └── widgets/
│   │
│   ├── assets/
│   ├── pubspec.yaml
│   └── analysis_options.yaml
│
├── runs/
│   └── detect/
│       └── <entrenamiento>/
│           └── weights/
│               └── best.pt
│
├── README.md
└── .gitignore
```

---

# Desarrollo

## Backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Flutter

```powershell
cd flutter_app
flutter pub get
```

Windows:

```powershell
flutter run -d windows
```

Web:

```powershell
flutter run -d chrome
```

---

# Construcción para distribución

Web:

```powershell
flutter build web
```

Windows:

```powershell
flutter build windows
```

Android:

```powershell
flutter build apk
```

Linux:

```powershell
flutter build linux
```

macOS:

```bash
flutter build macos
```

iOS:

```bash
flutter build ios
```

La disponibilidad de cada destino depende del sistema de desarrollo utilizado.

---

# Plan de trabajo

1. **Preparar el entorno**

   Instalar Python, PyTorch CUDA, Ultralytics, FastAPI y Flutter.

2. **Validar GPU**

   Comprobar:

   ```python
   torch.cuda.is_available()
   ```

   y verificar la NVIDIA RTX 4060.

3. **Validar el modelo**

   Colocar:

   ```text
   best.pt
   ```

   en:

   ```text
   backend/models/
   ```

4. **Crear la API Python**

   Implementar endpoints para imagen y vídeo.

5. **Crear la aplicación Flutter**

   Implementar una interfaz común para Web, Mobile y Desktop.

6. **Probar imágenes**

   Comprobar detecciones, confianza, clases y anotaciones.

7. **Probar vídeos**

   Comprobar procesamiento de frames, vídeo resultante y resumen.

8. **Evaluar y mejorar**

   Registrar errores, tiempos de inferencia, uso de VRAM y experiencia de usuario.

---

# Guía para agentes

* Mantener el idioma principal en español.
* Conservar exactamente las cuatro clases de AccessAI.
* Mantener YOLO26s como modelo del prototipo.
* Mantener la ejecución mediante NVIDIA CUDA.
* No añadir fallback silencioso a CPU.
* No incluir `best.pt`, vídeos ni otros archivos grandes en Git.
* Separar siempre la interfaz Flutter de la lógica de IA Python.
* Las modificaciones de inferencia deben probar tanto imágenes como vídeos.
* Los cambios de rutas deben contemplar correctamente la carga automática y manual del checkpoint.
* Mantener actualizado este README cuando cambien arquitectura, dependencias, endpoints o comandos.

---

# Estado del proyecto

```text
Modelo       YOLO26s
Clases       4
Backend      Python + FastAPI
Frontend     Flutter
Plataformas  Web / Android / iOS / Windows / Linux / macOS
GPU          NVIDIA RTX 4060 Laptop GPU 8 GB
Aceleración  CUDA
Inferencia   GPU obligatoria
```

## Objetivo

Transformar el prototipo original de Streamlit en una aplicación **AccessAI multiplataforma**, manteniendo la lógica de detección YOLO26s y utilizando:

```text
Flutter → interfaz
Python → backend
FastAPI → API
YOLO26s → detección
PyTorch → inferencia
CUDA → aceleración GPU
OpenCV → procesamiento multimedia
```

Esta estructura encaja mejor con tu objetivo de **“utilizar Flutter y Python para crear apps multiplataforma (Web, Mobile y de Escritorio)”** y mantiene la separación correcta entre interfaz y modelo de IA.
