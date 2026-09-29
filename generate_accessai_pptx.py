import json
from pathlib import Path

nb = {
 "cells": [
  {"cell_type":"markdown","metadata":{},"source":[
   "# AccessAI - Prototipo de detección urbana\n\n",
   "Notebook completo para preparar ROD-Dataset, remapear 25 clases a 4 categorías, entrenar YOLO26n en RTX 4060, evaluar en test y ejecutar inferencia.\n\n",
   "## Clases finales\n\n",
   "| ID | Clase |\n|---:|---|\n| 0 | `Obstaculo_Dinamico` |\n| 1 | `Obstaculo_Fijo` |\n| 2 | `Barrera_Arquitectonica` |\n| 3 | `Infraestructura_Peatonal` |\n\n",
   "**Configuración GPU:** batch fijo `8`, `imgsz=640`, `AMP=True`, `workers=0`, `cache='disk'`. No se usa `batch=-1` para evitar AutoBatch y su posible OOM."
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 01. Entorno y GPU"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "from pathlib import Path\nimport torch\n\nprint('=' * 70)\nprint('ACCESSAI - ENTORNO Y GPU')\nprint('=' * 70)\nprint(f'PyTorch: {torch.__version__}')\nprint(f'CUDA disponible: {torch.cuda.is_available()}')\nprint(f'CUDA de PyTorch: {torch.version.cuda}')\nprint(f'HIP: {torch.version.hip}')\n\nif torch.cuda.is_available():\n    props = torch.cuda.get_device_properties(0)\n    print(f'GPU: {torch.cuda.get_device_name(0)}')\n    print(f'GPU count: {torch.cuda.device_count()}')\n    print(f'Memoria GPU: {props.total_memory / 1024**3:.2f} GB')\n    print(f'Compute capability: {props.major}.{props.minor}')\n    print(f'Memoria reservada: {torch.cuda.memory_reserved(0) / 1024**3:.2f} GB')\n    print(f'Memoria asignada: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB')\nelse:\n    raise RuntimeError('CUDA no disponible. Se cancela el notebook para evitar entrenamiento CPU.')\nprint('=' * 70)"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 02. Comprobar Ultralytics"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "import ultralytics\nprint('Ultralytics:', ultralytics.__version__)\n"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 03. Configuración del dataset"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "from pathlib import Path\nimport shutil\nimport yaml\nfrom collections import Counter\n\nROOT = Path.cwd()\nDATASET_PATH = ROOT / 'DATA' / 'ROD-Dataset' / 'dataset'\nyaml_original_path = DATASET_PATH / 'data.yaml'\nyaml_nuevo_path = DATASET_PATH / 'data_filtrado.yaml'\n\nprint('Dataset:', DATASET_PATH)\nprint('Existe dataset:', DATASET_PATH.exists())\nprint('Existe data.yaml:', yaml_original_path.exists())\n\nif not DATASET_PATH.exists():\n    raise FileNotFoundError(f'No existe el dataset:\\n{DATASET_PATH}')\nif not yaml_original_path.exists():\n    raise FileNotFoundError(f'No existe:\\n{yaml_original_path}')"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 04. Mapeo de clases del ROD-Dataset"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "MAPEO_CLASES = {\n"
   "    0: 0, 2: 0, 3: 0, 8: 0, 10: 0, 15: 0, 16: 0,\n"
   "    5: 1, 6: 1, 9: 1, 12: 1, 13: 1, 17: 1, 18: 1,\n"
   "    19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1,\n"
   "    4: 2,\n"
   "    7: 3, 11: 3, 14: 3\n"
   "}\n\n"
   "NUEVOS_NOMBRES = [\n"
   "    'Obstaculo_Dinamico',\n"
   "    'Obstaculo_Fijo',\n"
   "    'Barrera_Arquitectonica',\n"
   "    'Infraestructura_Peatonal'\n"
   "]\n"
   "NUM_CLASSES = len(NUEVOS_NOMBRES)\n\n"
   "for idx, nombre in enumerate(NUEVOS_NOMBRES):\n"
   "    print(f'{idx}: {nombre}')\n"
   "print(f'Número de clases: {NUM_CLASSES}')"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 05. Crear `data_filtrado.yaml`"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "with open(yaml_original_path, 'r', encoding='utf-8') as f:\n"
   "    config_original = yaml.safe_load(f)\n\n"
   "config_nueva = {\n"
   "    'path': str(DATASET_PATH.resolve()),\n"
   "    'train': 'train/images',\n"
   "    'val': 'valid/images',\n"
   "    'test': 'test/images',\n"
   "    'nc': NUM_CLASSES,\n"
   "    'names': NUEVOS_NOMBRES\n"
   "}\n\n"
   "with open(yaml_nuevo_path, 'w', encoding='utf-8') as f:\n"
   "    yaml.safe_dump(config_nueva, f, sort_keys=False, allow_unicode=True)\n\n"
   "print('YAML creado:', yaml_nuevo_path)\nprint(yaml_nuevo_path.read_text(encoding='utf-8'))"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 06. Preparar etiquetas\n\nLas etiquetas originales se conservan en `labels_originales`. La transformación es idempotente."]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "def preparar_etiquetas(split):\n"
   "    split_dir = DATASET_PATH / split\n"
   "    labels_dir = split_dir / 'labels'\n"
   "    labels_originales_dir = split_dir / 'labels_originales'\n\n"
   "    if not split_dir.exists():\n"
   "        raise FileNotFoundError(f'No existe el split:\\n{split_dir}')\n\n"
   "    if labels_originales_dir.exists():\n"
   "        source_dir = labels_originales_dir\n"
   "        print(f'↪ {split}: usando labels_originales como fuente')\n"
   "    elif labels_dir.exists():\n"
   "        print(f'↪ {split}: guardando labels originales')\n"
   "        labels_dir.rename(labels_originales_dir)\n"
   "        source_dir = labels_originales_dir\n"
   "    else:\n"
   "        raise FileNotFoundError(f'No existe la carpeta labels en:\\n{split_dir}')\n\n"
   "    labels_filtradas_dir = split_dir / 'labels_filtradas'\n"
   "    if labels_filtradas_dir.exists():\n"
   "        shutil.rmtree(labels_filtradas_dir)\n"
   "    labels_filtradas_dir.mkdir(parents=True, exist_ok=True)\n\n"
   "    clases_originales = Counter()\n"
   "    clases_nuevas = Counter()\n"
   "    clases_descartadas = Counter()\n"
   "    archivos_procesados = 0\n\n"
   "    for archivo in sorted(source_dir.glob('*.txt')):\n"
   "        archivos_procesados += 1\n"
   "        ruta_salida = labels_filtradas_dir / archivo.name\n"
   "        nuevas_lineas = []\n\n"
   "        with open(archivo, 'r', encoding='utf-8') as f:\n"
   "            for linea in f:\n"
   "                partes = linea.strip().split()\n"
   "                if not partes:\n"
   "                    continue\n"
   "                try:\n"
   "                    clase_original = int(partes[0])\n"
   "                except ValueError:\n"
   "                    print(f'⚠️ Clase inválida en {archivo.name}: {partes[0]}')\n"
   "                    continue\n\n"
   "                clases_originales[clase_original] += 1\n\n"
   "                if clase_original not in MAPEO_CLASES:\n"
   "                    clases_descartadas[clase_original] += 1\n"
   "                    continue\n\n"
   "                clase_nueva = MAPEO_CLASES[clase_original]\n"
   "                partes[0] = str(clase_nueva)\n"
   "                nuevas_lineas.append(' '.join(partes) + '\\n')\n"
   "                clases_nuevas[clase_nueva] += 1\n\n"
   "        with open(ruta_salida, 'w', encoding='utf-8') as f:\n"
   "            f.writelines(nuevas_lineas)\n\n"
   "    if labels_dir.exists():\n"
   "        shutil.rmtree(labels_dir)\n"
   "    labels_filtradas_dir.rename(labels_dir)\n\n"
   "    print('\\n' + '-' * 70)\n"
   "    print(f'Split: {split}')\n"
   "    print(f'Archivos procesados: {archivos_procesados}')\n"
   "    print('Clases originales:', dict(sorted(clases_originales.items())))\n"
   "    print('Clases finales:')\n"
   "    for clase, nombre in enumerate(NUEVOS_NOMBRES):\n"
   "        print(f'  {clase} - {nombre}: {clases_nuevas[clase]}')\n"
   "    print('Clases descartadas:', dict(sorted(clases_descartadas.items())))\n\n"
   "for split in ['train', 'valid', 'test']:\n"
   "    preparar_etiquetas(split)"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 07. Comprobar estructura del dataset"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "for split in ['train', 'valid', 'test']:\n"
   "    split_dir = DATASET_PATH / split\n"
   "    images_dir = split_dir / 'images'\n"
   "    labels_dir = split_dir / 'labels'\n"
   "    originals_dir = split_dir / 'labels_originales'\n"
   "    image_count = len(list(images_dir.glob('*')))\n"
   "    label_count = len(list(labels_dir.glob('*.txt')))\n"
   "    original_count = len(list(originals_dir.glob('*.txt')))\n"
   "    print('=' * 70)\n"
   "    print(split)\n"
   "    print(f'Imágenes:          {image_count}')\n"
   "    print(f'Labels activas:    {label_count}')\n"
   "    print(f'Labels originales: {original_count}')"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 08. Entrenamiento YOLO26n\n\n**RTX 4060 Laptop 8 GB:** batch fijo `8`, `imgsz=640`, `AMP=True`, `workers=0`, `cache='disk'`. No se usa `batch=-1` para evitar AutoBatch."]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "import gc\n"
   "import ultralytics\n"
   "from ultralytics import YOLO\n\n"
   "gc.collect()\n"
   "torch.cuda.empty_cache()\n\n"
   "device = 0\n"
   "torch.backends.cuda.matmul.allow_tf32 = True\n"
   "torch.backends.cudnn.allow_tf32 = True\n\n"
   "MODEL_PATH = ROOT / 'yolo26n.pt'\n"
   "EPOCHS = 35\n"
   "PATIENCE = 8\n"
   "IMGSZ = 640\n"
   "BATCH = 8\n"
   "WORKERS = 0\n"
   "AMP = True\n"
   "OPTIMIZER = 'AdamW'\n"
   "LR0 = 0.001\n"
   "SEED = 42\n"
   "CACHE = 'disk'\n"
   "CLOSE_MOSAIC = 10\n"
   "PROJECT_DIR = ROOT / 'AccessAI_Proto3'\n"
   "RUN_NAME = 'yolo26n_4clases'\n\n"
   "if not MODEL_PATH.exists():\n"
   "    raise FileNotFoundError(f'No se encontró: {MODEL_PATH}')\n"
   "if not yaml_nuevo_path.exists():\n"
   "    raise FileNotFoundError(f'No existe: {yaml_nuevo_path}')\n\n"
   "props = torch.cuda.get_device_properties(device)\n"
   "print('=' * 72)\n"
   "print('ACCESSAI - YOLO26n - ENTRENAMIENTO GPU')\n"
   "print('=' * 72)\n"
   "print(f'Ultralytics : {ultralytics.__version__}')\n"
   "print(f'GPU         : {torch.cuda.get_device_name(device)}')\n"
   "print(f'VRAM total  : {props.total_memory / 1024**3:.2f} GB')\n"
   "print(f'Epochs      : {EPOCHS}')\n"
   "print(f'Batch       : {BATCH}')\n"
   "print(f'Image size  : {IMGSZ}')\n"
   "print(f'Workers     : {WORKERS}')\n"
   "print(f'AMP         : {AMP}')\n"
   "print(f'Optimizer   : {OPTIMIZER}')\n"
   "print(f'Cache       : {CACHE}')\n"
   "print('=' * 72)\n\n"
   "model = YOLO(str(MODEL_PATH))\n\n"
   "try:\n"
   "    results = model.train(\n"
   "        data=str(yaml_nuevo_path),\n"
   "        epochs=EPOCHS,\n"
   "        patience=PATIENCE,\n"
   "        imgsz=IMGSZ,\n"
   "        batch=BATCH,\n"
   "        device=device,\n"
   "        workers=WORKERS,\n"
   "        cache=CACHE,\n"
   "        amp=AMP,\n"
   "        optimizer=OPTIMIZER,\n"
   "        lr0=LR0,\n"
   "        cos_lr=True,\n"
   "        augment=True,\n"
   "        mosaic=1.0,\n"
   "        close_mosaic=CLOSE_MOSAIC,\n"
   "        mixup=0.0,\n"
   "        cls=1.0,\n"
   "        val=True,\n"
   "        save=True,\n"
   "        save_period=5,\n"
   "        plots=True,\n"
   "        seed=SEED,\n"
   "        project=str(PROJECT_DIR),\n"
   "        name=RUN_NAME,\n"
   "        exist_ok=False,\n"
   "        verbose=True\n"
   "    )\n"
   "except torch.cuda.OutOfMemoryError as exc:\n"
   "    gc.collect()\n"
   "    torch.cuda.empty_cache()\n"
   "    raise RuntimeError(\n"
   "        'CUDA OOM. Prueba BATCH=4; si persiste, BATCH=2.'\n"
   "    ) from exc\n\n"
   "print('\\n✅ ENTRENAMIENTO TERMINADO')\n"
   "print('Directorio:', results.save_dir)"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 09. Cargar `best.pt` entrenado"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "RUN_DIR = Path(results.save_dir)\n"
   "BEST_MODEL = RUN_DIR / 'weights' / 'best.pt'\n\n"
   "if not BEST_MODEL.exists():\n"
   "    raise FileNotFoundError(f'No se encontró best.pt en:\\n{BEST_MODEL}')\n\n"
   "trained_model = YOLO(str(BEST_MODEL))\n"
   "print('RUN_DIR:', RUN_DIR)\n"
   "print('BEST_MODEL:', BEST_MODEL)\n"
   "print('\\nClases:')\n"
   "for idx, name in trained_model.names.items():\n"
   "    print(idx, '->', name)"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 10. Evaluación en `test`"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "eval_batch = 8\n\n"
   "metrics = trained_model.val(\n"
   "    data=str(yaml_nuevo_path),\n"
   "    split='test',\n"
   "    imgsz=640,\n"
   "    batch=eval_batch,\n"
   "    device=device,\n"
   "    plots=True\n"
   ")\n\n"
   "print('\\n' + '=' * 70)\n"
   "print('MÉTRICAS TEST')\n"
   "print('=' * 70)\n"
   "print(f'mAP50:    {metrics.box.map50:.4f}')\n"
   "print(f'mAP50-95: {metrics.box.map:.4f}')"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 11. `results.csv` y curvas de entrenamiento"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "import pandas as pd\n"
   "import matplotlib.pyplot as plt\n\n"
   "results_csv = RUN_DIR / 'results.csv'\n"
   "if not results_csv.exists():\n"
   "    raise FileNotFoundError(f'No existe:\\n{results_csv}')\n\n"
   "df = pd.read_csv(results_csv)\n"
   "print(df.columns.tolist())"
  ]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "%matplotlib inline\n\n"
   "plt.figure(figsize=(12, 6))\n"
   "plt.plot(df['epoch'], df['train/box_loss'], label='Train Box Loss')\n"
   "plt.plot(df['epoch'], df['train/cls_loss'], label='Train Class Loss')\n"
   "plt.plot(df['epoch'], df['train/dfl_loss'], label='Train DFL Loss')\n"
   "plt.xlabel('Época')\n"
   "plt.ylabel('Loss')\n"
   "plt.title('AccessAI - Pérdidas de entrenamiento')\n"
   "plt.grid(True)\n"
   "plt.legend()\n"
   "plt.tight_layout()\n"
   "plt.show()"
  ]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "plt.figure(figsize=(12, 6))\n"
   "plt.plot(df['epoch'], df['metrics/mAP50(B)'], label='mAP50')\n"
   "plt.plot(df['epoch'], df['metrics/mAP50-95(B)'], label='mAP50-95')\n"
   "plt.xlabel('Época')\n"
   "plt.ylabel('mAP')\n"
   "plt.title('AccessAI - Métricas de detección')\n"
   "plt.grid(True)\n"
   "plt.legend()\n"
   "plt.tight_layout()\n"
   "plt.show()"
  ]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "plt.figure(figsize=(12, 6))\n"
   "plt.plot(df['epoch'], df['metrics/precision(B)'], label='Precision')\n"
   "plt.plot(df['epoch'], df['metrics/recall(B)'], label='Recall')\n"
   "plt.xlabel('Época')\n"
   "plt.ylabel('Valor')\n"
   "plt.title('AccessAI - Precision y Recall')\n"
   "plt.grid(True)\n"
   "plt.legend()\n"
   "plt.tight_layout()\n"
   "plt.show()"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 12. Seleccionar imagen de prueba"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "sample_candidates = [\n"
   "    ROOT / 'tests' / 'imgs' / 'image.png',\n"
   "    ROOT / 'tests' / 'imgs' / 'IMG_20170311_205902.jpg',\n"
   "    ROOT / 'DATA' / 'ROD-Dataset' / 'dataset' / 'test' / 'images' / 'IMG_19187.jpg'\n"
   "]\n\n"
   "image_path = next((p for p in sample_candidates if p.exists()), None)\n\n"
   "if image_path is None:\n"
   "    raise FileNotFoundError('No se encontró ninguna imagen de prueba.')\n\n"
   "print('Imagen:', image_path)"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 13. Inferencia"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "results_predict = trained_model.predict(\n"
   "    source=str(image_path),\n"
   "    conf=0.25,\n"
   "    imgsz=640,\n"
   "    device=device,\n"
   "    verbose=False\n"
   ")\n\n"
   "result = results_predict[0]\n"
   "print(f'\\nDetecciones encontradas: {len(result.boxes)}')\n\n"
   "if result.boxes is not None and len(result.boxes) > 0:\n"
   "    for idx, box in enumerate(result.boxes, start=1):\n"
   "        cls_id = int(box.cls[0])\n"
   "        cls_name = trained_model.names[cls_id]\n"
   "        confidence = float(box.conf[0])\n"
   "        coords = box.xyxy[0].tolist()\n"
   "        print(f'[{idx}] {cls_name} | conf={confidence:.3f} | bbox={coords}')\n"
   "else:\n"
   "    print('No se detectaron objetos con conf=0.25.')"
  ]},
  {"cell_type":"markdown","metadata":{},"source":["# 14. Guardar y mostrar imagen anotada"]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "import cv2\n\n"
   "output_dir = ROOT / 'resultados'\n"
   "output_dir.mkdir(parents=True, exist_ok=True)\n"
   "output_path = output_dir / 'accessai_resultado.jpg'\n\n"
   "annotated = result.plot()\n"
   "ok = cv2.imwrite(str(output_path), annotated)\n\n"
   "if not ok:\n"
   "    raise IOError(f'No se pudo guardar la imagen en:\\n{output_path}')\n\n"
   "print('✅ Imagen guardada en:', output_path)\n\n"
   "annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)\n"
   "plt.figure(figsize=(14, 8))\n"
   "plt.imshow(annotated_rgb)\n"
   "plt.axis('off')\n"
   "plt.title('AccessAI - Detección urbana')\n"
   "plt.tight_layout()\n"
   "plt.show()"
  ]},
  {"cell_type":"markdown","metadata":{},"source":[
   "# 15. Resumen del experimento\n\n",
   "Conservar al menos:\n",
   "- `best.pt`\n",
   "- `last.pt`\n",
   "- `results.csv`\n",
   "- `confusion_matrix.png`\n",
   "- `results.png`\n",
   "- imagen anotada de inferencia\n",
   "- mAP50 y mAP50-95\n",
   "- Precision y Recall\n\n",
   "El objetivo del prototipo es medir la capacidad del modelo para detectar las cuatro categorías seleccionadas del ROD-Dataset."
  ]},
  {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[
   "print('=' * 72)\n"
   "print('ACCESSAI - RESUMEN')\n"
   "print('=' * 72)\n"
   "print('Modelo:', BEST_MODEL)\n"
   "print('Resultados:', RUN_DIR)\n"
   "print(f'mAP50 test: {metrics.box.map50:.4f}')\n"
   "print(f'mAP50-95 test: {metrics.box.map:.4f}')\n"
   "print('CSV:', results_csv)\n"
   "print('Imagen:', output_path)\n"
   "print('=' * 72)"
  ]}
 ],
 "metadata": {
  "kernelspec": {"display_name":"Python 3","language":"python","name":"python3"},
  "language_info": {"name":"python","version":"3.11"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

path = Path("/mnt/data/AccessAI_YOLO26n_4clases_Stable.ipynb")
path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Notebook creado: {path}")
