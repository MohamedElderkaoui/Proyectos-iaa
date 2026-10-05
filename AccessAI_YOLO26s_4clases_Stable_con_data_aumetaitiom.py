# [markdown]
#  AccessAI - Prototipo de p urbana
#
# Notebook local para Windows 11 y NVIDIA CUDA. Prepara el ROD-Dataset con el mapeo original de 25 clases a las cuatro categorías del proyecto, entrena YOLO26s con aumentación de datos, evalúa el modelo y permite predecir imágenes de una carpeta local.
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
# El notebook no inicia entrenamiento si PyTorch no detecta CUDA. Los resultados se guardan en una carpeta única bajo `runs/detect/`.

# [markdown]
#  01. Configuración

import gc
import math
import platform
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import pandas as pd
import torch
import ultralytics
import yaml
from ultralytics import YOLO

print("Python:", sys.version)
print("PyTorch:", torch.__version__)
print("CUDA de PyTorch:", torch.version.cuda)
print("CUDA disponible:", torch.cuda.is_available())
print("Ultralytics:", ultralytics.__version__)
print("ok" if torch.cuda.is_available() else "no ok")       
if torch.cuda.is_available():
    gpu_properties = torch.cuda.get_device_properties(0)
    print("GPU:", torch.cuda.get_device_name(0))
    print("VRAM:", round(gpu_properties.total_memory / 1024**3, 2), "GB")
else:
    print("GPU: no detectada por CUDA")

# [markdown]
#  02. Diagnóstico del sistema

print("Sistema operativo:", platform.platform())
print("Carpeta actual del kernel:", Path.cwd())
print("Entorno Python activo:", Path(sys.prefix).name)
if platform.system() != "Windows":
    print("ADVERTENCIA: este notebook está preparado para Windows 11.")
if sys.version_info[:3] != (3, 11, 16):
    print("ADVERTENCIA: la versión objetivo de Python es 3.11.16.")
if torch.__version__ != "2.14.0+cu126":
    print("ADVERTENCIA: la versión objetivo de PyTorch es 2.14.0+cu126.")
if not ultralytics.__version__.startswith("8.4."):
    print("ADVERTENCIA: se espera Ultralytics de la serie 8.4.x.")
if Path(sys.prefix).name != "proyecto_yolo":
    print("ADVERTENCIA: selecciona el kernel Conda 'proyecto_yolo' antes de ejecutar el notebook.")

# [markdown]
#  03. Diagnóstico NVIDIA CUDA

CUDA_AVAILABLE = torch.cuda.is_available()
DEVICE = None
GPU_NAME = "No disponible"
GPU_VRAM_GB = 0.0
FREE_VRAM_GB = 0.0

if CUDA_AVAILABLE:
    DEVICE = 0
    GPU_NAME = torch.cuda.get_device_name(0)
    gpu_properties = torch.cuda.get_device_properties(0)
    GPU_VRAM_GB = gpu_properties.total_memory / 1024**3
    free_bytes, total_bytes = torch.cuda.mem_get_info(0)
    FREE_VRAM_GB = free_bytes / 1024**3

    print("PyTorch:", torch.__version__)
    print("CUDA compilado:", torch.version.cuda)
    print("CUDA disponible:", torch.cuda.is_available())
    print("GPU:", GPU_NAME)
    print("VRAM:", round(GPU_VRAM_GB, 2), "GB")
    print("VRAM libre:", round(FREE_VRAM_GB, 2), "GB")

    if "NVIDIA" not in GPU_NAME.upper():
        CUDA_AVAILABLE = False
        DEVICE = None
        print("ADVERTENCIA: no se detectó una GPU NVIDIA; entrenamiento detenido.")
else:
    print("PyTorch:", torch.__version__)
    print("CUDA compilado:", torch.version.cuda)
    print("CUDA disponible:", torch.cuda.is_available())
    print("ADVERTENCIA: CUDA no está disponible. El entrenamiento queda detenido.")
    print("Soluciona primero el controlador NVIDIA y PyTorch con CUDA.")

nvidia_smi = shutil.which("nvidia-smi")
if nvidia_smi:
    nvidia_report = subprocess.run(
        [nvidia_smi], capture_output=True, text=True, check=False
    )
    print("\nDiagnóstico nvidia-smi:")
    print(nvidia_report.stdout if nvidia_report.stdout else nvidia_report.stderr)
else:
    print("nvidia-smi no está disponible; se omite el diagnóstico opcional.")

# [markdown]
#  04. Rutas del proyecto

ROOT = Path.cwd()
DATASET_PATH = ROOT / "DATA" / "ROD-Dataset" / "dataset"
YAML_ORIGINAL_PATH = DATASET_PATH / "data.yaml"
YAML_FILTERED_PATH = DATASET_PATH / "data_filtrado.yaml"
MODEL_PATH = ROOT / "yolo26s.pt"
RUNS_DIR = ROOT / "runs" / "detect"

print("Raíz del proyecto:", ROOT)
print("Dataset:", DATASET_PATH)
print("Modelo inicial:", MODEL_PATH)

if not (ROOT / "DATA").is_dir():
    raise FileNotFoundError(
        f"No se encuentra la carpeta DATA en {ROOT}. "
        "Abre el notebook desde la raíz del proyecto AccessAI."
    )
if not DATASET_PATH.is_dir():
    raise FileNotFoundError(f"No existe el dataset esperado:\n{DATASET_PATH}")

# [markdown]
#  05. Dataset

if not YAML_ORIGINAL_PATH.is_file():
    raise FileNotFoundError(f"No existe el data.yaml original:\n{YAML_ORIGINAL_PATH}")

with YAML_ORIGINAL_PATH.open("r", encoding="utf-8") as yaml_file:
    CONFIG_ORIGINAL = yaml.safe_load(yaml_file)

for split_name, split_path in (
    ("train", DATASET_PATH / "train" / "images"),
    ("valid", DATASET_PATH / "valid" / "images"),
    ("test", DATASET_PATH / "test" / "images"),
):
    if not split_path.is_dir():
        raise FileNotFoundError(
            f"No se encuentra la carpeta de imágenes del split {split_name}:\n{split_path}"
        )

print("data.yaml original:", YAML_ORIGINAL_PATH)
print("Clases originales declaradas:", CONFIG_ORIGINAL.get("nc"))
print("Splits train/valid/test: encontrados")

# [markdown]
#  06. Verificación de las 4 clases

MAPEO_CLASES = {
    0: 0, 2: 0, 3: 0, 8: 0, 10: 0, 15: 0, 16: 0,
    5: 1, 6: 1, 9: 1, 12: 1, 13: 1, 17: 1, 18: 1,
    19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1,
    4: 2,
    7: 3, 11: 3, 14: 3,
}

