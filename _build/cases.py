#!/usr/bin/env python3
# Génère les études de cas (réalisations marketing). N'affiche que des faits vérifiés :
# chiffres publiés sur le site et dans Notion, descriptions relevées sur les sites en ligne.
import html, os
from urllib.parse import quote

OUT = os.path.expanduser('~/Developer/wanisite-site/realisations')
WA = 'https://wa.me/33624547342?text='

CASES = [
    dict(slug='clean-and-polish', nom='Clean &amp; Polish', nom_txt='Clean & Polish',
         title='Clean & Polish : 108 appels en 6 jours avec Meta Ads — Wanisite',
         desc='Campagne Meta Ads pour un lavage auto : 108 appels en 6 jours, à 1,49 € par appel.',
         h1='108 appels en 6&nbsp;jours pour <em class="it">Clean &amp; Polish</em>',
         lead='Une campagne Meta Ads pensée pour une seule chose : faire sonner le téléphone.',
         chiffres=[('108', 'appels reçus'), ('6 jours', 'de campagne'), ('1,49 €', 'par appel en moyenne')],
         client='Clean &amp; Polish propose du lavage auto et du remplacement de pare-brise à Aulnay-sous-Bois (93).',
         objectif='Recevoir des appels de clients. C\'est une campagne d\'appels, pas une campagne de visibilité : chaque euro sert à faire téléphoner.',
         mise_en_place='Une campagne Meta Ads avec l\'objectif « Appels ». Le clic mène au site de l\'entreprise, que nous avons aussi réalisé, avec le numéro bien visible.',
         image=('cleanpolish', 'Le site derrière la pub', 'Le site de Clean &amp; Polish, vers lequel mène la campagne.'),
         budget='Environ 160 € dépensés, soit 108 appels au coût moyen de 1,49 € par appel (calcul à partir de ces deux chiffres).',
         conclusion='À 1,49 € l\'appel, la campagne a coûté peu et généré 108 contacts directs en moins d\'une semaine.'),
    dict(slug='aesthetic-men', nom='Aesthetic Men', nom_txt='Aesthetic Men',
         title='Aesthetic Men : 51 appels en 9 jours avec Meta Ads — Wanisite',
         desc='Campagne Meta Ads pour Aesthetic Men, mésothérapie capillaire à Paris : 51 appels en 9 jours, à 2,39 € par appel.',
         h1='51 appels en 9&nbsp;jours pour <em class="it">Aesthetic Men</em>',
         lead='Une campagne Meta Ads pour Aesthetic Men, mésothérapie capillaire à Paris.',
         chiffres=[('51', 'appels reçus'), ('9 jours', 'de campagne'), ('2,39 €', 'par appel en moyenne')],
         client='Aesthetic Men propose de la mésothérapie capillaire à Paris 17.',
         objectif='Recevoir des appels de personnes intéressées par le soin.',
         mise_en_place='Une campagne Meta Ads orientée appels. Le clic mène au site de l\'entreprise, que nous avons également réalisé.',
         image=('aestheticmen', 'Le site derrière la pub', 'Le site d\'Aesthetic Men, vers lequel mène la campagne.'),
         budget='Environ 120 € dépensés, soit 51 appels au coût moyen de 2,39 € par appel (calcul à partir de ces deux chiffres).',
         conclusion='Pour un soin spécialisé, 51 personnes ont appelé en neuf jours, à 2,39 € l\'appel.'),
]

