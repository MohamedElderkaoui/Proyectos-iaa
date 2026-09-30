# AccessAI

AccessAI es un prototipo de visión artificial para detectar elementos relacionados con la accesibilidad urbana en imágenes de entornos peatonales.

El prototipo utiliza YOLO mediante Ultralytics. Actualmente emplea YOLO26, un modelo preentrenado de detección general. El siguiente paso del proyecto es entrenar un modelo específico con datos de accesibilidad urbana para detectar, entre otros elementos, aceras y rampas de acceso.

# Documentación relevante

DOCUMENTACIÓN YOLO:
https://docs.ultralytics.com/es/quickstart

DATASET: ROD-DATASET DE DETECCIÓN (YOLO26n)
https://www.kaggle.com/datasets/abtinzandi/obstacle-detection-dataset/data

DATASET: CURBS (BORDILLOS) DE SEGMENTACIÓN DE INSTANCIAS (YOLO26n-seg)
https://universe.roboflow.com/bielglasses/barcelona-streets

Hay que transformar los labels del dataset Curbs de segmentación de instancias a detección mediante bounding boxes. Todo el proceso está desarrollado en ACCESSAI_firstProto.ipynb

## Requisitos

- Python 3.10 o superior
- Un entorno virtual de Python

 # AccessAI

 ## Detección inteligente de accesibilidad urbana

 AccessAI es un proyecto de visión artificial desarrollado en el marco de Samsung Innovation Campus 2025-26. Su objetivo es analizar imágenes de espacios urbanos y detectar elementos relevantes para la accesibilidad peatonal, como aceras, rampas de acceso y posibles barreras.

 El repositorio contiene un prototipo ejecutable basado en YOLO y varios recursos de apoyo para la presentación y documentación del proyecto.

 > **Estado del proyecto:** primer prototipo realizado; hay que seguir mejorando los resultados de inferencia de imágenes propias.

 ## Índice