NUEVOS_NOMBRES = [
    "Obstaculo_Dinamico",
    "Obstaculo_Fijo",
    "Barrera_Arquitectonica",
    "Infraestructura_Peatonal",
]
NUM_CLASSES = 4

if CONFIG_ORIGINAL.get("nc") != 25:
    raise ValueError(
        "El data.yaml original no declara las 25 clases esperadas por el mapeo actual. "
        "Revisa el dataset antes de continuar."
    )
if len(NUEVOS_NOMBRES) != NUM_CLASSES:
    raise ValueError("La configuración debe conservar exactamente las cuatro clases del proyecto.")

for class_id, class_name in enumerate(NUEVOS_NOMBRES):
    print(f"{class_id}: {class_name}")

CONFIG_FILTRADA = {
    "path": str(DATASET_PATH.resolve()),
    "train": "train/images",
    "val": "valid/images",
    "test": "test/images",
    "nc": NUM_CLASSES,
    "names": NUEVOS_NOMBRES,
}
with YAML_FILTERED_PATH.open("w", encoding="utf-8") as yaml_file:
    yaml.safe_dump(CONFIG_FILTRADA, yaml_file, sort_keys=False, allow_unicode=True)

with YAML_FILTERED_PATH.open("r", encoding="utf-8") as yaml_file:
    CONFIG_FILTRADA = yaml.safe_load(yaml_file)

if CONFIG_FILTRADA.get("nc") != 4:
    raise ValueError("data_filtrado.yaml debe declarar nc: 4.")
if CONFIG_FILTRADA.get("names") != NUEVOS_NOMBRES:
    raise ValueError("Las clases de data_filtrado.yaml no coinciden con las clases del proyecto.")

print("\nYAML de entrenamiento:", YAML_FILTERED_PATH)
print("nc:", CONFIG_FILTRADA["nc"])
print("names:", CONFIG_FILTRADA["names"])

