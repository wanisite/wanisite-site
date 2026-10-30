#!/usr/bin/env python3
"""Publie le blog et met à jour le référencement de tout le site. Se relance sans risque (idempotent).

  python3 _build/publier.py

1. Articles : _blog/articles/AAAA-MM-JJ-slug.md → blog/<slug>.html (un article n'est publié que si sa date est passée).
2. Page de liste blog/index.html et flux blog/rss.xml.
3. sitemap.xml complet, avec dates de mise à jour.
4. Sur chaque page : pied de page avec les liens internes et fil d'Ariane (JSON-LD), entre des marqueurs.
"""
import datetime, html, json, os, re, subprocess, sys
from email.utils import format_datetime
from urllib.parse import quote

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.wanisitelab.com'
WA = 'https://wa.me/33624547342?text='
AUJOURDHUI = datetime.date.today()

SERVICES = [
    ('/services/site-vitrine.html', 'Site vitrine'),
    ('/services/reservation.html', 'Réservation en ligne'),
    ('/services/ecommerce.html', 'Boutique en ligne'),
    ('/services/logiciel-sur-mesure.html', 'Logiciel sur mesure'),
    ('/services/budget-marketing.html', 'Meta Ads et Google Ads'),
    ('/services/sourcing-chine.html', 'Sourcing en Chine'),
]
REALISATIONS = [('/realisations/clean-and-polish', 'Clean & Polish'), ('/realisations/aesthetic-men', 'Aesthetic Men')]


def lire(chemin):
    with open(os.path.join(RACINE, chemin), encoding='utf-8') as f:
        return f.read()


def ecrire(chemin, texte):
    chemin = os.path.join(RACINE, chemin)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    ancien = open(chemin, encoding='utf-8').read() if os.path.exists(chemin) else None
    if ancien != texte:
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(texte)
        print('écrit', os.path.relpath(chemin, RACINE))


def date_git(chemin):
    """Date du dernier commit qui a touché le fichier (sinon aujourd'hui)."""
    try:
        d = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', chemin], cwd=RACINE, capture_output=True, text=True).stdout.strip()
        return d or AUJOURDHUI.isoformat()
    except Exception:
        return AUJOURDHUI.isoformat()


# ---------------------------------------------------------------- Markdown minimal
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\w)', r'<em>\1</em>', t)

    def lien(m):
        texte, url = m.group(1), m.group(2)
        ext = url.startswith('http') and 'wanisitelab.com' not in url
        return f'<a href="{url}"' + (' target="_blank" rel="noopener"' if ext else '') + f'>{texte}</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lien, t)


def markdown(md):
    sortie, para, liste = [], [], None

    def fermer():
        nonlocal para, liste
        if para:
            sortie.append('<p>' + inline(' '.join(para)) + '</p>'); para = []
        if liste:
            balise, items = liste
            sortie.append(f'<{balise}>' + ''.join(f'<li>{inline(i)}</li>' for i in items) + f'</{balise}>'); liste = None

    for ligne in md.splitlines():
        l = ligne.strip()
        if not l:
            fermer(); continue
        m = re.match(r'^(#{2,3})\s+(.*)$', l)
        if m:
            fermer()
            n = len(m.group(1))
            ident = re.sub(r'[^a-z0-9]+', '-', m.group(2).lower().translate(str.maketrans('àâäéèêëîïôöùûüç', 'aaaeeeeiioouuuc'))).strip('-')
            sortie.append(f'<h{n} id="{ident}">{inline(m.group(2))}</h{n}>'); continue
        m = re.match(r'^(?:[-*]|(\d+)\.)\s+(.*)$', l)
        if m:
            balise = 'ol' if m.group(1) else 'ul'
            if para:
                fermer()
            if not liste or liste[0] != balise:
                fermer(); liste = (balise, [])
            liste[1].append(m.group(2)); continue
        if l.startswith('>'):
            fermer(); sortie.append('<blockquote>' + inline(l.lstrip('> ')) + '</blockquote>'); continue
        if liste:
            fermer()
        para.append(l)
    fermer()
    return '\n'.join(sortie)


def lire_article(nom):
    brut = lire(os.path.join('_blog', 'articles', nom))
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', brut, re.S)
    if not m:
        sys.exit(f'{nom} : en-tête --- manquant')
    meta = {}
    for l in m.group(1).splitlines():
        if ':' in l:
            k, v = l.split(':', 1); meta[k.strip()] = v.strip()
    for k in ('titre', 'description', 'date', 'slug'):
        if not meta.get(k):
            sys.exit(f'{nom} : champ « {k} » manquant')
    meta['corps'] = m.group(2)
    meta['date_obj'] = datetime.date.fromisoformat(meta['date'])
    return meta


