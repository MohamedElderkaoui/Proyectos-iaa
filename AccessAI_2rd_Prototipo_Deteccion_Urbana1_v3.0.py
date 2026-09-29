# [markdown]
#  AccessAI - Prototipo de detección urbana
#
# Este cuaderno implementa un experimento reproducible sobre el ROD-Dataset:
#
# 1. Comprobar entorno y GPU.
# 2. Comprobar Ultralytics.
# 3. Preparar el ROD-Dataset.
# 4. Filtrar y remapear las 25 clases originales a 4 categorías.
# 5. Crear `data_filtrado.yaml`.
# 6. Entrenar YOLO26M con AutoBatch en la GPU disponible.
# 7. Cargar `best.pt`.
# 8. Evaluar el modelo en `test`.
# 9. Visualizar las curvas del entrenamiento.
# 10. Ejecutar inferencia sobre una imagen y guardar el resultado.
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
# > Las etiquetas originales se conservan en `labels_originales`. El remapeo siempre usa esas etiquetas como fuente, por lo que ejecutar el notebook de nuevo no aplica un segundo remapeo.
#
# > **Alcance:** estas cuatro categorías son una agrupación experimental del ROD-Dataset. No equivalen a `sidewalk` y `curbramp` y sus métricas no constituyen una validación de accesibilidad urbana específica.

# [markdown]
# # Nota de configuración
#
# Se normaliza el notebook a **YOLO26M** porque es el modelo que aparece en el código actual y es mucho más razonable para una RTX 4060 Laptop GPU de 8 GB que intentar fijar un batch 64 con YOLO26X.
#
# `batch=-1` activa AutoBatch de Ultralytics. No se debe describir `batch=64` como AutoBatch.
#
# Para un experimento específico con `yolo26x.pt`, cambia `MODEL_NAME`, pero en 8 GB de VRAM conviene tratarlo como experimento separado y reducir agresivamente el batch.

# [markdown]
# # 01. Entorno y GPU

from pathlib import Path
import sys
import torch

print("=" * 70)
print("ACCESSAI - ENTORNO Y GPU")
print("=" * 70)

print(f"Python: {sys.executable}")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA de PyTorch: {torch.version.cuda}")
print(f"HIP: {torch.version.hip}")
print(f"CUDA disponible: {torch.cuda.is_available()}")

if not torch.cuda.is_available():
    raise RuntimeError(
        "CUDA no está disponible en este kernel de Jupyter. "
        "Selecciona el entorno 'proyecto_yolo' con PyTorch CUDA."
    )

device = 0
gpu_name = torch.cuda.get_device_name(device)
props = torch.cuda.get_device_properties(device)

print(f"GPU: {gpu_name}")
print(f"GPU count: {torch.cuda.device_count()}")
print(f"VRAM total: {props.total_memory / 1024**3:.2f} GB")
print(f"Compute capability: {props.major}.{props.minor}")
print(
    f"VRAM asignada: "
    f"{torch.cuda.memory_allocated(device) / 1024**3:.2f} GB"
)
print(
    f"VRAM reservada: "
    f"{torch.cuda.memory_reserved(device) / 1024**3:.2f} GB"
)

torch.set_float32_matmul_precision("high")
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

# Prueba real de CUDA
x = torch.zeros((1, 3, 640, 640), device=device)
print("✅ Tensor CUDA de prueba creado")
del x
torch.cuda.empty_cache()
print("✅ GPU funcionando correctamente")


# [markdown]
# # 02. Comprobar Ultralytics

import ultralytics

print("=" * 70)
print("ACCESSAI - ULTRALYTICS")
print("=" * 70)
print("Ultralytics:", ultralytics.__version__)


# [markdown]
# # 03. Configuración del proyecto y dataset
#
# Se busca automáticamente una carpeta que contenga `DATA/ROD-Dataset/dataset`, evitando depender de una única carpeta de trabajo de Jupyter.

from pathlib import Path
import yaml
import shutil
from collections import Counter