# [markdown]
#  07. Comprobación de imágenes y etiquetas

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def preparar_etiquetas(split_name):
    split_dir = DATASET_PATH / split_name
    active_labels_dir = split_dir / "labels"
    original_labels_dir = split_dir / "labels_originales"
    temporary_labels_dir = split_dir / "labels_filtradas_tmp"

    if not split_dir.is_dir():
        raise FileNotFoundError(f"No existe el split {split_name}:\n{split_dir}")
    if original_labels_dir.is_dir():
        source_dir = original_labels_dir
    elif active_labels_dir.is_dir():
        shutil.copytree(active_labels_dir, original_labels_dir)
        source_dir = original_labels_dir
        print(f"{split_name}: copia de seguridad original creada.")
    else:
        raise FileNotFoundError(
            f"No se encuentran etiquetas en {split_dir}. Se esperaba 'labels' o 'labels_originales'."
        )

    if temporary_labels_dir.exists():
        shutil.rmtree(temporary_labels_dir)
    temporary_labels_dir.mkdir(parents=True)

    class_counts = Counter()
    discarded_counts = Counter()
    for label_file in sorted(source_dir.glob("*.txt")):
        converted_lines = []
        with label_file.open("r", encoding="utf-8") as source_file:
            for line_number, line in enumerate(source_file, start=1):
                parts = line.strip().split()
                if not parts:
                    continue
                is_box = len(parts) == 5
                is_segment = len(parts) >= 7 and (len(parts) - 1) % 2 == 0
                if not is_box and not is_segment:
                    raise ValueError(
                        f"Etiqueta incorrecta en {label_file}, línea {line_number}: "
                        "se esperaba una caja YOLO (5 campos) o un polígono "
                        "(clase y al menos 3 pares x/y)."
                    )
                try:
                    original_class = int(parts[0])
                    box_values = [float(value) for value in parts[1:]]
                except ValueError as error:
                    raise ValueError(
                        f"Etiqueta no numérica en {label_file}, línea {line_number}."
                    ) from error
                if not all(math.isfinite(value) for value in box_values):
                    raise ValueError(
                        f"Coordenada no finita en {label_file}, línea {line_number}."
                    )
                if any(value < 0.0 or value > 1.0 for value in box_values):
                    raise ValueError(
                        f"Coordenadas fuera del rango 0..1 en {label_file}, línea {line_number}."
                    )
                if is_box and (box_values[2] == 0.0 or box_values[3] == 0.0):
                    raise ValueError(
                        f"Caja sin ancho o alto en {label_file}, línea {line_number}."
                    )
                if original_class not in MAPEO_CLASES:
                    if original_class < 0 or original_class >= 25:
                        raise ValueError(
                            f"ID de clase {original_class} no válido en {label_file}, línea {line_number}."
                        )
                    discarded_counts[original_class] += 1
                    continue

                new_class = MAPEO_CLASES[original_class]
                parts[0] = str(new_class)
                converted_lines.append(" ".join(parts))
                class_counts[new_class] += 1

        output_file = temporary_labels_dir / label_file.name
        output_file.write_text(
            "\n".join(converted_lines) + ("\n" if converted_lines else ""),
            encoding="utf-8",
        )

    if active_labels_dir.exists():
        shutil.rmtree(active_labels_dir)
    temporary_labels_dir.replace(active_labels_dir)

    images_dir = split_dir / "images"
    image_count = sum(
        1 for path in images_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    label_count = sum(1 for path in active_labels_dir.glob("*.txt"))
    print(f"{split_name}: {image_count} imágenes, {label_count} archivos de etiquetas.")
    print("  Objetos por clase:", dict(sorted(class_counts.items())))
    print("  Clases originales descartadas:", dict(sorted(discarded_counts.items())))


for split_name in ("train", "valid", "test"):
    preparar_etiquetas(split_name)

print("Preparación terminada. Las etiquetas originales permanecen en labels_originales.")

# [markdown]
#  08. Modelo YOLO26s

if not MODEL_PATH.is_file():
    raise FileNotFoundError(
        f"No se encuentra yolo26s.pt en:\n{MODEL_PATH}\n"
        "Coloca el checkpoint YOLO26s en la raíz del proyecto."
    )

model = YOLO("yolo26s.pt")
print("Modelo cargado:", MODEL_PATH)
print("Clases del dataset:", NUEVOS_NOMBRES)

# [markdown]
#  09. Configuración de entrenamiento
#
# En Jupyter sobre Windows se usa `workers=0` para evitar procesos de datos duplicados o problemas de arranque con multiprocessing. Puede reducir la velocidad de carga frente a `workers=4`, pero prioriza estabilidad.

# ============================================================
# ACCESSAI - 09. CONFIGURACIÓN RÁPIDA RTX 4060 8 GB
# ============================================================

EPOCHS = 40
PATIENCE = 7

IMGSZ = 640

# Batch conservador para YOLO26s en una RTX 4060 Laptop de 8 GB.
# Si se agota la VRAM, reducir a 4.
BATCH = 8

# Más trabajadores para acelerar la alimentación de la GPU.
WORKERS = 4

# Mixed Precision: mantener activado.
AMP = True

# Cargar el dataset en RAM para reducir I/O.
CACHE = "ram"

# Mosaic se desactiva en las últimas 10 épocas.
CLOSE_MOSAIC = 10

OPTIMIZER = "AdamW"

LR0 = 0.001
LRF = 0.01

SEED = 42

# RTX 4060 NVIDIA
DEVICE = 0

# Permitir pequeñas optimizaciones del entrenamiento.
# Reduce el coste de reproducibilidad estricta.
DETERMINISTIC = False

print("=" * 70)
print("ACCESSAI - CONFIGURACIÓN RÁPIDA PARA RTX 4060")
print("=" * 70)

print()
print("Modelo: YOLO26s")
print("GPU: NVIDIA RTX 4060 Laptop GPU 8 GB")

print()
print("Configuración:")
print(f"  Epochs:        {EPOCHS}")
print(f"  Patience:      {PATIENCE}")
print(f"  Image size:    {IMGSZ}")
print(f"  Batch:         {BATCH}")
print(f"  Workers:       {WORKERS}")
print(f"  AMP:           {AMP}")
print(f"  Cache:         {CACHE}")
print(f"  Close mosaic:  {CLOSE_MOSAIC}")
print(f"  Optimizer:     {OPTIMIZER}")
print(f"  LR0:           {LR0}")
print(f"  LRF:           {LRF}")
print(f"  Deterministic: {DETERMINISTIC}")
print(f"  Device:        {DEVICE}")

print()
print("Clases:")
for class_id, class_name in enumerate(NUEVOS_NOMBRES):
    print(f"  {class_id}: {class_name}")

# [markdown]
#  10. Entrenamiento

# ============================================================
# ACCESSAI - 10. ENTRENAMIENTO GPU
# NVIDIA RTX 4060 Laptop GPU 8 GB
# ============================================================

import gc
from datetime import datetime
from pathlib import Path
import datetime
import torch
from ultralytics import YOLO


# ============================================================
# 10.1 COMPROBAR GPU
# ============================================================

print("=" * 70)
print("ACCESSAI - ENTRENAMIENTO GPU")
print("=" * 70)

if not torch.cuda.is_available():
    raise RuntimeError(
        "ENTRENAMIENTO DETENIDO.\n"
        "PyTorch no detecta CUDA.\n"
        "No se utilizará CPU."
    )

DEVICE = 0
GPU_NAME = torch.cuda.get_device_name(DEVICE)

if "NVIDIA" not in GPU_NAME.upper():
    raise RuntimeError(
        f"ENTRENAMIENTO DETENIDO.\n"
        f"GPU detectada: {GPU_NAME}\n"
        "Se requiere una GPU NVIDIA."
    )

GPU_PROPERTIES = torch.cuda.get_device_properties(DEVICE)

GPU_VRAM_GB = (
    GPU_PROPERTIES.total_memory / 1024**3
)

free_bytes, total_bytes = torch.cuda.mem_get_info(DEVICE)

FREE_VRAM_GB = free_bytes / 1024**3
USED_VRAM_GB = (
    (total_bytes - free_bytes) / 1024**3
)

print()
print("PyTorch:", torch.__version__)
print("CUDA PyTorch:", torch.version.cuda)
print("CUDA disponible:", torch.cuda.is_available())
print("GPU:", GPU_NAME)
print(f"VRAM total: {GPU_VRAM_GB:.2f} GB")
print(f"VRAM usada: {USED_VRAM_GB:.2f} GB")
print(f"VRAM libre: {FREE_VRAM_GB:.2f} GB")
print("Dispositivo: cuda:0")


# ============================================================
# 10.2 COMPROBAR DATASET
# ============================================================

if not YAML_FILTERED_PATH.is_file():
    raise FileNotFoundError(
        f"No existe el YAML de entrenamiento:\n"
        f"{YAML_FILTERED_PATH}"
    )

if not DATASET_PATH.is_dir():
    raise FileNotFoundError(
        f"No existe el dataset:\n"
        f"{DATASET_PATH}"
    )

if CONFIG_FILTRADA.get("nc") != 4:
    raise ValueError(
        "El dataset debe contener exactamente 4 clases."
    )

if CONFIG_FILTRADA.get("names") != NUEVOS_NOMBRES:
    raise ValueError(
        "Las clases del YAML no coinciden con las clases de AccessAI."
    )

print()
print("Dataset:", DATASET_PATH)
print("YAML:", YAML_FILTERED_PATH)
print("nc:", CONFIG_FILTRADA["nc"])
print("names:", CONFIG_FILTRADA["names"])


# ============================================================
# 10.3 COMPROBAR MODELO
# ============================================================

if not MODEL_PATH.is_file():
    raise FileNotFoundError(
        f"No se encuentra YOLO26s:\n"
        f"{MODEL_PATH}"
    )

print()
print("Checkpoint:")
print(MODEL_PATH)


# ============================================================
# 10.4 LIMPIAR VRAM
# ============================================================

gc.collect()
torch.cuda.empty_cache()

free_bytes, total_bytes = torch.cuda.mem_get_info(DEVICE)
FREE_VRAM_GB = free_bytes / 1024**3

if FREE_VRAM_GB < 2.0:
    raise RuntimeError(
        f"Solo hay {FREE_VRAM_GB:.2f} GB de VRAM libre.\n"
        "Cierra aplicaciones que utilicen la GPU y vuelve a ejecutar."
    )

print()
print(f"VRAM libre antes del entrenamiento: {FREE_VRAM_GB:.2f} GB")


# ============================================================
# 10.5 CONFIGURACIÓN RÁPIDA
# ============================================================
def num_epochs_for_device(device_name):
    device_name = device_name.lower()
    if "rtx 4060" in device_name:
        return 40
    elif "rtx 4050" in device_name:
        return 35
    elif "rtx 4070" in device_name:
        return 45
    elif "rtx 4080" in device_name:
        return 50
    else:
        return 30  # Valor predeterminado para otros dispositivos
EPOCHS = num_epochs_for_device(GPU_NAME)
PATIENCE = 7

IMGSZ = 640
# ============================================================
# SELECCIÓN AUTOMÁTICA DE BATCH
# SEGÚN GPU + MODELO
# ============================================================

def num_batch_for_device_and_model(device_name, model_name):

    device_name = str(device_name).lower()
    model_name = str(model_name).lower()

    # --------------------------------------------------------
    # YOLO26s
    # --------------------------------------------------------

    if "yolo26s" in model_name:

        if "rtx 4060" in device_name:
            return 8

        elif "rtx 4050" in device_name:
            return 6

        elif "rtx 4070" in device_name:
            return 10

        elif "rtx 4080" in device_name:
            return 14

        elif "rtx 4090" in device_name:
            return 20

        else:
            return 4


    # --------------------------------------------------------
    # YOLO26n
    # --------------------------------------------------------

    elif "yolo26n" in model_name:

        if "rtx 4060" in device_name:
            return 16

        elif "rtx 4050" in device_name:
            return 12

        elif "rtx 4070" in device_name:
            return 20

        elif "rtx 4080" in device_name:
            return 24

        elif "rtx 4090" in device_name:
            return 32

        else:
            return 8


    # --------------------------------------------------------
    # YOLO26m
    # --------------------------------------------------------

    elif "yolo26m" in model_name:

        if "rtx 4060" in device_name:
            return 8

        elif "rtx 4050" in device_name:
            return 6

        elif "rtx 4070" in device_name:
            return 10

        elif "rtx 4080" in device_name:
            return 14

        elif "rtx 4090" in device_name:
            return 20

        else:
            return 4


    # --------------------------------------------------------
    # YOLO26x
    # --------------------------------------------------------

    elif "yolo26x" in model_name:

        if "rtx 4060" in device_name:
            return 4

        elif "rtx 4050" in device_name:
            return 2

        elif "rtx 4070" in device_name:
            return 6

        elif "rtx 4080" in device_name:
            return 8

        elif "rtx 4090" in device_name:
            return 12

        else:
            return 2


    # --------------------------------------------------------
    # OTROS MODELOS
    # --------------------------------------------------------

    else:
        return 8

BATCH = num_batch_for_device_and_model(GPU_NAME, "YOLO26s")

WORKERS = 4

AMP = True
CACHE = "ram"

CLOSE_MOSAIC = 10

# Augmentation is applied by the trainer to training batches only.
HSV_H = 0.015
HSV_S = 0.5
HSV_V = 0.3
TRANSLATE = 0.1
SCALE = 0.3
FLIPLR = 0.5
MOSAIC = 1.0
MIXUP = 0.0

OPTIMIZER = "AdamW"
LR0 = 0.001
LRF = 0.01

SEED = 42

DETERMINISTIC = False


print()
print("=" * 70)
print("CONFIGURACIÓN")
print("=" * 70)

print(f"Epochs:        {EPOCHS}")
print(f"Patience:      {PATIENCE}")
print(f"Image size:    {IMGSZ}")
print(f"Batch:         {BATCH}")
print(f"Workers:       {WORKERS}")
print(f"AMP:           {AMP}")
print(f"Cache:         {CACHE}")
print(f"Close Mosaic:  {CLOSE_MOSAIC}")
print(f"Augmentation:  hsv=({HSV_H}, {HSV_S}, {HSV_V}), translate={TRANSLATE}, scale={SCALE}")
print(f"Augmentation:  fliplr={FLIPLR}, mosaic={MOSAIC}, mixup={MIXUP}")
print(f"Optimizer:     {OPTIMIZER}")
print(f"LR0:           {LR0}")
print(f"LRF:           {LRF}")
print(f"Seed:          {SEED}")
print(f"Deterministic: {DETERMINISTIC}")
print(f"Device:        {DEVICE}")


# ============================================================
# 10.6 PREPARAR RUN
# ============================================================

RUNS_DIR = Path(RUNS_DIR).resolve()
RUNS_DIR.mkdir(parents=True, exist_ok=True)
from datetime import datetime
now_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
RUN_NAME = (
    "AccessAI_YOLO26s_4clases_RTX4060_FAST_"
    + now_str
)

print()
print("Nombre del entrenamiento:")
print(RUN_NAME)


# ============================================================
# 10.7 CARGAR YOLO26s
# ============================================================

model = YOLO(
    str(MODEL_PATH)
)

print()
print("Modelo cargado:")
print(model.names)


# ============================================================
# 10.8 ENTRENAMIENTO
# ============================================================

print()
print("=" * 70)
print("INICIANDO ENTRENAMIENTO EN RTX 4060")
print("=" * 70)

try:

    train_results = model.train(
        data=str(YAML_FILTERED_PATH),

        epochs=EPOCHS,
        imgsz=IMGSZ,
        batch=BATCH,

        device=DEVICE,

        workers=WORKERS,

        amp=AMP,
        cache=CACHE,

        patience=PATIENCE,

        close_mosaic=CLOSE_MOSAIC,
        hsv_h=HSV_H,
        hsv_s=HSV_S,
        hsv_v=HSV_V,
        translate=TRANSLATE,
        scale=SCALE,
        fliplr=FLIPLR,
        mosaic=MOSAIC,
        mixup=MIXUP,

        optimizer=OPTIMIZER,
        lr0=LR0,
        lrf=LRF,

        seed=SEED,
        deterministic=DETERMINISTIC,

        val=True,

        save=True,
        save_period=-1,

        plots=True,

        project=str(RUNS_DIR),
        name=RUN_NAME,
        exist_ok=False,

        verbose=True,
    )

except torch.cuda.OutOfMemoryError as error:

    gc.collect()
    torch.cuda.empty_cache()

    raise RuntimeError(
        "\nCUDA OUT OF MEMORY.\n\n"
        "El entrenamiento NO ha cambiado a CPU.\n\n"
        "Prueba únicamente:\n\n"
        "    BATCH = 4\n\n"
        "y vuelve a ejecutar la sección 10."
    ) from error


# ============================================================
# 10.9 OBTENER RESULTADOS
# ============================================================

RUN_DIR = Path(
    train_results.save_dir
).resolve()

BEST_MODEL = (
    RUN_DIR
    / "weights"
    / "best.pt"
)

LAST_MODEL = (
    RUN_DIR
    / "weights"
    / "last.pt"
)

RESULTS_CSV = (
    RUN_DIR
    / "results.csv"
)


# ============================================================
# 10.10 VERIFICAR ARCHIVOS
# ============================================================

if not RUN_DIR.is_dir():
    raise FileNotFoundError(
        f"No se creó el directorio:\n{RUN_DIR}"
    )

if not BEST_MODEL.is_file():
    raise FileNotFoundError(
        f"No se generó:\n{BEST_MODEL}"
    )

if not LAST_MODEL.is_file():
    raise FileNotFoundError(
        f"No se generó:\n{LAST_MODEL}"
    )


# ============================================================
# 10.11 INFORMACIÓN FINAL
# ============================================================

print()
print("=" * 70)
print("ENTRENAMIENTO TERMINADO")
print("=" * 70)

print()
print("GPU:", GPU_NAME)
print("Device: cuda:0")

print()
print("Run:")
print(RUN_DIR)

print()
print("Best model:")
print(BEST_MODEL)

print()
print("Last model:")
print(LAST_MODEL)

print()
print("Results CSV:")
print(RESULTS_CSV)


# ============================================================
# 10.12 VRAM FINAL
# ============================================================

free_bytes, total_bytes = torch.cuda.mem_get_info(DEVICE)

FREE_VRAM_GB = free_bytes / 1024**3
USED_VRAM_GB = (
    (total_bytes - free_bytes) / 1024**3
)

print()
print(f"VRAM usada: {USED_VRAM_GB:.2f} GB")
print(f"VRAM libre: {FREE_VRAM_GB:.2f} GB")


# ============================================================
# 10.13 LIMPIEZA
# ============================================================

del model

gc.collect()
torch.cuda.empty_cache()

print()
print("✅ Entrenamiento completado.")
print("✅ GPU utilizada:", GPU_NAME)
print("✅ best.pt generado.")
print("✅ last.pt generado.")
print("✅ No se utilizó CPU.")

# [markdown]
#  11. Validación

# Ejecuta la evaluación con el checkpoint YOLO26s generado por esta copia.
# si train_results ya está entrenado

if not BEST_MODEL.is_file():
    raise FileNotFoundError(f"No se encuentra el mejor modelo entrenado:\n{BEST_MODEL}")

trained_model = YOLO(str(BEST_MODEL))
EVAL_DIR = RUN_DIR / "test_evaluation"

try:
    metrics = trained_model.val(
        data=str(YAML_FILTERED_PATH),
        split="test",
        imgsz=IMGSZ,
        batch=BATCH,
        device=DEVICE,
        workers=WORKERS,
        plots=True,
        project=str(RUN_DIR),
        name="test_evaluation",
        exist_ok=False,
        verbose=True,
    )
except torch.cuda.OutOfMemoryError as error:
    gc.collect()
    torch.cuda.empty_cache()
    raise RuntimeError(
        "CUDA out of memory durante la evaluación de test. "
        "Reduce eval batch a 4 y vuelve a ejecutar la celda de validación."
    ) from error

print("Evaluación de test guardada en:", EVAL_DIR)
print("Modelo evaluado:", BEST_MODEL)

# [markdown]
#  12. Métricas

PRECISION = float(metrics.box.mp)
RECALL = float(metrics.box.mr)
MAP50 = float(metrics.box.map50)
MAP50_95 = float(metrics.box.map)

print("=" * 60)
print("MÉTRICAS GLOBALES EN TEST")
print("=" * 60)
print(f"Precision: {PRECISION:.4f}")
print(f"Recall:    {RECALL:.4f}")
print(f"mAP50:     {MAP50:.4f}")
print(f"mAP50-95:  {MAP50_95:.4f}")

class_precision = metrics.box.p
class_recall = metrics.box.r
class_map50 = metrics.box.ap50
class_map = metrics.box.ap
class_indices = metrics.box.ap_class_index

print("\nMÉTRICAS POR CLASE")
for metric_index, class_id in enumerate(class_indices):
    class_name = NUEVOS_NOMBRES[int(class_id)]
    print(
        f"{class_name}: Precision={class_precision[metric_index]:.4f}, "
        f"Recall={class_recall[metric_index]:.4f}, "
        f"mAP50={class_map50[metric_index]:.4f}, "
        f"mAP50-95={class_map[metric_index]:.4f}"
    )

# [markdown]
#  13. Predicción

# ============================================================
# ACCESSAI - SELECCIÓN DE CARPETA DE IMÁGENES DE PRUEBA
# ============================================================
#
# Función:
#   1. Detectar el directorio base del proyecto.
#   2. Buscar automáticamente tests/imgs.
#   3. Si no existe, usar DATASET_PATH/test/images.
#   4. Abrir un selector de carpetas de Windows.
#   5. Obtener todas las imágenes compatibles.
#   6. Crear IMAGE_DIR e IMAGE_PATHS.
#
# No realiza inferencia.
# No modifica imágenes.
# ============================================================

from tkinter import Tk, filedialog
from pathlib import Path


# ============================================================
# 1. EXTENSIONES DE IMAGEN COMPATIBLES
# ============================================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
    ".tif",
    ".tiff",
}


