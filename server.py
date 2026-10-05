"""Reflex image inference interface for the AccessAI four-class prototype."""

from __future__ import annotations

import asyncio
import base64
import threading
from pathlib import Path

import reflex as rx

from accessai_checkpoint import find_latest_four_class_checkpoint


PROJECT_ROOT = Path(__file__).resolve().parent
CLASS_NAMES = [
    "Obstaculo_Dinamico",
    "Obstaculo_Fijo",
    "Barrera_Arquitectonica",
    "Infraestructura_Peatonal",
]
IMAGE_UPLOAD_ID = "accessai_image"
MAX_IMAGE_BYTES = 20 * 1024 * 1024
DEFAULT_CONFIDENCE = 0.25

_MODEL = None
_MODEL_PATH: Path | None = None
_MODEL_LOCK = threading.Lock()


def _load_model():
    """Load the newest local four-class checkpoint on the available CUDA GPU."""
    global _MODEL, _MODEL_PATH

    import torch
    from ultralytics import YOLO

    if not torch.cuda.is_available():
        raise RuntimeError(
            "No se detecta CUDA. Esta app usa la GPU y no cambia a CPU."
        )

    with _MODEL_LOCK:
        if _MODEL is not None:
            return _MODEL, _MODEL_PATH

        checkpoint = find_latest_four_class_checkpoint(
            PROJECT_ROOT,
            Path.home(),
        )
        if checkpoint is None:
            raise FileNotFoundError(
                "No se encontró un best.pt de AccessAI de cuatro clases. "
                "Revisa runs/detect o ACCESSAI_MODEL_SEARCH_PATHS."
            )

        model = YOLO(str(checkpoint))
        names = model.names
        names_by_id = names if isinstance(names, dict) else dict(enumerate(names))
        ordered_names = [str(names_by_id[index]) for index in range(len(names_by_id))]
        if ordered_names != CLASS_NAMES:
            raise RuntimeError(
                "Las clases del checkpoint no coinciden con el esquema "
                "de cuatro clases configurado en la app."
            )

        _MODEL = model
        _MODEL_PATH = checkpoint
        return _MODEL, _MODEL_PATH


def _run_inference(image_bytes: bytes, confidence: float) -> tuple[str, list[str], str]:
    """Run one image through YOLO and return a data URI, detections and model path."""
    import cv2
    import numpy as np

    encoded_image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("El archivo no contiene una imagen compatible.")

    model, model_path = _load_model()
    with _MODEL_LOCK:
        result = model.predict(
            source=image,
            conf=confidence,
            imgsz=640,
            device=0,
            save=False,
            verbose=False,
        )[0]

    plotted = result.plot()
    height, width = plotted.shape[:2]
    scale = min(1.0, 1920 / max(height, width))
    if scale < 1.0:
        plotted = cv2.resize(
            plotted,
            (int(width * scale), int(height * scale)),
            interpolation=cv2.INTER_AREA,
        )
    success, output = cv2.imencode(
        ".jpg",
        plotted,
        [cv2.IMWRITE_JPEG_QUALITY, 88],
    )
    if not success:
        raise RuntimeError("No se pudo crear la imagen anotada.")

    class_names = model.names
    detections: list[str] = []
    if result.boxes is not None:
        for box in result.boxes:
            class_id = int(box.cls.item())
            if isinstance(class_names, dict):
                class_name = class_names.get(class_id, str(class_id))
            else:
                class_name = class_names[class_id]
            score = float(box.conf.item())
            x1, y1, x2, y2 = (int(value) for value in box.xyxy[0].tolist())
            detections.append(
                f"{class_name} · {score:.0%} · [{x1}, {y1}, {x2}, {y2}]"
            )

    image_uri = "data:image/jpeg;base64," + base64.b64encode(output).decode("ascii")
    return image_uri, detections, str(model_path)


class AccessAIState(rx.State):
    confidence: float = DEFAULT_CONFIDENCE
    is_processing: bool = False
    status: str = "Sube una imagen para empezar."
    annotated_image: str = ""
    detections: list[str] = []
    model_path: str = ""

    @rx.event
    def set_confidence(self, value: float):
        self.confidence = value

    @rx.var
    def has_detections(self) -> bool:
        return bool(self.detections)

    @rx.event
    def clear_result(self):
        self.annotated_image = ""
        self.detections = []
        self.model_path = ""
        self.status = "Sube una imagen para empezar."
        return rx.clear_selected_files(IMAGE_UPLOAD_ID)

    @rx.event
    async def analyze(self, files: list[rx.UploadFile]):
        if not files:
            self.status = "Selecciona una imagen primero."
            return

        uploaded = files[0]
        extension = Path(uploaded.name).suffix.casefold()
        if extension not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
            self.status = "Formato no compatible. Usa JPG, PNG, WEBP o BMP."
            return

        self.is_processing = True
        self.status = "Analizando imagen con el checkpoint local…"
        self.annotated_image = ""
        self.detections = []
        yield

        try:
            image_bytes = await uploaded.read(MAX_IMAGE_BYTES + 1)
            if len(image_bytes) > MAX_IMAGE_BYTES:
                raise ValueError("La imagen supera el límite de 20 MB.")
            result = await asyncio.to_thread(
                _run_inference,
                image_bytes,
                self.confidence,
            )
        except Exception as error:
            self.status = str(error)
        else:
            self.annotated_image, self.detections, self.model_path = result
            self.status = (
                "Sin detecciones con este umbral."
                if not self.detections
                else f"Detecciones: {len(self.detections)}"
            )
        finally:
            self.is_processing = False


