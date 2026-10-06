# AccessAI Streamlit

AccessAI is a computer-vision prototype for exploring urban accessibility. This app provides a Streamlit interface for running a YOLO26s checkpoint on images and videos, with inference restricted to an NVIDIA GPU detected by PyTorch CUDA.

> This is an experimental prototype, not a validated accessibility assessment system. A detection does not establish that a location is accessible or inaccessible. The checkpoint and its class performance must be evaluated on a representative, labeled dataset before real-world conclusions are drawn.

## Classes

| ID | Class |
| --: | --- |
| 0 | `Obstaculo_Dinamico` |
| 1 | `Obstaculo_Fijo` |
| 2 | `Barrera_Arquitectonica` |
| 3 | `Infraestructura_Peatonal` |

## Requirements

- Python 3.10 or later.
- An NVIDIA GPU with a compatible driver and CUDA-enabled PyTorch installation.
- `streamlit`, `opencv-python`, `torch`, and `ultralytics`.
- A trained AccessAI checkpoint (`best.pt`).

The current `requirements.txt` lists only Streamlit. Install the remaining app dependencies explicitly, and install the PyTorch build that matches your CUDA environment:

```powershell
python -m pip install streamlit opencv-python ultralytics
```

Install PyTorch using the official selector at https://pytorch.org/get-started/locally/ . Then verify CUDA:

```powershell
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CUDA unavailable')"
```

The app stops when CUDA is unavailable; it does not fall back to CPU.

## Checkpoint

The app searches under the project root in:

```text
runs/detect/AccessAI_YOLO26s_4clases_RTX4060_*/weights/best.pt
```

If multiple checkpoints match, it selects the most recently modified one. If no checkpoint is found, the UI allows a manual upload and writes it to `best_uploaded.pt` in the project root (the parent directory of `app/`). Do not commit model checkpoints or other large media files.

## Run

From the project root, activate the project's virtual environment and run:

```powershell
python -m streamlit run app/streamlit_app.py
```

Use the sidebar to set the confidence threshold and image size. The Image tab accepts JPG, JPEG, PNG, BMP, and WebP files. The Video tab accepts MP4, AVI, MOV, MKV, WMV, WebM, MPEG, and MPG files. Video inference writes Ultralytics output under:

```text
runs/detect/AccessAI_Streamlit_video/
```

The video-result display currently has a known issue: it references `VIDEO_EXTENSIONS`, which is not defined in the app. The inference output may be saved, but locating and displaying/downloading it can fail. See [PLAN.md](PLAN.md) for the repair and verification steps.

## App layout

```text
proyecto2/
├── app/
│   ├── streamlit_app.py
│   ├── requirements.txt
│   ├── README.md
│   ├── PLAN.md
│   └── AGENTS.md
├── runs/detect/<training>/weights/best.pt
└── best_uploaded.pt                 # optional manual upload
```

The app-specific implementation plan is in [PLAN.md](PLAN.md). Instructions for coding agents working on this app are in [AGENTS.md](AGENTS.md). The project-level documentation in the parent directory provides broader AccessAI context and may describe earlier project stages.
