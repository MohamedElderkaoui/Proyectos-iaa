# [markdown]
#  AccessAI - Prototipo de detección urbana
#
# Notebook completo para preparar ROD-Dataset, remapear 25 clases a 4 categorías, entrenar YOLO26n en RTX 4060, evaluar en test y ejecutar inferencia.
#
# # Clases finales
#
# | ID | Clase |
# |---:|---|
# | 0 | `Obstaculo_Dinamico` |
# | 1 | `Obstaculo_Fijo` |
# | 2 | `Barrera_Arquitectonica` |
# | 3 | `Infraestructura_Peatonal` |
#
# **Configuración GPU:** batch fijo `8`, `imgsz=640`, `AMP=True`, `workers=0`, `cache='disk'`. No se usa `batch=-1` para evitar AutoBatch y su posible OOM.

# [markdown]
#  01. Entorno y GPU

from pathlib import Path
import torch

print('=' * 70)
print('ACCESSAI - ENTORNO Y GPU')
print('=' * 70)
print(f'PyTorch: {torch.__version__}')
print(f'CUDA disponible: {torch.cuda.is_available()}')
print(f'CUDA de PyTorch: {torch.version.cuda}')
print(f'HIP: {torch.version.hip}')

if torch.cuda.is_available():
    props = torch.cuda.get_device_properties(0)
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'GPU count: {torch.cuda.device_count()}')
    print(f'Memoria GPU: {props.total_memory / 1024**3:.2f} GB')
    print(f'Compute capability: {props.major}.{props.minor}')
    print(f'Memoria reservada: {torch.cuda.memory_reserved(0) / 1024**3:.2f} GB')
    print(f'Memoria asignada: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB')
else:
    raise RuntimeError('CUDA no disponible. Se cancela el notebook para evitar entrenamiento CPU.')
print('=' * 70)

# [markdown]
#  02. Comprobar Ultralytics

import ultralytics
print('Ultralytics:', ultralytics.__version__)


# [markdown]
#  03. Configuración del dataset

from pathlib import Path
import shutil
import yaml
from collections import Counter

ROOT = Path.cwd()
DATASET_PATH = ROOT / 'DATA' / 'ROD-Dataset' / 'dataset'
yaml_original_path = DATASET_PATH / 'data.yaml'
yaml_nuevo_path = DATASET_PATH / 'data_filtrado.yaml'

print('Dataset:', DATASET_PATH)
print('Existe dataset:', DATASET_PATH.exists())
print('Existe data.yaml:', yaml_original_path.exists())

if not DATASET_PATH.exists():
    raise FileNotFoundError(f'No existe el dataset:\n{DATASET_PATH}')
if not yaml_original_path.exists():
    raise FileNotFoundError(f'No existe:\n{yaml_original_path}')

# [markdown]
#  04. Mapeo de clases del ROD-Dataset

MAPEO_CLASES = {
    0: 0, 2: 0, 3: 0, 8: 0, 10: 0, 15: 0, 16: 0,
    5: 1, 6: 1, 9: 1, 12: 1, 13: 1, 17: 1, 18: 1,
    19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1,
    4: 2,
    7: 3, 11: 3, 14: 3
}

NUEVOS_NOMBRES = [
    'Obstaculo_Dinamico',
    'Obstaculo_Fijo',
    'Barrera_Arquitectonica',
    'Infraestructura_Peatonal'
]
NUM_CLASSES = len(NUEVOS_NOMBRES)

for idx, nombre in enumerate(NUEVOS_NOMBRES):
    print(f'{idx}: {nombre}')
print(f'Número de clases: {NUM_CLASSES}')

# [markdown]
#  05. Crear `data_filtrado.yaml`

with open(yaml_original_path, 'r', encoding='utf-8') as f:
    config_original = yaml.safe_load(f)

config_nueva = {
    'path': str(DATASET_PATH.resolve()),
    'train': 'train/images',
    'val': 'valid/images',
    'test': 'test/images',
    'nc': NUM_CLASSES,
    'names': NUEVOS_NOMBRES
}