# ============================================================
# 2. DIRECTORIO BASE DEL PROYECTO
# ============================================================

if "__file__" not in globals():
    BOOT = Path.cwd().resolve()
else:
    BOOT = Path(__file__).parent.resolve()

print("=" * 70)
print("ACCESSAI - SELECCIÓN DE IMÁGENES")
print("=" * 70)

print()
print("Directorio base:")
print(BOOT)


# ============================================================
# 3. DATASET_PATH
# ============================================================
#
# Si DATASET_PATH ya existe en una celda anterior, se conserva.
# Si no existe, se intenta localizar automáticamente.
# ============================================================

if "DATASET_PATH" not in globals():

    posibles_dataset = [
        BOOT / "DATA",
        BOOT / "DATASET",
        BOOT / "dataset",
        BOOT.parent / "DATA",
        BOOT.parent / "DATASET",
        BOOT.parent / "dataset",
    ]

    DATASET_PATH = None

    for candidato in posibles_dataset:

        if candidato.is_dir():

            DATASET_PATH = candidato.resolve()

            print()
            print("DATASET_PATH detectado automáticamente:")
            print(DATASET_PATH)

            break


# ============================================================
# 4. CARPETA PREDETERMINADA
# ============================================================

DEFAULT_IMAGE_DIR = BOOT / "tests" / "imgs"


