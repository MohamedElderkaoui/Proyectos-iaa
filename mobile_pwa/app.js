const STORAGE_KEY = "accessai.streamlitUrl";
const form = document.querySelector("#connection-form");
const urlInput = document.querySelector("#streamlit-url");
const statusText = document.querySelector("#status");
const appSection = document.querySelector("#app-section");
const frame = document.querySelector("#streamlit-frame");
const openFullLink = document.querySelector("#open-full");
const indicator = document.querySelector("#connection-indicator");
const installButton = document.querySelector("#install-button");
let installPrompt = null;

function parseStreamlitUrl(value) {
  let url;
  try {
    url = new URL(value.trim());
  } catch {
    throw new Error("Escribe una URL completa, incluida https://.");
  }

  if (!["https:", "http:"].includes(url.protocol) || url.username || url.password) {
    throw new Error("Usa una URL HTTP o HTTPS sin credenciales.");
  }

  const isLoopback = ["localhost", "127.0.0.1", "[::1]"].includes(url.hostname);
  if (location.protocol === "https:" && url.protocol !== "https:" && !isLoopback) {
    throw new Error("Una PWA HTTPS solo puede abrir una app Streamlit HTTPS. Configura HTTPS en el servidor.");
  }

  url.hash = "";
  return url;
}

function connect(value, save = true) {
  const url = parseStreamlitUrl(value);
  const embedUrl = new URL(url.href);
  embedUrl.searchParams.set("embed", "true");

  if (save) localStorage.setItem(STORAGE_KEY, url.href);
  urlInput.value = url.href;
  frame.src = embedUrl.href;
  openFullLink.href = url.href;
  appSection.hidden = false;
  openFullLink.hidden = false;
  indicator.textContent = "Conectando…";
  statusText.textContent = "Si la vista no carga, comprueba que el servidor permite iframe y WebSocket desde el origen de esta PWA.";
  frame.addEventListener("load", () => {
    indicator.textContent = "Vista cargada";
  }, { once: true });
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  try {
    connect(urlInput.value);
    statusText.classList.remove("error");
  } catch (error) {
    statusText.textContent = error.message;
    statusText.classList.add("error");
  }
});

document.querySelector("#forget-button").addEventListener("click", () => {
  localStorage.removeItem(STORAGE_KEY);
  frame.removeAttribute("src");
  appSection.hidden = true;
  openFullLink.hidden = true;
  urlInput.value = "";
  statusText.textContent = "Dirección borrada de este dispositivo.";
  statusText.classList.remove("error");
});

window.addEventListener("online", () => {
  statusText.textContent = "Conexión disponible. La inferencia requiere que Streamlit también esté en línea.";
});
window.addEventListener("offline", () => {
  statusText.textContent = "Sin conexión. Solo está disponible esta pantalla; no se pueden ejecutar inferencias.";
  indicator.textContent = "Sin conexión";
});

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  installPrompt = event;
  installButton.hidden = false;
});

installButton.addEventListener("click", async () => {
  if (!installPrompt) return;
  installPrompt.prompt();
  await installPrompt.userChoice;
  installPrompt = null;
  installButton.hidden = true;
});

if ("serviceWorker" in navigator && window.isSecureContext) {
  navigator.serviceWorker.register("./sw.js").catch(() => {
    statusText.textContent = "No se pudo activar el modo offline del shell. La app necesita HTTPS para instalarse.";
  });
}

try {
  const savedUrl = localStorage.getItem(STORAGE_KEY);
  urlInput.value = savedUrl || `${location.origin}/`;
  if (savedUrl) connect(savedUrl, false);
} catch (error) {
  statusText.textContent = error.message;
}
