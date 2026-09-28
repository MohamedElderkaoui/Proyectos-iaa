# Informe de resultados — AccessAI

**Fecha de revisión:** 28 de septiembre de 2026  
**Proyecto:** AccessAI — prototipo de detección urbana  
**Alcance:** resultados experimentales disponibles en el repositorio; no constituye una validación de accesibilidad urbana.

## 1. Resumen ejecutivo

El repositorio conserva dos entrenamientos de YOLO26n sobre una versión filtrada del ROD-Dataset, con cuatro categorías agregadas. El entrenamiento más completo registró 35 épocas. En su mejor época de validación (época 34) obtuvo precisión **0,9085**, recall **0,8235**, mAP50 **0,91084** y mAP50-95 **0,71459**.

Estas cifras describen el rendimiento sobre la partición de validación del experimento. No se encontraron métricas guardadas de la partición de prueba. Además, las categorías evaluadas no son las clases específicas `sidewalk` y `curbramp`; por tanto, estos resultados no demuestran que el sistema detecte aceras o rampas ni que pueda determinar si un espacio es accesible.

## 2. Datos y clases

El experimento usa `DATA/ROD-Dataset/dataset`, con imágenes y etiquetas organizadas en tres particiones:

| Partición | Imágenes | Etiquetas |
|---|---:|---:|
| Entrenamiento (`train`) | 19.186 | 19.186 |
| Validación (`valid`) | 3.511 | 3.511 |
| Prueba (`test`) | 1.629 | 1.629 |
| **Total** | **24.326** | **24.326** |

El cuaderno transforma las 25 clases originales del dataset en estas cuatro categorías de experimento y excluye `Building`:

1. `Obstaculo_Dinamico`
2. `Obstaculo_Fijo`
3. `Barrera_Arquitectonica`
4. `Infraestructura_Peatonal`

Las cantidades siguientes son **instancias anotadas**, no número de imágenes por clase:

| Categoría | Train | Validación | Test | Total |
|---|---:|---:|---:|---:|
| Obstáculo dinámico | 15.411 | 2.587 | 781 | 18.779 |
| Obstáculo fijo | 10.614 | 1.552 | 846 | 13.012 |
| Barrera arquitectónica | 1.125 | 339 | 223 | 1.687 |
| Infraestructura peatonal | 4.215 | 993 | 468 | 5.676 |
| **Total de instancias** | **31.365** | **5.471** | **2.318** | **39.154** |

La distribución está desequilibrada: `Barrera_Arquitectonica` tiene muchas menos instancias que las demás categorías. Esto debe tenerse en cuenta al interpretar las métricas agregadas y al planificar la evaluación por clase.

## 3. Configuración registrada

Los dos archivos de configuración (`args.yaml`) registran, entre otros, estos parámetros:

- Modelo de partida: `yolo26n.pt`, con pesos preentrenados.
- Dataset: `data_filtrado.yaml`.
- Tamaño de imagen: 640 píxeles.
- Optimizador: AdamW.
- Semilla: 42; entrenamiento determinista activado.
- Aumento de datos: activado.
- Validación durante el entrenamiento: activada (`val=true`).
- Entrenamiento planificado: 35 épocas, paciencia 8 y AutoBatch (`batch=-1`).

## 4. Resultados disponibles

Las métricas proceden de `results.csv` y corresponden a la **validación**, no al conjunto de prueba. En cada fila se muestran las métricas de la época con mayor mAP50-95 del entrenamiento correspondiente.

| Entrenamiento | Épocas registradas | Mejor época | Precisión | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|---:|
| `yolo26n_4clases` | 16 | 16 | 0,86410 | 0,79205 | 0,87555 | 0,65951 |
| `yolo26n_4clases-2` | 35 | 34 | 0,90850 | 0,82350 | 0,91084 | 0,71459 |

En la última fila del segundo entrenamiento (época 35), las métricas fueron precisión 0,90194, recall 0,82774, mAP50 0,91125 y mAP50-95 0,71425. La selección de la época 34 en la tabla usa el mayor mAP50-95 registrado. El primer CSV contiene 16 épocas, aunque su configuración solicita 35; los artefactos disponibles no indican por qué terminó con 16.

El CSV no registra una métrica F1. El directorio del segundo entrenamiento sí conserva matrices de confusión y una gráfica de resultados, pero este informe no atribuye causas a errores por clase a partir de esos gráficos.

## 5. Ejecución reciente sin métricas

También hay una configuración de entrenamiento para `yolo26x` en `runs/AccessAI_Proto3_2026-09-28_13-24-23/yolo26x_4clases/args.yaml`. Está configurada para CPU y con `val=false`. En los artefactos disponibles al revisar el repositorio no aparecen para esa ejecución un `results.csv` ni pesos del modelo. Por ese motivo no se incluyen métricas de YOLO26x ni se considera una evaluación concluida.

## 6. Interpretación y limitaciones

- Los resultados de YOLO26n son una línea base experimental sobre categorías agrupadas del ROD-Dataset.
- La evaluación cuantitativa guardada es sobre `valid`; no hay resultados documentados sobre `test`.
- El esquema no contiene las clases objetivo `sidewalk` y `curbramp`. Una detección de infraestructura peatonal no equivale a localizar una acera o una rampa con etiquetas específicas.
- Las métricas agregadas no informan por sí solas del rendimiento de cada clase ni de la calidad de un itinerario peatonal.
- No se validó en este informe la integración de `best.pt` con la demo principal, ni se midió el rendimiento con imágenes urbanas externas al dataset.
- No hay coordenadas geográficas asociadas a las detecciones.

Por lo tanto, AccessAI sigue siendo un **prototipo**. Las detecciones no deben presentarse como prueba de accesibilidad o inaccesibilidad.

## 7. Próximos pasos recomendados

1. Evaluar el `best.pt` de `yolo26n_4clases-2` en el split `test` y guardar los parámetros y resultados de esa evaluación.
2. Informar precisión, recall, F1 y mAP por clase, junto con una revisión de falsos positivos y falsos negativos.
3. Revisar la representación de la clase minoritaria `Barrera_Arquitectonica` y la distribución de datos antes de extraer conclusiones comparativas.
4. Si el objetivo sigue siendo detectar aceras y rampas, seleccionar y documentar datos con esas anotaciones específicas, fijar el esquema de clases y volver a entrenar y evaluar sin mezclar los conjuntos.
5. Actualizar README y PLAN para reflejar los experimentos y distinguir el modelo experimental de la demo que describen actualmente.

## 8. Artefactos consultados

- `README.md` y `PLAN.md`.
- `AccessAI_2rd_Prototipo_Deteccion_Urbana1.ipynb` (incluye el mapeo, los recuentos y el flujo de evaluación previsto).
- `DATA/ROD-Dataset/dataset/data_filtrado.yaml`.
- `AccessAI_Proto3/yolo26n_4clases/args.yaml` y `results.csv`.
- `AccessAI_Proto3/yolo26n_4clases-2/args.yaml` y `results.csv`.
- `runs/AccessAI_Proto3_2026-09-28_13-24-23/yolo26x_4clases/args.yaml`.

El README y el PLAN aún describen el prototipo inicial con un modelo genérico y sin métricas. Este informe resume los artefactos experimentales adicionales presentes en el checkout revisado; no afirma que esos pesos estén integrados en la demo principal.
