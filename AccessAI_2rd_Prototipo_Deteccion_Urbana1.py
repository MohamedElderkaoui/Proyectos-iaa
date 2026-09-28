# [markdown]
# AccessAI - Prototipo de detección urbana
#
# Este cuaderno demuestra la base del proyecto AccessAI:
#
# 1. Comprobar entorno y GPU.
# 2. Preparar el ROD-Dataset.
# 3. Filtrar y remapear las clases a 4 categorías.
# 4. Crear un `data_filtrado.yaml`.
# 5. Entrenar YOLO26x en una GPU disponible.
# 6. Cargar `best.pt`.
# 7. Evaluar el modelo en `test`.
# 8. Mostrar curvas de entrenamiento.
# 9. Ejecutar inferencia sobre una imagen y guardar el resultado.
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
# > Importante: las etiquetas originales se conservan en `labels_originales` y nunca se usan como fuente para un segundo remapeo.
#
# ## Alcance de este experimento
#
# Se utiliza el ROD-Dataset con el mapeo de cuatro categorías ya definido en el proyecto. Este esquema agrupa clases genéricas y no equivale a las clases `sidewalk` y `curbramp`. Por tanto, los resultados de este prototipo no validan accesibilidad ni demuestran que un espacio sea accesible o inaccesible.
#

# [markdown]
#  01. Entorno y GPU
#
# Comprueba PyTorch y la disponibilidad de GPU antes de comenzar el entrenamiento.
#

# ============================================================
# ACCESSAI - 01. ENTORNO Y GPU
# ============================================================

from pathlib import Path
import os
import torch

print("=" * 70)
print("ACCESSAI - ENTORNO")
print("=" * 70)

print(f"PyTorch: {torch.__version__}")
print(f"CUDA disponible: {torch.cuda.is_available()}")
print(f"CUDA de PyTorch: {torch.version.cuda}")
print(f"HIP: {torch.version.hip}")

if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU count: {torch.cuda.device_count()}")

    props = torch.cuda.get_device_properties(0)

    print(
        f"Memoria GPU: "
        f"{props.total_memory / 1024**3:.2f} GB"
    )

    print(
        f"Compute capability: "
        f"{props.major}.{props.minor}"
    )

    print(
        f"Memoria reservada actualmente: "
        f"{torch.cuda.memory_reserved(0) / 1024**3:.2f} GB"
    )

    print(
        f"Memoria asignada actualmente: "
        f"{torch.cuda.memory_allocated(0) / 1024**3:.2f} GB"
    )
else:
   print("Este cuaderno requiere una GPU disponible en PyTorch. Selecciona un kernel con soporte GPU antes de continuar.")

print("=" * 70)


# [markdown]
#  02. Comprobar Ultralytics
#

# ============================================================
# ACCESSAI - 02. ULTRALYTICS
# ============================================================

import ultralytics

print("Ultralytics:", ultralytics.__version__)

!python -m pip show ultralytics


# [markdown]
#  03. Configuración del dataset
#
# Se usa una ruta relativa al proyecto para que el notebook sea más portable en Windows.
#

# ============================================================
# ACCESSAI - 03. CONFIGURACIÓN DATASET
# ============================================================

from pathlib import Path
import os
import shutil
import yaml
from collections import Counter

ROOT = Path.cwd()

DATASET_PATH = ROOT / "DATA" / "ROD-Dataset" / "dataset"

yaml_original_path = DATASET_PATH / "data.yaml"
yaml_nuevo_path = DATASET_PATH / "data_filtrado.yaml"

print("Dataset:")
print(DATASET_PATH)

print("\nExiste dataset:", DATASET_PATH.exists())
print("Existe data.yaml:", yaml_original_path.exists())

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"edNo existe el dataset:\n{DATASET_PATH}"
    )

if not yaml_original_path.exists():
    raise FileNotFoundError(
        f"No existe:\n{yaml_original_path}"
    )


# [markdown]
#  04. Mapeo de clases del ROD-Dataset
#

# ============================================================
# ACCESSAI - 04. MAPEO AMPLIADO DE CLASES
# ============================================================