def render(c):
    url = f'https://www.wanisitelab.com/realisations/{c["slug"]}'
    msg = f'Bonjour, j\'ai vu l\'étude de cas {c["nom_txt"]} et je voudrais un accompagnement pour mes campagnes.'
    chiffres = ''.join(f'<div class="card" style="text-align:center;"><div style="font-size:clamp(34px,5vw,52px);font-weight:800;letter-spacing:-.03em;color:var(--teal);line-height:1;">{n}</div><p style="margin-top:8px;">{l}</p></div>' for n, l in c['chiffres'])
    blocs = [('Le client', c['client']), ('L\'objectif', c['objectif']), ('Ce qu\'on a mis en place', c['mise_en_place'])]
    texte = ''.join(f'<div class="card"><h3>{t}</h3><p>{p}</p></div>' for t, p in blocs)
    img = ''
    if c['image']:
        f, t, cap = c['image']
        img = f'<section class="alt"><div class="wrap"><p class="eyebrow">Le support</p><h2>{t}.</h2><div class="shots" style="grid-template-columns:minmax(0,640px);"><figure><img src="/assets/realisations/{f}.webp" alt="{cap}" loading="lazy" style="aspect-ratio:16/10;"><figcaption>{cap}</figcaption></figure></div></div></section>'
    budget = f'<section><div class="wrap"><p class="eyebrow">Le budget</p><h2>Ce que ça a coûté.</h2><p class="sec-intro">{c["budget"]}</p></div></section>' if c['budget'] else ''
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
<title>{html.escape(c['title'])}</title>
<meta name="description" content="{html.escape(c['desc'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(c['title'])}">
<meta property="og:description" content="{html.escape(c['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="fr_FR">
<meta property="og:image" content="https://www.wanisitelab.com/assets/img/og-wanisite.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300..800&family=Playfair+Display:ital,wght@1,700&display=swap">
<link rel="stylesheet" href="/assets/service-light.css?v=2">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/"><img src="/assets/img/nav-logo.webp" alt="" width="46" height="30"><span>Wanisite</span></a>
    <nav class="menu" aria-label="Navigation">
      <a class="hide-m" href="/#budget">Toutes les réalisations</a>
      <a class="btn main cta" style="min-height:42px;padding:0 16px;font-size:15px;" href="{WA + quote(msg)}" target="_blank" rel="noopener">Demander un accompagnement</a>
    </nav>
  </div>
</header>
<main>
<section class="hero" style="padding-bottom:40px;">
  <div class="wrap" style="grid-template-columns:1fr;">
    <div>
      <p class="eyebrow">Étude de cas · Meta Ads</p>
      <h1>{c['h1']}</h1>
      <p class="lead">{c['lead']}</p>
    </div>
  </div>
</section>
<section style="padding-top:0;"><div class="wrap"><div class="grid g3" style="margin-top:0;">{chiffres}</div></div></section>
<section class="alt"><div class="wrap"><p class="eyebrow">La campagne</p><h2>Comment ça s'est passé.</h2><div class="grid g3">{texte}</div></div></section>
{img}
{budget}
<section class="alt"><div class="wrap"><p class="eyebrow">En résumé</p><h2>Ce qu'il faut retenir.</h2><p class="sec-intro">{c['conclusion']}</p>
<div class="note">Ce sont les résultats d'une campagne précise, pour une activité précise : ils ne sont pas une promesse pour une autre entreprise.</div></div></section>
<section style="padding-top:0;"><div class="wrap"><div class="final"><h2>Et pour votre activité ?</h2><p>Dites-nous ce que vous vendez et à qui. On vous explique ce qu'une campagne peut raisonnablement apporter, avant de dépenser un euro.</p>
<div class="actions"><a class="btn wa" href="{WA + quote(msg)}" target="_blank" rel="noopener">Demander un accompagnement</a><a class="btn ghost" href="/#budget">Voir les autres réalisations</a></div></div></div></section>
</main>
<footer><div class="wrap"><a href="/" style="text-decoration:none;font-weight:700;color:var(--ink);">Wanisite</a><span>© 2026 · waniscontact7679@gmail.com · +33 6 24 54 73 42</span></div></footer>
</body>
</html>
'''

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for c in CASES:
        with open(f'{OUT}/{c["slug"]}.html', 'w') as f:
            f.write(render(c))
        print('écrit', c['slug'])
