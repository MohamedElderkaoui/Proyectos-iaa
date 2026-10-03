# ============================================================
# ACCESSAI - STREAMLIT
# Detección urbana con YOLO26s
# 4 clases
# NVIDIA RTX 4060 Laptop GPU 8 GB
# ============================================================

import gc
import tempfile
from pathlib import Path

import cv2
import streamlit as st
import torch
from ultralytics import YOLO


# ============================================================
# 1. CONFIGURACIÓN STREAMLIT
# ============================================================

st.set_page_config(
    page_title="AccessAI - Detección Urbana",
    page_icon="♿",
    layout="wide",
)


# ============================================================
# 2. CONFIGURACIÓN DEL PROYECTO
# ============================================================

ROOT = Path(__file__).resolve().parent
print(f"Directorio raíz del proyecto: {ROOT}")


RUNS_DIR = ROOT / "runs" / "detect"

CLASS_NAMES = [
    "Obstaculo_Dinamico",
    "Obstaculo_Fijo",
    "Barrera_Arquitectonica",
    "Infraestructura_Peatonal",
]

DEFAULT_CONFIDENCE = 0.25
DEFAULT_IMGSZ = 640


# ============================================================
# 3. ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 20px;
        margin-bottom: 25px;
    }

    .class-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.3);
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. CABECERA
# ============================================================