"""
Mapeo de las 25 clases originales del ROD-Dataset hacia
4 categorías agregadas definidas para este experimento.

Clases originales:
0  Bike
1  Building
2  Car
3  Person
4  Stairs
5  Traffic sign
6  Electrical Pole
7  Road
8  Motorcycle
9  Dustbin
10 Dog
11 Manhole
12 Tree
13 Guard rail
14 Pedestrian crosswalk
15 Truck
16 Bus
17 Bench
18 Traffic Cone
19 Fire hydrant
20 Teraffic Barrel
21 Plant Pot
22 Electrical Box
23 Chair
24 Bicycle Rack

Building (ID 1) se conserva fuera del entrenamiento porque
representa principalmente contexto urbano y no una barrera
de accesibilidad directa.

Las etiquetas originales se conservan en `labels_originales`.
"""


# ------------------------------------------------------------
# 0. OBSTÁCULO DINÁMICO
# ------------------------------------------------------------
# Elementos móviles que pueden ocupar o bloquear el espacio
# de circulación peatonal.

# ------------------------------------------------------------
# 1. OBSTÁCULO FIJO
# ------------------------------------------------------------
# Elementos urbanos que pueden reducir el espacio disponible,
# generar obstáculos o interferir con la circulación.

# ------------------------------------------------------------
# 2. BARRERA ARQUITECTÓNICA
# ------------------------------------------------------------
# Elementos que pueden dificultar directamente la movilidad.

# ------------------------------------------------------------
# 3. INFRAESTRUCTURA PEATONAL
# ------------------------------------------------------------
# Elementos asociados a la infraestructura o al espacio peatonal.


MAPEO_CLASES = {

    # ========================================================
    # 0 -> Obstaculo_Dinamico
    # ========================================================

    0: 0,     # Bike
    2: 0,     # Car
    3: 0,     # Person
    8: 0,     # Motorcycle
    10: 0,    # Dog
    15: 0,    # Truck
    16: 0,    # Bus


    # ========================================================
    # 1 -> Obstaculo_Fijo
    # ========================================================

    5: 1,     # Traffic sign
    6: 1,     # Electrical Pole
    9: 1,     # Dustbin
    12: 1,    # Tree
    13: 1,    # Guard rail
    17: 1,    # Bench
    18: 1,    # Traffic Cone
    19: 1,    # Fire hydrant
    20: 1,    # Teraffic Barrel
    21: 1,    # Plant Pot
    22: 1,    # Electrical Box
    23: 1,    # Chair
    24: 1,    # Bicycle Rack


    # ========================================================
    # 2 -> Barrera_Arquitectonica
    # ========================================================

    4: 2,     # Stairs


    # ========================================================
    # 3 -> Infraestructura_Peatonal
    # ========================================================

    7: 3,     # Road
    11: 3,    # Manhole
    14: 3     # Pedestrian crosswalk
}


# ============================================================
# NOMBRES DE LAS CLASES FINALES
# ============================================================

NUEVOS_NOMBRES = [
    "Obstaculo_Dinamico",
    "Obstaculo_Fijo",
    "Barrera_Arquitectonica",
    "Infraestructura_Peatonal"
]

NUM_CLASSES = len(NUEVOS_NOMBRES)


# ============================================================
# CLASES EXCLUIDAS
# ============================================================

CLASES_IGNORADAS = {
    1: "Building"
}


# ============================================================
# LISTA DE CLASES ORIGINALES
# ============================================================

CLASES_ORIGINALES = [
    "Bike",
    "Building",
    "Car",
    "Person",
    "Stairs",
    "Traffic sign",
    "Electrical Pole",
    "Road",
    "Motorcycle",
    "Dustbin",
    "Dog",
    "Manhole",
    "Tree",
    "Guard rail",
    "Pedestrian crosswalk",
    "Truck",
    "Bus",
    "Bench",
    "Traffic Cone",
    "Fire hydrant",
    "Teraffic Barrel",
    "Plant Pot",
    "Electrical Box",
    "Chair",
    "Bicycle Rack"
]


# ============================================================
# MOSTRAR CLASES FINALES
# ============================================================