# ============================================================
# 5. FALLBACK AL DATASET DE TEST
# ============================================================

if not DEFAULT_IMAGE_DIR.is_dir():

    if "DATASET_PATH" in globals() and DATASET_PATH is not None:

        dataset_test_dir = (
            Path(DATASET_PATH)
            / "test"
            / "images"
        )

        if dataset_test_dir.is_dir():

            DEFAULT_IMAGE_DIR = dataset_test_dir

        else:

            print()
            print(
                "ADVERTENCIA: no se encontró "
                "DATASET_PATH/test/images"
            )

    else:

        print()
        print(
            "ADVERTENCIA: DATASET_PATH no está definido "
            "y no existe tests/imgs."
        )


# ============================================================
# 6. COMPROBAR CARPETA PREDETERMINADA
# ============================================================

print()
print("Carpeta predeterminada:")
print(DEFAULT_IMAGE_DIR)


# ============================================================
# 7. SELECTOR DE CARPETAS DE WINDOWS
# ============================================================

folder_picker = Tk()

folder_picker.withdraw()

folder_picker.attributes("-topmost", True)

try:

    selected_folder = filedialog.askdirectory(
        title="Selecciona la carpeta de imágenes de prueba",
        initialdir=str(DEFAULT_IMAGE_DIR),
        mustexist=True,
    )

