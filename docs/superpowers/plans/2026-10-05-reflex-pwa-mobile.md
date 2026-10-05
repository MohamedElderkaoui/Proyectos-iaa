# AccessAI Reflex and mobile PWA implementation plan

> **For agentic workers:** Implement inline in the current workspace; do not delegate. Track steps with checkboxes.

**Goal:** Add a four-class Reflex inference app and an installable mobile PWA shell that opens the existing Streamlit app.

**Architecture:** `server.py` provides Reflex UI and image inference using the newest matching local four-class `best.pt`. `mobile_pwa/` is a static installable PWA shell that stores the Streamlit URL and embeds the app; the existing Streamlit app remains the inference server used by that shell.

**Tech Stack:** Python, Reflex, Ultralytics YOLO, Streamlit, static HTML/CSS/JavaScript PWA.

**Spec:** User request in this conversation; repository constraints in `AGENTS.md`, `README.md`, and `PLAN.md`.

## Global Constraints

- AccessAI remains a prototype; detections are not proof of accessibility.
- Use only the existing four class names and matching four-class checkpoints.
- Choose the newest matching checkpoint by file modification time, as selected by the user.
- Keep the GPU-only inference behavior consistent with the existing Streamlit prototype.
- PWA install requires HTTPS in deployment; the inference server and model remain reachable online.
- Do not weaken Streamlit CORS/XSRF configuration without a known deployment origin.

## Review Focus

- No checkpoint exists in configured run roots: show a clear setup error.
- A newer non-four-class checkpoint exists: exclude it from candidates.
- The newest four-class run is not the run with highest mAP50-95: label selection as newest, not best-scoring.
- CUDA or image decode is unavailable: report an error without fabricating detections.
- The saved Streamlit URL is invalid or unreachable: offer a clear reconnect path.
- The device is offline: show the PWA shell's offline state and do not imply inference is available.

---

### Task 1: Reflex inference app

**Files:**
- Create: `server.py`, `rxconfig.py`, `requirements-reflex.txt`, `accessai_checkpoint.py`, `test_accessai_checkpoint.py`
- Modify: `app/streamlit_app.py` model run-directory resolution

**Interfaces:**
- `find_latest_four_class_checkpoint(project_root: Path, home_dir: Path, extra_roots: list[Path] | None = None) -> Path | None`
- Reflex page accepts one image, runs the four-class YOLO checkpoint on CUDA, and displays the annotated image and detections.

- [ ] Add standard-library tests for newest matching checkpoint selection and exclusion of non-four-class runs.
- [ ] Run those tests and confirm they fail before implementing the resolver.
- [ ] Implement the resolver and Reflex image inference page.
- [ ] Configure Reflex to import `server.py` and list its dependencies.
- [ ] Correct Streamlit's model run directory to the repository root.
- [ ] Run the resolver tests and Python syntax compilation.

### Task 2: Mobile PWA shell

**Files:**
- Create: `mobile_pwa/index.html`, `mobile_pwa/app.js`, `mobile_pwa/styles.css`, `mobile_pwa/manifest.webmanifest`, `mobile_pwa/sw.js`, `mobile_pwa/icons/`, `mobile_pwa/README.md`, `test_mobile_pwa.py`

**Interfaces:**
- Users enter a reachable Streamlit URL once; the shell stores it on-device and opens its `?embed=true` view.
- The service worker caches only the shell and provides an offline message; it does not claim to cache model inference.

- [ ] Add tests for valid install manifest fields and local asset references.
- [ ] Run them and confirm they fail before adding the PWA files.
- [ ] Implement a responsive PWA shell, manifest, icons, service worker, and setup notes.
- [ ] Run PWA checks and generate/inspect install icons.

### Task 3: Final project guidance

**Files:**
- Modify: `README.md`

- [ ] Document Reflex startup, PWA setup, HTTPS, Streamlit reachability, and the checkpoint-selection rule.
- [ ] State that PWA offline support covers the shell only and that detections remain unvalidated for real accessibility quality.
- [ ] Review changed files and report commands and remaining deployment requirements accurately.