print("=" * 70)
print("ACCESSAI - MAPEO DE CLASES")
print("=" * 70)

print("\nClases finales:")

for idx, nombre in enumerate(NUEVOS_NOMBRES):
    print(f"  {idx}: {nombre}")

print(f"\nNúmero de clases finales: {NUM_CLASSES}")


# ============================================================
# MOSTRAR MAPEO ORIGINAL -> FINAL
# ============================================================

print("\n" + "-" * 70)
print("MAPEO ORIGINAL -> FINAL")
print("-" * 70)

for clase_original, clase_final in sorted(MAPEO_CLASES.items()):

    nombre_original = CLASES_ORIGINALES[clase_original]
    nombre_final = NUEVOS_NOMBRES[clase_final]

    print(
        f"{clase_original:2d} | "
        f"{nombre_original:25s} -> "
        f"{clase_final} | "
        f"{nombre_final}"
    )


# ============================================================
# MOSTRAR CLASES IGNORADAS
# ============================================================

print("\n" + "-" * 70)
print("CLASES IGNORADAS")
print("-" * 70)

for clase, nombre in CLASES_IGNORADAS.items():
    print(f"  {clase}: {nombre}")


# ============================================================
# RESUMEN POR CATEGORÍA
# ============================================================

print("\n" + "=" * 70)
print("RESUMEN POR CATEGORÍA")
print("=" * 70)

for clase_final, nombre_final in enumerate(NUEVOS_NOMBRES):

    clases = [
        CLASES_ORIGINALES[clase_original]
        for clase_original, destino in MAPEO_CLASES.items()
        if destino == clase_final
    ]

    print(f"\n{clase_final}: {nombre_final}")

    for nombre in clases:
        print(f"   - {nombre}")


# ============================================================
# COMPROBACIÓN DEL MAPEO
# ============================================================

num_originales = len(CLASES_ORIGINALES)
num_mapeadas = len(MAPEO_CLASES)
num_ignoradas = len(CLASES_IGNORADAS)

assert num_mapeadas + num_ignoradas == num_originales

assert all(
    destino in range(NUM_CLASSES)
    for destino in MAPEO_CLASES.values()
)

print("\n" + "=" * 70)
print("COMPROBACIÓN")
print("=" * 70)
print(f"Clases originales : {num_originales}")
print(f"Clases mapeadas   : {num_mapeadas}")
print(f"Clases ignoradas  : {num_ignoradas}")
print(f"Clases finales    : {NUM_CLASSES}")
print("✅ Todas las clases originales están clasificadas.")


# [markdown]
# # 05. Crear `data_filtrado.yaml`
#

# ============================================================
# ACCESSAI - 05. NUEVO DATA.YAML
# ============================================================

with open(yaml_original_path, "r", encoding="utf-8") as f:
    config_original = yaml.safe_load(f)

print("Contenido original:")
print(config_original)

config_nueva = {
    "path": str(DATASET_PATH.resolve()),
    "train": "train/images",
    "val": "valid/images",
    "test": "test/images",
    "nc": NUM_CLASSES,
    "names": NUEVOS_NOMBRES
}

with open(yaml_nuevo_path, "w", encoding="utf-8") as f:
    yaml.safe_dump(
        config_nueva,
        f,
        sort_keys=False,
        allow_unicode=True
    )

print("\n✅ Nuevo YAML creado:")
print(yaml_nuevo_path)

print("\nContenido:")
with open(yaml_nuevo_path, "r", encoding="utf-8") as f:
    print(f.read())


# [markdown]
#  06. Preparar etiquetas
#
# La transformación es idempotente: siempre toma como fuente `labels_originales`, evitando remapear por segunda vez las etiquetas ya transformadas.
#

# ============================================================
# ACCESSAI - 06. PREPARAR ETIQUETAS
# ============================================================

