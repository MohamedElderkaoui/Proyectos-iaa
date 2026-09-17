AI Course

Capstone Project  
Action Plan

For students (instructor’s review required)

ⓒ2023 SAMSUNG. All rights reserved.

Samsung Electronics Corporate Citizenship Office holds the copyright of
this document.

This document is a literary property protected by copyright law so
reprint and reproduction without permission are prohibited.

To use this document other than the curriculum of Samsung Innovation
Campus, you must receive written consent from copyright holder.

<table>
<colgroup>
<col style="width: 29%" />
<col style="width: 70%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"><blockquote>
<p>Course</p>
</blockquote></th>
<th style="text-align: center;">AI Course</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;"><blockquote>
<p>Team Name</p>
</blockquote></td>
<td style="text-align: left;">AccessAI: AI-Based Urban Accessibility
Detection</td>
</tr>
<tr>
<td style="text-align: left;"><blockquote>
<p>Team Leader/</p>
<p>Members</p>
</blockquote></td>
<td style="text-align: left;"><p>&lt;Team leader&gt; /</p>
<p>&lt;member 1&gt;, &lt;member 2&gt;, …</p></td>
</tr>
<tr>
<td style="text-align: left;"><blockquote>
<p>Project Title</p>
</blockquote></td>
<td style="text-align: left;">AccessAI: AI-Based Urban Accessibility
Detection</td>
</tr>
<tr>
<td style="text-align: left;"><blockquote>
<p>Goal</p>
</blockquote></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td colspan="2" style="text-align: left;"><blockquote>
<p>El objetivo de este proyecto es desarrollar un sistema de
Inteligencia Artificial capaz de detectar elementos relacionados con la
accesibilidad en entornos urbanos y peatonales.</p>
<p>El sistema analizará imágenes de aceras e identificará elementos como
aceras y rampas de acceso, con la posibilidad de ampliar posteriormente
el modelo para detectar obstáculos, escaleras, superficies deterioradas
y otras barreras de accesibilidad.</p>
<p>A largo plazo, las predicciones del modelo podrían utilizarse como
base para desarrollar una aplicación que proporcione información sobre
la accesibilidad urbana y ayude en la navegación de personas con
movilidad reducida.</p>
</blockquote></td>
</tr>
<tr>
<td style="text-align: left;"><blockquote>
<p>Abstract</p>
</blockquote></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td colspan="2" style="text-align: left;"><blockquote>
<p>La accesibilidad urbana es un problema importante para las personas
que utilizan sillas de ruedas, andadores, carritos de bebé o que tienen
movilidad reducida. Una acera puede aparecer como accesible en un mapa
y, sin embargo, presentar barreras como bordillos elevados, ausencia de
rampas, obstáculos o superficies deterioradas.</p>
<p>Este proyecto propone desarrollar un sistema de visión artificial
capaz de analizar automáticamente imágenes de entornos urbanos y
detectar elementos relacionados con la accesibilidad.</p>
<p>Se estudiarán diferentes conjuntos de datos públicos, como Project
Sidewalk, Sidewalk Accessibility y Cityscapes, analizando sus imágenes,
clases, etiquetas y distribución de los datos.</p>
<p>El prototipo inicial se centrará en detectar aceras y rampas de
acceso. Posteriormente, el sistema podrá ampliarse para detectar otros
tipos de barreras y utilizar la información obtenida junto con
coordenadas geográficas para construir un futuro mapa de
accesibilidad.</p>
</blockquote></td>
</tr>
<tr>
<td style="text-align: left;"><blockquote>
<p>Method</p>
</blockquote></td>
<td style="text-align: left;"></td>
</tr>
<tr>
<td colspan="2" style="text-align: left;"><blockquote>
<p>&lt;El proyecto seguirá una metodología basada en aprendizaje
supervisado y visión artificial.</p>
<p>En primer lugar, se analizarán los conjuntos de datos disponibles
teniendo en cuenta el número de imágenes, las clases existentes, la
calidad de las etiquetas, la distribución entre clases y el número de
objetos presentes en las imágenes.</p>
<p>Posteriormente, los datos serán limpiados y divididos en conjuntos de
entrenamiento, validación y prueba.</p>
<p>Se estudiarán dos posibles enfoques:</p>
<p><strong>1. Clasificación de imágenes:</strong> utilización de
MobileNetV2 mediante transfer learning para clasificar imágenes según
diferentes categorías de accesibilidad.</p>
<p><strong>2. Detección de objetos:</strong> utilización de YOLOv8n para
detectar y localizar elementos relacionados con la accesibilidad, como
aceras y rampas.</p>
<p>Para el primer prototipo se priorizará la detección de objetos
mediante YOLOv8n, ya que permite obtener tanto la clase del elemento
detectado como su localización dentro de la imagen.</p>
<p>Cuando sea necesario, se aplicarán técnicas de aumento de datos como
ajustes de brillo y contraste, zoom y recortes controlados para reducir
el sobreajuste.</p>
<p>Para evaluar los modelos se utilizarán métricas adecuadas al
problema. En clasificación se podrán utilizar Accuracy, Balanced
Accuracy, Precision, Recall, F1-score y ROC-AUC. En detección se
utilizarán principalmente Precision, Recall, F1-score y mAP.</p>
<p>También se estudiará el uso de Early Stopping y optimización de
hiperparámetros mediante Optuna.</p>
<p>Finalmente, el modelo entrenado se integrará en un pequeño prototipo
que permitirá introducir una imagen y visualizar los elementos de
accesibilidad detectados.</p>
</blockquote></td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 29%" />
<col style="width: 70%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"><blockquote>
<p>Data</p>
</blockquote></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2"><blockquote>
<p>Se utilizarán principalmente conjuntos de datos públicos relacionados
con la accesibilidad urbana y la visión artificial.</p>
<p>Los principales candidatos serán <strong>Project Sidewalk</strong>,
<strong>Sidewalk Accessibility</strong> y <strong>Cityscapes</strong>.
Se analizarán sus imágenes y anotaciones para determinar cuáles son más
adecuadas para el objetivo del proyecto.</p>
<p>Los datos se descargarán desde las fuentes oficiales o repositorios
públicos correspondientes. Antes del entrenamiento se realizará un
análisis del número de imágenes, clases, distribución de los datos,
calidad de las etiquetas y número de objetos por imagen.</p>
<p>Los datos se dividirán en conjuntos de entrenamiento, validación y
prueba. Cuando sea necesario, se aplicarán técnicas de aumento de datos
para mejorar la capacidad de generalización del modelo.</p>
<p>El modelo utilizará las imágenes y sus etiquetas para aprender a
detectar elementos relacionados con la accesibilidad, principalmente
<strong>aceras y rampas de acceso</strong>, y posteriormente otros
posibles obstáculos.</p>
</blockquote></td>
</tr>
<tr>
<td style="text-align: left;"><blockquote>
<p>Expected<br />
Outcome</p>
</blockquote></td>
<td></td>
</tr>
<tr>
<td colspan="2"><blockquote>
<p>Se espera desarrollar un modelo de visión artificial capaz de
analizar una imagen de una zona peatonal y detectar automáticamente
elementos relacionados con la accesibilidad.</p>
<p>El prototipo deberá mostrar visualmente las detecciones realizadas
por el modelo, indicando el tipo de elemento y su localización dentro de
la imagen.</p>
<p>Como resultado final se espera obtener un prototipo funcional que
demuestre la utilidad de la Inteligencia Artificial para analizar
espacios urbanos y detectar posibles barreras de accesibilidad.</p>
<p>A largo plazo, este sistema podría integrarse con información
geográfica y coordenadas GPS para crear un mapa de accesibilidad urbana.
Esto podría facilitar la identificación de zonas con posibles barreras y
servir como base para futuras herramientas de navegación orientadas a
personas con movilidad reducida.</p>
</blockquote></td>
</tr>
<tr>
<td style="text-align: left;"><blockquote>
<p>Role by<br />
Member</p>
</blockquote></td>
<td></td>
</tr>
<tr>
<td colspan="2"><blockquote>
<p><strong>Miembro 1 — Datos</strong></p>
</blockquote>
<ul>
<li><p>Búsqueda y análisis de datasets.</p></li>
<li><p>Descarga y organización de los datos.</p></li>
<li><p>Limpieza y preparación de las imágenes.</p></li>
<li><p>Análisis de clases y distribución de los datos.</p></li>
</ul>
<blockquote>
<p><strong>Miembro 2 — Machine Learning</strong></p>
</blockquote>
<ul>
<li><p>Preparación del modelo.</p></li>
<li><p>Entrenamiento de MobileNetV2 y/o YOLOv8n.</p></li>
<li><p>Ajuste de hiperparámetros.</p></li>
<li><p>Evaluación mediante las métricas seleccionadas.</p></li>
</ul>
<blockquote>
<p><strong>Miembro 3 — Aplicación</strong></p>
</blockquote>
<ul>
<li><p>Desarrollo del prototipo.</p></li>
<li><p>Integración del modelo entrenado.</p></li>
<li><p>Diseño de la interfaz.</p></li>
<li><p>Visualización de las detecciones.</p></li>
</ul>
<blockquote>
<p><strong>Trabajo conjunto</strong></p>
<p>Todos los miembros participarán en el análisis de resultados,
pruebas, documentación, preparación de la presentación y revisión final
del proyecto.</p>
</blockquote></td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 29%" />
<col style="width: 70%" />
</colgroup>
<thead>
<tr>
<th style="text-align: left;"><blockquote>
<p>Schedule<br />
Summary</p>
</blockquote></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2"><blockquote>
<p>&lt;Provide a summarized schedule.&gt;</p>
<p>&lt;Use the provided WBS workbook for more detailed action
plan.&gt;</p>
</blockquote></td>
</tr>
<tr>
<td style="text-align: left;"><blockquote>
<p>Comment &amp;<br />
Assessment</p>
</blockquote></td>
<td></td>
</tr>
<tr>
<td colspan="2"><blockquote>
<p>&lt;Comment and assessment <strong>by the
instructor.</strong>&gt;</p>
</blockquote></td>
</tr>
</tbody>
</table>
