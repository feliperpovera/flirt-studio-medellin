"""Genera las páginas de apoyo y el blog a partir de content.py, reutilizando
estilos, header, footer y tracking de index.html para que no se desincronicen.
Uso: python3 tools/build_pages.py   (desde la raíz del repo)"""
import re, json, html, datetime, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import PAGES, POSTS

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://flirtstudiowebcam.com"
TODAY = datetime.date.today().isoformat()
src = (ROOT / "index.html").read_text(encoding="utf-8")

def between(a, b):
    i = src.index(a); return src[i:src.index(b, i) + len(b)]

def absolutize(s):
    s = s.replace('href="#', 'href="/#').replace('src="assets/', 'src="/assets/')
    return s.replace('href="privacy.html"', 'href="/privacy.html"')

head_tracking = src[src.index("<!-- Consent Mode"):src.index("<title>")]
style = between("<style>", "</style>")
header = absolutize(between("<!-- ============ NAV", "</header>"))
footer = absolutize(src[src.index("<!-- ============ FOOTER"):src.index("<script>", src.index('<div class="mobile-cta">'))])

EXTRA_CSS = """<style>
  .page{padding:150px 0 80px}
  .article{max-width:780px;margin:0 auto}
  .article h1{font-size:clamp(2.1rem,4.6vw,3.2rem);margin-bottom:18px}
  .article .lead{font-size:1.15rem;color:var(--muted);margin-bottom:34px}
  .article h2{font-size:1.65rem;margin:44px 0 14px}
  .article h3{font-size:1.2rem;margin:26px 0 8px}
  .article p,.article li{color:#e6d9e4;margin-bottom:14px}
  .article ul,.article ol{padding-left:22px;margin-bottom:18px}
  .article a:not(.btn){color:var(--rose);text-decoration:underline}
  .crumbs{font-size:.85rem;color:var(--muted);margin-bottom:22px}
  .crumbs a{color:var(--muted)!important;text-decoration:none!important}
  .box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:26px 28px;margin:30px 0}
  .box p:last-child{margin-bottom:0}
  .cta-box{text-align:center;background:var(--grad-soft)}
  .cta-box .btn{margin-top:8px}
  .related{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:18px}
  .related a{display:block;background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:18px;text-decoration:none!important;color:var(--text)!important;font-weight:700}
  .related a span{display:block;font-weight:400;color:var(--muted);font-size:.9rem;margin-top:6px}
  .post-list{display:grid;gap:18px}
  .meta{font-size:.85rem;color:var(--muted);margin-bottom:26px}
</style>"""

SCRIPT = """<script>
  const header=document.getElementById('header');
  addEventListener('scroll',()=>header.classList.toggle('scrolled',scrollY>30));
  header.classList.add('scrolled');
  const burger=document.getElementById('burger'),navLinks=document.getElementById('navLinks');
  burger.addEventListener('click',()=>navLinks.classList.toggle('open'));
  (function(){
    const banner=document.getElementById('cookieBanner'); if(!banner)return;
    let decided=false; try{decided=!!localStorage.getItem('flirt_consent');}catch(e){}
    if(!decided) setTimeout(()=>banner.classList.add('show'),1200);
    function decide(v){
      try{localStorage.setItem('flirt_consent',v);}catch(e){}
      if(v==='granted'&&typeof gtag==='function'){gtag('consent','update',{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'});}
      (window.dataLayer=window.dataLayer||[]).push({event:'cookie_consent',consent_state:v});
      banner.classList.remove('show');
    }
    document.getElementById('cookieAccept').addEventListener('click',()=>decide('granted'));
    document.getElementById('cookieReject').addEventListener('click',()=>decide('denied'));
  })();
  document.querySelectorAll('a[href*="wa.me"]').forEach(a=>a.addEventListener('click',()=>{
    (window.dataLayer=window.dataLayer||[]).push({event:'whatsapp_click',contact_method:'whatsapp',
      wa_location:a.dataset.waLocation||a.id||'sin-ubicacion',wa_button_id:a.id||'',link_url:a.href,
      link_text:(a.textContent||'').trim().slice(0,80),page_path:location.pathname});
  }));
</script>"""

WA_ICON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.5 15.3L2 22l4.8-1.5A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-2.9.9.9-2.8-.2-.3A8 8 0 1 1 12 20z"/></svg>'

def cta(msg, loc, label, text):
    url = "https://wa.me/573332268616?text=" + re.sub(r"\s", "%20", html.escape(msg, quote=True)).replace(",", "%2C")
    return (f'<div class="box cta-box"><p>{text}</p>'
            f'<a href="{url}" id="wa-{loc}" class="btn btn-primary wa-click" data-wa-location="{loc}" '
            f'target="_blank" rel="noopener">{WA_ICON} {label}</a></div>')