with open(yaml_nuevo_path, 'w', encoding='utf-8') as f:
    yaml.safe_dump(config_nueva, f, sort_keys=False, allow_unicode=True)

print('YAML creado:', yaml_nuevo_path)
print(yaml_nuevo_path.read_text(encoding='utf-8'))

# [markdown]
#  06. Preparar etiquetas
#
# Las etiquetas originales se conservan en `labels_originales`. La transformación es idempotente.

def preparar_etiquetas(split):
    split_dir = DATASET_PATH / split
    labels_dir = split_dir / 'labels'
    labels_originales_dir = split_dir / 'labels_originales'

    if not split_dir.exists():
        raise FileNotFoundError(f'No existe el split:\n{split_dir}')

    if labels_originales_dir.exists():
        source_dir = labels_originales_dir
        print(f'↪ {split}: usando labels_originales como fuente')
    elif labels_dir.exists():
        print(f'↪ {split}: guardando labels originales')
        labels_dir.rename(labels_originales_dir)
        source_dir = labels_originales_dir
    else:
        raise FileNotFoundError(f'No existe la carpeta labels en:\n{split_dir}')

    labels_filtradas_dir = split_dir / 'labels_filtradas'
    if labels_filtradas_dir.exists():
        shutil.rmtree(labels_filtradas_dir)
    labels_filtradas_dir.mkdir(parents=True, exist_ok=True)

    clases_originales = Counter()
    clases_nuevas = Counter()
    clases_descartadas = Counter()
    archivos_procesados = 0

    for archivo in sorted(source_dir.glob('*.txt')):
        archivos_procesados += 1
        ruta_salida = labels_filtradas_dir / archivo.name
        nuevas_lineas = []

        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                partes = linea.strip().split()
                if not partes:
                    continue
                try:
                    clase_original = int(partes[0])
                except ValueError:
                    print(f'⚠️ Clase inválida en {archivo.name}: {partes[0]}')
                    continue

                clases_originales[clase_original] += 1

                if clase_original not in MAPEO_CLASES:
                    clases_descartadas[clase_original] += 1
                    continue

                clase_nueva = MAPEO_CLASES[clase_original]
                partes[0] = str(clase_nueva)
                nuevas_lineas.append(' '.join(partes) + '\n')
                clases_nuevas[clase_nueva] += 1

        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.writelines(nuevas_lineas)

    if labels_dir.exists():
        shutil.rmtree(labels_dir)
    labels_filtradas_dir.rename(labels_dir)

    print('\n' + '-' * 70)
    print(f'Split: {split}')
    print(f'Archivos procesados: {archivos_procesados}')
    print('Clases originales:', dict(sorted(clases_originales.items())))
    print('Clases finales:')
    for clase, nombre in enumerate(NUEVOS_NOMBRES):
        print(f'  {clase} - {nombre}: {clases_nuevas[clase]}')
    print('Clases descartadas:', dict(sorted(clases_descartadas.items())))

for split in ['train', 'valid', 'test']:
    preparar_etiquetas(split)

# [markdown]
#  07. Comprobar estructura del dataset

for split in ['train', 'valid', 'test']:
    split_dir = DATASET_PATH / split
    images_dir = split_dir / 'images'
    labels_dir = split_dir / 'labels'
    originals_dir = split_dir / 'labels_originales'
    image_count = len(list(images_dir.glob('*')))
    label_count = len(list(labels_dir.glob('*.txt')))
    original_count = len(list(originals_dir.glob('*.txt')))
    print('=' * 70)
    print(split)
    print(f'Imágenes:          {image_count}')
    print(f'Labels activas:    {label_count}')
    print(f'Labels originales: {original_count}')

# [markdown]
#  08. Entrenamiento YOLO26x
#
# **RTX 4060 Laptop 8 GB:** batch fijo `8`, `imgsz=640`, `AMP=True`, `workers=0`, `cache='disk'`. No se usa `batch=-1` para evitar AutoBatch.