def preparar_etiquetas(split):
    """
    Conserva las etiquetas originales y genera las etiquetas
    filtradas/remapeadas de forma segura.

    La transformación es idempotente:
    ejecutar esta función varias veces NO remapea etiquetas
    que ya fueron transformadas.
    """

    split_dir = DATASET_PATH / split

    labels_dir = split_dir / "labels"
    labels_originales_dir = split_dir / "labels_originales"

    if not split_dir.exists():
        raise FileNotFoundError(
            f"No existe el split:\n{split_dir}"
        )

    if labels_originales_dir.exists():
        source_dir = labels_originales_dir
        print(f"↪ {split}: usando labels_originales como fuente")
    elif labels_dir.exists():
        print(f"↪ {split}: guardando labels originales")
        labels_dir.rename(labels_originales_dir)
        source_dir = labels_originales_dir
    else:
        raise FileNotFoundError(
            f"No existe la carpeta labels en:\n{split_dir}"
        )

    labels_filtradas_dir = split_dir / "labels_filtradas"

    if labels_filtradas_dir.exists():
        shutil.rmtree(labels_filtradas_dir)

    labels_filtradas_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    clases_originales = Counter()
    clases_nuevas = Counter()
    clases_descartadas = Counter()

    archivos_procesados = 0

    for archivo in sorted(source_dir.glob("*.txt")):
        archivos_procesados += 1

        ruta_salida = labels_filtradas_dir / archivo.name
        nuevas_lineas = []

        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split()

                if not partes:
                    continue

                try:
                    clase_original = int(partes[0])
                except ValueError:
                    print(
                        f"⚠️ Clase inválida en {archivo.name}: "
                        f"{partes[0]}"
                    )
                    continue

                clases_originales[clase_original] += 1

                if clase_original not in MAPEO_CLASES:
                    clases_descartadas[clase_original] += 1
                    continue

                clase_nueva = MAPEO_CLASES[clase_original]
                partes[0] = str(clase_nueva)

                nuevas_lineas.append(
                    " ".join(partes) + "\n"
                )

                clases_nuevas[clase_nueva] += 1

        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.writelines(nuevas_lineas)

    if labels_dir.exists():
        shutil.rmtree(labels_dir)

    labels_filtradas_dir.rename(labels_dir)

    print("\n" + "-" * 70)
    print(f"Split: {split}")
    print("-" * 70)
    print(f"Archivos procesados: {archivos_procesados}")

    print("\nClases originales encontradas:")
    for clase, cantidad in sorted(clases_originales.items()):
        print(f"  {clase}: {cantidad}")

    print("\nClases finales:")
    for clase, nombre in enumerate(NUEVOS_NOMBRES):
        print(f"  {clase} - {nombre}: {clases_nuevas[clase]}")

    print("\nClases descartadas:")
    if clases_descartadas:
        for clase, cantidad in sorted(clases_descartadas.items()):
            print(f"  {clase}: {cantidad}")
    else:
        print("  Ninguna")

    print(f"\n✅ {split} preparado correctamente.")


for split in ["train", "valid", "test"]:
    preparar_etiquetas(split)


# [markdown]
#  07. Comprobar estructura del dataset
#

# ============================================================
# ACCESSAI - 07. COMPROBACIÓN DATASET
# ============================================================

for split in ["train", "valid", "test"]:
    split_dir = DATASET_PATH / split

    images_dir = split_dir / "images"
    labels_dir = split_dir / "labels"
    originals_dir = split_dir / "labels_originales"

    image_count = len(list(images_dir.glob("*")))
    label_count = len(list(labels_dir.glob("*.txt")))
    original_count = len(list(originals_dir.glob("*.txt")))

    print("=" * 70)
    print(split)
    print(f"Imágenes:           {image_count}")
    print(f"Labels activas:     {label_count}")
    print(f"Labels originales:  {original_count}")


# [markdown]
#  08. Entrenamiento yolo26x
#
# Configuración existente del prototipo; el entrenamiento exige GPU y usa AutoBatch para dimensionar el lote:
#
# - `batch=-1`: AutoBatch.
# - `cache="ram"`: reduce la lectura repetitiva de disco si hay RAM suficiente.
# - `amp=True`: mixed precision.
# - `workers=4`: valor conservador para Windows.
# - `close_mosaic=10`: desactiva Mosaic al final del entrenamiento.
# - `patience=8`: early stopping.
#