finally:

    folder_picker.destroy()


# ============================================================
# 8. DETERMINAR CARPETA FINAL
# ============================================================

if selected_folder:

    IMAGE_DIR = Path(selected_folder).resolve()

    print()
    print("✅ Carpeta seleccionada:")
    print(IMAGE_DIR)

else:

    IMAGE_DIR = DEFAULT_IMAGE_DIR.resolve()

    print()
    print(
        "ℹ️ No se seleccionó ninguna carpeta."
    )

    print(
        "Se utilizará la carpeta predeterminada:"
    )

    print(IMAGE_DIR)


# ============================================================
# 9. COMPROBAR QUE EXISTE
# ============================================================

if not IMAGE_DIR.is_dir():

    raise FileNotFoundError(
        f"\nNo existe la carpeta de imágenes:\n"
        f"{IMAGE_DIR}"
    )


# ============================================================
# 10. BUSCAR IMÁGENES
# ============================================================

IMAGE_PATHS = sorted(
    [
        path
        for path in IMAGE_DIR.iterdir()
        if (
            path.is_file()
            and path.suffix.lower() in IMAGE_EXTENSIONS
        )
    ],
    key=lambda path: path.name.lower()
)


# ============================================================
# 11. COMPROBAR QUE HAY IMÁGENES
# ============================================================

if not IMAGE_PATHS:

    raise FileNotFoundError(
        f"\nNo hay imágenes compatibles en:\n"
        f"{IMAGE_DIR}\n\n"
        f"Extensiones admitidas:\n"
        f"{', '.join(sorted(IMAGE_EXTENSIONS))}"
    )


# ============================================================
# 12. RESULTADO
# ============================================================

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)

print()
print(f"Carpeta de imágenes: {IMAGE_DIR}")
print(f"Imágenes encontradas: {len(IMAGE_PATHS)}")


# ============================================================
# 13. MOSTRAR IMÁGENES ENCONTRADAS
# ============================================================

print()
print("Lista de imágenes:")

for index, image_path in enumerate(IMAGE_PATHS, start=1):

    print(
        f"{index:03d}. {image_path.name}"
    )


# ============================================================
# 14. RESUMEN DE VARIABLES PARA LAS SIGUIENTES CELDAS
# ============================================================

print()
print("=" * 70)
print("VARIABLES PREPARADAS")
print("=" * 70)

print()
print("IMAGE_DIR:")
print(IMAGE_DIR)

print()
print("IMAGE_PATHS:")
print(f"{len(IMAGE_PATHS)} imágenes listas para inferencia.")

print()
print("✅ Celda completada correctamente.")

# [markdown]
# ## Ejecutar predicción

from datetime import datetime
from pathlib import Path
from tkinter import Tk, filedialog
import gc

import torch
from ultralytics import YOLO

CONFIDENCE = 0.25
IMGSZ = 640
PREDICTION_DEVICE = 0 if torch.cuda.is_available() else "cpu"
ROOT = Path.cwd().resolve()
RUNS_DIR = ROOT / "runs" / "detect"

print("ACCESSAI - INFERENCIA YOLO26s")
print("CUDA disponible:", torch.cuda.is_available())
print("Dispositivo:", PREDICTION_DEVICE)
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("ADVERTENCIA: inferencia en CPU.")

if "IMAGE_DIR" in globals() and Path(IMAGE_DIR).is_dir():
    IMAGE_DIR = Path(IMAGE_DIR).resolve()
else:
    default_image_dir = ROOT / "tests" / "imgs"
    if not default_image_dir.is_dir() and "DATASET_PATH" in globals():
        default_image_dir = Path(DATASET_PATH) / "test" / "images"
    folder_picker = Tk()
    folder_picker.withdraw()
    folder_picker.attributes("-topmost", True)
    try:
        selected_folder = filedialog.askdirectory(
            title="Selecciona la carpeta de imágenes de prueba",
            initialdir=str(default_image_dir),
            mustexist=True,
        )
    finally:
        folder_picker.destroy()
    if not selected_folder:
        raise FileNotFoundError("No se seleccionó una carpeta de imágenes.")
    IMAGE_DIR = Path(selected_folder).resolve()

if not IMAGE_DIR.is_dir():
    raise FileNotFoundError(f"No existe la carpeta de imágenes:\n{IMAGE_DIR}")

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
IMAGE_PATHS = [
    path for path in IMAGE_DIR.iterdir()
    if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
]
IMAGE_PATHS.sort()
if not IMAGE_PATHS:
    raise FileNotFoundError(f"No hay imágenes compatibles en:\n{IMAGE_DIR}")

RUNS_DIR.mkdir(parents=True, exist_ok=True)
model_candidates = []
existing_model = globals().get("BEST_MODEL")
if existing_model is not None:
    existing_model = Path(existing_model).resolve()
    if existing_model.is_file() and "YOLO26S" in str(existing_model).upper():
        model_candidates.append(existing_model)

for candidate in RUNS_DIR.glob("AccessAI_YOLO26s_4clases_RTX4060_*/weights/best.pt"):
    candidate = candidate.resolve()
    if candidate.is_file() and candidate not in model_candidates:
        model_candidates.append(candidate)

model_candidates.sort()
if model_candidates:
    BEST_MODEL = model_candidates[-1]
    print("Modelo YOLO26s más reciente:", BEST_MODEL)
else:
    print("No se encontró automáticamente un best.pt de una ejecución YOLO26s.")
    model_picker = Tk()
    model_picker.withdraw()
    model_picker.attributes("-topmost", True)
    try:
        selected_model = filedialog.askopenfilename(
            title="Selecciona best.pt de una ejecución YOLO26s",
            initialdir=str(RUNS_DIR),
            filetypes=[("Modelo PyTorch", "*.pt"), ("Todos los archivos", "*.*")],
        )
    finally:
        model_picker.destroy()
    if not selected_model:
        raise FileNotFoundError("No se seleccionó un checkpoint YOLO26s.")
    BEST_MODEL = Path(selected_model).resolve()
    if not BEST_MODEL.is_file() or "YOLO26S" not in str(BEST_MODEL).upper():
        raise ValueError(
            "Checkpoint no aceptado: selecciona best.pt dentro de una ejecución "
            "cuyo nombre incluya YOLO26s."
        )