# ============================================================
# ACCESSAI - YOLO26M
# ENTRENAMIENTO RÁPIDO + OPTIMIZADO
# RTX 4060 LAPTOP GPU 8 GB
# DATASET COMPLETO - 4 CLASES
# ============================================================

import gc
from pathlib import Path

import torch
import ultralytics
from ultralytics import YOLO


# ============================================================
# 1. LIMPIEZA DE MEMORIA
# ============================================================

gc.collect()

if torch.cuda.is_available():
    torch.cuda.empty_cache()


# ============================================================
# 2. CONFIGURACIÓN GPU
# ============================================================

DEVICE = 0

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True


# ============================================================
# 3. RUTAS
# ============================================================

MODEL_PATH = ROOT / "yolo26m.pt"

PROJECT_DIR = ROOT / "AccessAI_Proto3"

RUN_NAME = "yolo26m_4clases_fast"


# ============================================================
# 4. CONFIGURACIÓN DEL ENTRENAMIENTO
# ============================================================

EPOCHS =1
PATIENCE = 10

IMGSZ = 640

# AutoBatch:
# -1 = Ultralytics calcula automáticamente el batch
# según la VRAM disponible.
BATCH = 4
# Tu GPU puede alimentar mejor el entrenamiento
# que con workers=0.
WORKERS = 4

AMP = True

OPTIMIZER = "AdamW"

LR0 = 0.001

SEED = 42

CACHE = "disk"

# Desactivar mosaic durante las últimas 8 épocas.
CLOSE_MOSAIC = 8


# ============================================================
# 5. COMPROBACIONES
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"No se encontró el modelo:\n{MODEL_PATH}"
    )

if not yaml_nuevo_path.exists():
    raise FileNotFoundError(
        f"No existe el dataset YAML:\n{yaml_nuevo_path}"
    )


# ============================================================
# 6. COMPROBAR CUDA
# ============================================================

if not torch.cuda.is_available():
    raise RuntimeError(
        "CUDA no está disponible.\n"
        "PyTorch no puede utilizar la RTX 4060."
    )


# ============================================================
# 7. INFORMACIÓN GPU
# ============================================================

props = torch.cuda.get_device_properties(DEVICE)

print("=" * 72)
print("ACCESSAI - YOLO26M - ENTRENAMIENTO RÁPIDO")
print("=" * 72)

print(f"Ultralytics : {ultralytics.__version__}")
print(f"PyTorch     : {torch.__version__}")
print(f"CUDA        : {torch.version.cuda}")

print(f"GPU         : {torch.cuda.get_device_name(DEVICE)}")

print(
    f"VRAM total  : "
    f"{props.total_memory / 1024**3:.2f} GB"
)

print("-" * 72)

print(f"Modelo      : YOLO26M")
print(f"Dataset     : 4 clases")
print(f"Train       : 19.186 imágenes")
print(f"Valid       : 3.511 imágenes")
print(f"Test        : 1.629 imágenes")

print("-" * 72)

print(f"Epochs      : {EPOCHS}")
print(f"Patience    : {PATIENCE}")
print(f"Batch       : AUTO (-1)")
print(f"Image size  : {IMGSZ}")
print(f"Workers     : {WORKERS}")
print(f"AMP         : {AMP}")
print(f"Optimizer   : {OPTIMIZER}")
print(f"LR0         : {LR0}")
print(f"Cache       : {CACHE}")
print(f"Mosaic      : 1.0")
print(f"Close Mosaic: {CLOSE_MOSAIC}")

print("=" * 72)


# ============================================================
# 8. LIMPIEZA CUDA
# ============================================================

torch.cuda.empty_cache()


# ============================================================
# 9. CARGAR YOLO26M
# ============================================================

model = YOLO(str(MODEL_PATH))

print()
print("✅ Modelo cargado:")
print(MODEL_PATH)
print()


# ============================================================
# 10. ENTRENAMIENTO
# ============================================================