def encontrar_raiz_proyecto():
    actual = Path.cwd().resolve()
    candidatos = [actual] + list(actual.parents)

    for candidato in candidatos:
        dataset = candidato / "DATA" / "ROD-Dataset" / "dataset"
        if dataset.exists():
            return candidato

    return actual

ROOT = encontrar_raiz_proyecto()
DATASET_PATH = ROOT / "DATA" / "ROD-Dataset" / "dataset"

yaml_original_path = DATASET_PATH / "data.yaml"
yaml_nuevo_path = DATASET_PATH / "data_filtrado.yaml"

print("ROOT:")
print(ROOT)
print("\nDataset:")
print(DATASET_PATH)
print("\nExiste dataset:", DATASET_PATH.exists())
print("Existe data.yaml:", yaml_original_path.exists())

if not DATASET_PATH.exists():
    raise FileNotFoundError(f"No existe el dataset:\n{DATASET_PATH}")

if not yaml_original_path.exists():
    raise FileNotFoundError(f"No existe:\n{yaml_original_path}")


# [markdown]
# # 04. Mapeo de clases del ROD-Dataset

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
    "Bicycle Rack",
]

MAPEO_CLASES = {
    # 0 -> Obstaculo_Dinamico
    0: 0,   # Bike
    2: 0,   # Car
    3: 0,   # Person
    8: 0,   # Motorcycle
    10: 0,  # Dog
    15: 0,  # Truck
    16: 0,  # Bus

    # 1 -> Obstaculo_Fijo
    5: 1,   # Traffic sign
    6: 1,   # Electrical Pole
    9: 1,   # Dustbin
    12: 1,  # Tree
    13: 1,  # Guard rail
    17: 1,  # Bench
    18: 1,  # Traffic Cone
    19: 1,  # Fire hydrant
    20: 1,  # Teraffic Barrel
    21: 1,  # Plant Pot
    22: 1,  # Electrical Box
    23: 1,  # Chair
    24: 1,  # Bicycle Rack

    # 2 -> Barrera_Arquitectonica
    4: 2,   # Stairs

    # 3 -> Infraestructura_Peatonal
    7: 3,   # Road
    11: 3,  # Manhole
    14: 3,  # Pedestrian crosswalk
}

NUEVOS_NOMBRES = [
    "Obstaculo_Dinamico",
    "Obstaculo_Fijo",
    "Barrera_Arquitectonica",
    "Infraestructura_Peatonal",
]

CLASES_IGNORADAS = {
    1: "Building",
}

NUM_CLASSES = len(NUEVOS_NOMBRES)

# Comprobaciones estructurales
assert len(CLASES_ORIGINALES) == 25
assert len(MAPEO_CLASES) + len(CLASES_IGNORADAS) == len(CLASES_ORIGINALES)
assert set(MAPEO_CLASES) | set(CLASES_IGNORADAS) == set(range(25))
assert all(0 <= destino < NUM_CLASSES for destino in MAPEO_CLASES.values())

print("=" * 70)
print("ACCESSAI - MAPEO DE CLASES")
print("=" * 70)

print("\nClases finales:")
for idx, nombre in enumerate(NUEVOS_NOMBRES):
    print(f"{idx}: {nombre}")

print("\nMAPEO ORIGINAL -> FINAL")
for clase_original, clase_final in sorted(MAPEO_CLASES.items()):
    print(
        f"{clase_original:2d} | "
        f"{CLASES_ORIGINALES[clase_original]:25s} -> "
        f"{clase_final} | "
        f"{NUEVOS_NOMBRES[clase_final]}"
    )

print("\nCLASES IGNORADAS")
for clase, nombre in CLASES_IGNORADAS.items():
    print(f"{clase}: {nombre}")


# [markdown]
# # 05. Crear `data_filtrado.yaml`

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
    "names": NUEVOS_NOMBRES,
}