trained_model = YOLO(str(BEST_MODEL))
print("Clases del modelo:", trained_model.names)
print("Imágenes:", len(IMAGE_PATHS))

PREDICTION_NAME = "AccessAI_YOLO26s_predictions_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
PREDICTION_DIR = RUNS_DIR / PREDICTION_NAME

gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()

try:
    results_predict = trained_model.predict(
        source=str(IMAGE_DIR),
        conf=CONFIDENCE,
        imgsz=IMGSZ,
        device=PREDICTION_DEVICE,
        project=str(RUNS_DIR),
        name=PREDICTION_NAME,
        exist_ok=False,
        save=True,
        verbose=False,
    )
except torch.cuda.OutOfMemoryError as error:
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    raise RuntimeError(
        "CUDA out of memory durante la inferencia. Cierra otras aplicaciones que usen GPU e inténtalo de nuevo."
    ) from error

CLASS_COUNTS = {}
TOTAL_DETECTIONS = 0
for image_result in results_predict:
    boxes = image_result.boxes
    detection_count = len(boxes) if boxes is not None else 0
    TOTAL_DETECTIONS += detection_count
    print(f"{Path(image_result.path).name}: {detection_count} detecciones")
    if boxes is not None and boxes.cls is not None:
        for class_id in boxes.cls.tolist():
            class_id = int(class_id)
            if isinstance(trained_model.names, dict):
                class_name = trained_model.names.get(class_id, str(class_id))
            else:
                class_name = trained_model.names[class_id]
            CLASS_COUNTS[class_name] = CLASS_COUNTS.get(class_name, 0) + 1

print("Total de detecciones:", TOTAL_DETECTIONS)
print("Detecciones por clase:", CLASS_COUNTS)
print("Predicciones guardadas en:", PREDICTION_DIR)
if torch.cuda.is_available():
    free_bytes, total_bytes = torch.cuda.mem_get_info(0)
    print(f"VRAM usada: {(total_bytes - free_bytes) / 1024**3:.2f} GB / {total_bytes / 1024**3:.2f} GB")

# Configuración compatible con scripts de Python: no se usa magia de notebook.
try:
    import matplotlib
    matplotlib.use("Agg", force=True)
except Exception:
    pass


# [markdown]
#  14. Evaluación visual

# Las vistas y métricas se generarán al ejecutar este notebook con YOLO26s.
# Mostrar una predicción ya disponible; generar una vista previa solo si hace falta.
if "results_predict" in globals() and results_predict:
    first_result = results_predict[0]
    annotated = first_result.plot()
    if annotated is not None:
        annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(14, 8))
        plt.imshow(annotated_rgb)
        plt.axis("off")
        plt.title(f"AccessAI - {Path(first_result.path).name}")
        plt.tight_layout()
        plt.show()
    else:
        print("No se pudo generar la vista anotada del primer resultado.")
elif "trained_model" in globals() and "IMAGE_DIR" in globals():
    print("No hay resultados de inferencia; se genera una vista previa sin guardar archivos.")
    preview_results = trained_model.predict(
        source=str(IMAGE_DIR),
        conf=0.25,
        imgsz=640,
        device=0 if torch.cuda.is_available() else "cpu",
        project=str(RUNS_DIR) if "RUNS_DIR" in globals() else str(Path.cwd()),
        name="preview_annotated",
        exist_ok=True,
        save=False,
        verbose=False,
    )
    if preview_results:
        first_result = preview_results[0]
        annotated = first_result.plot()
        if annotated is not None:
            annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            plt.figure(figsize=(14, 8))
            plt.imshow(annotated_rgb)
            plt.axis("off")
            plt.title(f"AccessAI - {Path(first_result.path).name}")
            plt.tight_layout()
            plt.show()
        else:
            print("No se pudo crear la vista previa anotada.")
    else:
        print("La vista previa no devolvió resultados.")
else:
    print("No hay resultados ni modelo cargado para mostrar una imagen anotada.")

# Limitar la lectura de métricas al run actual para no mostrar resultados antiguos.
run_directory = None
if globals().get("RUN_DIR") is not None:
    candidate_run = Path(RUN_DIR).resolve()
    if candidate_run.is_dir():
        run_directory = candidate_run
elif globals().get("BEST_MODEL") is not None:
    candidate_model = Path(BEST_MODEL).resolve()
    if candidate_model.is_file() and candidate_model.name.lower() == "best.pt":
        run_directory = candidate_model.parent.parent

results_csv = run_directory / "results.csv" if run_directory is not None else None
if results_csv is not None and results_csv.is_file():
    training_history = pd.read_csv(results_csv)
    training_history.columns = training_history.columns.str.strip()

    loss_columns = [
        column for column in ("train/box_loss", "train/cls_loss", "train/dfl_loss")
        if column in training_history.columns
    ]
    if loss_columns and "epoch" in training_history.columns:
        plt.figure(figsize=(12, 6))
        for column in loss_columns:
            plt.plot(training_history["epoch"], training_history[column], label=column)
        plt.xlabel("Época")
        plt.ylabel("Loss")
        plt.title("Pérdidas de entrenamiento")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    map_columns = [
        column for column in ("metrics/mAP50(B)", "metrics/mAP50-95(B)")
        if column in training_history.columns
    ]
    if map_columns and "epoch" in training_history.columns:
        plt.figure(figsize=(12, 6))
        for column in map_columns:
            plt.plot(training_history["epoch"], training_history[column], label=column)
        plt.xlabel("Época")
        plt.ylabel("mAP")
        plt.title("Métricas de validación por época")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
else:
    print("No hay results.csv para una ejecución identificada; no se usarán métricas de otro run.")

# EVAL_DIR puede no existir si no se ejecutó el entrenamiento y la validación.
evaluation_dir = None
if globals().get("EVAL_DIR") is not None:
    candidate_evaluation_dir = Path(EVAL_DIR).resolve()
    if candidate_evaluation_dir.is_dir():
        evaluation_dir = candidate_evaluation_dir
elif run_directory is not None:
    candidate_evaluation_dir = run_directory / "test_evaluation"
    if candidate_evaluation_dir.is_dir():
        evaluation_dir = candidate_evaluation_dir

