# AccessAI móvil (PWA)

Esta carpeta contiene la fuente de una PWA móvil para la app Streamlit. La PWA abre Streamlit en un iframe y guarda su URL solo en el almacenamiento local del dispositivo; no guarda imágenes ni resultados. El modelo sigue ejecutándose en el servidor Streamlit, así que la inferencia necesita conexión y una GPU CUDA disponible en ese servidor.

## Desarrollo local

Desde la raíz del repositorio, publica los archivos en la carpeta estática de Streamlit y arranca la app:

```powershell
python mobile_pwa/publish_to_streamlit.py
streamlit run app/streamlit_app.py
```

Abre `http://localhost:8501/app/static/mobile_pwa/index.html`. La URL de Streamlit se rellena con el mismo origen para mantener el shell y la inferencia bajo el mismo host. localhost solo permite el desarrollo en ese equipo.

## Instalación en un móvil

1. Ejecuta Streamlit en un equipo accesible desde el móvil y expón la app completa con HTTPS.
2. Ejecuta `python mobile_pwa/publish_to_streamlit.py` antes de iniciar Streamlit.
3. Abre `https://tu-servidor/app/static/mobile_pwa/index.html` desde el navegador del móvil y elige **Guardar y abrir**. La dirección predeterminada carga Streamlit desde el mismo origen.
4. Instálala desde el menú del navegador. Chrome y Samsung Internet pueden ofrecer la instalación en Android; Safari permite añadirla a la pantalla de inicio en iOS.

El manifiesto y los iconos describen la instalación; el service worker conserva la pantalla de acceso para mostrarla sin conexión. La vista Streamlit y la inferencia no funcionan offline. Los navegadores exigen HTTPS para la instalación web, excepto en `localhost` y `127.0.0.1` para desarrollo.

## Inserción de Streamlit

La PWA añade `?embed=true` a la URL. El modo recomendado sirve la PWA desde `app/static/mobile_pwa` y carga Streamlit desde el mismo origen, por lo que no requiere cambios de CORS o XSRF. Streamlit documenta el iframe para apps públicas de Community Cloud; una instalación propia debe probarse con su proxy HTTPS.

Si alojas la PWA y Streamlit en orígenes distintos, configura Streamlit con el origen real de la PWA en `server.corsAllowedOrigins` y `server.xsrfCookieSameSite = "none"`, manteniendo XSRF habilitado y sirviendo ambos sitios por HTTPS. No uses comodines en la lista CORS ni compartas URLs con credenciales. Consulta la [configuración oficial de Streamlit](https://docs.streamlit.io/develop/api-reference/configuration/config.toml) antes de ajustar el proxy.

La PWA es un envoltorio móvil del Streamlit existente. La interfaz Reflex de cuatro clases se ejecuta por separado desde la raíz con `reflex run`.