st.markdown(
    '<div class="main-title">AccessAI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Prototipo de detección urbana para accesibilidad"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# 5. DETECCIÓN GPU
# ============================================================

CUDA_AVAILABLE = torch.cuda.is_available()

if CUDA_AVAILABLE:
    DEVICE = 0
    GPU_NAME = torch.cuda.get_device_name(0)

    gpu_properties = torch.cuda.get_device_properties(0)

    GPU_VRAM_GB = (
        gpu_properties.total_memory / 1024**3
    )

else:
    DEVICE = None
    GPU_NAME = "No disponible"
    GPU_VRAM_GB = 0.0


# ============================================================
# 6. SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Configuración")

    confidence = st.slider(
        "Confianza mínima",
        min_value=0.05,
        max_value=0.95,
        value=DEFAULT_CONFIDENCE,
        step=0.05,
    )

    imgsz = st.selectbox(
        "Tamaño de imagen",
        [416, 512, 640, 768, 960],
        index=2,
    )

    st.divider()

    st.subheader("Hardware")

    if CUDA_AVAILABLE:

        st.success("CUDA disponible")

        st.write(f"**GPU:** {GPU_NAME}")
        st.write(f"**VRAM:** {GPU_VRAM_GB:.2f} GB")
        st.write("**Device:** cuda:0")

    else:

        st.error("CUDA no disponible")

        st.write(
            "La aplicación no utilizará CPU automáticamente."
        )

    st.divider()

    st.subheader("Clases")

    for class_id, class_name in enumerate(CLASS_NAMES):

        st.write(
            f"**{class_id}** — {class_name}"
        )


# ============================================================
# 7. BUSCAR BEST.PT
# ============================================================

def buscar_best_model():

    candidatos = []

    if not RUNS_DIR.is_dir():
        return []

    for path in RUNS_DIR.glob(
        "AccessAI_YOLO26s_4clases_RTX4060_*/weights/best.pt"
    ):
        if path.is_file():
            candidatos.append(path.resolve())

    candidatos.sort(
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    return candidatos


# ============================================================
# 8. CARGAR MODELO
# ============================================================

@st.cache_resource
def cargar_modelo(model_path):

    model = YOLO(str(model_path))

    return model


model_candidates = buscar_best_model()


if not model_candidates:

    st.error(
        "No se encontró automáticamente ningún best.pt."
    )

    st.info(
        "Debe existir una estructura como:\n\n"
        "runs/detect/"
        "AccessAI_YOLO26s_4clases_RTX4060_*/"
        "weights/best.pt"
    )

    model_file = st.file_uploader(
        "Selecciona manualmente best.pt",
        type=["pt"],
    )

    if model_file is not None:

        temporary_model = (
            ROOT / "best_uploaded.pt"
        )

        temporary_model.write_bytes(
            model_file.getbuffer()
        )

        BEST_MODEL = temporary_model

    else:

        st.stop()

else:

    BEST_MODEL = model_candidates[0]


# ============================================================
# 9. VALIDACIÓN CUDA
# ============================================================

if not CUDA_AVAILABLE:

    st.error(
        "ENTRENAMIENTO/INFERENCIA GPU DETENIDA\n\n"
        "PyTorch no detecta CUDA. "
        "AccessAI no cambiará automáticamente a CPU."
    )

    st.stop()


# ============================================================
# 10. CARGAR YOLO
# ============================================================

try:

    model = cargar_modelo(BEST_MODEL)

except Exception as error:

    st.error(
        f"No se pudo cargar el modelo:\n\n{error}"
    )

    st.stop()


# ============================================================
# 11. INFORMACIÓN DEL MODELO
# ============================================================

st.caption(
    f"Modelo: `{BEST_MODEL}`"
)

with st.expander("Información del modelo"):

    st.write(
        "Clases detectadas por el checkpoint:"
    )

    st.write(model.names)

    st.write(
        f"GPU: {GPU_NAME}"
    )

    st.write(
        f"VRAM: {GPU_VRAM_GB:.2f} GB"
    )


# ============================================================
# 12. PESTAÑAS
# ============================================================

tab_image, tab_video, tab_info = st.tabs(
    [
        "🖼️ Imagen",
        "🎥 Vídeo",
        "ℹ️ Proyecto",
    ]
)


# ============================================================
# 13. INFERENCIA IMAGEN
# ============================================================

with tab_image:

    st.header(
        "Detección en imagen"
    )

    uploaded_image = st.file_uploader(
        "Selecciona una imagen",
        type=[
            "jpg",
            "jpeg",
            "png",
            "bmp",
            "webp",
        ],
        key="image_upload",
    )

    if uploaded_image is not None:

        file_suffix = Path(
            uploaded_image.name
        ).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_suffix,
        ) as temporary_file:

            temporary_file.write(
                uploaded_image.getbuffer()
            )

            image_path = temporary_file.name

        st.image(
            uploaded_image,
            caption="Imagen original",
            use_container_width=True,
        )

        if st.button(
            "🔎 Ejecutar detección",
            type="primary",
            key="predict_image",
        ):

            with st.spinner(
                "Ejecutando YOLO26s en la RTX 4060..."
            ):

                try:

                    gc.collect()
                    torch.cuda.empty_cache()

                    results = model.predict(
                        source=image_path,
                        conf=confidence,
                        imgsz=imgsz,
                        device=DEVICE,
                        save=False,
                        verbose=False,
                    )

                    result = results[0]

                    annotated = result.plot()

                    annotated_rgb = cv2.cvtColor(
                        annotated,
                        cv2.COLOR_BGR2RGB,
                    )

                    st.image(
                        annotated_rgb,
                        caption="Resultado AccessAI",
                        use_container_width=True,
                    )

                    # ------------------------------------------------
                    # DETECCIONES
                    # ------------------------------------------------

                    boxes = result.boxes

                    total_detections = (
                        len(boxes)
                        if boxes is not None
                        else 0
                    )

                    st.metric(
                        "Detecciones",
                        total_detections,
                    )

                    class_counts = {}

                    if (
                        boxes is not None
                        and boxes.cls is not None
                    ):

                        for class_id in boxes.cls.tolist():

                            class_id = int(class_id)

                            if isinstance(
                                model.names,
                                dict,
                            ):

                                class_name = model.names.get(
                                    class_id,
                                    str(class_id),
                                )

                            else:

                                class_name = model.names[
                                    class_id
                                ]

                            class_counts[
                                class_name
                            ] = (
                                class_counts.get(
                                    class_name,
                                    0,
                                )
                                + 1
                            )

                    if class_counts:

                        st.subheader(
                            "Detecciones por clase"
                        )

                        for class_name, count in (
                            class_counts.items()
                        ):

                            st.write(
                                f"**{class_name}:** {count}"
                            )

                except torch.cuda.OutOfMemoryError:

                    gc.collect()
                    torch.cuda.empty_cache()

                    st.error(
                        "CUDA OUT OF MEMORY.\n\n"
                        "Reduce el tamaño de imagen "
                        "o cierra otras aplicaciones "
                        "que utilicen la RTX 4060."
                    )

                except Exception as error:

                    st.error(
                        f"Error durante la inferencia:\n\n"
                        f"{error}"
                    )


# ============================================================
# 14. INFERENCIA VIDEO
# ============================================================

with tab_video:

    st.header(
        "Detección en vídeo"
    )

    uploaded_video = st.file_uploader(
        "Selecciona un vídeo",
        type=[
            "mp4",
            "avi",
            "mov",
            "mkv",
            "wmv",
            "webm",
            "mpeg",
            "mpg",
        ],
        key="video_upload",
    )

    if uploaded_video is not None:

        st.video(
            uploaded_video
        )

        if st.button(
            "🎥 Ejecutar detección en vídeo",
            type="primary",
            key="predict_video",
        ):

            video_suffix = Path(
                uploaded_video.name
            ).suffix

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=video_suffix,
            ) as temporary_video:

                temporary_video.write(
                    uploaded_video.getbuffer()
                )

                video_path = temporary_video.name

            prediction_name = (
                "AccessAI_Streamlit_video"
            )

            try:

                gc.collect()
                torch.cuda.empty_cache()

                with st.spinner(
                    "Procesando vídeo con YOLO26s..."
                ):

                    results = model.predict(
                        source=video_path,
                        conf=confidence,
                        imgsz=imgsz,
                        device=DEVICE,
                        save=True,
                        project=str(RUNS_DIR),
                        name=prediction_name,
                        exist_ok=True,
                        verbose=False,
                    )

                output_dir = (
                    RUNS_DIR / prediction_name
                )

                st.success(
                    "Inferencia de vídeo terminada."
                )

                st.write(
                    f"**Salida:** `{output_dir}`"
                )

                st.write(
                    f"**Frames procesados:** "
                    f"{len(results)}"
                )

                # ------------------------------------------------
                # RESUMEN
                # ------------------------------------------------

                class_counts = {}
                total_detections = 0

                for frame_result in results:

                    boxes = frame_result.boxes

                    if boxes is None:
                        continue

                    total_detections += len(
                        boxes
                    )

                    if boxes.cls is None:
                        continue

                    for class_id in (
                        boxes.cls.tolist()
                    ):

                        class_id = int(class_id)

                        if isinstance(
                            model.names,
                            dict,
                        ):

                            class_name = model.names.get(
                                class_id,
                                str(class_id),
                            )

                        else:

                            class_name = model.names[
                                class_id
                            ]

                        class_counts[
                            class_name
                        ] = (
                            class_counts.get(
                                class_name,
                                0,
                            )
                            + 1
                        )

                st.metric(
                    "Detecciones totales",
                    total_detections,
                )

                if class_counts:

                    st.subheader(
                        "Detecciones por clase"
                    )

                    for class_name, count in (
                        class_counts.items()
                    ):

                        st.write(
                            f"**{class_name}:** {count}"
                        )

                # ------------------------------------------------
                # BUSCAR VIDEO RESULTANTE
                # ------------------------------------------------

                video_outputs = []

                for output_file in output_dir.iterdir():

                    if (
                        output_file.is_file()
                        and output_file.suffix.lower()
                        in VIDEO_EXTENSIONS
                    ):

                        video_outputs.append(
                            output_file
                        )

                if video_outputs:

                    output_video = video_outputs[0]

                    st.subheader(
                        "Vídeo procesado"
                    )

                    video_bytes = (
                        output_video.read_bytes()
                    )

                    st.video(
                        video_bytes
                    )

                    st.download_button(
                        label="⬇️ Descargar vídeo procesado",
                        data=video_bytes,
                        file_name=(
                            "AccessAI_"
                            + output_video.name
                        ),
                        mime="video/mp4",
                    )

            except torch.cuda.OutOfMemoryError:

                gc.collect()
                torch.cuda.empty_cache()

                st.error(
                    "CUDA OUT OF MEMORY durante "
                    "la inferencia de vídeo."
                )

            except Exception as error:

                st.error(
                    f"Error durante el procesamiento:\n\n"
                    f"{error}"
                )


# ============================================================
# 15. INFORMACIÓN DEL PROYECTO
# ============================================================

with tab_info:

    st.header(
        "AccessAI - Detección urbana"
    )

    st.write(
        """
        AccessAI es un prototipo de visión artificial
        basado en YOLO26s para identificar elementos
        relacionados con la accesibilidad urbana.
        """
    )

    st.subheader(
        "Clases"
    )

    for class_id, class_name in enumerate(
        CLASS_NAMES
    ):

        st.markdown(
            f"""
            <div class="class-card">
            <b>{class_id}</b> — {class_name}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader(
        "Configuración"
    )

    configuration_data = {
        "Modelo": "YOLO26s",
        "Clases": 4,
        "Image size": imgsz,
        "Confidence": confidence,
        "GPU": GPU_NAME,
        "CUDA": str(torch.version.cuda),
        "Device": "cuda:0",
        "VRAM": f"{GPU_VRAM_GB:.2f} GB",
    }

    st.table(
        configuration_data
    )

    st.subheader(
        "Modelo utilizado"
    )

    st.code(
        str(BEST_MODEL),
        language="text",
    )

    st.success(
        "AccessAI está utilizando la GPU NVIDIA "
        "para la inferencia."
    )