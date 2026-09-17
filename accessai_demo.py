"""
AccessAI - Prototipo de detección de accesibilidad urbana

Uso:
    python accessai_demo.py --image "ruta/a/imagen.jpg"

Instalación:
    pip install ultralytics

NOTA:
    yolov8n.pt es un modelo preentrenado de detección general.
    Para detectar las clases específicas de AccessAI
    (por ejemplo: sidewalk, curbramp, obstacle), primero
    necesitaremos entrenar un modelo propio con nuestro dataset.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ultralytics import YOLO


def analizar_imagen(
    image_path: Path,
    model_path: str = "yolov8n.pt",
    confidence: float = 0.25,
    output_path: Path = Path("resultados/accessai_resultado.jpg"),
) -> None:
    """Carga YOLO, analiza una imagen y guarda el resultado."""

    if not image_path.exists():
        raise FileNotFoundError(
            f"No existe la imagen indicada: {image_path}"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 60)
    print("ACCESSAI - ACCESIBILIDAD URBANA")
    print("=" * 60)
    print(f"Imagen : {image_path}")
    print(f"Modelo : {model_path}")
    print(f"Conf.  : {confidence}")
    print()

    print("[1/3] Cargando modelo...")
    model = YOLO(model_path)

    print("[2/3] Analizando imagen...")
    results = model.predict(
        source=str(image_path),
        conf=confidence,
        save=False,
        verbose=False,
    )

    if not results:
        print("No se ha obtenido ningún resultado.")
        return

    result = results[0]

    print("[3/3] Procesando detecciones...")
    print("-" * 60)

    detecciones = 0

    if result.boxes is not None:
        detecciones = len(result.boxes)

        for numero, box in enumerate(result.boxes, start=1):
            clase_id = int(box.cls[0].item())
            confianza = float(box.conf[0].item())
            nombre = model.names.get(clase_id, str(clase_id))

            coordenadas = [
                round(float(valor), 1)
                for valor in box.xyxy[0].tolist()
            ]

            print(
                f"{numero:02d}. "
                f"{nombre:<20} "
                f"confianza={confianza:.2%} "
                f"bbox={coordenadas}"
            )

    if detecciones == 0:
        print("No se han detectado objetos.")

    print("-" * 60)

    # Generamos una imagen anotada.
    annotated = result.plot()

    # OpenCV está disponible como dependencia de Ultralytics.
    import cv2

    success = cv2.imwrite(str(output_path), annotated)

    if not success:
        raise RuntimeError(
            f"No se pudo guardar el resultado en: {output_path}"
        )

    print(f"\nResultado guardado en:")
    print(output_path.resolve())

    print("\n" + "=" * 60)
    print("IMPORTANTE PARA LA PRESENTACIÓN")
    print("=" * 60)
    print(
        "Este modelo todavía no representa el modelo final de AccessAI."
    )
    print(
        "El siguiente paso será entrenarlo con un dataset de "
        "accesibilidad urbana."
    )
    print(
        "Clases objetivo iniciales: sidewalk y curbramp."
    )
    print("=" * 60 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Demo de visión artificial para AccessAI."
    )

    parser.add_argument(
        "--image",
        required=True,
        help="Ruta de la imagen que se quiere analizar.",
    )

    parser.add_argument(
        "--model",
        default="yolov8n.pt",
        help="Ruta al modelo .pt. Por defecto: yolov8n.pt",
    )

    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Umbral de confianza. Por defecto: 0.25",
    )

    parser.add_argument(
        "--output",
        default="resultados/accessai_resultado.jpg",
        help="Ruta del resultado anotado.",
    )

    args = parser.parse_args()

    try:
        if not 0.0 < args.conf <= 1.0:
            raise ValueError(
                "El valor de --conf debe estar entre 0 y 1."
            )

        analizar_imagen(
            image_path=Path(args.image),
            model_path=args.model,
            confidence=args.conf,
            output_path=Path(args.output),
        )

    except FileNotFoundError as error:
        print(f"\nERROR: {error}")
        sys.exit(1)

    except Exception as error:
        print(f"\nERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
