from __future__ import annotations

import base64
import tempfile
import uuid
from pathlib import Path

import cv2
import flet as ft
import torch
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT.parent / "runs" / "detect"


def find_best_model() -> Path | None:
    if not RUNS_DIR.exists():
        return None

    candidates: list[Path] = []
    for path in RUNS_DIR.glob("AccessAI_YOLO26s_4clases_RTX4060_*/weights/best.pt"):
        if path.is_file():
            candidates.append(path)

    if not candidates:
        fallback = ROOT.parent / "best_uploaded.pt"
        if fallback.exists():
            return fallback
        return None

    candidates.sort(key=lambda item: item.stat().st_mtime, reverse=True)
    return candidates[0]


def get_gpu_status() -> tuple[bool, str, float, int | None]:
    if not torch.cuda.is_available():
        return False, "No disponible", 0.0, None

    gpu_name = torch.cuda.get_device_name(0)
    vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    return True, gpu_name, vram_gb, 0


def format_detection_output(result) -> str:
    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        return "No se detectaron objetos con el umbral actual."

    names = result.names
    lines = ["Detecciones:"]
    for idx in range(len(boxes.cls)):
        class_id = int(boxes.cls[idx])
        confidence = float(boxes.conf[idx])
        if isinstance(names, dict):
            class_name = names.get(class_id, f"Clase_{class_id}")
        elif isinstance(names, (list, tuple)) and 0 <= class_id < len(names):
            class_name = names[class_id]
        else:
            class_name = f"Clase_{class_id}"
        lines.append(f"- {class_name}: {confidence:.2f} ({idx + 1})")
    return "\n".join(lines)


def make_empty_png_data_url() -> str:
    return (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB4L0AAAAAABLR0lG"
        "dGxJwAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJ0UkGAAAAAJ3pQAAAAB"
        "JRU5ErkJggg=="
    )


def main(page: ft.Page):
    page.title = "AccessAI - Flet"
    page.padding = 22
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    cuda_available, gpu_name, gpu_vram, device = get_gpu_status()

    selected_image = ft.Text("Sin imagen seleccionada")
    status_text = ft.Text("Listo para analizar")
    preview = ft.Image(src=make_empty_png_data_url(), width=700, height=430, fit=ft.BoxFit.CONTAIN)
    result_panel = ft.TextField(
        value="Aquí aparecerán las detecciones.",
        read_only=True,
        multiline=True,
        min_lines=9,
        max_lines=12,
        width=700,
    )

    model_path = find_best_model()
    default_model_name = str(model_path) if model_path else "yolov8n.pt"
    model_dropdown = ft.Dropdown(
        label="Modelo",
        width=360,
        value=default_model_name,
        options=[
            ft.DropdownOption(default_model_name),
            ft.DropdownOption("yolov8n.pt"),
            ft.DropdownOption("yolov8s.pt"),
            ft.DropdownOption("yolov8m.pt"),
        ],
    )

    confidence_slider = ft.Slider(
        min=0.05,
        max=0.95,
        value=0.25,
        divisions=18,
        label="Confianza mínima",
        width=360,
    )

    size_slider = ft.Slider(
        min=320,
        max=1280,
        value=640,
        divisions=10,
        label="Tamaño de imagen",
        width=360,
    )

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    current_file_path: Path | None = None

    async def on_file_selected(_):
        nonlocal current_file_path
        if file_picker.result is None or file_picker.result.files is None:
            return

        selected_file = file_picker.result.files[0]
        file_bytes = selected_file.read()

        upload_dir = Path(tempfile.gettempdir()) / "accessai_uploads"
        upload_dir.mkdir(exist_ok=True)

        current_file_path = upload_dir / selected_file.name
        current_file_path.write_bytes(file_bytes)

        preview.src_base64 = base64.b64encode(file_bytes).decode("utf-8")
        selected_image.value = selected_file.name
        status_text.value = "Imagen cargada. Listo para inferencia."
        page.update()

    file_picker.on_result = on_file_selected

    async def run_detection(_):
        nonlocal current_file_path
        if current_file_path is None:
            status_text.value = "Primero selecciona una imagen."
            page.update()
            return

        model_name = model_dropdown.value or "yolov8n.pt"

        try:
            status_text.value = "Ejecutando detección..."
            page.update()

            if not cuda_available:
                raise RuntimeError("CUDA no disponible en este entorno. La inferencia está detenida.")

            model = YOLO(model_name)
            results = model(
                str(current_file_path),
                conf=float(confidence_slider.value),
                imgsz=int(size_slider.value),
                device=device,
                verbose=False,
            )

            if not results or len(results) == 0:
                raise ValueError("La inferencia no devolvió resultados.")

            annotated = results[0].plot()
            annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

            output_path = Path(tempfile.gettempdir()) / f"accessai_{uuid.uuid4().hex}.png"
            cv2.imwrite(str(output_path), cv2.cvtColor(annotated_rgb, cv2.COLOR_RGB2BGR))

            preview.src = str(output_path)
            preview.fit = ft.BoxFit.CONTAIN
            result_panel.value = format_detection_output(results[0])
            status_text.value = "Detección completada."
            page.update()

        except Exception as exc:  # pragma: no cover - UI path
            result_panel.value = f"Error al ejecutar la detección:\n{exc}"
            status_text.value = "La detección falló."
            page.update()

    async def open_image_picker(_):
        await file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE,
            dialog_title="Elige una imagen para AccessAI",
        )

    choose_button = ft.FilledButton("Seleccionar imagen", on_click=open_image_picker)
    analyze_button = ft.FilledButton("Ejecutar detección", on_click=run_detection)

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("AccessAI", size=34, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Prototipo Flet para detección urbana y accesibilidad.",
                            size=16,
                            color=ft.Colors.BLUE_700,
                        ),
                        ft.Divider(),
                        ft.Row([choose_button, analyze_button]),
                        ft.Row([selected_image]),
                        ft.Divider(),
                        ft.Text("Configuración del modelo", weight=ft.FontWeight.BOLD),
                        ft.Row([model_dropdown]),
                        ft.Row([confidence_slider]),
                        ft.Row([size_slider]),
                        ft.Divider(),
                        ft.Text("Estado:", weight=ft.FontWeight.BOLD),
                        status_text,
                        ft.Divider(),
                        ft.Text("Hardware", weight=ft.FontWeight.BOLD),
                        ft.Text(f"CUDA: {'Disponible' if cuda_available else 'No disponible'}"),
                        ft.Text(f"GPU: {gpu_name}"),
                        ft.Text(f"VRAM: {gpu_vram:.2f} GB" if cuda_available else "VRAM: 0.00 GB"),
                        ft.Text(f"Device: {'cuda:0' if cuda_available else 'cpu'}"),
                    ],
                    width=420,
                    spacing=12,
                ),
                ft.Column(
                    [
                        ft.Text("Vista previa", weight=ft.FontWeight.BOLD),
                        preview,
                        ft.Divider(),
                        ft.Text("Resultados", weight=ft.FontWeight.BOLD),
                        result_panel,
                    ],
                    width=700,
                    spacing=12,
                ),
            ],
            spacing=24,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )


if __name__ == "__main__":
    ft.run(main)
