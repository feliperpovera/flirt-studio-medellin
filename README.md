# Flirt Studio Medellín — Landing Page

Landing page estática para **Flirt Studio Medellín** (estudio webcam). Página de una sola
vista, optimizada para móvil y rendimiento, lista para enviar al cliente.

## 🌐 Sitio en vivo

Una vez publicada en GitHub Pages estará disponible en:

> `https://<usuario>.github.io/<repositorio>/`

(La URL exacta aparece en **Settings → Pages** del repositorio.)

## 📁 Estructura

```
.
├── index.html          # Sitio completo (HTML + CSS + JS en un solo archivo)
├── assets/
│   ├── flirt-logo.png  # Logo (optimizado: 2.2 MB → 140 KB)
│   ├── favicon.png     # Ícono del navegador
│   ├── chaturbate.png  # Logos de plataformas
│   ├── livejasmin.jpeg
│   └── camsoda.png
├── .nojekyll           # Sirve los archivos tal cual en GitHub Pages
└── README.md
```

## ✨ Características

- **100% estática y autocontenida** — sin frameworks, sin paso de compilación.
  Funciona abriendo `index.html` o en cualquier hosting estático.
- **Optimizada para móvil** — menú desplegable, CTAs a pantalla completa, sin
  desbordamientos, objetivos táctiles ≥ 44 px.
- **Rendimiento** — logo optimizado, imágenes con dimensiones explícitas y carga
  diferida, fuentes con `display=swap`, animaciones respetuosas con
  `prefers-reduced-motion`.
- **Navegación** — barra de navegación en escritorio con resaltado de la sección
  activa, menú overlay en móvil, scroll suave con compensación del header fijo.
- **SEO y redes sociales** — metadatos Open Graph / Twitter, `lang="es"`, favicon.

## 🛠️ Editar contenido

Todo el contenido vive en `index.html`. Puntos clave a personalizar:

- **WhatsApp:** se usa el número `573332268616` en todos los botones. Búscalo y
  reemplázalo si cambia.
- **Redes sociales:** enlaces de TikTok, Instagram y X en el footer.
- **`<link rel="canonical">` y `og:url`:** actualmente apuntan a un dominio de
  ejemplo. Reemplázalos por la URL final (Pages o dominio propio).
- **Fotos:** las secciones con `[ FOTO ]` son marcadores de posición listos para
  reemplazar por fotografía editorial real.

## 🚀 Vista previa local

```bash
python3 -m http.server 4173
# abrir http://localhost:4173
```

---

© 2026 Flirt Studio · Medellín, Colombia