with open(yaml_nuevo_path, "w", encoding="utf-8") as f:
    yaml.safe_dump(
        config_nueva,
        f,
        sort_keys=False,
        allow_unicode=True,
    )

print("\n✅ Nuevo YAML creado:")
print(yaml_nuevo_path)

print("\nContenido:")
print(yaml_nuevo_path.read_text(encoding="utf-8"))


# [markdown]
# # 06. Preparar etiquetas
#
# La transformación siempre parte de `labels_originales`.
#
# - Si `labels_originales` no existe, se conserva la carpeta `labels` actual.
# - Se genera `labels_filtradas` desde las originales.
# - Después se reemplaza `labels` por las etiquetas remapeadas.
# - Al volver a ejecutar, nunca se utiliza el remapeo anterior como fuente.

def preparar_etiquetas(split):
    split_dir = DATASET_PATH / split
    labels_dir = split_dir / "labels"
    labels_originales_dir = split_dir / "labels_originales"
    labels_filtradas_dir = split_dir / "labels_filtradas"

    if not split_dir.exists():
        raise FileNotFoundError(f"No existe el split:\n{split_dir}")

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

    if labels_filtradas_dir.exists():
        shutil.rmtree(labels_filtradas_dir)
    labels_filtradas_dir.mkdir(parents=True, exist_ok=True)

    # Evita reusar un estado previo de `labels` que pudiera quedar
    # después de una ejecución anterior incompleta.
    if labels_dir.exists():
        shutil.rmtree(labels_dir)

    clases_originales = Counter()
    clases_nuevas = Counter()
    clases_descartadas = Counter()
    archivos_procesados = 0
    lineas_validas = 0
    lineas_invalidas = 0

    for archivo in sorted(source_dir.glob("*.txt")):
        archivos_procesados += 1
        ruta_salida = labels_filtradas_dir / archivo.name
        nuevas_lineas = []

        with open(archivo, "r", encoding="utf-8") as f:
            for numero_linea, linea in enumerate(f, start=1):
                partes = linea.strip().split()

                if not partes:
                    continue

                try:
                    clase_original = int(partes[0])
                except ValueError:
                    lineas_invalidas += 1
                    print(
                        f"⚠️ Clase inválida en "
                        f"{archivo.name}:{numero_linea} -> {partes[0]}"
                    )
                    continue

                if len(partes) != 5:
                    lineas_invalidas += 1
                    print(
                        f"⚠️ Formato YOLO inesperado en "
                        f"{archivo.name}:{numero_linea} -> {linea.strip()}"
                    )
                    continue

                clases_originales[clase_original] += 1
                lineas_validas += 1

                if clase_original not in MAPEO_CLASES:
                    clases_descartadas[clase_original] += 1
                    continue

                clase_nueva = MAPEO_CLASES[clase_original]
                partes[0] = str(clase_nueva)
                nuevas_lineas.append(" ".join(partes) + "\n")
                clases_nuevas[clase_nueva] += 1

        ruta_salida.write_text("".join(nuevas_lineas), encoding="utf-8")

    labels_filtradas_dir.rename(labels_dir)

    print("\n" + "-" * 70)
    print(f"Split: {split}")
    print("-" * 70)
    print(f"Archivos procesados: {archivos_procesados}")
    print(f"Líneas YOLO válidas: {lineas_validas}")
    print(f"Líneas inválidas: {lineas_invalidas}")

    print("\nClases finales:")
    for clase, nombre in enumerate(NUEVOS_NOMBRES):
        print(f"{clase} - {nombre}: {clases_nuevas[clase]}")

    print("\nClases descartadas:")
    if clases_descartadas:
        for clase, cantidad in sorted(clases_descartadas.items()):
            nombre = CLASES_ORIGINALES[clase] if 0 <= clase < 25 else "desconocida"
            print(f"{clase} - {nombre}: {cantidad}")
    else:
        print("Ninguna")

    print(f"\n✅ {split} preparado correctamente.")


