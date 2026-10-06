# AccessAI Streamlit App Plan

## Goal

Maintain a reliable GPU-only Streamlit prototype for running the four-class AccessAI YOLO checkpoint on images and videos. Keep this plan scoped to the app; dataset strategy and overall project milestones remain in the project-level plan.

## Current state

- The Streamlit interface exposes image, video, and project-information tabs.
- The sidebar exposes confidence and inference image-size controls.
- The app searches for a recent trained checkpoint and also supports manual upload.
- CUDA is required; inference stops if PyTorch cannot access it.
- Image inference displays an annotated image and per-class counts.
- Video inference requests saved output, but its result-discovery path references the undefined `VIDEO_EXTENSIONS` name. Video playback/download is therefore not verified.
- `app/requirements.txt` currently lists Streamlit only, although runtime imports also require OpenCV, PyTorch, and Ultralytics.
- No evidence in this app alone establishes the model's real-world accessibility performance.

## Priorities

### 1. Make the app reproducible

- Declare all Python runtime dependencies in the app dependency file, while documenting that the PyTorch CUDA wheel must match the local driver/runtime setup.
- Document and test the supported Python, PyTorch, Ultralytics, and CUDA combination on the target NVIDIA GPU.
- Keep checkpoints, uploaded media, and generated runs out of version control.

### 2. Complete and verify inference workflows

- Define the supported output-video extensions and use them when discovering the saved result.
- Verify the annotated video can be played and downloaded after inference.
- Verify image and video temporary files are cleaned up on success and failure.
- Check behavior for empty detections, invalid uploads, missing checkpoints, and CUDA out-of-memory errors.

### 3. Validate checkpoint compatibility

- Confirm the checkpoint has exactly the expected four classes and the intended class order before presenting results.
- Test automatic checkpoint selection and manual upload independently.
- Avoid implying model accuracy or accessibility judgments without evaluation on a relevant held-out dataset.

## Acceptance checks

- App starts with the documented command in the configured Python environment.
- CUDA status and selected device are accurate; no CPU fallback occurs.
- A representative image produces an annotated result and class counts.
- A representative video produces a saved output that can be displayed and downloaded.
- Missing or incompatible checkpoints produce a clear error.
- README, this plan, dependency declarations, and app behavior agree.
