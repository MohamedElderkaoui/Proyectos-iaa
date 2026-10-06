# Agent Instructions: AccessAI Streamlit App

These instructions apply to files in `app/`. The parent directory contains broader AccessAI project documentation; use this app README and plan as the source of truth for the current Streamlit implementation.

## Project facts

- The app is Streamlit with Ultralytics YOLO, PyTorch, and OpenCV. Do not describe Flutter or FastAPI as implemented; they are not present in this app.
- Inference requires CUDA and must not silently fall back to CPU.
- The expected class order is `Obstaculo_Dinamico`, `Obstaculo_Fijo`, `Barrera_Arquitectonica`, `Infraestructura_Peatonal`.
- Treat AccessAI as an experimental prototype. Never claim accessibility accuracy, model quality, or production readiness without evaluation evidence.
- Checkpoint discovery, manual upload, output paths, and temporary-file handling are part of the app behavior; account for each when changing model or inference code.

## Working rules

- Read `README.md`, `PLAN.md`, and the relevant part of `streamlit_app.py` before changing this app.
- Keep edits scoped to the requested behavior and follow existing Python and Streamlit patterns.
- Do not invent class labels, model metrics, dataset facts, or hardware compatibility claims.
- Do not commit model checkpoints, uploaded images/videos, generated inference outputs, or secrets.
- Keep dependency documentation synchronized with imports. PyTorch CUDA installation depends on the target environment and must be called out separately when necessary.
- For inference changes, consider both image and video paths, CUDA errors, missing/incompatible checkpoints, and empty detections.
- Update the app README or plan when commands, dependencies, supported inputs, checkpoint selection, or limitations change.

## Validation and reporting

- Run a focused syntax, import, or behavior check for the changed code when the environment permits.
- Do not claim successful GPU inference unless it was actually run on a CUDA-capable environment with a suitable checkpoint and sample input.
- Report what was checked and identify any unavailable GPU, model, media, or runtime dependency that prevented end-to-end validation.