for split in ["train", "valid", "test"]:
    preparar_etiquetas(split)


# [markdown]
# # 07. Comprobar estructura del dataset

print("=" * 70)
print("ACCESSAI - ESTRUCTURA DEL DATASET")
print("=" * 70)

for split in ["train", "valid", "test"]:
    split_dir = DATASET_PATH / split
    images_dir = split_dir / "images"
    labels_dir = split_dir / "labels"
    originals_dir = split_dir / "labels_originales"

    image_count = len(list(images_dir.glob("*")))
    label_count = len(list(labels_dir.glob("*.txt")))
    original_count = len(list(originals_dir.glob("*.txt")))

    print("\n" + "=" * 70)
    print(split)
    print("=" * 70)
    print(f"Imágenes:          {image_count}")
    print(f"Labels activas:    {label_count}")
    print(f"Labels originales: {original_count}")

    if image_count == 0:
        raise RuntimeError(f"No hay imágenes en {images_dir}")
    if original_count == 0:
        raise RuntimeError(f"No hay etiquetas originales en {originals_dir}")
    if label_count == 0:
        raise RuntimeError(f"No hay etiquetas activas en {labels_dir}")


# [markdown]
# # 08. Entrenamiento YOLO26M

# ============================================================
# ACCESSAI - 08. ENTRENAMIENTO PARA RTX 4060 8 GB
# YOLO26X - 4 CLASES
# ============================================================

import datetime
import gc
from pathlib import Path
import sys

import torch
import yaml
from ultralytics import YOLO


print("=" * 75)
print("ACCESSAI - ENTRENAMIENTO YOLO26X")
print("=" * 75)


# ============================================================
# 1. COMPROBAR CUDA
# ============================================================

if not torch.cuda.is_available():
    raise RuntimeError(
        "CUDA no está disponible en este kernel de Jupyter. "
        "Selecciona el entorno de Python/PyTorch con soporte CUDA."
    )

device = 0

print("Python:", sys.executable)
print("PyTorch:", torch.__version__)
print("CUDA:", torch.version.cuda)
print("GPU:", torch.cuda.get_device_name(device))


# ============================================================
# 2. LIMPIAR MEMORIA GPU
# ============================================================

gc.collect()
torch.cuda.empty_cache()

free_memory, total_memory = torch.cuda.mem_get_info(device)

print("\nMemoria GPU disponible antes del entrenamiento:")
print(f"  Libre: {free_memory / 1024**3:.2f} GB")
print(f"  Total: {total_memory / 1024**3:.2f} GB")


# ============================================================
# 3. DATASET
# ============================================================

if "yaml_nuevo_path" not in globals():
    raise RuntimeError(
        "No existe yaml_nuevo_path. "
        "Ejecuta primero las celdas de preparación del dataset."
    )

yaml_nuevo_path = Path(yaml_nuevo_path)

if not yaml_nuevo_path.exists():
    raise FileNotFoundError(
        f"No existe el YAML:\n{yaml_nuevo_path}"
    )

with open(
    yaml_nuevo_path,
    "r",
    encoding="utf-8"
) as f:
    data_yaml = yaml.safe_load(f)


dataset_nc = data_yaml.get("nc")
dataset_names = data_yaml.get("names")


if dataset_nc != 4:
    raise ValueError(
        f"El YAML tiene nc={dataset_nc}, "
        "pero el experimento necesita 4 clases."
    )

if not dataset_names or len(dataset_names) != 4:
    raise ValueError(
        f"El YAML tiene {len(dataset_names) if dataset_names else 0} clases, "
        "pero deberían ser 4."
    )


print("\nDataset:")
print("  YAML:", yaml_nuevo_path)
print("  Clases:", dataset_nc)
print("  Nombres:", dataset_names)


# ============================================================
# 4. MODELO
# ============================================================

MODEL_NAME = "yolo26x.pt"

print("\nCargando modelo:")
print(" ", MODEL_NAME)

model = YOLO(MODEL_NAME)