try:

    results = model.train(

        # ----------------------------------------------------
        # DATASET
        # ----------------------------------------------------

        data=str(yaml_nuevo_path),

        # ----------------------------------------------------
        # DURACIÓN
        # ----------------------------------------------------

        epochs=EPOCHS,

        patience=PATIENCE,

        # ----------------------------------------------------
        # RESOLUCIÓN
        # ----------------------------------------------------

        imgsz=IMGSZ,

        # ----------------------------------------------------
        # GPU
        # ----------------------------------------------------

        device=DEVICE,

        # ----------------------------------------------------
        # BATCH AUTOMÁTICO
        # ----------------------------------------------------

        batch=BATCH,

        # ----------------------------------------------------
        # DATA LOADER
        # ----------------------------------------------------

        workers=WORKERS,

        # ----------------------------------------------------
        # CACHE
        # ----------------------------------------------------

        cache=CACHE,

        # ----------------------------------------------------
        # MIXED PRECISION
        # ----------------------------------------------------

        amp=AMP,

        # ----------------------------------------------------
        # OPTIMIZER
        # ----------------------------------------------------

        optimizer=OPTIMIZER,

        lr0=LR0,

        # ----------------------------------------------------
        # LEARNING RATE
        # ----------------------------------------------------

        cos_lr=True,

        # ----------------------------------------------------
        # AUGMENTATION
        # ----------------------------------------------------

        augment=True,

        mosaic=1.0,

        close_mosaic=CLOSE_MOSAIC,

        mixup=0.0,

        # ----------------------------------------------------
        # CLASS LOSS
        # ----------------------------------------------------

        cls=1.0,

        # ----------------------------------------------------
        # VALIDACIÓN
        # ----------------------------------------------------

        val=True,

        # ----------------------------------------------------
        # GUARDADO
        # ----------------------------------------------------

        save=True,

        save_period=5,

        # ----------------------------------------------------
        # GRÁFICAS
        # ----------------------------------------------------

        plots=True,

        # ----------------------------------------------------
        # SEMILLA
        # ----------------------------------------------------

        seed=SEED,

        # ----------------------------------------------------
        # DIRECTORIOS
        # ----------------------------------------------------

        project=str(PROJECT_DIR),

        name=RUN_NAME,

        exist_ok=False,

        # ----------------------------------------------------
        # VERBOSE
        # ----------------------------------------------------

        verbose=True

    )


# ============================================================
# 11. CONTROL DE OOM
# ============================================================

except torch.cuda.OutOfMemoryError as exc:

    gc.collect()
    torch.cuda.empty_cache()

    raise RuntimeError(
        "\n"
        "====================================================\n"
        "CUDA OUT OF MEMORY\n"
        "====================================================\n"
        "La RTX 4060 se ha quedado sin VRAM.\n"
        "\n"
        "Cambia:\n"
        "    BATCH = -1\n"
        "\n"
        "por:\n"
        "    BATCH = 4\n"
        "\n"
        "===================================================="
    ) from exc


# ============================================================
# 12. RESULTADOS
# ============================================================

print()
print("=" * 72)
print("✅ ENTRENAMIENTO TERMINADO")
print("=" * 72)

print()
print("Directorio:")
print(results.save_dir)

print()
print("BEST:")
print(results.save_dir / "weights" / "best.pt")

print()
print("LAST:")
print(results.save_dir / "weights" / "last.pt")

print()
print("CSV:")
print(results.save_dir / "results.csv")

print()
print("PLOTS:")
print(results.save_dir / "results.png")

print("=" * 72)

# [markdown]
#  08.2 retrain
#


# ============================================================
# ACCESSAI - RESUMEN CORRECTO DEL DATASET
# ============================================================

from pathlib import Path

# ------------------------------------------------------------
# RUTA DEL DATASET
# ------------------------------------------------------------


from pathlib import Path
from ultralytics import YOLO

RUN_DIR = Path(results.save_dir)
BEST_MODEL = RUN_DIR / "weights" / "best.pt"

print("RUN_DIR:")
print(RUN_DIR)

