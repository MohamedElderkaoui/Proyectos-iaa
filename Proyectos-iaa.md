This file is a merged representation of the entire codebase, combined into a single document by Repomix.
The content has been processed where content has been compressed (code blocks are separated by ⋮---- delimiter).

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.gitignore
ACCESSAI_firstProto_colab.ipynb
ACCESSAI_firstProto.ipynb
ActionPlan.txt
dependencias.txt
generate_accessai_pptx_v2_0_2.py
generate_accessai_pptx.py
inspect_theme.py
PLAN.md
README.md
```

# Files

## File: .gitignore
````
/.venv
/~$AccessAI_Capstone_Presentation_v2_0_2.pptx
/~$C_AI_Capstone Project_Action Plan(6).txt
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[codz]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#   Usually these files are written by a python script from a template
#   before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py.cover
*.lcov
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
# Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
# uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
# poetry.lock
# poetry.toml

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#   pdm recommends including project-wide configuration in pdm.toml, but excluding .pdm-python.
#   https://pdm-project.org/en/latest/usage/project/#working-with-version-control
# pdm.lock
# pdm.toml
.pdm-python
.pdm-build/

# pixi
#   Similar to Pipfile.lock, it is generally recommended to include pixi.lock in version control.
# pixi.lock
#   Pixi creates a virtual environment in the .pixi directory, just like venv module creates one
#   in the .venv directory. It is recommended not to include this directory in version control.
.pixi/*
!.pixi/config.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule*
celerybeat.pid

# Redis
*.rdb
*.aof
*.pid

# RabbitMQ
mnesia/
rabbitmq/
rabbitmq-data/

# ActiveMQ
activemq-data/

# SageMath parsed files
*.sage.py

# Environments
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#   JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#   be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#   and can be added to the global gitignore or merged into this file.  For a more nuclear
#   option (not recommended) you can uncomment the following to ignore the entire idea folder.
# .idea/

# Abstra
#   Abstra is an AI-powered process automation framework.
#   Ignore directories containing user credentials, local state, and settings.
#   Learn more at https://abstra.io/docs
.abstra/

# Visual Studio Code
#   Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore that
#   can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#   and can be added to the global gitignore or merged into this file. However, if you prefer, you
#   could uncomment the following to ignore the entire vscode folder
# .vscode/
# Temporary file for partial code execution
tempCodeRunnerFile.py

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Marimo
marimo/_static/
marimo/_lsp/
__marimo__/

# Streamlit
.streamlit/secrets.toml

# Dataset
dataset/
ROD-Dataset/
````

## File: ACCESSAI_firstProto_colab.ipynb
````
{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "7d359207-6043-4b22-9080-b807129c9f39",
   "metadata": {
    "id": "7d359207-6043-4b22-9080-b807129c9f39"
   },
   "source": [
    "# ACCESSAI: First Proto"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7e13ffe6-a4ec-4a1a-a76e-cd49c50ce6ec",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "7e13ffe6-a4ec-4a1a-a76e-cd49c50ce6ec",
    "outputId": "015dc4e4-802e-47af-c64a-6f277e56511f"
   },
   "outputs": [],
   "source": [
    "!pip install ultralytics"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "eaea658d-02eb-4362-8cdd-888c4a9283f5",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "eaea658d-02eb-4362-8cdd-888c4a9283f5",
    "outputId": "436f1a80-595d-43fb-b90f-cb88918106a0"
   },
   "outputs": [],
   "source": [
    "!nvidia-smi"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "cb9ddd0f-ad95-492c-b69a-f63887beb131",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "cb9ddd0f-ad95-492c-b69a-f63887beb131",
    "outputId": "235c4e6f-df09-4995-ea54-76a75aee51e5"
   },
   "outputs": [],
   "source": [
    "from ultralytics import YOLO\n",
    "import torch\n",
    "import os\n",
    "import yaml\n",
    "import requests"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ETyHiA18hFNI",
   "metadata": {
    "id": "ETyHiA18hFNI"
   },
   "outputs": [],
   "source": [
    "!unzip -q /content/dataset.zip -d /content/"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "18363f81-22eb-484f-8248-3b5818f7d465",
   "metadata": {
    "id": "18363f81-22eb-484f-8248-3b5818f7d465"
   },
   "outputs": [],
   "source": [
    "DATASET_PATH = \"dataset\"  # Ajusta si es necesario"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "aa44627f-239e-49d2-91d5-1e8ba390662d",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "aa44627f-239e-49d2-91d5-1e8ba390662d",
    "outputId": "7bd77145-bfde-4d58-e092-da7ca3f4f011"
   },
   "outputs": [],
   "source": [
    "# 1. Verificar la estructura de carpetas\n",
    "print(\"Estructura del dataset:\")\n",
    "for split in ['train', 'valid', 'test']:\n",
    "    split_path = os.path.join(DATASET_PATH, split)\n",
    "    if os.path.exists(split_path):\n",
    "        images_path = os.path.join(split_path, 'images')\n",
    "        labels_path = os.path.join(split_path, 'labels')\n",
    "        n_images = len(os.listdir(images_path)) if os.path.exists(images_path) else 0\n",
    "        n_labels = len(os.listdir(labels_path)) if os.path.exists(labels_path) else 0\n",
    "        print(f\"  {split}: {n_images} imágenes, {n_labels} labels\")\n",
    "    else:\n",
    "        print(f\"  {split}: ❌ No existe\")\n",
    "\n",
    "# 2. Leer el data.yaml\n",
    "yaml_path = os.path.join(DATASET_PATH, \"data.yaml\")\n",
    "with open(yaml_path, 'r') as f:\n",
    "    data_config = yaml.safe_load(f)\n",
    "\n",
    "print(\"\\nContenido del data.yaml:\")\n",
    "print(f\"  nc: {data_config.get('nc')}\")\n",
    "print(f\"  names: {data_config.get('names')}\")\n",
    "print(f\"  train: {data_config.get('train')}\")\n",
    "print(f\"  val: {data_config.get('val')}\")\n",
    "print(f\"  test: {data_config.get('test')}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ac85175b-6dd3-4d97-b570-41abbb288b28",
   "metadata": {
    "id": "ac85175b-6dd3-4d97-b570-41abbb288b28"
   },
   "source": [
    "#### IMPORTANTE: Habrá que reducir el número de clases y seleccionar aquellas que consideremos más importantes para la detección de barreras de accesibilidad urbana. También habrá que compensar el desbalance entre las clases seleccionadas si este existiera."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c2b83505-c31c-4e0b-a26b-7b5ab0977a28",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "c2b83505-c31c-4e0b-a26b-7b5ab0977a28",
    "outputId": "383780dd-2345-41a9-e8f9-b7c7471e988b"
   },
   "outputs": [],
   "source": [
    "# Descarga del modelo preentrenado y validación inicial con el dataset.\n",
    "!yolo val model=yolo26n.pt data=dataset/data.yaml"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7513b281-5fd8-450e-a35f-4fbec88a4c1c",
   "metadata": {
    "id": "7513b281-5fd8-450e-a35f-4fbec88a4c1c"
   },
   "source": [
    "#### mAP: mean Average Precision, métrica estándar para evaluar modelos de detección de objetos, que mide cuán bueno es el modelo detectando objetos y localizándolos correctamente. maP50 a 0.0333, MUY BAJO, el modelo intenta detectar las clases de nuestro dataset pero solo conoce las clases mediante las que ha sido entrenado"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "91c4a512-6d4e-4420-8726-d62c1b51f1be",
   "metadata": {
    "id": "91c4a512-6d4e-4420-8726-d62c1b51f1be"
   },
   "outputs": [],
   "source": [
    "model = YOLO(\"yolo26n.pt\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "512c0dba-7efb-44ce-ae0c-57eefe5da7f5",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "512c0dba-7efb-44ce-ae0c-57eefe5da7f5",
    "outputId": "72d533c8-c48a-46d3-947c-03ea8fe49476"
   },
   "outputs": [],
   "source": [
    "# Entenamiento base del modelo, punto de partida:\n",
    "\n",
    "results = model.train(\n",
    "    data=\"dataset/data.yaml\",\n",
    "    epochs=50,\n",
    "    imgsz=640,\n",
    "    batch=16,\n",
    "    device=0    # Activa la GPU\n",
    ")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d397dc69-fd06-4bd9-872a-89ccf88bc2b7",
   "metadata": {
    "id": "d397dc69-fd06-4bd9-872a-89ccf88bc2b7"
   },
   "source": [
    "### Métricas del entrenamiento\n",
    "\n",
    "Durante el entrenamiento, Ultralytics muestra una serie de métricas que reflejan el rendimiento del modelo. Estas son las más importantes:\n",
    "\n",
    "#### Pérdidas (Losses)\n",
    "\n",
    "| Métrica | ¿Qué mide? | ¿Qué esperar? |\n",
    "| :--- | :--- | :--- |\n",
    "| **box_loss** | Error en la localización de las bounding boxes (coordenadas). | Debe bajar con las épocas. |\n",
    "| **cls_loss** | Error en la clasificación de cada objeto (¿es un coche? ¿una persona?). | Debe bajar con las épocas. |\n",
    "| **l1_loss** | Pérdida auxiliar de regresión que ayuda a estabilizar el entrenamiento. | Debe bajar con las épocas. |\n",
    "\n",
    "#### Métricas de evaluación (Box)\n",
    "\n",
    "| Métrica | ¿Qué mide? | ¿Qué esperar? |\n",
    "| :--- | :--- | :--- |\n",
    "| **Precision (P)** | De todos los objetos que el modelo detecta, ¿cuántos son correctos? | Cuanto más alto, mejor. Cercano a 1.0 es ideal. |\n",
    "| **Recall (R)** | De todos los objetos reales, ¿cuántos detecta el modelo? | Cuanto más alto, mejor. Cercano a 1.0 es ideal. |\n",
    "| **mAP50** | Precisión media con un umbral de solapamiento (IoU) del 50%. | Cuanto más alto, mejor. >0.90 es excelente. |\n",
    "| **mAP50-95** | Precisión media promediada sobre umbrales de IoU de 50% a 95%. | Cuanto más alto, mejor. >0.70 es muy bueno. |\n",
    "\n",
    "#### Otras métricas\n",
    "\n",
    "| Métrica | ¿Qué mide? |\n",
    "| :--- | :--- |\n",
    "| **Instances** | Número de objetos anotados en el batch actual. |\n",
    "| **GPU_mem** | Memoria de la GPU utilizada durante el entrenamiento. |\n",
    "| **Size** | Tamaño de las imágenes de entrada (ej. 640x640). |\n",
    "\n",
    "#### ¿Qué es el IoU?\n",
    "\n",
    "El **IoU** (Intersection over Union) mide el solapamiento entre la bounding box predicha y la real. Va de 0 (sin solapamiento) a 1 (solapamiento perfecto). Un IoU de 0.5 significa que la predicción cubre al menos el 50% del objeto real.\n",
    "\n",
    "#### ¿Qué es el mAP?\n",
    "\n",
    "El **mAP** (mean Average Precision) es la métrica estándar para evaluar modelos de detección de objetos. Combina Precision y Recall en un solo número. Un mAP alto significa que el modelo detecta los objetos correctamente y con buena localización."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5638b670-903b-4abf-9d28-30935962f150",
   "metadata": {
    "id": "5638b670-903b-4abf-9d28-30935962f150"
   },
   "source": [
    "Si el mAP es bueno (>0.90) → Documentar y pasar a la demo.\n",
    "\n",
    "Si el mAP es bajo (<0.80) → Analizar qué clases fallan y considerar:\n",
    "\n",
    "    Más épocas.\n",
    "\n",
    "    Data augmentation específico.\n",
    "\n",
    "    Ajuste de hiperparámetros con model.tune().\n",
    "\n",
    "Si la demo falla mucho → Documentar la limitación de dominio y proponer fine-tuning con imágenes locales como trabajo futuro."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ca06181a-6250-463d-b38b-54a3cecf08f8",
   "metadata": {
    "id": "ca06181a-6250-463d-b38b-54a3cecf08f8"
   },
   "outputs": [],
   "source": [
    "model = YOLO(\"runs/detect/train/weights/best.pt\")  # Cargamos el mejor modelo"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c957b103-6669-4b1f-81be-f179986b63f3",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "c957b103-6669-4b1f-81be-f179986b63f3",
    "outputId": "870d6d5e-2c93-4879-c0a3-dc7631a69924"
   },
   "outputs": [],
   "source": [
    "metrics = model.val(data=\"dataset/data.yaml\", split=\"test\")  # Evaluamos"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "80395950-e704-4d06-b71d-3aba0990fa9b",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "80395950-e704-4d06-b71d-3aba0990fa9b",
    "outputId": "0c342c51-92f3-498b-9f52-30a09650ebe4"
   },
   "outputs": [],
   "source": [
    "print(f\"mAP50: {metrics.box.map50:.4f}\")\n",
    "print(f\"mAP50-95: {metrics.box.map:.4f}\")\n",
    "print(f\"Precision: {metrics.box.mp:.4f}\")\n",
    "print(f\"Recall: {metrics.box.mr:.4f}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bffcbfaf-5db3-4cfb-a79f-800e2f3cfc05",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 850
    },
    "id": "bffcbfaf-5db3-4cfb-a79f-800e2f3cfc05",
    "outputId": "51ed58ee-f9ee-4ab9-b67b-728706745963"
   },
   "outputs": [],
   "source": [
    "from PIL import Image\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "img = Image.open(\"runs/detect/train/confusion_matrix_normalized.png\")  # Matriz de confusión\n",
    "plt.figure(figsize=(14, 12))\n",
    "plt.imshow(img)\n",
    "plt.axis('off')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0f190f4b-ab4d-43b5-88ee-ae667453b092",
   "metadata": {
    "id": "0f190f4b-ab4d-43b5-88ee-ae667453b092"
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "accelerator": "GPU",
  "colab": {
   "gpuType": "T4",
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python (yoloEnv)",
   "language": "python",
   "name": "yoloenv"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.16"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
````

## File: ACCESSAI_firstProto.ipynb
````
{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "7d359207-6043-4b22-9080-b807129c9f39",
   "metadata": {},
   "source": [
    "# ACCESSAI: First Proto"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7e13ffe6-a4ec-4a1a-a76e-cd49c50ce6ec",
   "metadata": {},
   "outputs": [],
   "source": [
    "from ultralytics import YOLO\n",
    "import torch\n",
    "import os\n",
    "import yaml\n",
    "import requests\n",
    "from collections import Counter\n",
    "import matplotlib.pyplot as plt\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "eaea658d-02eb-4362-8cdd-888c4a9283f5",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(f\"¿GPU disponible? {torch.cuda.is_available()}\")\n",
    "print(f\"Dispositivo: {torch.cuda.get_device_name(0)}\")\n",
    "print(f\"Versión HIP: {torch.version.hip}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "aa44627f-239e-49d2-91d5-1e8ba390662d",
   "metadata": {},
   "outputs": [],
   "source": [
    "DATASET_PATH = \"dataset\"  # Ajusta si es necesario\n",
    "\n",
    "# 1. Verificar la estructura de carpetas\n",
    "print(\"Estructura del dataset:\")\n",
    "for split in ['train', 'valid', 'test']:\n",
    "    split_path = os.path.join(DATASET_PATH, split)\n",
    "    if os.path.exists(split_path):\n",
    "        images_path = os.path.join(split_path, 'images')\n",
    "        labels_path = os.path.join(split_path, 'labels')\n",
    "        n_images = len(os.listdir(images_path)) if os.path.exists(images_path) else 0\n",
    "        n_labels = len(os.listdir(labels_path)) if os.path.exists(labels_path) else 0\n",
    "        print(f\"  {split}: {n_images} imágenes, {n_labels} labels\")\n",
    "    else:\n",
    "        print(f\"  {split}: ❌ No existe\")\n",
    "\n",
    "# 2. Leer el data.yaml\n",
    "yaml_path = os.path.join(DATASET_PATH, \"data.yaml\")\n",
    "with open(yaml_path, 'r') as f:\n",
    "    data_config = yaml.safe_load(f)\n",
    "\n",
    "print(\"\\nContenido del data.yaml:\")\n",
    "print(f\"  nc: {data_config.get('nc')}\")\n",
    "print(f\"  names: {data_config.get('names')}\")\n",
    "print(f\"  train: {data_config.get('train')}\")\n",
    "print(f\"  val: {data_config.get('val')}\")\n",
    "print(f\"  test: {data_config.get('test')}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "87b16689-281f-4330-9cb1-d38438bd0a96",
   "metadata": {},
   "outputs": [],
   "source": [
    "with open(os.path.join(DATASET_PATH, \"data.yaml\"), 'r') as f:\n",
    "    data_config = yaml.safe_load(f)\n",
    "    \n",
    "class_names = data_config['names']\n",
    "\n",
    "def contar_clases(labels_path):\n",
    "    contador = Counter()\n",
    "    for label_file in os.listdir(labels_path):\n",
    "        if label_file.endswith('.txt'):\n",
    "            with open(os.path.join(labels_path, label_file), 'r') as f:\n",
    "                for line in f:\n",
    "                    parts = line.strip().split()\n",
    "                    if len(parts) >= 5:  # Formato YOLO Detección: clase x y w h\n",
    "                        class_id = int(parts[0])\n",
    "                        contador[class_id] += 1\n",
    "                        \n",
    "    return contador\n",
    "\n",
    "\n",
    "conteo_train = contar_clases(os.path.join(DATASET_PATH, \"train\", \"labels\"))\n",
    "conteo_val = contar_clases(os.path.join(DATASET_PATH, \"valid\", \"labels\"))\n",
    "conteo_test = contar_clases(os.path.join(DATASET_PATH, \"test\", \"labels\"))\n",
    "\n",
    "\n",
    "df_clases = pd.DataFrame({\n",
    "    'Clase': class_names,\n",
    "    'Train': [conteo_train.get(i, 0) for i in range(len(class_names))],\n",
    "    'Valid': [conteo_val.get(i, 0) for i in range(len(class_names))],\n",
    "    'Test': [conteo_test.get(i, 0) for i in range(len(class_names))]\n",
    "})\n",
    "\n",
    "\n",
    "df_clases['Total'] = df_clases['Train'] + df_clases['Valid'] + df_clases['Test']   # Total\n",
    "df_clases['% del total'] = (df_clases['Total'] / df_clases['Total'].sum() * 100).round(2)   # Porcentaje\n",
    "\n",
    "\n",
    "df_clases = df_clases.sort_values('Total', ascending=False).reset_index(drop=True)   # Sorting\n",
    "\n",
    "print(\"DISTRIBUCIÓN DE CLASES EN EL DATASET\")\n",
    "print(\"=\" * 70)\n",
    "print(df_clases.to_string(index=False))\n",
    "print(\"=\" * 70)\n",
    "print(f\"Total de instancias: {df_clases['Total'].sum()}\") # Total de instancias/bounding boxes/objetos detectados"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ac85175b-6dd3-4d97-b570-41abbb288b28",
   "metadata": {},
   "source": [
    "#### IMPORTANTE: Habrá que reducir el número de clases y seleccionar aquellas que consideremos más importantes para la detección de barreras de accesibilidad urbana. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c2b83505-c31c-4e0b-a26b-7b5ab0977a28",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Descarga del modelo preentrenado y validación inicial con el dataset\n",
    "!yolo val model=yolo26n.pt data=dataset/data.yaml name=val_inicial"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7513b281-5fd8-450e-a35f-4fbec88a4c1c",
   "metadata": {},
   "source": [
    "#### mAP: mean Average Precision, métrica estándar para evaluar modelos de detección de objetos, que mide cuán bueno es el modelo detectando objetos y localizándolos correctamente. maP50 a 0.0333, MUY BAJO, el modelo intenta detectar las clases de nuestro dataset pero solo conoce las clases mediante las que ha sido entrenado"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "91c4a512-6d4e-4420-8726-d62c1b51f1be",
   "metadata": {},
   "outputs": [],
   "source": [
    "model = YOLO(\"yolo26n.pt\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "512c0dba-7efb-44ce-ae0c-57eefe5da7f5",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Entenamiento base del modelo, punto de partida:\n",
    "\n",
    "results = model.train(\n",
    "    data=\"dataset/data.yaml\",\n",
    "    epochs=40,          \n",
    "    imgsz=640,          \n",
    "    batch=16,\n",
    "    device=0    # Activa la GPU\n",
    ")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d397dc69-fd06-4bd9-872a-89ccf88bc2b7",
   "metadata": {},
   "source": [
    "### Métricas del entrenamiento\n",
    "\n",
    "Durante el entrenamiento, Ultralytics muestra una serie de métricas que reflejan el rendimiento del modelo. Estas son las más importantes:\n",
    "\n",
    "#### Pérdidas (Losses)\n",
    "\n",
    "| Métrica | ¿Qué mide? | ¿Qué esperar? |\n",
    "| :--- | :--- | :--- |\n",
    "| **box_loss** | Error en la localización de las bounding boxes (coordenadas). | Debe bajar con las épocas. |\n",
    "| **cls_loss** | Error en la clasificación de cada objeto (¿es un coche? ¿una persona?). | Debe bajar con las épocas. |\n",
    "| **l1_loss** | Pérdida auxiliar de regresión que ayuda a estabilizar el entrenamiento. | Debe bajar con las épocas. |\n",
    "\n",
    "#### Métricas de evaluación (Box)\n",
    "\n",
    "| Métrica | ¿Qué mide? | ¿Qué esperar? |\n",
    "| :--- | :--- | :--- |\n",
    "| **Precision (P)** | De todos los objetos que el modelo detecta, ¿cuántos son correctos? | Cuanto más alto, mejor. Cercano a 1.0 es ideal. |\n",
    "| **Recall (R)** | De todos los objetos reales, ¿cuántos detecta el modelo? | Cuanto más alto, mejor. Cercano a 1.0 es ideal. |\n",
    "| **mAP50** | Precisión media con un umbral de solapamiento (IoU) del 50%. | Cuanto más alto, mejor. >0.90 es excelente. |\n",
    "| **mAP50-95** | Precisión media promediada sobre umbrales de IoU de 50% a 95%. | Cuanto más alto, mejor. >0.70 es muy bueno. |\n",
    "\n",
    "#### Otras métricas\n",
    "\n",
    "| Métrica | ¿Qué mide? |\n",
    "| :--- | :--- |\n",
    "| **Instances** | Número de objetos anotados en el batch actual. |\n",
    "| **GPU_mem** | Memoria de la GPU utilizada durante el entrenamiento. |\n",
    "| **Size** | Tamaño de las imágenes de entrada (ej. 640x640). |\n",
    "\n",
    "#### ¿Qué es el IoU?\n",
    "\n",
    "El **IoU** (Intersection over Union) mide el solapamiento entre la bounding box predicha y la real. Va de 0 (sin solapamiento) a 1 (solapamiento perfecto). Un IoU de 0.5 significa que la predicción cubre al menos el 50% del objeto real.\n",
    "\n",
    "#### ¿Qué es el mAP?\n",
    "\n",
    "El **mAP** (mean Average Precision) es la métrica estándar para evaluar modelos de detección de objetos. Combina Precision y Recall en un solo número. Un mAP alto significa que el modelo detecta los objetos correctamente y con buena localización."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5638b670-903b-4abf-9d28-30935962f150",
   "metadata": {},
   "source": [
    "Si el mAP es bueno (>0.90) → Documentar y pasar a la demo.\n",
    "\n",
    "Si el mAP es bajo (<0.80) → Analizar qué clases fallan y considerar:\n",
    "\n",
    "    Más épocas.\n",
    "\n",
    "    Data augmentation específico.\n",
    "\n",
    "    Ajuste de hiperparámetros con model.tune().\n",
    "\n",
    "Si la demo falla mucho → Documentar la limitación de dominio y proponer fine-tuning con imágenes locales como trabajo futuro."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ca06181a-6250-463d-b38b-54a3cecf08f8",
   "metadata": {},
   "outputs": [],
   "source": [
    "model = YOLO(\"runs/detect/train-2/weights/best.pt\")  # Cargamos el mejor modelo"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c957b103-6669-4b1f-81be-f179986b63f3",
   "metadata": {},
   "outputs": [],
   "source": [
    "metrics = model.val(data=\"dataset/data.yaml\", split=\"test\")  # Evaluamos"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "80395950-e704-4d06-b71d-3aba0990fa9b",
   "metadata": {},
   "outputs": [],
   "source": [
    "print(f\"mAP50: {metrics.box.map50:.4f}\")\n",
    "print(f\"mAP50-95: {metrics.box.map:.4f}\")\n",
    "print(f\"Precision: {metrics.box.mp:.4f}\")\n",
    "print(f\"Recall: {metrics.box.mr:.4f}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bffcbfaf-5db3-4cfb-a79f-800e2f3cfc05",
   "metadata": {},
   "outputs": [],
   "source": [
    "from PIL import Image\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "img = Image.open(\"runs/detect/train-2/confusion_matrix_normalized.png\")  # Matriz de confusión normalizada\n",
    "plt.figure(figsize=(14, 12))\n",
    "plt.imshow(img)\n",
    "plt.axis('off')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0f190f4b-ab4d-43b5-88ee-ae667453b092",
   "metadata": {},
   "source": [
    "### Evaluación con imágenes propias"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "878e96a2-2f8f-423e-9d6c-fd92b119b401",
   "metadata": {},
   "outputs": [],
   "source": [
    "from pathlib import Path\n",
    "import cv2\n",
    "\n",
    "model = YOLO(\"runs/detect/train-2/weights/best.pt\")\n",
    "print(model.names)\n",
    "print(f\"Total clases: {len(model.names)}\")\n",
    "\n",
    "imgs_dir = Path(\"tests/imgs/\")\n",
    "output_dir = Path(\"tests/results_imgs/\")\n",
    "output_dir.mkdir(exist_ok=True)\n",
    "\n",
    "EXTENSIONES = {\".jpg\", \".jpeg\", \".png\", \".bmp\", \".webp\", \".tif\", \".tiff\"}\n",
    "\n",
    "for img_path in sorted(imgs_dir.iterdir()):\n",
    "    if not img_path.is_file() or img_path.suffix.lower() not in EXTENSIONES:\n",
    "        continue\n",
    "\n",
    "    results = model(img_path, conf=0.2, device=\"cpu\")  # conf = umbral de confianza\n",
    "    r = results[0]\n",
    "\n",
    "    print(f\"\\n--- {img_path.name} ---\")\n",
    "    if len(r.boxes) == 0:\n",
    "        print(\"  (sin detecciones)\") \n",
    "    else:\n",
    "        for box in r.boxes:\n",
    "            clase = model.names[int(box.cls)]\n",
    "            conf = float(box.conf)\n",
    "            xyxy = box.xyxy[0].tolist()\n",
    "            print(f\"  {clase:20s} conf={conf:.2f}  bbox={[round(v) for v in xyxy]}\")\n",
    "\n",
    "    annotated = r.plot()\n",
    "    cv2.imwrite(str(output_dir / img_path.name), annotated)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b41b5089-359d-476a-8147-6b32d58cbeb6",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (yoloEnv)",
   "language": "python",
   "name": "yoloenv"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.16"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
````

## File: ActionPlan.txt
````
AI Course
Capstone Project 
Action Plan

For students (instructor’s review required)








?2023 SAMSUNG. All rights reserved.
Samsung Electronics Corporate Citizenship Office holds the copyright of this document.
This document is a literary property protected by copyright law so reprint and reproduction without permission are prohibited. 
To use this document other than the curriculum of Samsung Innovation Campus, you must receive written consent from copyright holder.



CourseAI CourseTeam Name AccessAI: AI-Based Urban Accessibility DetectionTeam Leader/
Members <Team leader> /
 <member 1>, <member 2>, …Project Title AccessAI: AI-Based Urban Accessibility DetectionGoalEl objetivo de este proyecto es desarrollar un sistema de Inteligencia Artificial capaz de detectar elementos relacionados con la accesibilidad en entornos urbanos y peatonales.

El sistema analizará imágenes de aceras e identificará elementos como aceras y rampas de acceso, con la posibilidad de ampliar posteriormente el modelo para detectar obstáculos, escaleras, superficies deterioradas y otras barreras de accesibilidad.

A largo plazo, las predicciones del modelo podrían utilizarse como base para desarrollar una aplicación que proporcione información sobre la accesibilidad urbana y ayude en la navegación de personas con movilidad reducida.AbstractLa accesibilidad urbana es un problema importante para las personas que utilizan sillas de ruedas, andadores, carritos de bebé o que tienen movilidad reducida. Una acera puede aparecer como accesible en un mapa y, sin embargo, presentar barreras como bordillos elevados, ausencia de rampas, obstáculos o superficies deterioradas.
Este proyecto propone desarrollar un sistema de visión artificial capaz de analizar automáticamente imágenes de entornos urbanos y detectar elementos relacionados con la accesibilidad.
Se estudiarán diferentes conjuntos de datos públicos, como Project Sidewalk, Sidewalk Accessibility y Cityscapes, analizando sus imágenes, clases, etiquetas y distribución de los datos.
El prototipo inicial se centrará en detectar aceras y rampas de acceso. Posteriormente, el sistema podrá ampliarse para detectar otros tipos de barreras y utilizar la información obtenida junto con coordenadas geográficas para construir un futuro mapa de accesibilidad.
Method<El proyecto seguirá una metodología basada en aprendizaje supervisado y visión artificial.
En primer lugar, se analizarán los conjuntos de datos disponibles teniendo en cuenta el número de imágenes, las clases existentes, la calidad de las etiquetas, la distribución entre clases y el número de objetos presentes en las imágenes.
Posteriormente, los datos serán limpiados y divididos en conjuntos de entrenamiento, validación y prueba.
Se estudiarán dos posibles enfoques:
1. Clasificación de imágenes: utilización de MobileNetV2 mediante transfer learning para clasificar imágenes según diferentes categorías de accesibilidad.
2. Detección de objetos: utilización de YOLOv8n para detectar y localizar elementos relacionados con la accesibilidad, como aceras y rampas.
Para el primer prototipo se priorizará la detección de objetos mediante YOLOv8n, ya que permite obtener tanto la clase del elemento detectado como su localización dentro de la imagen.
Cuando sea necesario, se aplicarán técnicas de aumento de datos como ajustes de brillo y contraste, zoom y recortes controlados para reducir el sobreajuste.
Para evaluar los modelos se utilizarán métricas adecuadas al problema. En clasificación se podrán utilizar Accuracy, Balanced Accuracy, Precision, Recall, F1-score y ROC-AUC. En detección se utilizarán principalmente Precision, Recall, F1-score y mAP.
También se estudiará el uso de Early Stopping y optimización de hiperparámetros mediante Optuna.
Finalmente, el modelo entrenado se integrará en un pequeño prototipo que permitirá introducir una imagen y visualizar los elementos de accesibilidad detectados.


DataSe utilizarán principalmente conjuntos de datos públicos relacionados con la accesibilidad urbana y la visión artificial.
Los principales candidatos serán Project Sidewalk, Sidewalk Accessibility y Cityscapes. Se analizarán sus imágenes y anotaciones para determinar cuáles son más adecuadas para el objetivo del proyecto.
Los datos se descargarán desde las fuentes oficiales o repositorios públicos correspondientes. Antes del entrenamiento se realizará un análisis del número de imágenes, clases, distribución de los datos, calidad de las etiquetas y número de objetos por imagen.
Los datos se dividirán en conjuntos de entrenamiento, validación y prueba. Cuando sea necesario, se aplicarán técnicas de aumento de datos para mejorar la capacidad de generalización del modelo.
El modelo utilizará las imágenes y sus etiquetas para aprender a detectar elementos relacionados con la accesibilidad, principalmente aceras y rampas de acceso, y posteriormente otros posibles obstáculos.
Expected 
OutcomeSe espera desarrollar un modelo de visión artificial capaz de analizar una imagen de una zona peatonal y detectar automáticamente elementos relacionados con la accesibilidad.
El prototipo deberá mostrar visualmente las detecciones realizadas por el modelo, indicando el tipo de elemento y su localización dentro de la imagen.
Como resultado final se espera obtener un prototipo funcional que demuestre la utilidad de la Inteligencia Artificial para analizar espacios urbanos y detectar posibles barreras de accesibilidad.
A largo plazo, este sistema podría integrarse con información geográfica y coordenadas GPS para crear un mapa de accesibilidad urbana. Esto podría facilitar la identificación de zonas con posibles barreras y servir como base para futuras herramientas de navegación orientadas a personas con movilidad reducida.
Role by 
MemberMiembro 1 — Datos
* Búsqueda y análisis de datasets.
* Descarga y organización de los datos.
* Limpieza y preparación de las imágenes.
* Análisis de clases y distribución de los datos.
Miembro 2 — Machine Learning
* Preparación del modelo.
* Entrenamiento de MobileNetV2 y/o YOLOv8n.
* Ajuste de hiperparámetros.
* Evaluación mediante las métricas seleccionadas.
Miembro 3 — Aplicación
* Desarrollo del prototipo.
* Integración del modelo entrenado.
* Diseño de la interfaz.
* Visualización de las detecciones.
Trabajo conjunto
Todos los miembros participarán en el análisis de resultados, pruebas, documentación, preparación de la presentación y revisión final del proyecto.


Schedule 
Summary<Provide a summarized schedule.>
<Use the provided WBS workbook for more detailed action plan.>Comment & 
Assessment<Comment and assessment by the instructor.>
````

## File: dependencias.txt
````
# Name                            Version            Build            Channel
_libgcc_mutex                     0.1                main
_openmp_mutex                     5.1                52_gnu
anyio                             4.15.1             pypi_0           pypi
asttokens                         3.0.1              py311h06a4308_0
brotlicffi                        1.2.0.1            py311h7354ed3_0
bzip2                             1.0.8              h5eee18b_6
ca-certificates                   2026.8.13          h06a4308_0
certifi                           2026.7.22          py311h06a4308_0
cffi                              2.1.1              py311h3b52fac_0
charset-normalizer                3.5.1              pypi_0           pypi
cloudpickle                       3.1.2              pypi_0           pypi
comm                              0.2.3              py311h06a4308_0
contourpy                         1.3.3              pypi_0           pypi
cuda-bindings                     13.4.2             pypi_0           pypi
cuda-pathfinder                   1.8.2              pypi_0           pypi
cuda-toolkit                      13.0.3.0           pypi_0           pypi
cycler                            0.12.1             pypi_0           pypi
debugpy                           1.8.21             py311h7354ed3_0
decorator                         5.3.1              py311h06a4308_0
executing                         2.2.1              py311h06a4308_1
filelock                          4.0.1              pypi_0           pypi
fonttools                         4.65.0             pypi_0           pypi
fsspec                            2026.9.0           pypi_0           pypi
idna                              3.20               pypi_0           pypi
ipykernel                         7.3.0              py311h7040dfc_0
ipython                           9.15.0             py311h06a4308_0
ipython_pygments_lexers           1.1.1              py311h06a4308_0
jedi                              0.20.0             py311h06a4308_0
jinja2                            3.1.6              pypi_0           pypi
jupyter_client                    8.10.0             py311h06a4308_0
jupyter_core                      5.9.1              py311h06a4308_0
kiwisolver                        1.5.1              pypi_0           pypi
ld_impl_linux-64                  2.44               h9e0c5a2_3
libexpat                          2.8.4              h7354ed3_0
libffi                            3.4.8              h06d3fd0_3
libgcc                            15.2.0             h69a1729_8
libgcc-ng                         15.2.0             h166f726_8
libnsl                            2.0.0              h5eee18b_0
libsodium                         1.0.21             h83fc4cd_1
libstdcxx                         15.2.0             h39759b7_8
libuuid                           1.41.5             h5eee18b_0
libxcb                            1.17.0             h9b100fa_0
libzlib                           1.3.2              h47b2149_0
markupsafe                        3.0.3              pypi_0           pypi
matplotlib                        3.11.2             pypi_0           pypi
matplotlib-inline                 0.2.2              py311h06a4308_0
mpmath                            1.3.0              pypi_0           pypi
ncurses                           6.6                hfaaeb4e_0
nest-asyncio2                     1.7.2              py311h06a4308_0
networkx                          3.6.1              pypi_0           pypi
numpy                             2.4.6              pypi_0           pypi
nvidia-cublas                     13.1.1.3           pypi_0           pypi
nvidia-cuda-cupti                 13.0.85            pypi_0           pypi
nvidia-cuda-nvrtc                 13.0.88            pypi_0           pypi
nvidia-cuda-runtime               13.0.96            pypi_0           pypi
nvidia-cudnn-cu13                 9.24.0.43          pypi_0           pypi
nvidia-cufft                      12.0.0.61          pypi_0           pypi
nvidia-cufile                     1.15.1.6           pypi_0           pypi
nvidia-curand                     10.4.0.35          pypi_0           pypi
nvidia-cusolver                   12.0.4.66          pypi_0           pypi
nvidia-cusparse                   12.6.3.3           pypi_0           pypi
nvidia-cusparselt-cu13            0.8.1              pypi_0           pypi
nvidia-ml-py                      13.610.43          pypi_0           pypi
nvidia-nccl-cu13                  2.30.7             pypi_0           pypi
nvidia-nvjitlink                  13.4.92            pypi_0           pypi
nvidia-nvshmem-cu13               3.4.5              pypi_0           pypi
nvidia-nvtx                       13.0.85            pypi_0           pypi
opencv-python                     5.0.0.93           pypi_0           pypi
openssl                           3.5.8              h1b28b03_0
packaging                         26.3               py311h06a4308_0
parso                             0.8.7              py311h06a4308_0
pexpect                           4.9.0              py311h06a4308_1
pi-heif                           1.4.0              pypi_0           pypi
pillow                            12.3.0             pypi_0           pypi
pip                               26.2.1             pyhc872135_0
platformdirs                      4.11.0             py311h06a4308_0
polars                            1.44.2             pypi_0           pypi
polars-runtime-32                 1.44.2             pypi_0           pypi
prompt-toolkit                    3.0.53             py311h06a4308_0
prompt_toolkit                    3.0.53             hd3eb1b0_0
psutil                            7.2.2              py311h47b2149_0
pthread-stubs                     0.3                h47b2149_2
ptyprocess                        0.7.0              pyhd3eb1b0_3
pure_eval                         0.2.3              py311h06a4308_0
pycparser                         3.0                py311h06a4308_0
pygments                          2.20.0             py311h06a4308_0
pyparsing                         3.3.2              pypi_0           pypi
pysocks                           1.7.1              py311h06a4308_1
python                            3.11.16            h17756b0_0
python-dateutil                   2.9.0post0         py311h06a4308_2
pytorch-triton-rocm               3.5.1              pypi_0           pypi
pyyaml                            6.0.3              py311h591646f_0
pyzmq                             27.2.0             py311hfb5a9c0_0
readline                          8.3                hc2a1206_0
requests                          2.34.2             py311h06a4308_0
rocm                              7.13.0             pypi_0           pypi
rocm-sdk-core                     7.13.0             pypi_0           pypi
rocm-sdk-libraries-gfx120x-all    7.13.0             pypi_0           pypi
setuptools                        81.0.0             pypi_0           pypi
six                               1.17.0             py311h06a4308_0
sqlite                            3.53.4             h795bf6d_0
stack_data                        0.6.3              py311h06a4308_0
sympy                             1.14.0             pypi_0           pypi
tk                                8.6.15             h54e0aa7_0
torch                             2.11.0+rocm7.13.0  pypi_0           pypi
torchaudio                        2.11.0+rocm7.13.0  pypi_0           pypi
torchvision                       0.26.0+rocm7.13.0  pypi_0           pypi
tornado                           6.5.8              py311h47b2149_0
traitlets                         5.15.0             py311h06a4308_0
triton                            3.6.0+rocm7.13.0   pypi_0           pypi
typing-extensions                 4.16.0             py311h06a4308_0
typing_extensions                 4.16.0             py311h06a4308_0
tzdata                            2026c              he532380_0
ultralytics                       8.4.157            pypi_0           pypi
ultralytics-platform              0.1.49             pypi_0           pypi
ultralytics-thop                  2.1.6              pypi_0           pypi
urllib3                           2.8.0              pypi_0           pypi
wcwidth                           0.8.2              py311h06a4308_0
wheel                             0.47.0             py311h06a4308_0
xorg-libx11                       1.8.13             h65de747_0
xorg-libxau                       1.0.12             h9b100fa_0
xorg-libxdmcp                     1.1.5              h9b100fa_0
xorg-xorgproto                    2025.1             h47b2149_0
xz                                5.8.2              h448239c_0
yaml                              0.2.5              h591646f_1
zeromq                            4.3.5              hf801bfb_2
zlib                              1.3.2              h47b2149_0
````

## File: generate_accessai_pptx_v2_0_2.py
````python
OUT_PATH = r"c:\III DIPLOMA DE EXTENSIÓN UNIVERSITARIA EN INTELIGENCIA ARTIFICIAL AVANZADA SAMSUNG INNOVATION CAMPUS (2025-26)\MÓDULO 10. Proyectos\AccessAI_Capstone_Presentation_v2_0_2.pptx"
⋮----
# Samsung theme extracted from Theme3.thmx
THEME = {
⋮----
def set_bg(slide, color=THEME["lt1"])
⋮----
fill = slide.background.fill
⋮----
def add_text(slide, left, top, width, height, text, size=20, bold=False, color=THEME["dk2"], align=PP_ALIGN.LEFT, font_name='Samsung Sharp Sans')
⋮----
box = slide.shapes.add_textbox(left, top, width, height)
tf = box.text_frame
⋮----
p = tf.paragraphs[0]
⋮----
def add_bullets(slide, left, top, width, height, items, font_size=18, color=THEME["dk2"])
⋮----
p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
⋮----
def add_card(slide, left, top, width, height, title, body, accent=THEME["accent1"])
⋮----
card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
⋮----
strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.12))
⋮----
box = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.7), width - Inches(0.36), height - Inches(0.9))
⋮----
def add_step(slide, left, top, width, height, label, color=THEME["accent5"])
⋮----
step = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
⋮----
tf = step.text_frame
⋮----
def add_arrow(slide, x1, y1, x2, y2)
⋮----
arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x1, y1, x2 - x1, y2 - y1)
⋮----
prs = Presentation()
⋮----
# Slide 1
slide = prs.slides.add_slide(prs.slide_layouts[6])
⋮----
band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.28))
⋮----
card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.4), Inches(1.7), Inches(2.8), Inches(2.3))
⋮----
# Slide 2
⋮----
# Slide 3
⋮----
# Slide 4
⋮----
# Slide 5
⋮----
# Slide 6
````

## File: generate_accessai_pptx.py
````python
OUT_PATH = r"c:\III DIPLOMA DE EXTENSIÓN UNIVERSITARIA EN INTELIGENCIA ARTIFICIAL AVANZADA SAMSUNG INNOVATION CAMPUS (2025-26)\MÓDULO 10. Proyectos\AccessAI_Capstone_Presentation_Branding.pptx"
⋮----
def set_background(slide, color=RGBColor(245, 247, 250))
⋮----
fill = slide.background.fill
⋮----
def add_title(slide, title, subtitle=None)
⋮----
title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.0), Inches(0.8))
tf = title_box.text_frame
p = tf.paragraphs[0]
run = p.add_run()
⋮----
sub_box = slide.shapes.add_textbox(Inches(0.6), Inches(1.0), Inches(11.5), Inches(0.4))
tf2 = sub_box.text_frame
p2 = tf2.paragraphs[0]
run2 = p2.add_run()
⋮----
def add_bullets(slide, x, y, w, h, items, font_size=18, color=RGBColor(29, 41, 57), bullet_color=RGBColor(26, 115, 232))
⋮----
box = slide.shapes.add_textbox(x, y, w, h)
tf = box.text_frame
⋮----
p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
⋮----
def add_card(slide, left, top, width, height, title, body, accent=RGBColor(26, 115, 232), title_color=RGBColor(16, 35, 72), body_color=RGBColor(55, 67, 84))
⋮----
shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
⋮----
bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.12))
⋮----
title_box = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.22), width - Inches(0.3), Inches(0.5))
⋮----
body_box = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.7), width - Inches(0.3), height - Inches(0.9))
tf2 = body_box.text_frame
⋮----
def add_flow_box(slide, left, top, width, height, text, fill_color, text_color=RGBColor(255,255,255))
⋮----
box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
⋮----
def add_arrow(slide, x1, y1, x2, y2)
⋮----
arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x1, y1, x2 - x1, y2 - y1)
⋮----
def add_brand_block(slide, left, top, width, height, text, fill_color, font_size=12)
⋮----
block = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
⋮----
tf = block.text_frame
⋮----
def add_logo_marker(slide, left, top, width, height, label, fill_color, text_color=RGBColor(255,255,255), font_size=12)
⋮----
marker = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
⋮----
tf = marker.text_frame
⋮----
prs = Presentation()
⋮----
# Slide 1: Title
slide = prs.slides.add_slide(prs.slide_layouts[6])
⋮----
header_band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.28))
⋮----
# institutional branding strip in Samsung palette
⋮----
team = slide.shapes.add_textbox(Inches(0.7), Inches(1.15), Inches(5.2), Inches(0.5))
tf = team.text_frame
⋮----
title = slide.shapes.add_textbox(Inches(0.7), Inches(1.7), Inches(11.5), Inches(1.3))
tf2 = title.text_frame
⋮----
subtitle = slide.shapes.add_textbox(Inches(0.7), Inches(3.05), Inches(8.5), Inches(0.7))
tf3 = subtitle.text_frame
p3 = tf3.paragraphs[0]
⋮----
# accent shapes with Samsung palette
accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.3), Inches(1.8), Inches(2.9), Inches(2.4))
⋮----
mini = slide.shapes.add_textbox(Inches(9.6), Inches(2.15), Inches(2.3), Inches(1.1))
tf4 = mini.text_frame
p4 = tf4.paragraphs[0]
⋮----
footer = slide.shapes.add_textbox(Inches(0.7), Inches(6.7), Inches(9.5), Inches(0.4))
tf5 = footer.text_frame
p5 = tf5.paragraphs[0]
⋮----
# Slide 2: Problem and objective
⋮----
# Slide 3: Data and methodology
⋮----
# Slide 4: Workflow
⋮----
# Slide 5: Results and demo
⋮----
# Slide 6: Impact and Next Steps
````

## File: inspect_theme.py
````python
path = r"c:\III DIPLOMA DE EXTENSIÓN UNIVERSITARIA EN INTELIGENCIA ARTIFICIAL AVANZADA SAMSUNG INNOVATION CAMPUS (2025-26)\MÓDULO 10. Proyectos\Theme3.thmx"
⋮----
xml = z.read('theme/theme/theme1.xml').decode('utf-8', 'ignore')
⋮----
colors = sorted(set(re.findall(r'val="([A-Fa-f0-9]{6})"', xml)))
````

## File: PLAN.md
````markdown
Plan de Proyecto — Proyecto Jupiter NB (AccessAI)
> Nota: "Proyecto Jupiter NB" es el nombre interno de trabajo de AccessAI: AI-Based Urban Accessibility Detection, proyecto desarrollado en el marco de Samsung Innovation Campus 2025-26. Este documento consolida el Action Plan del curso y el estado técnico actual descrito en el README en una hoja de ruta operativa.

## Resumen

AccessAI (Jupiter NB) es un sistema de visión artificial que analiza imágenes de entornos urbanos y peatonales para detectar elementos relacionados con la accesibilidad, empezando por aceras y rampas de acceso. El prototipo actual usa YOLOv8n preentrenado de propósito general; el objetivo del proyecto es sustituirlo por un modelo entrenado específicamente para clases de accesibilidad.

## 1. Objetivo

Principal: desarrollar un sistema capaz de analizar una imagen de una zona peatonal y localizar automáticamente elementos relacionados con la accesibilidad urbana.

A largo plazo: combinar las detecciones con coordenadas GPS para construir un mapa de accesibilidad que ayude en la navegación de personas con movilidad reducida.

## 2. Estado actual

- ✅ Prototipo funcional (accessai_demo.py) que carga una imagen, ejecuta YOLO y guarda una copia anotada con bounding boxes. - ✅ Generadores de presentación (generate_accessai_pptx.py, generate_accessai_pptx_v2_0_2.py) con el tema de Samsung. - ⚠️ El modelo en uso (yolov8n.pt) es genérico — no está entrenado con clases de accesibilidad. Una detección actual no implica que una acera o rampa sea realmente accesible.

❌ Sin dataset propio integrado en el repositorio todavía.
❌ Sin métricas de entrenamiento ni interfaz de usuario. - ❌ Sin información geográfica en las detecciones.
## 3. Metodología

1. Selección de datos: evaluar Project Sidewalk, Sidewalk Accessibility y Cityscapes según número de imágenes, clases, calidad de etiquetas y distribución. 2. Preparación: limpieza, conversión de anotaciones a formato YOLO, y división en train / validation / test. 3. Modelado — dos enfoques a estudiar: - Clasificación de imágenes: MobileNetV2 vía transfer learning. - Detección de objetos (prioritaria para el primer prototipo): YOLOv8n, porque da clase y localización. 4. Aumento de datos (si hace falta): brillo/contraste, zoom, recortes controlados, para reducir sobreajuste. 5. Entrenamiento: con Early Stopping y ajuste de hiperparámetros vía Optuna. 6. Evaluación: - Clasificación → Accuracy, Balanced Accuracy, Precision, Recall, F1-score, ROC-AUC. - Detección → Precision, Recall, F1-score, mAP. 7. Integración: modelo final embebido en el prototipo (accessai_demo.py o su evolución) con visualización de detecciones.

## 4. Datos

| Dataset | Rol | Por confirmar | |---|---|---| | Project Sidewalk | Candidato principal | Cobertura de clases sidewalk / curbramp, calidad de etiquetas | | Sidewalk Accessibility | Candidato | Formato de anotaciones, tamaño del dataset | | Cityscapes | Candidato / complemento | Relevancia de clases urbanas para accesibilidad |

Criterios de selección final: disponibilidad de anotaciones, compatibilidad de clases con el objetivo (sidewalk, curbramp inicialmente), calidad de imágenes, distribución de clases.

## 5. Arquitectura del prototipo (actual)

<span data-diff-end="54"></span> <span data-diff-start="55"></span>Imagen urbana → accessai_demo.py → Modelo YOLO → Detecciones y confianza<span data-diff-end="55"></span> <span data-diff-start="56"></span>→ Bounding boxes anotadas → resultados/accessai_resultado.jpg<span data-diff-end="56"></span> <span data-diff-start="57"></span>

## 6. Hoja de ruta

### Fase 1 — Análisis de datos - [ ] Descargar y explorar Project Sidewalk, Sidewalk Accessibility y Cityscapes - [ ] Documentar número de imágenes, clases, distribución y calidad de etiquetas - [ ] Seleccionar el dataset (o combinación) definitivo

Fase 2 — Preparación
 Limpiar y normalizar los datos
 Convertir anotaciones al formato YOLO - [ ] Crear splits train / val / test
 Definir configuración de clases (mínimo: sidewalk, curbramp)
Fase 3 — Entrenamiento
- [ ] Entrenar baseline con YOLOv8n - [ ] (Opcional) Probar MobileNetV2 con transfer learning como comparación - [ ] Aplicar aumento de datos si hay sobreajuste - [ ] Ajustar hiperparámetros con Optuna + Early Stopping

Fase 4 — Evaluación
 Calcular Precision, Recall, F1 y mAP por clase
 Revisar falsos positivos / falsos negativos
 Probar el modelo con imágenes nuevas no vistas
Fase 5 — Integración
 Sustituir yolov8n.pt por el modelo entrenado en accessai_demo.py - [ ] Añadir procesamiento por lotes o una interfaz mínima de usuario - [ ] (Ampliación futura) explorar integración con coordenadas GPS
### Fase 6 — Documentación y entrega

 Actualizar README con resultados reales del modelo entrenado - [ ] Preparar presentación final (generate_accessai_pptx_v2_0_2.py) - [ ] Revisión conjunta y pruebas finales del equipo
## 7. Roles del equipo

Miembro 1 — Datos - Búsqueda y análisis de datasets - Descarga y organización de los datos - Limpieza y preparación de las imágenes - Análisis de clases y distribución

Miembro 2 — Machine Learning - Preparación del modelo - Entrenamiento de MobileNetV2 y/o YOLOv8n - Ajuste de hiperparámetros - Evaluación con las métricas seleccionadas

Miembro 3 — Aplicación - Desarrollo del prototipo - Integración del modelo entrenado - Diseño de la interfaz - Visualización de las detecciones

Trabajo conjunto: análisis de resultados, pruebas, documentación, presentación y revisión final.

8. Riesgos y limitaciones conocidas
No hay todavía dataset propio integrado en el repositorio.
El modelo genérico actual puede dar una falsa sensación de "ya funciona" — no está validado para accesibilidad real. - La demo procesa una imagen a la vez (sin procesamiento por lotes todavía). - Sin datos geográficos, las detecciones no se pueden ubicar en un mapa aún.
## 9. Próximos pasos inmediatos

1. Cerrar la selección de dataset (Fase 1). 2. Definir el esquema de clases final antes de anotar/convertir nada. 3. Preparar el primer split de entrenamiento para tener una baseline entrenable cuanto antes.

--- Generado a partir de SIC_AI_Capstone Project_Action Plan(6).md y README.md. Actualizar este archivo a medida que avancen las fases.
````

## File: README.md
````markdown
# AccessAI

AccessAI es un prototipo de visión artificial para detectar elementos relacionados con la accesibilidad urbana en imágenes de entornos peatonales.

El prototipo utiliza YOLO mediante Ultralytics. Actualmente emplea `yolov26n.pt`, un modelo preentrenado de detección general. El siguiente paso del proyecto es entrenar un modelo específico con datos de accesibilidad urbana para detectar, entre otros elementos, aceras y rampas de acceso.

## Requisitos

- Python 3.10 o superior
- Un entorno virtual de Python

 # AccessAI

 ## Detección inteligente de accesibilidad urbana

 AccessAI es un proyecto de visión artificial desarrollado en el marco de Samsung Innovation Campus 2025-26. Su objetivo es analizar imágenes de espacios urbanos y detectar elementos relevantes para la accesibilidad peatonal, como aceras, rampas de acceso y posibles barreras.

 El repositorio contiene un prototipo ejecutable basado en YOLO y varios recursos de apoyo para la presentación y documentación del proyecto.

 > **Estado del proyecto:** prototipo técnico inicial. La demo funciona con un modelo YOLO preentrenado de detección general; todavía no es un modelo entrenado específicamente con clases de accesibilidad urbana.

 ## Índice

- [AccessAI](#accessai)
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
  - [Generación de la presentación](#generación-de-la-presentación)
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

 ## Uso de la demo

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

 ## Generación de la presentación

 El generador basado en el tema de Samsung requiere `python-pptx`.

 ```powershell
 python generate_accessai_pptx_v2_0_2.py
 ```

 Este script genera `AccessAI_Capstone_Presentation_v2_0_2.pptx` en la carpeta del proyecto. La ruta de salida está definida dentro del script y debe cambiarse si se ejecuta en otra ubicación.

 También existe una versión alternativa:

 ```powershell
 python generate_accessai_pptx.py
 ```

 El archivo `Theme3.thmx` y la función `inspect_theme.py` se utilizan como recursos de referencia para el estilo de la presentación.

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

DOCUMENTACIÓN YOLO:
https://docs.ultralytics.com/es/quickstart

DATASET: ROD-DATASET DE DETECCIÓN (YOLO26n)
https://www.kaggle.com/datasets/abtinzandi/obstacle-detection-dataset/data

DATASET: BARCELONA STREETS DATASET DE SEGMENTACIÓN DE INSTANCIAS (YOLO26n-seg)
https://universe.roboflow.com/bielglasses/barcelona-streets

(Hay que descargar el Barcelona Dataset en el formato adecuado. Para ello, hay que darle a la sección de dataset, descargar la versión más reciente (v36), descargarlo en ZIP file y seleccionar YOLO26 en el selector de "Image and Annotation Format" para que esté adaptado a los modelos YOLO. Por último, seleccionar "Download ZIP to computer" en Download options y descomprimirlo en la carpeta del proyecto)



 Para reducir el sobreajuste pueden evaluarse aumentos como brillo, contraste, zoom y recortes controlados. El conjunto de prueba debe mantenerse separado del entrenamiento para obtener una evaluación representativa.

 ## Estructura del proyecto

 ```text
 .
 |-- accessai_demo.py
 |-- generate_accessai_pptx.py
 |-- generate_accessai_pptx_v2_0_2.py
 |-- inspect_theme.py
 |-- Theme3.thmx
 |-- SIC_AI_Capstone Project_Action Plan(6).md
 |-- SIC_AI_Capstone Project_Final Report(11).md
 |-- resultados/                         # Se crea al ejecutar la demo
 |-- .venv/                              # Entorno local, no versionado
 `-- README.md
 ```

 Además, la carpeta contiene presentaciones, plantillas y documentos PDF de referencia del curso.

 ## Limitaciones y próximos pasos

 ### Limitaciones actuales

 - No existe todavía un dataset específico de AccessAI integrado en el repositorio.
 - `yolov8n.pt` es un modelo general y no está entrenado para las clases finales del proyecto.
 - La demo procesa una imagen cada vez.
 - No se incluyen todavía métricas de entrenamiento ni una interfaz de usuario.
 - Las detecciones no contienen información geográfica.

 ### Próximos pasos técnicos

 1. Seleccionar y documentar el dataset definitivo.
 2. Convertir las anotaciones al formato compatible con YOLO.
 3. Crear la configuración de clases y los conjuntos `train`, `val` y `test`.
 4. Entrenar un modelo específico para accesibilidad urbana.
 5. Medir precision, recall, F1 y mAP por clase.
 6. Revisar falsos positivos y falsos negativos.
 7. Sustituir `yolov8n.pt` por el modelo entrenado.
 8. Añadir procesamiento por lotes o una interfaz de usuario.
 9. Estudiar la integración con localización geográfica y mapas.

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

 - [Plan de acción del proyecto](SIC_AI_Capstone%20Project_Action%20Plan(6).md)
 - [Plantilla del informe final](SIC_AI_Capstone%20Project_Final%20Report(11).md)
 - [Demo de detección](accessai_demo.py)
 - [Generador de presentación v2](generate_accessai_pptx_v2_0_2.py)

 ## Licencia y materiales del curso

 Los documentos de Samsung Innovation Campus incluidos en esta carpeta pueden estar sujetos a las condiciones de uso y derechos de autor indicados en cada documento. Este README describe el prototipo AccessAI y no modifica esas condiciones.
````