def page(p, kind):
    url = f"{SITE}/{p['slug']}/"
    crumbs = [("Inicio", "/")]
    if kind == "post": crumbs.append(("Blog", "/blog/"))
    crumbs.append((p["h1"], None))
    crumb_html = " › ".join(f'<a href="{u}">{html.escape(n)}</a>' if u else html.escape(n) for n, u in crumbs)
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (u or f"/{p['slug']}/")}
        for i, (n, u) in enumerate(crumbs)]}]
    if kind == "post":
        ld.append({"@context": "https://schema.org", "@type": "Article", "headline": p["h1"], "description": p["desc"],
                   "datePublished": p.get("date", TODAY), "dateModified": TODAY, "inLanguage": "es-CO",
                   "author": {"@type": "Organization", "name": "Equipo Flirt Studio", "url": SITE + "/"},
                   "publisher": {"@type": "Organization", "name": "Flirt Studio", "logo": SITE + "/assets/logo.png"},
                   "image": SITE + "/assets/" + p.get("img", "promo-2.jpg"), "mainEntityOfPage": url})
    if p.get("faq"):
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
            for q, a in p["faq"]]})
    faq_html = ""
    if p.get("faq"):
        faq_html = "<h2>Preguntas frecuentes</h2>" + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in p["faq"])
    rel = [x for x in PAGES + POSTS if x["slug"] in p.get("related", [])]
    rel_html = ""
    if rel:
        rel_html = '<h2>Sigue leyendo</h2><div class="related">' + "".join(
            f'<a href="/{x["slug"]}/">{html.escape(x["h1"])}<span>{html.escape(x["desc"][:90])}…</span></a>' for x in rel) + "</div>"
    meta = f'<div class="meta">Por el equipo de Flirt Studio · Actualizado {TODAY}</div>' if kind == "post" else ""
    body = p["body"].replace("{CTA}", cta(p["wa_msg"], p["wa_loc"], p.get("cta_label", "Escríbenos por WhatsApp"), p.get("cta_text", "¿Lista para empezar? Te respondemos en menos de 30 minutos.")))
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
{head_tracking}<title>{html.escape(p['title'])}</title>
<meta name="description" content="{html.escape(p['desc'], quote=True)}" />
<link rel="canonical" href="{url}" />
<meta name="theme-color" content="#0c0710" />
<link rel="icon" type="image/png" href="/assets/favicon.png" />
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
<meta property="og:type" content="{'article' if kind == 'post' else 'website'}" />
<meta property="og:site_name" content="Flirt Studio" />
<meta property="og:locale" content="es_CO" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{html.escape(p['title'], quote=True)}" />
<meta property="og:description" content="{html.escape(p['desc'], quote=True)}" />
<meta property="og:image" content="{SITE}/assets/{p.get('img', 'promo-2.jpg')}" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
{style}
{EXTRA_CSS}
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PTP5D5KM" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<div class="bg-scene"></div>
{header}
<main class="page"><div class="wrap"><article class="article">
<div class="crumbs">{crumb_html}</div>
<h1>{p['h1']}</h1>
{meta}<p class="lead">{p['lead']}</p>
{body}
{faq_html}
{rel_html}
</article></div></main>
{footer}
{SCRIPT}
</body>
</html>
"""

def blog_index():
    items = "".join(f'<a href="/{x["slug"]}/">{html.escape(x["h1"])}<span>{html.escape(x["desc"])}</span></a>' for x in POSTS)
    p = {"slug": "blog", "title": "Blog Flirt Studio — Tips y mejores prácticas para modelos webcam",
         "desc": "Tips para modelos webcam: iluminación, cámara, privacidad, rutina e inglés. Guías prácticas del equipo de Flirt Studio, estudio webcam en Medellín.",
         "h1": "Tips y mejores prácticas para modelos webcam",
         "lead": "Guías prácticas del equipo de Flirt Studio para que transmitas con más seguridad, mejor imagen y más constancia.",
         "body": f'<div class="related post-list">{items}</div>{{CTA}}', "wa_msg": "Hola, leí el blog y quiero ser modelo webcam", "wa_loc": "blog-index"}
    return p

def main():
    pages = [(p, "page") for p in PAGES] + [(p, "post") for p in POSTS] + [(blog_index(), "page")]
    for p, kind in pages:
        out = ROOT / p["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(p, kind), encoding="utf-8")
        print("ok", "/" + p["slug"] + "/")
    urls = [("", "1.0"), ("privacy.html", "0.3")] + [(p["slug"] + "/", "0.8" if k == "page" else "0.6") for p, k in pages]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls) + "</urlset>\n", encoding="utf-8")
    print("sitemap:", len(urls), "URLs")

if __name__ == "__main__":
    main()