print("\nBEST MODEL:")
print(BEST_MODEL)

print("\nExiste:", BEST_MODEL.exists())

if not BEST_MODEL.exists():
    raise FileNotFoundError(
        f"No se encontró best.pt en:\n{BEST_MODEL}"
    )

trained_model = YOLO(str(BEST_MODEL))

print("\n✅ Modelo AccessAI cargado")

print("\nClases:")
for idx, name in trained_model.names.items():
    print(idx, "->", name)
# ------------------------------------------------------------
# EXTENSIONES DE IMAGEN
# ------------------------------------------------------------

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

# ------------------------------------------------------------
# FUNCIÓN PARA CONTAR IMÁGENES
# ------------------------------------------------------------

def contar_imagenes(images_dir):
    if not images_dir.exists():
        return 0

    return sum(
        1
        for archivo in images_dir.iterdir()
        if archivo.is_file()
        and archivo.suffix.lower() in IMAGE_EXTENSIONS
    )


# ------------------------------------------------------------
# FUNCIÓN PARA CONTAR LABELS
# ------------------------------------------------------------

def contar_labels(labels_dir):
    if not labels_dir.exists():
        return 0

    return sum(
        1
        for archivo in labels_dir.iterdir()
        if archivo.is_file()
        and archivo.suffix.lower() == ".txt"
    )


# ------------------------------------------------------------
# MOSTRAR INFORMACIÓN
# ------------------------------------------------------------

print("=" * 70)
print("ACCESSAI - RESUMEN DEL DATASET")
print("=" * 70)

print(f"Dataset: {DATASET_PATH}")
print()

total_imagenes = 0
total_labels = 0
total_originales = 0

# ------------------------------------------------------------
# TRAIN / VALID / TEST
# ------------------------------------------------------------

for split in ["train", "valid", "test"]:

    split_dir = DATASET_PATH / split

    images_dir = split_dir / "images"
    labels_dir = split_dir / "labels"
    labels_originales_dir = split_dir / "labels_originales"

    # Imágenes reales
    num_imagenes = contar_imagenes(images_dir)

    # Labels activas
    num_labels = contar_labels(labels_dir)

    # Labels originales
    num_originales = contar_labels(labels_originales_dir)

    # Acumulados
    total_imagenes += num_imagenes
    total_labels += num_labels
    total_originales += num_originales

    print("-" * 70)
    print(f"{split.upper()}")
    print("-" * 70)

    print(f"Imágenes:          {num_imagenes:,}".replace(",", "."))
    print(f"Labels activas:    {num_labels:,}".replace(",", "."))
    print(f"Labels originales: {num_originales:,}".replace(",", "."))

# ------------------------------------------------------------
# TOTALES
# ------------------------------------------------------------

print()
print("=" * 70)
print("TOTAL DATASET")
print("=" * 70)

print(
    f"Imágenes totales:          "
    f"{total_imagenes:,}".replace(",", ".")
)

print(
    f"Labels activas totales:    "
    f"{total_labels:,}".replace(",", ".")
)

print(
    f"Labels originales totales: "
    f"{total_originales:,}".replace(",", ".")
)

# ------------------------------------------------------------
# PORCENTAJES
# ------------------------------------------------------------

if total_imagenes > 0:

    train_images = contar_imagenes(
        DATASET_PATH / "train" / "images"
    )

    valid_images = contar_imagenes(
        DATASET_PATH / "valid" / "images"
    )

    test_images = contar_imagenes(
        DATASET_PATH / "test" / "images"
    )

    print()
    print("=" * 70)
    print("DISTRIBUCIÓN")
    print("=" * 70)

    print(
        f"Train: {train_images / total_imagenes * 100:.2f}%"
    )

    print(
        f"Valid: {valid_images / total_imagenes * 100:.2f}%"
    )

    print(
        f"Test : {test_images / total_imagenes * 100:.2f}%"
    )

print()
print("=" * 70)
print("✅ COMPROBACIÓN FINAL")
print("=" * 70)

