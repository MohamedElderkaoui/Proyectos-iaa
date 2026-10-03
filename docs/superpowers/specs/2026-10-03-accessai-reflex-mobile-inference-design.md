# AccessAI mobile web inference prototype

## Status

Draft for user review. This design follows the approved scope: Reflex, a mobile-friendly image inference page, and a JSON API for detection results with an annotated image. Implementation must wait until this written design is approved.

## Purpose

Provide a small mobile-browser interface and API so a user can submit one urban image and inspect the YOLO model's detections. The output remains an experimental prototype result; it is not a finding that a place is accessible or inaccessible.

## Repository context

- `README.md` and `PLAN.md` describe AccessAI as a prototype and caution that detections are not proof of accessibility.
- `DATA/ROD-Dataset/dataset/data.yaml` declares the original 25 ROD classes. A local training run references `data_filtrado.yaml` and stores a `best.pt` checkpoint, but the run artifact alone does not establish real-world accessibility validity.
- There is no current Reflex or FastAPI application in the repository, and neither package is installed in `.venv_accessai`.
- Several local model checkpoints exist. The application must not guess which checkpoint to use.

## Approved scope

### Mobile web page

Create a responsive Reflex page for a mobile browser. The page lets the user select an image, submit it, see progress or a readable error, view the annotated image, and inspect each detection's class, confidence, and bounding-box coordinates. Show a short notice that detections are unvalidated prototype output and cannot establish accessibility.

### Inference API

Extend the Reflex ASGI application with a FastAPI route through Reflex's `api_transformer` integration.

`POST /api/predict`

- Input: one uploaded image and optional `conf` value, default `0.25`; accept confidence values greater than `0` and at most `1`.
- Processing: validate and decode the image in memory, run inference at image size `640`, and render the model's annotation.
- Output: JSON containing the original filename, a list of detections (`class_id`, `class_name`, `confidence`, and pixel `bbox_xyxy`), and the annotated JPEG as a base64 data URL. Class names come from the loaded checkpoint, not a second hard-coded schema.
- Do not save uploaded or annotated images to disk, and do not persist requests.

### Model configuration

Require `ACCESSAI_MODEL_PATH` to point to an existing `.pt` checkpoint. Fail clearly at startup if the setting is missing or invalid; do not silently choose a generic or local `best.pt` checkpoint. Load the model once per server process and serialize inference calls around that model instance.

## Architecture and data flow

```text
Mobile browser
  -> Reflex upload page
  -> POST /api/predict (FastAPI route mounted in Reflex)
  -> in-memory image validation
  -> configured YOLO checkpoint
  -> JSON detections + annotated image data URL
  -> Reflex page renders the result
```

The web page and API run as one application in this prototype. The same route can also be called by another mobile client. The initial deployment target is a developer-controlled local network; public hosting, accounts, and authentication are outside this version.

## Error handling

- Return `400` for unsupported, malformed, or undecodable image input and invalid confidence values.
- Return `413` when the upload exceeds the configured size limit.
- Return a clear service error when the model cannot be loaded or inference fails, without returning local filesystem paths or stack traces to clients.
- Keep request processing in memory and reject files that are not recognized as supported images.

## Dependencies and files

- Add a dedicated web-app dependency file for Reflex (which supplies the FastAPI runtime) rather than changing the existing environment export wholesale.
- Add the Reflex application, route, and inference adapter under a clearly named `accessai_mobile/` package.
- Add `.env.example` documenting `ACCESSAI_MODEL_PATH` and local run settings without including model weights or secrets.
- Update `README.md` with local setup, how to select a checkpoint, how a phone on the same network reaches the app, the endpoint contract, and prototype limitations.
- Do not modify the existing training notebooks or their current working-tree changes.

## Out of scope

- Native Android/iOS packaging.
- Accounts, authentication, storage, detection history, GPS, maps, or database.
- Training, dataset conversion, class remapping, or claims about model accuracy.
- Public cloud deployment or a production security posture.

## Acceptance criteria

1. The Reflex page works at a narrow mobile viewport and handles image selection, loading, success, and error states.
2. `/api/predict` accepts a valid image and returns the documented JSON fields, using the configured checkpoint's class names.
3. Missing/invalid checkpoint configuration, invalid confidence, invalid image, and oversized uploads produce clear failures.
4. Neither input nor output images are written to disk by the web request path.
5. The page and API state clearly that outputs are prototype detections, not accessibility determinations.
6. Existing notebook and script changes remain untouched.

## Self-review

- Scope is limited to the approved single-image mobile web flow and its inference endpoint.
- Model selection is explicit and does not promote any local checkpoint as validated.
- The 25 original dataset classes are not assumed to be the model's output schema; output names are read from the configured checkpoint.
- No persistent storage, GPS, account, or cloud behavior is implied by the design.
