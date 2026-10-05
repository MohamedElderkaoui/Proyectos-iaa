# AccessAI móvil (PWA)

Esta carpeta contiene la fuente de una PWA móvil para la app Streamlit. La PWA abre Streamlit en un iframe y guarda su URL solo en el almacenamiento local del dispositivo; no guarda imágenes ni resultados. El modelo sigue ejecutándose en el servidor Streamlit, así que la inferencia necesita conexión y una GPU CUDA disponible en ese servidor.

## Desarrollo local

Sirve la carpeta PWA y la app Streamlit por separado:

```powershell
python -m http.server 8080 --directory mobile_pwa
streamlit run app/streamlit_app.py
```

Abre `http://localhost:8080` en el mismo equipo y configura `http://localhost:8501` como URL de Streamlit. El modo offline del shell funciona en localhost; la inferencia puede requerir CORS/XSRF para estos dos puertos distintos.

## Instalación en un móvil

1. Ejecuta Streamlit en un equipo accesible desde el móvil.
2. Configura un reverse proxy HTTPS que sirva `mobile_pwa/` en `/mobile_pwa/` y reenvíe el resto de rutas al servidor Streamlit de `localhost:8501`. `Caddyfile.example` muestra esa configuración para un dominio propio.
3. Abre `https://tu-servidor/mobile_pwa/` desde el navegador del móvil y elige **Guardar y abrir**. La dirección predeterminada carga Streamlit desde el mismo origen.
4. Instálala desde el menú del navegador. Chrome y Samsung Internet pueden ofrecer la instalación en Android; Safari permite añadirla a la pantalla de inicio en iOS.

El manifiesto y los iconos describen la instalación; el service worker conserva la pantalla de acceso para mostrarla sin conexión. La vista Streamlit y la inferencia no funcionan offline. Los navegadores exigen HTTPS para la instalación web, excepto en `localhost` y `127.0.0.1` para desarrollo.

## Inserción de Streamlit

La PWA añade `?embed=true` a la URL. Sirve el shell y Streamlit bajo el mismo origen con el reverse proxy para evitar diferencias entre puertos y hosts. Streamlit documenta el iframe para apps públicas de Community Cloud; una instalación propia debe probarse con su proxy HTTPS.

Si alojas la PWA y Streamlit en orígenes distintos, configura Streamlit con el origen real de la PWA en `server.corsAllowedOrigins` y `server.xsrfCookieSameSite = "none"`, manteniendo XSRF habilitado y sirviendo ambos sitios por HTTPS. No uses comodines en la lista CORS ni compartas URLs con credenciales. Consulta la [configuración oficial de Streamlit](https://docs.streamlit.io/develop/api-reference/configuration/config.toml) antes de ajustar el proxy.

La PWA es un envoltorio móvil del Streamlit existente. La interfaz Reflex de cuatro clases se ejecuta por separado desde la raíz con `reflex run`.