if total_imagenes == total_labels:
    print("✅ Cada imagen tiene una label activa.")
else:
    print(
        "⚠️ Imágenes y labels activas no coinciden."
    )

if total_labels == total_originales:
    print("✅ Labels activas y originales coinciden.")
else:
    print(
        "ℹ️ Labels activas y originales tienen cantidades diferentes."
    )

print("=" * 70)


# [markdown]
#  09. Cargar `best.pt` entrenado

RUN_DIR = Path(results.save_dir)
BEST_MODEL = RUN_DIR / 'weights' / 'best.pt'

if not BEST_MODEL.exists():
    raise FileNotFoundError(f'No se encontró best.pt en:\n{BEST_MODEL}')

trained_model = YOLO(str(BEST_MODEL))
print('RUN_DIR:', RUN_DIR)
print('BEST_MODEL:', BEST_MODEL)
print('\nClases:')
for idx, name in trained_model.names.items():
    print(idx, '->', name)

# [markdown]
#  10. Evaluación en `test`

eval_batch = 8

metrics = trained_model.val(
    data=str(yaml_nuevo_path),
    split='test',
    imgsz=640,
    batch=eval_batch,
    device=DEVICE,
    plots=True
)

print('\n' + '=' * 70)
print('MÉTRICAS TEST')
print('=' * 70)
print(f'mAP50:    {metrics.box.map50:.4f}')
print(f'mAP50-95: {metrics.box.map:.4f}')

# [markdown]
#  11. `results.csv` y curvas de entrenamiento

# ============================================================
# 08.3 - CARGAR Y ANALIZAR RESULTS.CSV
# ============================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. LOCALIZAR EL ÚLTIMO ENTRENAMIENTO
# ============================================================

RUN_DIR = None

# Si existe RUN_DIR y contiene results.csv, utilizarlo
if "RUN_DIR" in globals():

    if RUN_DIR is not None:
        RUN_DIR = Path(RUN_DIR)

        if not (RUN_DIR / "results.csv").exists():
            RUN_DIR = None


# ============================================================
# 2. SI NO EXISTE, BUSCAR AUTOMÁTICAMENTE
# ============================================================

if RUN_DIR is None:

    # --------------------------------------------------------
    # Primero intentar utilizar results.save_dir
    # --------------------------------------------------------

    if "results" in globals():

        if hasattr(results, "save_dir"):

            run_root = Path(results.save_dir).parent.resolve()

        else:

            run_root = ROOT / "AccessAI_Proto3"

    else:

       run_root = Path(results.save_dir).parent.resolve()
    # --------------------------------------------------------
    # Buscar todos los entrenamientos
    # --------------------------------------------------------

    candidates = sorted(
        [
            p
            for p in run_root.glob("*")
            if p.is_dir()
            and (p / "results.csv").exists()
        ],
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )


    # --------------------------------------------------------
    # Comprobar resultados
    # --------------------------------------------------------

    if not candidates:

        raise FileNotFoundError(
            "No se encontró ningún entrenamiento con "
            "'results.csv'.\n\n"
            f"Directorio buscado:\n{run_root}"
        )


    RUN_DIR = candidates[0]


# ============================================================
# 3. RUTA RESULTS.CSV
# ============================================================

results_csv = RUN_DIR / "results.csv"
RESULTS_CSV = results_csv

if not results_csv.exists():

    raise FileNotFoundError(
        f"No existe:\n{results_csv}"
    )


# ============================================================
# 4. CARGAR CSV
# ============================================================

df = pd.read_csv(results_csv)


# ============================================================
# 5. LIMPIAR NOMBRES DE COLUMNAS
# ============================================================

df.columns = df.columns.str.strip()


# ============================================================
# 6. INFORMACIÓN
# ============================================================

print("=" * 72)
print("ACCESSAI - RESULTADOS DEL ENTRENAMIENTO")
print("=" * 72)

print()
print("RUN DIR:")
print(RUN_DIR)