# ---------------------------------------------------------------- gabarits
def pied_liens():
    s = ''.join(f'<a href="{u}">{html.escape(n)}</a>' for u, n in SERVICES)
    return ('<!--pied-liens--><nav class="pied-liens" aria-label="Liens du site" style="width:min(1120px,100% - 40px);margin:18px auto 0;padding:16px 0 4px;'
            'border-top:1px solid rgba(127,140,150,.25);display:flex;flex-wrap:wrap;gap:8px 18px;font-size:14px;">'
            f'<a href="/">Accueil</a>{s}<a href="/blog/">Blog</a><a href="/#realisations">Réalisations</a></nav>'
            '<style>.pied-liens a{color:inherit;opacity:.75;text-decoration:none;}.pied-liens a:hover{opacity:1;text-decoration:underline;}</style><!--/pied-liens-->')


def ariane(elements):
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": SITE + u} for i, (u, n) in enumerate(elements, 1)]}
    return '<!--ariane--><script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script><!--/ariane-->'


def remplacer_bloc(s, nom, bloc, ancre_avant):
    """Remplace le bloc <!--nom-->…<!--/nom--> ou l'insère juste avant `ancre_avant` (première occurrence)."""
    motif = re.compile(rf'<!--{nom}-->.*?<!--/{nom}-->', re.S)
    if motif.search(s):
        return motif.sub(lambda _: bloc, s, count=1)
    i = s.find(ancre_avant)
    if i < 0:
        sys.exit(f'ancre « {ancre_avant} » introuvable pour {nom}')
    return s[:i] + bloc + s[i:]