# ============================================================
# ACCESSAI - 08. ENTRENAMIENTO (OPTIMIZADO PARA RTX 4060 8GB)
# ============================================================

import datetime
from pathlib import Path  # Asegurar compatibilidad de rutas
import torch
from ultralytics import YOLO


ahora_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
project_ahora_str = f"AccessAI_Proto3_{ahora_str}"

if torch.cuda.is_available():
    device = 0
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    print("GPU:", torch.cuda.get_device_name(device))
    print(
        "Memoria total GPU:",
        round(torch.cuda.get_device_properties(device).total_memory / (1024**3), 2),
        "GB",
    )
else:
    device = "cpu"
    print("⚠️ No se detectó GPU disponible. El entrenamiento se ejecutará en CPU.")

print("Dispositivo final:", device)

# Definición de ROOT si no venía declarada previamente en tu celda anterior
ROOT = Path(".").resolve()  # Ajustar si tu ROOT apunta a otra carpeta
MODEL_PATH = ROOT / "yolo26x.pt"


if not MODEL_PATH.exists():
    raise FileNotFoundError(f"No se encontró:\n{MODEL_PATH}")

if not yaml_nuevo_path.exists():
    raise FileNotFoundError(
        f"No existe el dataset configurado:\n{yaml_nuevo_path}"
    )

model = YOLO(str(MODEL_PATH))

print("\nModelo cargado:")
print(MODEL_PATH)

# --- CONFIGURACIÓN OPTIMIZADA PARA DATASETS GRANDES Y MODELOS XL ---
# Forzamos un batch bajo (4 u 8) para evitar que la GPU de 8GB colapse.
# Si con 4 funciona bien y tienes VRAM libre, puedes subir a 8.
train_batch = 32 if torch.cuda.is_available() else 1
print(f"Batch de entrenamiento: {train_batch}")
train_workers = 4 if torch.cuda.is_available() else 0
print(f"Workers de entrenamiento: {train_workers}")
results = model.train(
    data=str(yaml_nuevo_path),
    epochs=85,
    patience=8,
    imgsz=640,
    batch=32,
    device=device,
    workers=train_workers,
    cache=False,
    amp=True,
    optimizer="AdamW",
    lr0=0.001,
    cos_lr=True,
    # --- Aumentaciones ---
    augment=True,
    mosaic=1.0,
    close_mosaic=10,
    mixup=0.0,
    cls=1.0,
    # --- Guardado y Métricas ---
    save=True,
    save_period=5,
    plots=True,
    seed=42,
    project=str(ROOT / "runs" / project_ahora_str),
    name="yolo26x_4clases",
    exist_ok=False,
    # --- Optimizaciones de Tiempo Aclimatadas ---
    val=False,  # Evaluará únicamente al final del entrenamiento completo.
    overlap_mask=False,  # Apaga procesamiento de segmentación innecesario.
    multi_scale=False,  # Mantiene las imágenes estrictas a 640x640 fijas.
)


print("\n✅ ENTRENAMIENTO TERMINADO")
print("Directorio:", results.save_dir)


# [markdown]
#  09. Cargar el `best.pt` entrenado
#
# A partir de aquí usamos el modelo entrenado de AccessAI, no el `yolo26x.pt` preentrenado.
#

# ============================================================
# ACCESSAI - 09. CARGAR BEST.PT
# ============================================================

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


# [markdown]
#  10. Evaluación en el conjunto `test`
#

# ============================================================
# ACCESSAI - 10. EVALUACIÓN TEST
# ============================================================

eval_batch = 16

metrics = trained_model.val(
    data=str(yaml_nuevo_path),
    split="test",
    imgsz=640,
    batch=eval_batch,
    device=device,
    plots=True
)

print("\n" + "=" * 70)
print("MÉTRICAS TEST")
print("=" * 70)

print(f"mAP50:     {metrics.box.map50:.4f}")
print(f"mAP50-95:  {metrics.box.map:.4f}")


# [markdown]
#  11. Cargar `results.csv` y visualizar curvas
#

# ============================================================
# ACCESSAI - 11. CARGAR MÉTRICAS
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt

results_csv = RUN_DIR / "results.csv"

print("CSV:")
print(results_csv)

if not results_csv.exists():
    raise FileNotFoundError(
        f"No existe:\n{results_csv}"
    )

df = pd.read_csv(results_csv)

print("\nColumnas:")
print(df.columns.tolist())


# ============================================================
# ACCESSAI - 11.1 LOSS
# ============================================================
%matplotlib inline
plt.figure(figsize=(12, 6))

plt.plot(
    df["epoch"],
    df["train/box_loss"],
    label="Train Box Loss"
)

plt.plot(
    df["epoch"],
    df["train/cls_loss"],
    label="Train Class Loss"
)

plt.plot(
    df["epoch"],
    df["train/dfl_loss"],
    label="Train DFL Loss"
)

plt.xlabel("Época")
plt.ylabel("Loss")
plt.title("AccessAI - Pérdidas de entrenamiento")

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


# ============================================================
# ACCESSAI - 11.2 mAP
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    df["epoch"],
    df["metrics/mAP50(B)"],
    label="mAP50"
)

plt.plot(
    df["epoch"],
    df["metrics/mAP50-95(B)"],
    label="mAP50-95"
)

plt.xlabel("Época")
plt.ylabel("mAP")
plt.title("AccessAI - Métricas de detección")

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


# ============================================================
# ACCESSAI - 11.3 PRECISION / RECALL
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    df["epoch"],
    df["metrics/precision(B)"],
    label="Precision"
)

plt.plot(
    df["epoch"],
    df["metrics/recall(B)"],
    label="Recall"
)

plt.xlabel("Época")
plt.ylabel("Valor")
plt.title("AccessAI - Precision y Recall")

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


# [markdown]
#  12. Seleccionar una imagen de prueba
#
# El notebook busca una de varias rutas habituales dentro del proyecto.
#

# ============================================================
# ACCESSAI - 12. SELECCIONAR IMAGEN
# ============================================================

from pathlib import Path
import cv2
import matplotlib.pyplot as plt

ROOT = Path.cwd()

sample_candidates = [
    ROOT / "tests" / "imgs" / "image.png",
    ROOT / "tests" / "imgs" / "IMG_20170311_205902.jpg",
    ROOT / "DATA" / "ROD-Dataset" / "dataset" / "test" / "images" / "IMG_19187.jpg",
]

image_path = next(
    (p for p in sample_candidates if p.exists()),
    None
)

if image_path is None:
    raise FileNotFoundError(
        "No se encontró ninguna imagen de prueba."
    )

print("Imagen:")
print(image_path)


# [markdown]
#  13. Inferencia
#

# ============================================================
# ACCESSAI - 13. INFERENCIA
# ============================================================

results_predict = trained_model.predict(
    source=str(image_path),
    conf=0.25,
    imgsz=640,
    device=device,
    verbose=False
)

result = results_predict[0]

print(
    f"\nDetecciones encontradas: "
    f"{len(result.boxes)}"
)

if result.boxes is not None and len(result.boxes) > 0:

    for idx, box in enumerate(
        result.boxes,
        start=1
    ):
        cls_id = int(box.cls[0])
        cls_name = trained_model.names[cls_id]
        confidence = float(box.conf[0])
        coords = box.xyxy[0].tolist()

        print(
            f"[{idx}] "
            f"{cls_name} | "
            f"conf={confidence:.3f} | "
            f"bbox={coords}"
        )
else:
    print(
        "No se detectaron objetos con conf=0.25."
    )


# [markdown]
#  14. Guardar y mostrar la imagen anotada
#

# ============================================================
# ACCESSAI - 14. RESULTADO
# ============================================================

output_dir = ROOT / "resultados"

output_dir.mkdir(
    parents=True,
    exist_ok=True
)

output_path = (
    output_dir /
    "accessai_resultado.jpg"
)

annotated = result.plot()

ok = cv2.imwrite(
    str(output_path),
    annotated
)

if not ok:
    raise IOError(
        f"No se pudo guardar la imagen en:\n{output_path}"
    )