print()
print("RESULTS CSV:")
print(results_csv)

print()
print("ÉPOCAS REGISTRADAS:")
print(len(df))

print()
print("COLUMNAS:")
for columna in df.columns:
    print(f"  - {columna}")

print("=" * 72)

%matplotlib inline

plt.figure(figsize=(12, 6))
plt.plot(df['epoch'], df['train/box_loss'], label='Train Box Loss')
plt.plot(df['epoch'], df['train/cls_loss'], label='Train Class Loss')
plt.plot(df['epoch'], df['train/dfl_loss'], label='Train DFL Loss')
plt.xlabel('Época')
plt.ylabel('Loss')
plt.title('AccessAI - Pérdidas de entrenamiento')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(df['epoch'], df['metrics/mAP50(B)'], label='mAP50')
plt.plot(df['epoch'], df['metrics/mAP50-95(B)'], label='mAP50-95')
plt.xlabel('Época')
plt.ylabel('mAP')
plt.title('AccessAI - Métricas de detección')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(df['epoch'], df['metrics/precision(B)'], label='Precision')
plt.plot(df['epoch'], df['metrics/recall(B)'], label='Recall')
plt.xlabel('Época')
plt.ylabel('Valor')
plt.title('AccessAI - Precision y Recall')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# [markdown]
#  12. Seleccionar imagen de prueba

sample_candidates = [
    ROOT / 'tests' / 'imgs' / 'image.png',
    ROOT / 'tests' / 'imgs' / 'IMG_20170311_205902.jpg',
    ROOT / 'DATA' / 'ROD-Dataset' / 'dataset' / 'test' / 'images' / 'IMG_19187.jpg'
]

image_path = next((p for p in sample_candidates if p.exists()), None)

if image_path is None:
    raise FileNotFoundError('No se encontró ninguna imagen de prueba.')

print('Imagen:', image_path)

# [markdown]
#  13. Inferencia

results_predict = trained_model.predict(
    source=str(image_path),
    conf=0.25,
    imgsz=640,
    device=DEVICE,
    verbose=False
)

result = results_predict[0]
print(f'\nDetecciones encontradas: {len(result.boxes)}')

if result.boxes is not None and len(result.boxes) > 0:
    for idx, box in enumerate(result.boxes, start=1):
        cls_id = int(box.cls[0])
        cls_name = trained_model.names[cls_id]
        confidence = float(box.conf[0])
        coords = box.xyxy[0].tolist()
        print(f'[{idx}] {cls_name} | conf={confidence:.3f} | bbox={coords}')
else:
    print('No se detectaron objetos con conf=0.25.')

# [markdown]
#  14. Guardar y mostrar imagen anotada

import cv2

output_dir = ROOT / 'resultados'
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / 'accessai_resultado.jpg'

annotated = result.plot()
ok = cv2.imwrite(str(output_path), annotated)

if not ok:
    raise IOError(f'No se pudo guardar la imagen en:\n{output_path}')

print('✅ Imagen guardada en:', output_path)

annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(14, 8))
plt.imshow(annotated_rgb)
plt.axis('off')
plt.title('AccessAI - Detección urbana')
plt.tight_layout()
plt.show()

# [markdown]
#  15. Resumen del experimento
#
# Conservar al menos:
# - `best.pt`
# - `last.pt`
# - `results.csv`
# - `confusion_matrix.png`
# - `results.png`
# - imagen anotada de inferencia
# - mAP50 y mAP50-95
# - Precision y Recall
#
# El objetivo del prototipo es medir la capacidad del modelo para detectar las cuatro categorías seleccionadas del ROD-Dataset.

print('=' * 72)
print('ACCESSAI - RESUMEN')
print('=' * 72)
print('Modelo:', BEST_MODEL)
print('Resultados:', RUN_DIR)
print(f'mAP50 test: {metrics.box.map50:.4f}')
print(f'mAP50-95 test: {metrics.box.map:.4f}')
print('CSV:', results_csv)
print('Imagen:', output_path)
print('=' * 72)