GABARIT = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
<title>{titre_page}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{titre_og}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Wanisite">
<meta property="og:image" content="https://www.wanisitelab.com/assets/img/og-wanisite.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://www.wanisitelab.com/assets/img/og-wanisite.jpg">
<link rel="alternate" type="application/rss+xml" title="Blog Wanisite" href="/blog/rss.xml">
<link rel="icon" type="image/png" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300..900&family=JetBrains+Mono:wght@400..700&family=Playfair+Display:ital,wght@1,700&display=swap">
{jsonld}
<link rel="stylesheet" href="/assets/service-da.css?v=8">
<style>
  .blog{{padding:40px 0 80px;}}
  .blog .wrap{{width:min(760px,100% - 40px);}}
  .fil{{font-family:var(--mono);font-size:12px;letter-spacing:.06em;color:var(--muted);margin:0 0 22px;}}
  .fil a{{color:inherit;}}
  .blog h1{{font-size:clamp(32px,5vw,50px);line-height:1.12;letter-spacing:-.035em;margin:0;}}
  .chapeau{{font-size:clamp(18px,2.2vw,21px);color:var(--muted);margin:18px 0 0;line-height:1.55;}}
  .meta-art{{font-family:var(--mono);font-size:12px;color:var(--muted);margin:18px 0 0;padding-bottom:22px;border-bottom:1px solid var(--line);}}
  .corps{{font-size:18px;line-height:1.75;color:var(--ink);}}
  .corps h2{{font-size:clamp(24px,3vw,30px);margin:46px 0 12px;letter-spacing:-.025em;line-height:1.2;max-width:none;}}
  .corps h3{{font-size:21px;margin:30px 0 8px;}}
  .corps p{{margin:0 0 18px;}}
  .corps ul,.corps ol{{margin:0 0 20px;padding-left:22px;}} .corps li{{margin:6px 0;}}
  .corps a{{color:var(--teal);font-weight:600;}}
  .corps strong{{color:var(--ink);}}
  .corps blockquote{{margin:24px 0;padding:14px 18px;border-left:3px solid var(--teal);background:rgba(0,201,201,.06);color:var(--ink);}}
  .encart{{margin:44px 0 0;padding:26px;border:1px solid rgba(0,201,201,.3);border-radius:16px;background:linear-gradient(160deg,#e6fafa,#f4fbfb 60%,#ffffff);}}
  .encart h2{{margin:0;font-size:24px;max-width:none;}} .encart p{{color:var(--muted);margin:10px 0 0;}}
  .encart .actions{{margin-top:18px;}}
  .liste-blog{{list-style:none;margin:34px 0 0;padding:0;border-top:2px solid var(--ink);}}
  .liste-blog li{{padding:22px 0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:120px minmax(0,1fr);gap:4px 22px;}}
  .liste-blog time{{font-family:var(--mono);font-size:12px;color:var(--muted);padding-top:6px;}}
  .liste-blog a{{font-size:22px;font-weight:800;letter-spacing:-.02em;color:var(--ink);text-decoration:none;line-height:1.25;}}
  .liste-blog a:hover{{color:var(--teal);}}
  .liste-blog p{{grid-column:2;margin:4px 0 0;color:var(--muted);font-size:16px;}}
  @media (max-width:620px){{.liste-blog li{{grid-template-columns:1fr;}} .liste-blog p{{grid-column:1;}} .corps{{font-size:17px;}}}}
</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/"><img src="/assets/img/nav-logo.webp" alt="" width="46" height="30"><span>Wanisite</span></a>
    <nav class="menu" aria-label="Navigation">
      <a class="hide-m" href="/blog/">Blog</a>
      <a class="hide-m" href="/#realisations">Réalisations</a>
      <a class="btn main cta" style="min-height:42px;padding:0 16px;font-size:15px;" href="{wa}" target="_blank" rel="noopener">Demander un devis</a>
    </nav>
  </div>
</header>
<main class="blog"><div class="wrap">
{contenu}
</div></main>
<footer>
  <div class="wrap">
    <a href="/" style="text-decoration:none;font-weight:700;color:var(--ink);">Wanisite</a>
    <span>© 2026 · waniscontact7679@gmail.com · +33 6 24 54 73 42</span>
  </div>
{pied}</footer>
</body>
</html>
'''

ORGA = {"@type": "Organization", "name": "Wanisite", "url": SITE, "logo": SITE + "/assets/img/apple-touch-icon.png"}


def page_article(a):
    url = f"{SITE}/blog/{a['slug']}.html"
    service = a.get('service', '')
    lien_service, nom_service = (service.split('|', 1) + [''])[:2] if '|' in service else ('', '')
    encart = ''
    if lien_service.strip():
        encart = (f'<aside class="encart"><h2>{html.escape(nom_service.strip())}</h2>'
                  f'<p>Wanisite s’en occupe pour vous : devis gratuit, prix fixe annoncé avant de commencer.</p>'
                  f'<div class="actions"><a class="btn main" href="{lien_service.strip()}">Voir le service</a>'
                  f'<a class="btn ghost" href="{WA}{quote("Bonjour, j’ai lu votre article : " + a["titre"])}" target="_blank" rel="noopener">En parler sur WhatsApp</a></div></aside>')
    jsonld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a['titre'], "description": a['description'],
              "datePublished": a['date'], "dateModified": a.get('maj', a['date']), "inLanguage": "fr-FR",
              "mainEntityOfPage": url, "image": SITE + "/assets/img/og-wanisite.jpg", "author": ORGA, "publisher": ORGA}
    if a.get('mots_cles'):
        jsonld["keywords"] = a['mots_cles']
    contenu = (f'<p class="fil"><a href="/">Accueil</a> / <a href="/blog/">Blog</a></p>'
               f'<article><h1>{html.escape(a["titre"])}</h1><p class="chapeau">{html.escape(a["description"])}</p>'
               f'<p class="meta-art">Publié le <time datetime="{a["date"]}">{date_fr(a["date_obj"])}</time> · Wanisite · {temps_lecture(a["corps"])} min de lecture</p>'
               f'<div class="corps">{markdown(a["corps"])}</div>{encart}</article>')
    return GABARIT.format(titre_page=html.escape(a['titre'] + ' — Wanisite'), titre_og=html.escape(a['titre']), description=html.escape(a['description']),
                          url=url, og_type='article', wa=WA + 'Bonjour%2C%20je%20voudrais%20un%20devis.',
                          jsonld='<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>\n' +
                          ariane([('/', 'Accueil'), ('/blog/', 'Blog'), (f"/blog/{a['slug']}.html", a['titre'])]), contenu=contenu, pied=pied_liens())


MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
def date_fr(d): return f'{d.day} {MOIS[d.month - 1]} {d.year}'
def temps_lecture(md): return max(1, round(len(re.findall(r'\w+', md)) / 220))


def page_liste(articles):
    items = ''.join(f'<li><time datetime="{a["date"]}">{date_fr(a["date_obj"])}</time><a href="/blog/{a["slug"]}.html">{html.escape(a["titre"])}</a>'
                    f'<p>{html.escape(a["description"])}</p></li>' for a in articles)
    contenu = ('<p class="fil"><a href="/">Accueil</a> / Blog</p><h1>Le blog Wanisite</h1>'
               '<p class="chapeau">Sites internet, réservation, e-commerce, publicité et sourcing en Chine : des conseils concrets pour les commerces et les indépendants.</p>'
               + (f'<ol class="liste-blog">{items}</ol>' if items else '<p class="meta-art">Premier article bientôt en ligne.</p>'))
    jsonld = {"@context": "https://schema.org", "@type": "Blog", "name": "Le blog Wanisite", "url": SITE + "/blog/", "inLanguage": "fr-FR", "publisher": ORGA,
              "blogPost": [{"@type": "BlogPosting", "headline": a['titre'], "url": f"{SITE}/blog/{a['slug']}.html", "datePublished": a['date']} for a in articles[:20]]}
    return GABARIT.format(titre_page='Blog Wanisite : site internet, e-commerce, publicité et sourcing', titre_og='Le blog Wanisite',
                          description='Conseils concrets pour les commerces et les indépendants : site internet, réservation en ligne, boutique, publicité Meta et sourcing en Chine.',
                          url=SITE + '/blog/', og_type='website', wa=WA + 'Bonjour%2C%20je%20voudrais%20un%20devis.',
                          jsonld='<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>\n' + ariane([('/', 'Accueil'), ('/blog/', 'Blog')]),
                          contenu=contenu, pied=pied_liens())


def rss(articles):
    items = ''.join(f'''  <item><title>{html.escape(a["titre"])}</title><link>{SITE}/blog/{a["slug"]}.html</link><guid>{SITE}/blog/{a["slug"]}.html</guid>
    <pubDate>{format_datetime(datetime.datetime.combine(a["date_obj"], datetime.time(8), datetime.timezone.utc))}</pubDate><description>{html.escape(a["description"])}</description></item>
''' for a in articles[:30])
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>Le blog Wanisite</title><link>{SITE}/blog/</link><language>fr-FR</language>
  <description>Conseils concrets pour les commerces et les indépendants.</description>
{items}</channel></rss>
'''


def sitemap(articles):
    pages = [('/', 'index.html', '1.0', 'weekly')] + [(u, u.lstrip('/'), '0.8', 'monthly') for u, _ in SERVICES] \
        + [(u, u.lstrip('/') + '.html', '0.7', 'monthly') for u, _ in REALISATIONS] + [('/blog/', 'blog/index.html', '0.7', 'weekly')]
    lignes = [f'  <url><loc>{SITE}{u}</loc><lastmod>{date_git(f)}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>' for u, f, p, c in pages]
    lignes += [f'  <url><loc>{SITE}/blog/{a["slug"]}.html</loc><lastmod>{a.get("maj", a["date"])}</lastmod><changefreq>yearly</changefreq><priority>0.6</priority></url>' for a in articles]
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(lignes) + '\n</urlset>\n'


def referencer_pages():
    """Pied de page avec liens internes + fil d'Ariane sur les pages services et réalisations ; lien Blog sur l'accueil."""
    for u, nom in SERVICES:
        f = u.lstrip('/')
        s = lire(f)
        s = remplacer_bloc(s, 'pied-liens', pied_liens(), '</footer>')
        s = remplacer_bloc(s, 'ariane', ariane([('/', 'Accueil'), (u, nom)]), '</head>')
        ecrire(f, s)
    for u, nom in REALISATIONS:
        f = u.lstrip('/') + '.html'
        s = lire(f)
        s = remplacer_bloc(s, 'pied-liens', pied_liens(), '</footer>')
        s = remplacer_bloc(s, 'ariane', ariane([('/', 'Accueil'), ('/#realisations', 'Réalisations'), (u, nom)]), '</head>')
        ecrire(f, s)
    s = lire('index.html')
    s = remplacer_bloc(s, 'pied-liens', pied_liens(), '</footer>')
    ecrire('index.html', s)


def main():
    dossier = os.path.join(RACINE, '_blog', 'articles')
    tous = [lire_article(n) for n in sorted(os.listdir(dossier)) if n.endswith('.md')] if os.path.isdir(dossier) else []
    publies = sorted([a for a in tous if a['date_obj'] <= AUJOURDHUI], key=lambda a: a['date'], reverse=True)
    slugs = [a['slug'] for a in tous]
    if len(slugs) != len(set(slugs)):
        sys.exit('deux articles ont le même slug')
    for a in publies:
        ecrire(f"blog/{a['slug']}.html", page_article(a))
    ecrire('blog/index.html', page_liste(publies))
    ecrire('blog/rss.xml', rss(publies))
    referencer_pages()
    ecrire('sitemap.xml', sitemap(publies))
    print(f'{len(publies)} article(s) publié(s), {len(tous) - len(publies)} programmé(s) plus tard')


if __name__ == '__main__':
    main()
