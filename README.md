# Flirt Studio — Modelaje Digital en Medellín

Sitio web estático de **Flirt Studio** (Medellín). Una sola página con galería de
habitaciones, videos, filosofía del equipo, beneficios y contacto por WhatsApp.

## 🌐 Sitio en vivo

**https://flirtstudiowebcam.com/**

## 📁 Estructura

```
.
├── index.html      # Sitio completo (HTML + CSS + JS en un solo archivo)
├── privacy.html    # Política de privacidad
├── assets/         # Imágenes, logo, favicon y videos
├── .nojekyll       # Sirve los archivos tal cual en GitHub Pages
└── README.md
```

## ✨ Características

- **100% estático** — sin frameworks ni paso de compilación. Funciona en cualquier
  hosting estático.
- **Optimizado para móvil** — menú hamburguesa, barra fija inferior con CTA de
  WhatsApp, botones a todo el ancho sin recortes.
- **Rendimiento** — videos recomprimidos, imágenes con carga diferida (`lazy`),
  posters en los videos y `preload="none"` para que solo se descarguen al reproducir.
- **Consentimiento de cookies** — banner con Google Consent Mode v2 (todo denegado
  por defecto hasta que la persona acepte) + Google Tag Manager.
- **SEO y redes sociales** — metadatos Open Graph / Twitter, JSON-LD `LocalBusiness`,
  canonical y favicon.

## 🎬 Peso de los videos

Los videos originales pesaban **118 MB**. Se recomprimieron a 540p/720p H.264
(compatible con todos los navegadores) quedando en ~53 MB:

| Video               | Antes | Ahora | Uso                        |
|---------------------|-------|-------|----------------------------|
| `instructional.mp4` | 69 MB | 34 MB | Clic para reproducir       |
| `promo.mp4`         | 49 MB | 17 MB | Clic para reproducir       |
| `dance.mp4`         | 2 MB  | 2 MB  | Fondo del CTA (autoplay)   |

> Los dos primeros usan `preload="none"`, así que **no se descargan** hasta que la
> visitante los reproduce. Solo el de 2 MB carga automáticamente.

## 🛠️ Editar contenido

- **WhatsApp:** número `573332268616` en todos los botones.
- **Redes:** Instagram y TikTok en el footer.
- **`canonical` / `og:url` / JSON-LD:** apuntan a la URL de GitHub Pages. Si se
  compra un dominio propio, hay que actualizarlos.
- **Google Tag Manager:** contenedor `GTM-PTP5D5KM`.

## 🚀 Vista previa local

```bash
python3 -m http.server 4199
```

Luego abrir http://localhost:4199

---

© Flirt Studio · Medellín, Colombia
