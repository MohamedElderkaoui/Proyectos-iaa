# ACCESSAI — Plan de migración de Streamlit a Flet

## 1. Objetivo

Migrar la aplicación **AccessAI** desarrollada con Streamlit a una aplicación equivalente construida con **Flet**, manteniendo la funcionalidad principal de detección urbana mediante YOLO26s.

La aplicación debe utilizar el modelo entrenado `best.pt`, trabajar con las 4 clases de AccessAI y utilizar la NVIDIA RTX 4060 mediante CUDA cuando esté disponible.

---

## 2. Aplicación actual: Streamlit

La aplicación Streamlit contiene:

- Configuración de página.
- Detección de CUDA.
- Identificación de GPU y VRAM.
- Configuración de confianza.
- Configuración de `imgsz`.
- Búsqueda automática de `best.pt`.
- Carga manual de `best.pt`.
- Carga del modelo YOLO.
- Inferencia de imágenes.
- Inferencia de vídeos.
- Visualización de imágenes anotadas.
- Conteo de detecciones.
- Conteo de detecciones por clase.
- Información del proyecto.
- Información del modelo.
- Manejo de errores CUDA.
- Uso explícito de `device=0`.

### Clases

```python
CLASS_NAMES = [
    "Obstaculo_Dinamico",
    "Obstaculo_Fijo",
    "Barrera_Arquitectonica",
    "Infraestructura_Peatonal",
]
```

---

# 3. Arquitectura Flet propuesta

```text
AccessAI/
│
├── app/
│   ├── main.py
│   ├── detector.py
│   ├── model_manager.py
│   ├── gpu.py
│   └── ui/
│       ├── image_view.py
│       ├── video_view.py
│       └── project_view.py
│
├── runs/
│   └── detect/
│       └── AccessAI_YOLO26s_4clases_RTX4060_*/
│           └── weights/
│               └── best.pt
│
├── requirements.txt
├── README.md
└── plan2.md
```

Para una primera versión se puede mantener todo en `main.py`. Después se recomienda separar la lógica en módulos.

---

# 4. Equivalencias Streamlit → Flet

| Streamlit | Flet |
|---|---|
| `st.set_page_config()` | `page.title`, `page.theme_mode`, propiedades de `Page` |
| `st.sidebar` | `NavigationRail`, `Container`, `Column` o panel lateral |
| `st.slider()` | `ft.Slider` |
| `st.selectbox()` | `ft.Dropdown` |
| `st.file_uploader()` | `ft.FilePicker` |
| `st.button()` | `ft.FilledButton` / `ft.ElevatedButton` |
| `st.image()` | `ft.Image` |
| `st.video()` | `ft.Video` o componente multimedia equivalente |
| `st.metric()` | `ft.Card` / `ft.Container` + `ft.Text` |
| `st.tabs()` | `ft.Tabs` |
| `st.expander()` | `ft.ExpansionTile` / panel equivalente |
| `st.table()` | `ft.DataTable` |
| `st.success()` | `ft.Text` / `ft.Container` |
| `st.error()` | `ft.Text` / `ft.Container` |
| `st.spinner()` | `ft.ProgressRing` / `ProgressBar` |
| `st.download_button()` | descarga mediante el mecanismo de archivos de Flet |

---

# 5. `main.py`

Responsabilidades:

```text
main.py
│
├── Crear Page
├── Crear navegación
├── Crear panel de configuración
├── Crear vista Imagen
├── Crear vista Vídeo
├── Crear vista Proyecto
├── Conectar botones
└── Actualizar UI
```

El `main.py` no debería contener toda la lógica de YOLO cuando el proyecto crezca.

---

# 6. `model_manager.py`

Responsabilidades:

1. Buscar automáticamente el último `best.pt`.
2. Permitir seleccionar manualmente un modelo.
3. Cargar el modelo YOLO.
4. Mantener el modelo en memoria.
5. Evitar ejecutar `YOLO(model_name)` en cada detección.

Funciones previstas:

```python
def find_best_model() -> Path | None:
    ...

def load_model(model_path: Path):
    ...

def get_model_names(model):
    ...
```

---

# 7. Búsqueda del modelo

Mantener la estructura:

```text
runs/detect/
└── AccessAI_YOLO26s_4clases_RTX4060_*/
    └── weights/
        └── best.pt
```

La búsqueda debe seleccionar el checkpoint más reciente mediante `stat().st_mtime`.

Fallback:

```text
ROOT/best_uploaded.pt
```

Si no existe ningún modelo:

```text
No se encontró ningún best.pt.
Selecciona manualmente un modelo.
```

---

# 8. GPU y CUDA

La versión Flet debe mantener la comprobación existente:

```python
torch.cuda.is_available()
```

Si CUDA está disponible:

```python
DEVICE = 0
GPU_NAME = torch.cuda.get_device_name(0)
```

También obtener:

```python
torch.cuda.get_device_properties(0)
```

para calcular la VRAM.