print("✅ Modelo YOLO26X cargado")


# ============================================================
# 5. CONFIGURACIÓN
# ============================================================

imgsz = 640

# YOLO26X:
# Ultralytics recomienda batches pequeños de 4-8.
# Empezamos con 8; si aparece OOM -> usar 4.
train_batch = 8

train_workers = 4

epochs = 10
patience = 10

print("\nConfiguración:")
print(f"  Modelo:      {MODEL_NAME}")
print(f"  Imagen:      {imgsz}x{imgsz}")
print(f"  Batch:       {train_batch}")
print(f"  Workers:     {train_workers}")
print(f"  Epochs:      {epochs}")
print(f"  Patience:    {patience}")
print("  AMP:         True")
print("  Cache:       False")
print("  Optimizer:   AdamW")
print("  lr0:         0.001")
print("  Cos LR:      True")
print("  Mosaic:      0.8")
print("  Mixup:       0.0")


# ============================================================
# 6. NOMBRE DEL EXPERIMENTO
# ============================================================

ahora_str = datetime.datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)

run_root = (
    Path(ROOT)
    / "runs"
    / f"AccessAI_YOLO26X_{ahora_str}"
)


# ============================================================
# 7. ENTRENAMIENTO
# ============================================================

print("\n" + "=" * 75)
print("INICIANDO ENTRENAMIENTO YOLO26X")
print("=" * 75)

results = model.train(
    data=yaml_nuevo_path,
    imgsz=imgsz,
    batch=train_batch,
    workers=train_workers,
    epochs=epochs,
    patience=patience,
    device=device,
    #.........
)


# ============================================================
# 8. RESULTADOS
# ============================================================

RUN_DIR = Path(results.save_dir)

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


print("\n" + "=" * 75)
print("✅ ENTRENAMIENTO YOLO26X TERMINADO")
print("=" * 75)

print("\nRun:")
print(RUN_DIR)

print("\nbest.pt:")
print(BEST_MODEL)
print("Existe:", BEST_MODEL.exists())

print("\nlast.pt:")
print(LAST_MODEL)
print("Existe:", LAST_MODEL.exists())


# ============================================================
# 9. MEMORIA GPU FINAL
# ============================================================

print("\nMemoria GPU:")

print(
    "  Pico reservado:",
    round(
        torch.cuda.max_memory_reserved(device)
        / 1024**3,
        2
    ),
    "GB"
)

free_memory, total_memory = torch.cuda.mem_get_info(device)

print(
    "  Libre actualmente:",
    round(
        free_memory / 1024**3,
        2
    ),
    "GB"
)

# [markdown]
# # 09. Cargar `best.pt`

from ultralytics import YOLO

if not BEST_MODEL.exists():
    raise FileNotFoundError(f"No se encontró best.pt en:\n{BEST_MODEL}")

trained_model = YOLO(str(BEST_MODEL))

print("=" * 70)
print("ACCESSAI - MODELO ENTRENADO")
print("=" * 70)
print("Ruta:", BEST_MODEL)

print("\nClases:")
for idx, name in trained_model.names.items():
    print(f"{idx} -> {name}")

print("\n✅ Modelo AccessAI cargado")


# [markdown]
# # 10. Evaluación en `test`

eval_batch = 16

test_results_dir = RUN_DIR / "test_eval"
test_results_dir.mkdir(parents=True, exist_ok=True)

metrics = trained_model.val(
    data=str(yaml_nuevo_path),
    split="test",
    imgsz=640,
    batch=eval_batch,
    device=device,
    plots=True,
    project=str(test_results_dir),
    name="results",
)

precision = float(metrics.box.mp)
recall = float(metrics.box.mr)

if precision + recall > 0:
    f1 = 2 * precision * recall / (precision + recall)
else:
    f1 = 0.0