- [AccessAI](#accessai)
  - [Documentación relevante] (#docus)
  - [Requisitos](#requisitos)
- [AccessAI](#accessai-1)
  - [Detección inteligente de accesibilidad urbana](#detección-inteligente-de-accesibilidad-urbana)
  - [Índice](#índice)
  - [Motivación](#motivación)
  - [Objetivos](#objetivos)
    - [Objetivo principal](#objetivo-principal)
    - [Objetivos iniciales](#objetivos-iniciales)
    - [Posibles ampliaciones](#posibles-ampliaciones)
  - [Arquitectura del prototipo](#arquitectura-del-prototipo)
  - [Requisitos](#requisitos-1)
  - [Instalación](#instalación)
    - [Windows PowerShell](#windows-powershell)
  - [Uso de la demo](#uso-de-la-demo)
    - [Ejecución mínima](#ejecución-mínima)
    - [Ejecución con parámetros personalizados](#ejecución-con-parámetros-personalizados)
    - [Opciones de línea de comandos](#opciones-de-línea-de-comandos)
  - [Interpretación de resultados](#interpretación-de-resultados)
  - [Metodología prevista](#metodología-prevista)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Limitaciones y próximos pasos](#limitaciones-y-próximos-pasos)
    - [Limitaciones actuales](#limitaciones-actuales)
    - [Próximos pasos técnicos](#próximos-pasos-técnicos)
  - [Solución de problemas](#solución-de-problemas)
    - [`ModuleNotFoundError: No module named 'ultralytics'`](#modulenotfounderror-no-module-named-ultralytics)
    - [No se encuentra la imagen](#no-se-encuentra-la-imagen)
    - [No se guarda la imagen de salida](#no-se-guarda-la-imagen-de-salida)
    - [No hay detecciones](#no-hay-detecciones)
  - [Documentación relacionada](#documentación-relacionada)
  - [Licencia y materiales del curso](#licencia-y-materiales-del-curso)

 ## Motivación

 Los mapas pueden indicar que una zona es transitable, aunque una persona con movilidad reducida encuentre obstáculos reales: bordillos elevados, ausencia de rampas, superficies deterioradas, escaleras u objetos que bloquean el paso.

 AccessAI estudia cómo utilizar visión artificial para convertir imágenes urbanas en información estructurada sobre accesibilidad. A largo plazo, las detecciones podrían combinarse con coordenadas geográficas para construir mapas de accesibilidad más útiles y actualizados.

 ## Objetivos

 ### Objetivo principal

 Desarrollar un sistema capaz de analizar imágenes de entornos peatonales y localizar elementos relacionados con la accesibilidad urbana.

 ### Objetivos iniciales

 1. Analizar datasets públicos de imágenes urbanas y accesibilidad.
 2. Identificar clases útiles para el problema, inicialmente `sidewalk` y `curbramp`.
 3. Preparar anotaciones para entrenamiento, validación y prueba.
 4. Entrenar y evaluar un detector de objetos específico.
 5. Mostrar las detecciones sobre la imagen original mediante bounding boxes.

 ### Posibles ampliaciones

 - Obstáculos en aceras.
 - Escaleras y cambios de nivel.
 - Bordillos sin rebaje.
 - Superficies deterioradas.
 - Integración con coordenadas GPS.
 - Aplicación o mapa orientado a personas con movilidad reducida.

 ## Arquitectura del prototipo

 ```mermaid
 flowchart LR
     A[Imagen urbana] --> B[accessai_demo.py]
     B --> C[Modelo YOLO]
     C --> D[Detecciones y confianza]
     D --> E[Bounding boxes anotadas]
     E --> F[resultados/accessai_resultado.jpg]
 ```

 El flujo actual es el siguiente:

 1. Se recibe una imagen mediante `--image`.
 2. Se carga el modelo indicado mediante `--model`.
 3. YOLO genera las detecciones con el umbral `--conf`.
 4. El script muestra clase, confianza y coordenadas de cada detección.
 5. Se guarda una copia anotada en la ruta indicada mediante `--output`.

 ## Requisitos

 - Windows, macOS o Linux.
 - Python 3.10 o superior.
 - Un entorno virtual recomendado.
 - Dependencias de Python:
   - `ultralytics` para cargar y ejecutar YOLO.
   - `opencv-python`, instalado normalmente como dependencia de Ultralytics, para guardar la imagen anotada.
   - `python-pptx` para generar las presentaciones.

 ## Instalación

 Desde la carpeta raíz del proyecto, crea y activa un entorno virtual.

 ### Windows PowerShell

 ```powershell
 python -m venv .venv
 .\.venv\Scripts\Activate.ps1
 python -m pip install --upgrade pip
 python -m pip install ultralytics python-pptx
 ```

 Si PowerShell bloquea la activación del entorno para la sesión actual:

 ```powershell
 Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
 .\.venv\Scripts\Activate.ps1
 ```

 Comprueba que el intérprete activo es el del entorno:

 ```powershell
 python -c "import sys; print(sys.executable)"
 ```

 ## Uso de la demo (PRIORIDAD: DEMO EN LOCAL)

 ### Ejecución mínima

 Analiza una imagen y guarda el resultado en `resultados/accessai_resultado.jpg`:

 ```powershell
 python accessai_demo.py --image "datos\acera.jpg"
 ```

 La primera ejecución puede descargar automáticamente `yolov8n.pt` si el archivo no existe localmente.

 ### Ejecución con parámetros personalizados

 ```powershell
 python accessai_demo.py `
   --image "datos\acera.jpg" `
   --model "modelos\accessai.pt" `
   --conf 0.40 `
   --output "resultados\acera_anotada.jpg"
 ```

 ### Opciones de línea de comandos

 | Opción | Obligatoria | Valor predeterminado | Descripción |
 |---|---:|---|---|
 | `--image` | Sí | Sin valor | Ruta de la imagen de entrada. |
 | `--model` | No | `yolov8n.pt` | Ruta a un modelo YOLO en formato `.pt`. |
 | `--conf` | No | `0.25` | Umbral de confianza, estrictamente mayor que 0 y menor o igual que 1. |
 | `--output` | No | `resultados/accessai_resultado.jpg` | Ruta de la imagen anotada de salida. |

 Para consultar la ayuda cuando las dependencias estén instaladas:

 ```powershell
 python accessai_demo.py --help
 ```

 ## Interpretación de resultados

 La consola muestra una línea por detección con:

 - Nombre de la clase detectada.
 - Confianza del modelo.
 - Bounding box en formato `[x1, y1, x2, y2]`.

 La imagen anotada se guarda automáticamente y la carpeta de salida se crea si todavía no existe.

 Con el modelo genérico actual, las clases detectadas pertenecen al conjunto de entrenamiento original de YOLO. Por tanto, una detección de una clase general no debe interpretarse como una confirmación de que una acera o rampa sea accesible.

 ## Metodología prevista

 ```mermaid
 flowchart TD
     A[Seleccionar datasets] --> B[Revisar clases y anotaciones]
     B --> C[Limpiar y normalizar datos]
     C --> D[Separar train, validation y test]
     D --> E[Entrenar detector YOLO]
     E --> F[Evaluar precision, recall, F1 y mAP]
     F --> G[Probar con imágenes nuevas]
     G --> H[Integrar en un prototipo de accesibilidad]
 ```

 ## Estructura del proyecto

 ```text
 .
 |-- ACCESSAI_fistProto: Primer Prototipo (30/9/26)
 |-- prototipoACCESSAI_JMJ-Team: Presentación del primer prototipo/demo
 |-- ACCESSAI_firstProto_colab (NO ACTUALIZADO)
 |-- Planificacion_JMJ-Tean: Planificación temporal del proyecto
 |-- accessai_demo.py
 |-- ActionPlan.docx/.txt: Plan de acción del proyecto
 |-- proyecto.pdf (ideas iniciales del proyecto, NO ACTUALIZADO)
 |-- tutoGPU.odt: tutorial con algunos pasos para configurar el uso de la GPU en el entrenamiento de los modelos, así como para Colab.
 |-- dependencias.txt: Dependencias para el proyecto (NO ACTUALIZADO)
 |-- resultados/                         # Se crea al ejecutar la demo
 |-- .venv/                              # Entorno local, no versionado
 `-- README.md
 ```

 Además, la carpeta contiene presentaciones, plantillas y documentos PDF de referencia del curso.

 ## Limitaciones y próximos pasos

 ### Limitaciones actuales

 - (Especificar limitaciones tras el primer prototipo)

 ### Próximos pasos técnicos

 1. Entrenar un modelo específico para accesibilidad urbana con los mejores resultados posibles.
 2. Medir precision, recall, F1 y mAP por clase.
 3. Revisar falsos positivos y falsos negativos.
 5. Añadir procesamiento por lotes o una interfaz de usuario. (A futuro)
 6. Estudiar la integración con localización geográfica y mapas. (A futuro)

 ## Solución de problemas

 ### `ModuleNotFoundError: No module named 'ultralytics'`

 Activa el entorno virtual e instala la dependencia:

 ```powershell
 .\.venv\Scripts\Activate.ps1
 python -m pip install ultralytics
 ```

 ### No se encuentra la imagen

 Comprueba que la ruta de `--image` es correcta. En Windows, utiliza comillas si contiene espacios:

 ```powershell
 python accessai_demo.py --image "C:\proyectos\accessai\datos\acera.jpg"
 ```

 ### No se guarda la imagen de salida

 Comprueba que la ruta de `--output` apunta a una carpeta con permisos de escritura. El script crea la carpeta de salida, pero no puede resolver permisos insuficientes o rutas inválidas.

 ### No hay detecciones

 El modelo puede no reconocer los elementos de accesibilidad porque todavía es un modelo general. También puede probarse un umbral menor, siempre dentro del rango válido:

 ```powershell
 python accessai_demo.py --image "datos\acera.jpg" --conf 0.15
 ```

 Reducir el umbral puede aumentar los falsos positivos; no sustituye al entrenamiento de un modelo específico.

 ## Documentación relacionada

 - [Plan de acción del proyecto](ActionPlan.docx)
 - [Demo de detección](ACCESSAI_firstProto.ipynb)
 - [Generador de presentación v2](generate_accessai_pptx_v2_0_2.py)

 ## Licencia y materiales del curso

 Los documentos de Samsung Innovation Campus incluidos en esta carpeta pueden estar sujetos a las condiciones de uso y derechos de autor indicados en cada documento. Este README describe el prototipo AccessAI y no modifica esas condiciones.
