# Plan de Proyecto — Proyecto Jupiter NB (AccessAI)

> **Nota:** "Proyecto Jupiter NB" es el nombre interno de trabajo de **AccessAI: AI-Based Urban Accessibility Detection**, proyecto desarrollado en el marco de Samsung Innovation Campus 2025-26. Este documento consolida el Action Plan del curso y el estado técnico actual descrito en el README en una hoja de ruta operativa.

## Resumen

AccessAI (Jupiter NB) es un sistema de visión artificial que analiza imágenes de entornos urbanos y peatonales para detectar elementos relacionados con la accesibilidad, empezando por **aceras** y **rampas de acceso**. El prototipo actual usa YOLOv8n preentrenado de propósito general; el objetivo del proyecto es sustituirlo por un modelo entrenado específicamente para clases de accesibilidad.

## 1. Objetivo

**Principal:** desarrollar un sistema capaz de analizar una imagen de una zona peatonal y localizar automáticamente elementos relacionados con la accesibilidad urbana.

**A largo plazo:** combinar las detecciones con coordenadas GPS para construir un mapa de accesibilidad que ayude en la navegación de personas con movilidad reducida.

## 2. Estado actual

- ✅ Prototipo funcional (`accessai_demo.py`) que carga una imagen, ejecuta YOLO y guarda una copia anotada con bounding boxes.
- ✅ Generadores de presentación (`generate_accessai_pptx.py`, `generate_accessai_pptx_v2_0_2.py`) con el tema de Samsung.
- ⚠️ El modelo en uso (`yolov8n.pt`) es genérico — **no** está entrenado con clases de accesibilidad. Una detección actual no implica que una acera o rampa sea realmente accesible.
-  ❌ Sin dataset propio integrado en el repositorio todavía.
- ❌ Sin métricas de entrenamiento ni interfaz de usuario.
- ❌ Sin información geográfica en las detecciones.

## 3. Metodología

1. **Selección de datos:** evaluar Project Sidewalk, Sidewalk Accessibility y Cityscapes según número de imágenes, clases, calidad de etiquetas y distribución.
2. **Preparación:** limpieza, conversión de anotaciones a formato YOLO, y división en train / validation / test.
3. **Modelado — dos enfoques a estudiar:**
   - *Clasificación de imágenes:* MobileNetV2 vía transfer learning.
   - *Detección de objetos (prioritaria para el primer prototipo):* YOLOv8n, porque da clase **y** localización.
4. **Aumento de datos** (si hace falta): brillo/contraste, zoom, recortes controlados, para reducir sobreajuste.
5. **Entrenamiento:** con Early Stopping y ajuste de hiperparámetros vía Optuna.
6. **Evaluación:**
   - Clasificación → Accuracy, Balanced Accuracy, Precision, Recall, F1-score, ROC-AUC.
   - Detección → Precision, Recall, F1-score, mAP.
7. **Integración:** modelo final embebido en el prototipo (`accessai_demo.py` o su evolución) con visualización de detecciones.

## 4. Datos

| Dataset | Rol | Por confirmar |
|---|---|---|
| Project Sidewalk | Candidato principal | Cobertura de clases `sidewalk` / `curbramp`, calidad de etiquetas |
| Sidewalk Accessibility | Candidato | Formato de anotaciones, tamaño del dataset |
| Cityscapes | Candidato / complemento | Relevancia de clases urbanas para accesibilidad |

Criterios de selección final: disponibilidad de anotaciones, compatibilidad de clases con el objetivo (`sidewalk`, `curbramp` inicialmente), calidad de imágenes, distribución de clases.

## 5. Arquitectura del prototipo (actual)

```
Imagen urbana → accessai_demo.py → Modelo YOLO → Detecciones y confianza
→ Bounding boxes anotadas → resultados/accessai_resultado.jpg
```

## 6. Hoja de ruta

### Fase 1 — Análisis de datos
- [ ] Descargar y explorar Project Sidewalk, Sidewalk Accessibility y Cityscapes
- [ ] Documentar número de imágenes, clases, distribución y calidad de etiquetas
- [ ] Seleccionar el dataset (o combinación) definitivo

### Fase 2 — Preparación
- [ ] Limpiar y normalizar los datos
- [ ] Convertir anotaciones al formato YOLO
- [ ] Crear splits `train` / `val` / `test`
- [ ] Definir configuración de clases (mínimo: `sidewalk`, `curbramp`)

### Fase 3 — Entrenamiento
- [ ] Entrenar baseline con YOLOv8n
- [ ] (Opcional) Probar MobileNetV2 con transfer learning como comparación
- [ ] Aplicar aumento de datos si hay sobreajuste
- [ ] Ajustar hiperparámetros con Optuna + Early Stopping

### Fase 4 — Evaluación
- [ ] Calcular Precision, Recall, F1 y mAP por clase
- [ ] Revisar falsos positivos / falsos negativos
- [ ] Probar el modelo con imágenes nuevas no vistas

### Fase 5 — Integración
- [ ] Sustituir `yolov8n.pt` por el modelo entrenado en `accessai_demo.py`
- [ ] Añadir procesamiento por lotes o una interfaz mínima de usuario
- [ ] (Ampliación futura) explorar integración con coordenadas GPS

### Fase 6 — Documentación y entrega
- [ ] Actualizar README con resultados reales del modelo entrenado
- [ ] Preparar presentación final (`generate_accessai_pptx_v2_0_2.py`)
- [ ] Revisión conjunta y pruebas finales del equipo

## 7. Roles del equipo

**Miembro 1 — Datos**
- Búsqueda y análisis de datasets
- Descarga y organización de los datos
- Limpieza y preparación de las imágenes
- Análisis de clases y distribución

**Miembro 2 — Machine Learning**
- Preparación del modelo
- Entrenamiento de MobileNetV2 y/o YOLOv8n
- Ajuste de hiperparámetros
- Evaluación con las métricas seleccionadas

**Miembro 3 — Aplicación**
- Desarrollo del prototipo
- Integración del modelo entrenado
- Diseño de la interfaz
- Visualización de las detecciones

**Trabajo conjunto:** análisis de resultados, pruebas, documentación, presentación y revisión final.

## 8. Riesgos y limitaciones conocidas

- No hay todavía dataset propio integrado en el repositorio.
- El modelo genérico actual puede dar una falsa sensación de "ya funciona" — no está validado para accesibilidad real.
- La demo procesa una imagen a la vez (sin procesamiento por lotes todavía).
- Sin datos geográficos, las detecciones no se pueden ubicar en un mapa aún.

## 9. Próximos pasos inmediatos

1. Cerrar la selección de dataset (Fase 1).
2. Definir el esquema de clases final antes de anotar/convertir nada.
3. Preparar el primer split de entrenamiento para tener una baseline entrenable cuanto antes.

---
*Generado a partir de `SIC_AI_Capstone Project_Action Plan(6).md` y `README.md`. Actualizar este archivo a medida que avancen las fases.*