print("\n" + "=" * 70)
print("MÉTRICAS TEST")
print("=" * 70)
print(f"Precision:  {precision:.4f}")
print(f"Recall:     {recall:.4f}")
print(f"F1:         {f1:.4f}")
print(f"mAP50:      {metrics.box.map50:.4f}")
print(f"mAP50-95:   {metrics.box.map:.4f}")

print("\nResultados de test guardados en:")
print(test_results_dir)


# [markdown]
# # 11. Curvas del entrenamiento

import pandas as pd
import matplotlib.pyplot as plt

RESULTS_CSV = RUN_DIR / "results.csv"

if not RESULTS_CSV.exists():
    raise FileNotFoundError(f"No existe:\n{RESULTS_CSV}")

df = pd.read_csv(RESULTS_CSV)

print("Columnas disponibles:")
print(df.columns.tolist())


# 11.1 Loss de entrenamiento
loss_columns = [
    "train/box_loss",
    "train/cls_loss",
    "train/dfl_loss",
]

available_losses = [c for c in loss_columns if c in df.columns]

plt.figure(figsize=(12, 6))
for column in available_losses:
    plt.plot(
        df["epoch"],
        df[column],
        label=column.replace("train/", "").replace("_", " ").title(),
    )

plt.xlabel("Época")
plt.ylabel("Loss")
plt.title("AccessAI - Pérdidas de entrenamiento")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# 11.2 mAP
map_columns = [
    "metrics/mAP50(B)",
    "metrics/mAP50-95(B)",
]

available_map = [c for c in map_columns if c in df.columns]

plt.figure(figsize=(12, 6))
for column in available_map:
    plt.plot(
        df["epoch"],
        df[column],
        label=column.replace("metrics/", "").replace("(B)", ""),
    )

plt.xlabel("Época")
plt.ylabel("mAP")
plt.title("AccessAI - Evolución de mAP")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# 11.3 Precision y Recall
pr_columns = [
    "metrics/precision(B)",
    "metrics/recall(B)",
]

available_pr = [c for c in pr_columns if c in df.columns]

plt.figure(figsize=(12, 6))
for column in available_pr:
    nombre = (
        column.replace("metrics/", "")
        .replace("(B)", "")
        .capitalize()
    )
    plt.plot(df["epoch"], df[column], label=nombre)

plt.xlabel("Época")
plt.ylabel("Valor")
plt.title("AccessAI - Precision y Recall")
plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# 11.4 Loss de validación
validation_columns = [
    "val/box_loss",
    "val/cls_loss",
    "val/dfl_loss",
]

available_validation = [c for c in validation_columns if c in df.columns]

if available_validation:
    plt.figure(figsize=(12, 6))

    for column in available_validation:
        plt.plot(
            df["epoch"],
            df[column],
            label=column.replace("val/", "Val ").replace("_", " ").title(),
        )

    plt.xlabel("Época")
    plt.ylabel("Loss")
    plt.title("AccessAI - Loss de validación")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print("No hay columnas de loss de validación en results.csv.")


# 11.5 Resumen de métricas de la última época
metricas_finales = {}

column_map = {
    "mAP50": "metrics/mAP50(B)",
    "mAP50-95": "metrics/mAP50-95(B)",
    "Precision": "metrics/precision(B)",
    "Recall": "metrics/recall(B)",
}

for nombre, columna in column_map.items():
    if columna in df.columns:
        metricas_finales[nombre] = float(df[columna].iloc[-1])

if metricas_finales:
    plt.figure(figsize=(10, 6))
    nombres = list(metricas_finales.keys())
    valores = list(metricas_finales.values())

    plt.bar(nombres, valores)
    plt.ylabel("Valor")
    plt.ylim(0, 1)
    plt.title("AccessAI - Métricas de la última época")
    plt.grid(axis="y")

    for i, valor in enumerate(valores):
        plt.text(
            i,
            min(valor + 0.02, 0.98),
            f"{valor:.3f}",
            ha="center",
        )

    plt.tight_layout()
    plt.show()


# [markdown]
# # 12. Distribución de clases

