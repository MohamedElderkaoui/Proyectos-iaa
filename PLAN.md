# Plan de proyecto — AccessAI

> Este documento refleja las decisiones actuales del equipo y se ajusta a la evidencia disponible en el repositorio. No incluye supuestos ni avances no verificados.

## 1. Objetivo final del proyecto

Desarrollar una demo funcional de detección visual para accesibilidad urbana, centrada en dos clases objetivo:
- `sidewalk`
- `curbramp`

La prioridad es que la demo funcione con un modelo entrenado para estas clases y permita visualizar los resultados sobre imágenes peatonales, sin ampliar el alcance a funciones no previstas en esta etapa.

## 2. Decisiones de alcance fijadas por el equipo

1. Un único dataset para el desarrollo inicial.
2. Solo dos clases objetivo: `sidewalk` y `curbramp`.
3. Enfoque en una demo funcional, no en un sistema completo con mapas, geolocalización ni múltiples módulos de producto.

## 3. Estado verificado del repositorio

### Existe en este proyecto
- Demo de detección basada en YOLO: `accessai_demo.py`.
- Generadores de presentación: `generate_accessai_pptx.py` y `generate_accessai_pptx_v2_0_2.py`.
- Documentación del proyecto: `README.md`.
- Recursos de presentación: `Theme3.thmx` y `inspect_theme.py`.

### Todavía no está implementado
- Dataset propio de accesibilidad urbana integrado en el repositorio.
- Entrenamiento real para AccessAI.
- Modelo entrenado con `sidewalk` y `curbramp`.
- Métricas de entrenamiento verificables.
- Interfaz de usuario más allá de la demo de línea de comandos.
- Integración con GPS, map tiles u otros componentes geográficos.

### Estado real del modelo actual
- El modelo en uso en la documentación es `yolov8n.pt`, un modelo general preentrenado.
- La documentación indica explícitamente que este modelo no está entrenado para accesibilidad urbana.
- Por tanto, la demo actual sirve como base técnica, pero no como validación del problema real.

## 4. Alcance real de la fase actual

La fase actual debe centrarse en:
1. preparar un dataset único útil para el problema,
2. definir exactamente las dos clases objetivo,
3. convertir anotaciones al formato compatible con YOLO,
4. entrenar un modelo inicial para `sidewalk` y `curbramp`,
5. integrar ese modelo en la demo funcional,
6. documentar resultados reales del sistema.

## 5. Datasets mencionados en la documentación

La documentación menciona tres candidatos:
- Project Sidewalk
- Sidewalk Accessibility
- Cityscapes

Con la decisión actual de trabajar con un único dataset, se elegirá uno de estos como fuente principal y no se combinarán varias fuentes en la fase inicial. La elección debe basarse en:
- disponibilidad de anotaciones,
- compatibilidad con las clases objetivo,
- calidad de las imágenes,
- distribución de ejemplos por clase,
- viabilidad de preparación en formato YOLO.

## 6. Metodología operativa

### Fase 1 — Elección del dataset único
- [ ] Revisar los candidatos documentados: Project Sidewalk, Sidewalk Accessibility y Cityscapes.
- [ ] Evaluar número de imágenes, calidad de anotaciones y compatibilidad con `sidewalk` y `curbramp`.
- [ ] Elegir un único dataset para la fase inicial.
- [ ] Registrar la decisión y justificarla en la documentación del proyecto.

### Fase 2 — Preparación de datos
- [ ] Verificar el formato de anotaciones del dataset seleccionado.
- [ ] Limpiar y normalizar imágenes y etiquetas.
- [ ] Convertir las anotaciones al formato requerido por YOLO.
- [ ] Definir la configuración de clases con exactamente `sidewalk` y `curbramp`.
- [ ] Crear particiones `train`, `val` y `test`.

### Fase 3 — Entrenamiento del baseline
- [ ] Entrenar un primer modelo YOLO con las dos clases objetivo.
- [ ] Guardar configuración, pesos y resultados del entrenamiento.
- [ ] Revisar si hace falta ajuste de hiperparámetros.
- [ ] Documentar la línea base del modelo.

### Fase 4 — Evaluación
- [ ] Medir precision, recall, F1 y mAP por clase.
- [ ] Revisar errores en falsos positivos y falsos negativos.
- [ ] Probar el modelo con imágenes nuevas no vistas.
- [ ] Registrar la interpretación de los resultados.

### Fase 5 — Integración en la demo funcional
- [ ] Sustituir el modelo genérico actual por el modelo entrenado.
- [ ] Verificar que la demo ejecuta detecciones sobre imágenes reales.
- [ ] Confirmar que la salida con bounding boxes se genera correctamente.
- [ ] Mantener la demo como pieza funcional y documentada.

### Fase 6 — Cierre de documentación
- [ ] Actualizar README con el estado real del modelo entrenado.
- [ ] Preparar la presentación final del proyecto.
- [ ] Alinear plan, informe y README con la evidencia real.

## 7. Criterio de éxito de esta fase

La fase inicial se considera exitosa si:
- se tiene un único dataset elegido y preparado,
- las clases del problema son exactamente `sidewalk` y `curbramp`,
- se obtiene un modelo entrenado para esas dos clases,
- la demo funciona detectando sobre imágenes reales,
- el proyecto documenta los resultados de forma honesta y verificable.

## 8. Riesgos y limitaciones reales

- El repositorio no incluye todavía el dataset final ni el modelo entrenado.
- El modelo genérico actual no tiene validez para este problema específico.
- La demo actual solo funciona como prueba técnica de flujo, no como evidencia de rendimiento real.
- Si el dataset elegido no tiene buena cobertura de las dos clases, la calidad del modelo puede verse limitada.

## 9. Decisiones pendientes mínimas

Antes de continuar con la fase de entrenamiento, todavía se requiere confirmar:
1. cuál de los datasets candidatos será el único usado,
2. si la clase `curbramp` se usará con el nombre exacto o si se requiere un esquema de etiquetas equivalente,
3. el criterio de aceptabilidad de la demo funcional para la entrega.

## 10. Conclusión

El proyecto ya tiene una base técnica útil, pero la fase de avance real debe centrarse en un dataset único, dos clases objetivo y una demo funcional basada en un modelo entrenado para esas clases. La siguiente acción útil es escoger el dataset definitivo y preparar los datos para el primer entrenamiento.

---
*Fuente principal: README.md y contenido disponible en el workspace. Este plan mantiene el alcance real del proyecto y evita inventar progreso no verificado.*