Información que debe mostrarse:

```text
CUDA: Disponible
GPU: NVIDIA GeForce RTX 4060 Laptop GPU
Device: cuda:0
VRAM: X GB
```

Si CUDA no está disponible:

```text
CUDA no disponible
```

La aplicación puede bloquear la inferencia si el proyecto exige GPU.

---

# 9. Panel de configuración

El panel lateral Flet debe contener:

## Confianza

```python
ft.Slider(
    min=0.05,
    max=0.95,
    value=0.25,
)
```

## Tamaño de imagen

Valores:

```text
416
512
640
768
960
```

Valor recomendado inicialmente:

```text
640
```

## Hardware

Mostrar:

```text
CUDA
GPU
VRAM
Device
```

## Clases

Mostrar:

```text
0 — Obstaculo_Dinamico
1 — Obstaculo_Fijo
2 — Barrera_Arquitectonica
3 — Infraestructura_Peatonal
```

---

# 10. Vista Imagen

La vista debe permitir:

```text
Seleccionar imagen
        ↓
Mostrar imagen original
        ↓
Ejecutar detección
        ↓
YOLO26s
        ↓
RTX 4060
        ↓
Imagen anotada
        ↓
Resultados
```

Formatos:

```text
jpg
jpeg
png
bmp
webp
```

---

# 11. Inferencia YOLO

La llamada debe mantener explícitamente:

```python
results = model.predict(
    source=image_path,
    conf=confidence,
    imgsz=imgsz,
    device=DEVICE,
    save=False,
    verbose=False,
)
```

Esto mantiene el comportamiento de la versión Streamlit.

---

# 12. Imagen anotada

Utilizar:

```python
result.plot()
```

El resultado devuelve una imagen con:

- bounding boxes
- clase
- confianza

En caso de necesitar RGB:

```python
annotated = result.plot()
annotated_rgb = cv2.cvtColor(
    annotated,
    cv2.COLOR_BGR2RGB,
)
```

Después mostrarla mediante `ft.Image`.

---

# 13. Resultados

Mostrar como mínimo:

```text
Detecciones totales: 7
```

Y por clase:

```text
Obstaculo_Dinamico: 2
Obstaculo_Fijo: 1
Barrera_Arquitectonica: 3
Infraestructura_Peatonal: 1
```

También se recomienda mostrar:

```text
Confianza media
Confianza máxima
Tiempo de inferencia
```

---

# 14. Detalles de cada detección

Para cada bounding box:

```text
Clase
Confianza
X1
Y1
X2
Y2
```

Ejemplo:

```text
Obstaculo_Fijo
Confianza: 0.91
Bounding box:
x1=120
y1=85
x2=340
y2=420
```

Esto permitirá posteriormente construir funciones de análisis espacial.

---

# 15. Vista Vídeo

La segunda sección debe permitir:

```text
Seleccionar vídeo
        ↓
Procesar vídeo
        ↓
YOLO26s frame-by-frame
        ↓
Guardar vídeo anotado
        ↓
Mostrar resultado
        ↓
Descargar resultado
```

Formatos previstos:

```text
mp4
avi
mov
mkv
wmv
webm
mpeg
mpg
```

---

# 16. Procesamiento de vídeo

Utilizar:

```python
model.predict(
    source=video_path,
    conf=confidence,
    imgsz=imgsz,
    device=DEVICE,
    save=True,
    project=str(RUNS_DIR),
    name="AccessAI_Flet_video",
    exist_ok=True,
    verbose=False,
)
```

El resultado debe guardarse dentro de:

```text
runs/detect/AccessAI_Flet_video/
```

---

# 17. Estadísticas del vídeo

Calcular:

```text
Frames procesados
Detecciones totales
Detecciones por clase
Confianza media
```

Ejemplo:

```text
Frames procesados: 842

Detecciones totales: 1.923

Obstaculo_Dinamico: 542
Obstaculo_Fijo: 387
Barrera_Arquitectonica: 613
Infraestructura_Peatonal: 381
```

---

# 18. Vista Proyecto

Crear una sección equivalente a:

```text
AccessAI — Detección urbana
```

Mostrar:

```text
Modelo: YOLO26s
Clases: 4
Image size: 640
Confidence: 0.25
GPU: NVIDIA RTX 4060
CUDA: versión instalada
Device: cuda:0
VRAM: X GB
```

También mostrar:

```text
Ruta del modelo:
runs/detect/.../weights/best.pt
```

---

# 19. Gestión de memoria GPU

Antes de una inferencia:

```python
gc.collect()
torch.cuda.empty_cache()
```

En caso de:

```python
torch.cuda.OutOfMemoryError
```

mostrar:

```text
CUDA OUT OF MEMORY.

Reduce el tamaño de imagen o cierra otras
aplicaciones que utilicen la RTX 4060.
```

También se puede recomendar:

```text
640 → 512 → 416
```

si aparece falta de VRAM.

---

# 20. Carga del modelo