if evaluation_dir is not None:
    confusion_matrix = evaluation_dir / "confusion_matrix.png"
    if confusion_matrix.is_file():
        confusion_image = cv2.imread(str(confusion_matrix))
        if confusion_image is None:
            raise IOError(f"No se pudo abrir la matriz de confusión:\n{confusion_matrix}")
        plt.figure(figsize=(10, 8))
        plt.imshow(cv2.cvtColor(confusion_image, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.title("Matriz de confusión en test")
        plt.tight_layout()
        plt.show()
    else:
        print("No se encontró la matriz de confusión:", confusion_matrix)
else:
    print("No hay carpeta de evaluación de test disponible; se omite la matriz de confusión.")

# [markdown]
#  15. Resumen final

if RESULTS_CSV.is_file():
    EPOCHS_COMPLETED = len(pd.read_csv(RESULTS_CSV))
else:
    EPOCHS_COMPLETED = EPOCHS

print("=" * 60)
print("ACCESSAI - RESUMEN DEL ENTRENAMIENTO")
print("=" * 60)
print("Modelo:", "YOLO26s")
print("Clases:", ", ".join(NUEVOS_NOMBRES))
print("GPU:", GPU_NAME)
print("VRAM:", f"{GPU_VRAM_GB:.2f} GB")
print("CUDA:", f"{torch.version.cuda} (disponible={torch.cuda.is_available()})")
print("Épocas:", EPOCHS_COMPLETED)
print("Imagen:", IMAGE_DIR)
print("Batch:", BATCH)
print("Precision:", f"{PRECISION:.4f}")
print("Recall:", f"{RECALL:.4f}")
print("mAP50:", f"{MAP50:.4f}")
print("mAP50-95:", f"{MAP50_95:.4f}")
print("Best model:", BEST_MODEL)
print("Run:", RUN_DIR)
print("=" * 60)

# [markdown]
#  16 .inferacia video

import os
from pathlib import Path
from tkinter import Tk, filedialog
from datetime import datetime

# Ejecutar después de cargar el checkpoint YOLO26s de este notebook.
# Reutiliza `trained_model`, `RUNS_DIR`, `BEST_MODEL`, `torch` y `YOLO` ya cargados en el notebook.

VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".wmv", ".webm", ".mpeg", ".mpg"}


def _safe_path(value, *, create_parents=False):
    if value is None:
        raise ValueError("La ruta es nula.")

    raw = str(value).strip()
    if not raw or "\x00" in raw:
        raise ValueError(f"Ruta no válida: {value!r}")

    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path

    if os.name == "nt":
        drive = path.drive
        cleaned_parts = []
        for part in path.parts:
            if part in ("/", "\\"):
                continue
            # Evita nombres de dispositivos reservados y caracteres no válidos en Windows.
            if part.lower() in {"con", "prn", "aux", "nul"}:
                part = f"_{part}"
            cleaned = "".join(ch for ch in part if ch not in '<>:"|?*')
            if cleaned:
                cleaned_parts.append(cleaned)
        if drive:
            path = Path(drive, *cleaned_parts)
        else:
            path = Path(*cleaned_parts)

    if create_parents:
        path.parent.mkdir(parents=True, exist_ok=True)

    return path.resolve(strict=False)


ROOT = _safe_path(Path.cwd().resolve())
RUNS_DIR = _safe_path(globals().get("RUNS_DIR", ROOT / "runs" / "detect"), create_parents=True)

if "trained_model" not in globals():
    if "BEST_MODEL" not in globals():
        raise FileNotFoundError("No existe `trained_model` ni `BEST_MODEL` en el notebook. Carga primero el modelo entrenado.")
    trained_model = YOLO(str(_safe_path(BEST_MODEL)))

# Selector de video
video_picker = Tk()
video_picker.withdraw()
video_picker.attributes("-topmost", True)
try:
    video_path = filedialog.askopenfilename(
        title="Selecciona un video para inferencia",
        initialdir=str(ROOT),
        filetypes=[("Video", " ".join(f"*{ext}" for ext in sorted(VIDEO_EXTENSIONS))), ("Todos los archivos", "*.*")],
    )
finally:
    video_picker.destroy()

if not video_path:
    raise FileNotFoundError("No se seleccionó ningún video para inferencia.")

VIDEO_PATH = _safe_path(video_path)
if not VIDEO_PATH.is_file():
    raise FileNotFoundError(f"No existe el video:\n{VIDEO_PATH}")
if VIDEO_PATH.suffix.lower() not in VIDEO_EXTENSIONS:
    raise ValueError(f"Extensión no soportada: {VIDEO_PATH.suffix}. Usa un video compatible.")

CONFIDENCE = 0.25
IMGSZ = 640
PREDICTION_DEVICE = 0 if torch.cuda.is_available() else "cpu"

PREDICTION_NAME = "AccessAI_video_predictions_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
PREDICTION_DIR = _safe_path(RUNS_DIR / PREDICTION_NAME, create_parents=True)

print("=" * 70)
print("ACCESSAI - INFERENCIA SOBRE VIDEO")
print("=" * 70)
print("Video:", VIDEO_PATH)
print("Modelo:", getattr(trained_model, "ckpt_path", "modelo en memoria"))
print("Dispositivo:", PREDICTION_DEVICE)
print("Salida:", PREDICTION_DIR)

results_video = trained_model.predict(
    source=str(VIDEO_PATH),
    conf=CONFIDENCE,
    imgsz=IMGSZ,
    device=PREDICTION_DEVICE,
    project=str(RUNS_DIR),
    name=PREDICTION_NAME,
    exist_ok=False,
    save=True,
    verbose=False,
)

print()
print("✅ Inferencia finalizada.")
print("📁 Carpeta de salida:", PREDICTION_DIR)
print("🔢 Frames procesados:", len(results_video) if isinstance(results_video, list) else "resultado no listado")

# Muestra resumen por clase si hay detecciones
class_counts = {}
total_detections = 0

for frame_result in results_video:
    boxes = frame_result.boxes
    if boxes is not None:
        total_detections += len(boxes)
        for cls_id in boxes.cls.tolist():
            cls_id = int(cls_id)
            class_name = trained_model.names.get(cls_id, str(cls_id)) if isinstance(trained_model.names, dict) else trained_model.names[cls_id]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

print()
print("Detecciones totales:", total_detections)
print("Detecciones por clase:", class_counts)

# Si quieres abrir la primera vista anotada del video
try:
    first_result = results_video[0]
    annotated = first_result.plot()
    if annotated is not None:
        annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(14, 8))
        plt.imshow(annotated_rgb)
        plt.axis("off")
        plt.title(f"AccessAI - {VIDEO_PATH.name}")
        plt.tight_layout()
        plt.show()
    else:
        print("No se pudo renderizar una vista anotada del primer frame del video.")
except Exception as exc:
    print(f"No se pudo visualizar la vista previa del video: {exc}")

!python -m pip install flask flask-cors streamlit 