conteo_clases = {nombre: 0 for nombre in NUEVOS_NOMBRES}
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

                if 0 <= clase_id < NUM_CLASSES:
                    conteo_clases[NUEVOS_NOMBRES[clase_id]] += 1

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
    print("⚠️ No se encontró el directorio de labels de train.")


# [markdown]
# # 13. Matrices de confusión

confusion_candidates = [
    RUN_DIR / "confusion_matrix.png",
    RUN_DIR / "confusion_matrix_normalized.png",
    test_results_dir / "results" / "confusion_matrix.png",
    test_results_dir / "results" / "confusion_matrix_normalized.png",
]

for confusion_path in confusion_candidates:
    if confusion_path.exists():
        image = plt.imread(confusion_path)

        plt.figure(figsize=(12, 10))
        plt.imshow(image)
        plt.axis("off")
        plt.title(f"AccessAI - {confusion_path.name}")
        plt.tight_layout()
        plt.show()

        print("Matriz encontrada:", confusion_path)


# [markdown]
# # 14. Seleccionar una imagen de prueba

import cv2
import matplotlib.pyplot as plt

sample_candidates = [
    ROOT / "tests" / "imgs" / "image.png",
    ROOT / "tests" / "imgs" / "IMG_20170311_205902.jpg",
    DATASET_PATH / "test" / "images" / "IMG_19187.jpg",
]

image_path = next(
    (p for p in sample_candidates if p.exists()),
    None,
)

if image_path is None:
    # Fallback: primera imagen disponible del test.
    test_images = sorted((DATASET_PATH / "test" / "images").glob("*"))
    image_path = test_images[0] if test_images else None

if image_path is None:
    raise FileNotFoundError("No se encontró ninguna imagen de prueba.")

print("Imagen:")
print(image_path)


# [markdown]
# # 15. Inferencia

results_predict = trained_model.predict(
    source=str(image_path),
    conf=0.25,
    imgsz=640,
    device=device,
    verbose=False,
)

result = results_predict[0]

print(f"Detecciones encontradas: {len(result.boxes)}")

if result.boxes is not None and len(result.boxes) > 0:
    for idx, box in enumerate(result.boxes, start=1):
        cls_id = int(box.cls[0])
        cls_name = trained_model.names[cls_id]
        confidence = float(box.conf[0])
        coords = [round(float(x), 2) for x in box.xyxy[0].tolist()]

        print(
            f"[{idx}] "
            f"{cls_name} | "
            f"conf={confidence:.3f} | "
            f"bbox={coords}"
        )
else:
    print("No se detectaron objetos con conf=0.25.")


# [markdown]
# # 16. Guardar y mostrar la imagen anotada

output_dir = ROOT / "resultados"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "accessai_resultado.jpg"

annotated = result.plot()

ok = cv2.imwrite(str(output_path), annotated)

if not ok:
    raise IOError(f"No se pudo guardar la imagen en:\n{output_path}")

print("✅ Imagen guardada en:")
print(output_path)

annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(14, 8))
plt.imshow(annotated_rgb)
plt.axis("off")
plt.title("AccessAI - Detección urbana")
plt.tight_layout()
plt.show()


# [markdown]
# # 17. Resumen del experimento
#
# Conserva al menos:
#
# - `best.pt`
# - `last.pt`
# - `results.csv`
# - `confusion_matrix.png`
# - `results.png`
# - imagen anotada de inferencia
# - mAP50
# - mAP50-95
# - Precision
# - Recall
# - F1 derivado de Precision y Recall
#
# ## Interpretación
#
# Las métricas corresponden exclusivamente al experimento de cuatro categorías agrupadas sobre el ROD-Dataset. No deben presentarse como una medición directa de accesibilidad urbana.
#
# El siguiente paso del proyecto sería estudiar un dataset/clase realmente específico de accesibilidad, por ejemplo para elementos como `sidewalk` o `curbramp`, si esas clases son necesarias para el objetivo final.