print("✅ Imagen guardada en:")
print(output_path)

annotated_rgb = cv2.cvtColor(
    annotated,
    cv2.COLOR_BGR2RGB
)

plt.figure(figsize=(14, 8))
plt.imshow(annotated_rgb)
plt.axis("off")
plt.title("AccessAI - Detección urbana")
plt.tight_layout()
plt.show()


# [markdown]
#  15. Resumen del experimento
#
# Al terminar, conserva al menos:
#
# - `best.pt`
# - `results.csv`
# - `confusion_matrix.png`
# - `results.png`
# - imagen anotada de inferencia
# - valores de `mAP50`, `mAP50-95`, Precision y Recall
#
# El objetivo de este prototipo es medir la capacidad del modelo para detectar las cuatro categorías seleccionadas del ROD-Dataset.
#
# Nota: las métricas describen únicamente este experimento sobre las cuatro categorías agrupadas del ROD-Dataset; no constituyen validación de detección específica de accesibilidad.
#

# ============================================================
# ACCESSAI - 11. GRÁFICOS DEL ENTRENAMIENTO Y EVALUACIÓN
# ============================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------
# Rutas
# ------------------------------------------------------------

RUN_DIR = Path(results.save_dir)
RESULTS_CSV = RUN_DIR / "results.csv"

print("=" * 70)
print("ACCESSAI - GRÁFICOS")
print("=" * 70)
print("Directorio del entrenamiento:", RUN_DIR)
print("results.csv:", RESULTS_CSV)

if not RESULTS_CSV.exists():
    raise FileNotFoundError(
        f"No se encontró results.csv en:\n{RESULTS_CSV}\n"
        "Ejecuta primero el entrenamiento."
    )

df = pd.read_csv(RESULTS_CSV)

print("\nColumnas disponibles:")
print(df.columns.tolist())


# ============================================================
# GRÁFICO 1 - LOSSES
# ============================================================

loss_columns = [
    "train/box_loss",
    "train/cls_loss",
    "train/dfl_loss"
]

available_losses = [
    column for column in loss_columns
    if column in df.columns
]

plt.figure(figsize=(12, 6))

for column in available_losses:
    plt.plot(
        df["epoch"],
        df[column],
        label=column.replace("train/", "").replace("_", " ").title()
    )

plt.xlabel("Época")
plt.ylabel("Loss")
plt.title("AccessAI - Pérdidas de entrenamiento")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# ============================================================
# GRÁFICO 2 - mAP
# ============================================================

map_columns = [
    "metrics/mAP50(B)",
    "metrics/mAP50-95(B)"
]

available_map = [
    column for column in map_columns
    if column in df.columns
]

plt.figure(figsize=(12, 6))

for column in available_map:
    plt.plot(
        df["epoch"],
        df[column],
        label=column.replace("metrics/", "").replace("(B)", "")
    )

plt.xlabel("Época")
plt.ylabel("mAP")
plt.title("AccessAI - Evolución de mAP")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# ============================================================
# GRÁFICO 3 - PRECISION Y RECALL
# ============================================================

pr_columns = [
    "metrics/precision(B)",
    "metrics/recall(B)"
]

available_pr = [
    column for column in pr_columns
    if column in df.columns
]

plt.figure(figsize=(12, 6))

for column in available_pr:
    nombre = (
        column
        .replace("metrics/", "")
        .replace("(B)", "")
        .capitalize()
    )

    plt.plot(
        df["epoch"],
        df[column],
        label=nombre
    )

plt.xlabel("Época")
plt.ylabel("Valor")
plt.title("AccessAI - Precision y Recall")
plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# ============================================================
# GRÁFICO 4 - TRAIN VS VALIDATION LOSS
# ============================================================

validation_columns = [
    "val/box_loss",
    "val/cls_loss",
    "val/dfl_loss"
]

available_validation = [
    column for column in validation_columns
    if column in df.columns
]

if available_validation:

    plt.figure(figsize=(12, 6))

    for column in available_validation:
        plt.plot(
            df["epoch"],
            df[column],
            label=column.replace("val/", "Val ").replace("_", " ").title()
        )

    plt.xlabel("Época")
    plt.ylabel("Loss")
    plt.title("AccessAI - Loss de validación")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ============================================================