No hacer esto dentro de cada botón:

```python
model = YOLO(model_name)
```

La estrategia recomendada es:

```text
Aplicación inicia
      ↓
Buscar best.pt
      ↓
Cargar YOLO26s
      ↓
Mantener modelo en memoria
      ↓
Imagen / vídeo utilizan el mismo modelo
```

Esto reduce el tiempo de espera.

---

# 21. Estado de la aplicación

Crear estados:

```text
LISTO
IMAGEN_CARGADA
PROCESANDO
COMPLETADO
ERROR
```

Ejemplo:

```text
🟢 Listo para analizar

🟡 Ejecutando detección...

🟢 Detección completada.

🔴 La detección falló.
```

---

# 22. Diseño Flet

Propuesta:

```text
┌──────────────────────────────────────────────────────────────┐
│ ACCESSAI                                      GPU: RTX 4060  │
├───────────────┬──────────────────────────────────────────────┤
│               │                                              │
│ 🖼 Imagen     │              VISTA PRINCIPAL                 │
│               │                                              │
│ 🎥 Vídeo      │        ┌────────────────────────┐            │
│               │        │                        │            │
│ ℹ Proyecto    │        │    Imagen / Vídeo      │            │
│               │        │                        │            │
│               │        └────────────────────────┘            │
│               │                                              │
│ Configuración │              RESULTADOS                      │
│               │                                              │
│ Confianza     │  Detecciones: 7                              │
│ [────●────]   │  Obstaculo_Fijo: 2                           │
│               │  Barrera_Arquitectonica: 3                   │
│ Img size      │  Infraestructura_Peatonal: 2                 │
│ [640]         │                                              │
│               │                                              │
└───────────────┴──────────────────────────────────────────────┘
```

---

# 23. Primera versión funcional

La primera versión Flet debe implementar únicamente:

```text
1. Inicio
2. Buscar best.pt
3. Cargar YOLO26s
4. Detectar CUDA
5. Seleccionar imagen
6. Ejecutar detección
7. Mostrar imagen anotada
8. Mostrar detecciones
9. Mostrar clases
10. Mostrar GPU
```

Una vez estable:

```text
11. Vídeo
12. Estadísticas
13. Descarga
14. Dashboard
15. Historial
```

---

# 24. Segunda fase

Añadir dashboard:

```text
┌──────────────┬──────────────┬──────────────┐
│ Detecciones  │ Conf. media  │ Inferencia   │
│     127      │     0.84     │    31 ms     │
└──────────────┴──────────────┴──────────────┘
```

Gráficos:

```text
Detecciones por clase
        ↓
Bar chart
```

```text
Confianza
        ↓
Histograma
```

```text
Inferencia
        ↓
FPS / ms
```

---

# 25. Tercera fase — AccessAI completo

Arquitectura final:

```text
                    ACCESSAI
                       │
          ┌────────────┼────────────┐
          │            │            │
       IMAGEN        VÍDEO       PROYECTO
          │            │            │
          └────────────┼────────────┘
                       │
                    YOLO26s
                       │
                  CUDA / GPU
                       │
                RTX 4060 Laptop
                       │
          ┌────────────┼────────────┐
          │            │            │
       Boxes        Classes      Confidence
          │            │            │
          └────────────┼────────────┘
                       │
                    DASHBOARD
```

---

# 26. Requisitos

Archivo `requirements.txt` inicial:

```text
flet
ultralytics
torch
torchvision
opencv-python
numpy
```

Si se utiliza procesamiento adicional:

```text
pandas
matplotlib
```

---

# 27. Ejecución

Desarrollo:

```bash
python app/main.py
```

También se puede utilizar el comando correspondiente de Flet según el modo de despliegue elegido.

---

# 28. Criterios de éxito

La migración se considera correcta cuando:

- [ ] Flet inicia correctamente.
- [ ] Detecta CUDA.
- [ ] Detecta la RTX 4060.
- [ ] Encuentra automáticamente `best.pt`.
- [ ] Carga YOLO26s.
- [ ] Permite seleccionar una imagen.
- [ ] Ejecuta inferencia con `device=0`.
- [ ] Muestra bounding boxes.
- [ ] Muestra las 4 clases.
- [ ] Muestra confianza.
- [ ] Cuenta detecciones.
- [ ] Procesa vídeo.
- [ ] Guarda el vídeo procesado.
- [ ] Muestra información del modelo.
- [ ] Maneja errores de CUDA.
- [ ] Permite ajustar `confidence`.
- [ ] Permite ajustar `imgsz`.

---

# 29. Resultado final esperado

La aplicación final será:

```text
AccessAI Flet
│
├── Dashboard
├── Detección de imágenes
├── Detección de vídeo
├── Estadísticas
├── Información del modelo
├── Información GPU/CUDA
└── Configuración
```

La migración debe conservar la lógica de detección de la aplicación Streamlit y cambiar principalmente la capa de interfaz de usuario de Streamlit a Flet.