def _detection_list() -> rx.Component:
    return rx.foreach(
        AccessAIState.detections,
        lambda item: rx.text(item, class_name="detection-row"),
    )


def index() -> rx.Component:
    return rx.box(
        rx.box(
            rx.text("ACCESSAI", class_name="eyebrow"),
            rx.heading("Análisis urbano", size="8"),
            rx.text(
                "Prototipo de detección en imágenes peatonales",
                class_name="subtitle",
            ),
            class_name="hero",
        ),
        rx.box(
            rx.heading("Analiza una imagen", size="5"),
            rx.text(
                "Checkpoint de cuatro clases elegido automáticamente por "
                "fecha de modificación. La versión más reciente puede no "
                "ser la que tenga el mAP más alto.",
                class_name="muted",
            ),
            rx.upload(
                rx.vstack(
                    rx.text("Toca para elegir una imagen", class_name="upload-title"),
                    rx.text("JPG, PNG, WEBP o BMP · máximo 20 MB", class_name="muted"),
                    align="center",
                    spacing="2",
                ),
                id=IMAGE_UPLOAD_ID,
                accept={
                    "image/jpeg": [".jpg", ".jpeg"],
                    "image/png": [".png"],
                    "image/webp": [".webp"],
                    "image/bmp": [".bmp"],
                },
                max_files=1,
                max_size=MAX_IMAGE_BYTES,
                width="100%",
                class_name="upload-area",
            ),
            rx.hstack(
                rx.text("Confianza mínima", class_name="muted"),
                rx.text(AccessAIState.confidence, " ", class_name="value"),
                justify="between",
                width="100%",
            ),
            rx.slider(
                min=0.05,
                max=0.95,
                step=0.05,
                default_value=DEFAULT_CONFIDENCE,
                on_change=AccessAIState.set_confidence,
                width="100%",
            ),
            rx.vstack(
                rx.button(
                    "Analizar imagen",
                    on_click=AccessAIState.analyze(rx.upload_files(IMAGE_UPLOAD_ID)),
                    disabled=AccessAIState.is_processing,
                    class_name="primary-button",
                    width="100%",
                ),
                rx.button(
                    "Limpiar",
                    on_click=AccessAIState.clear_result,
                    class_name="secondary-button",
                    width="100%",
                ),
                width="100%",
                align="stretch",
            ),
            rx.text(AccessAIState.status, role="status", class_name="status"),
            rx.cond(
                AccessAIState.model_path != "",
                rx.text("Checkpoint: ", AccessAIState.model_path, class_name="muted"),
                rx.fragment(),
            ),
            class_name="panel",
        ),
        rx.cond(
            AccessAIState.annotated_image != "",
            rx.box(
                rx.heading("Resultado", size="5"),
                rx.image(
                    src=AccessAIState.annotated_image,
                    alt="Imagen urbana anotada por el modelo AccessAI",
                    width="100%",
                    border_radius="14px",
                ),
                rx.cond(
                    AccessAIState.has_detections,
                    rx.vstack(
                        rx.heading("Detecciones", size="4"),
                        _detection_list(),
                        align="stretch",
                        width="100%",
                    ),
                    rx.text("No se detectaron objetos con este umbral.", class_name="muted"),
                ),
                class_name="panel result-panel",
            ),
            rx.fragment(),
        ),
        rx.box(
            rx.heading("Clases del prototipo", size="4"),
            rx.text("Obstaculo Dinamico", class_name="class-chip"),
            rx.text("Obstaculo Fijo", class_name="class-chip"),
            rx.text("Barrera Arquitectonica", class_name="class-chip"),
            rx.text("Infraestructura Peatonal", class_name="class-chip"),
            class_name="panel class-panel",
        ),
        rx.text(
            "AccessAI es un prototipo. Las detecciones no demuestran que un "
            "espacio sea accesible o inaccesible; el modelo requiere evaluación "
            "con datos pertinentes.",
            class_name="disclaimer",
        ),
        class_name="page-shell",
    )


app = rx.App(
    stylesheets=["/styles.css"],
    style={
        "font_family": "Inter, system-ui, sans-serif",
        "color": "#102a43",
        "background": "#f2f7fb",
    },
)
app.add_page(index, title="AccessAI · Análisis urbano")