# GRÁFICO 5 - RESUMEN FINAL
# ============================================================

metricas_finales = {}

if "metrics/mAP50(B)" in df.columns:
    metricas_finales["mAP50"] = float(df["metrics/mAP50(B)"].iloc[-1])

if "metrics/mAP50-95(B)" in df.columns:
    metricas_finales["mAP50-95"] = float(df["metrics/mAP50-95(B)"].iloc[-1])

if "metrics/precision(B)" in df.columns:
    metricas_finales["Precision"] = float(df["metrics/precision(B)"].iloc[-1])

if "metrics/recall(B)" in df.columns:
    metricas_finales["Recall"] = float(df["metrics/recall(B)"].iloc[-1])

if metricas_finales:

    plt.figure(figsize=(10, 6))

    nombres = list(metricas_finales.keys())
    valores = list(metricas_finales.values())

    plt.bar(nombres, valores)

    plt.ylabel("Valor")
    plt.ylim(0, 1)
    plt.title("AccessAI - Métricas finales del entrenamiento")
    plt.grid(axis="y")

    for i, valor in enumerate(valores):
        plt.text(
            i,
            min(valor + 0.02, 0.98),
            f"{valor:.3f}",
            ha="center"
        )

    plt.tight_layout()
    plt.show()


# ============================================================
# GRÁFICO 6 - DISTRIBUCIÓN DE CLASES DEL DATASET
# ============================================================

conteo_clases = {}

for clase_id, nombre in enumerate(NUEVOS_NOMBRES):
    conteo_clases[nombre] = 0

train_labels_dir = DATASET_PATH / "train" / "labels"

if train_labels_dir.exists():

    for label_file in train_labels_dir.glob("*.txt"):

        with open(label_file, "r", encoding="utf-8") as f:

            for line in f:

                partes = line.strip().split()

                if not partes:
                    continue

                try:
                    clase_id = int(partes[0])
                except ValueError:
                    continue

                if 0 <= clase_id < len(NUEVOS_NOMBRES):
                    nombre = NUEVOS_NOMBRES[clase_id]
                    conteo_clases[nombre] += 1

    nombres = list(conteo_clases.keys())
    cantidades = list(conteo_clases.values())

    plt.figure(figsize=(12, 6))
    plt.bar(nombres, cantidades)

    plt.xlabel("Clase")
    plt.ylabel("Número de objetos")
    plt.title("AccessAI - Distribución de clases en train")
    plt.xticks(rotation=15)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

    print("\nDistribución de clases:")
    for nombre, cantidad in conteo_clases.items():
        print(f"{nombre:30s}: {cantidad}")

else:
    print("\n⚠️ No se encontró el directorio de labels de train.")


# ============================================================
# GRÁFICO 7 - MATRIZ DE CONFUSIÓN
# ============================================================

confusion_candidates = [
    RUN_DIR / "confusion_matrix.png",
    RUN_DIR / "confusion_matrix_normalized.png",
]

confusion_path = next(
    (
        path
        for path in confusion_candidates
        if path.exists()
    ),
    None
)

if confusion_path is not None:

    image = plt.imread(confusion_path)

    plt.figure(figsize=(12, 10))
    plt.imshow(image)
    plt.axis("off")
    plt.title("AccessAI - Matriz de confusión")
    plt.tight_layout()
    plt.show()

    print("\nMatriz de confusión:")
    print(confusion_path)

else:
    print(
        "\n⚠️ No se encontró la matriz de confusión.\n"
        "Ultralytics debe generar confusion_matrix.png durante la validación."
    )


# ============================================================
# RESUMEN DE GRÁFICOS
# ============================================================

print("\n" + "=" * 70)
print("GRÁFICOS GENERADOS")
print("=" * 70)

print("1. Loss de entrenamiento")
print("2. mAP50 y mAP50-95")
print("3. Precision y Recall")
print("4. Loss de validación")
print("5. Métricas finales")
print("6. Distribución de clases")
print("7. Matriz de confusión")


