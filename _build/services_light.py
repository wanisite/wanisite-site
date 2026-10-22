#!/usr/bin/env python3
# Génère les pages de services au design clair (site vitrine, e-commerce, réservation).
import json, html, os

OUT = os.path.expanduser('~/Developer/wanisite-site/services')
WA = 'https://wa.me/33624547342?text='
def wa(msg):
    from urllib.parse import quote
    return WA + quote(msg)

def page(slug, title, desc, svc_name, quote_msg, project_msg, hero, body, faq):
    ld_faq = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False)
    ld_svc = json.dumps({"@context": "https://schema.org", "@type": "Service", "serviceType": svc_name,
        "provider": {"@type": "Organization", "name": "Wanisite", "url": "https://www.wanisitelab.com"},
        "areaServed": "FR", "description": desc}, ensure_ascii=False)
    url = f'https://www.wanisitelab.com/services/{slug}.html'
    faq_html = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in faq)
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="fr_FR">
<meta property="og:image" content="https://www.wanisitelab.com/assets/img/og-wanisite.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://www.wanisitelab.com/assets/img/og-wanisite.jpg">
<link rel="icon" type="image/png" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@300..800&family=Playfair+Display:ital,wght@1,700&display=swap">
<script type="application/ld+json">{ld_svc}</script>
<script type="application/ld+json">{ld_faq}</script>
<link rel="stylesheet" href="/assets/service-light.css?v=2">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/"><img src="/assets/img/nav-logo.webp" alt="" width="46" height="30"><span>Wanisite</span></a>
    <nav class="menu" aria-label="Navigation">
      <a class="hide-m" href="/#realisations">Réalisations</a>
      <a class="hide-m" href="#exemples">Exemples</a>
      <a class="hide-m" href="#faq">Questions</a>
      <a class="btn main cta" style="min-height:42px;padding:0 16px;font-size:15px;" href="{wa(quote_msg)}" target="_blank" rel="noopener">Demander un devis</a>
    </nav>
  </div>
</header>
<main id="top">
{hero}
{body}
<section id="faq">
  <div class="wrap" style="max-width:820px;">
    <p class="eyebrow">Questions fréquentes</p>
    <h2>Ce que l'on nous demande souvent.</h2>
    {faq_html}
  </div>
</section>
<section style="padding-top:0;">
  <div class="wrap">
    <div class="final">
      <h2>Parlons de votre projet.</h2>
      <p>Décrivez-nous votre activité en quelques mots. On revient vers vous avec des idées concrètes et un devis gratuit.</p>
      <div class="actions">
        <a class="btn wa" href="{wa(project_msg)}" target="_blank" rel="noopener">Demander un devis</a>
        <a class="btn ghost" href="/#rdv">Prendre rendez-vous</a>
        <a class="btn ghost" href="/#realisations">Voir les réalisations</a>
      </div>
    </div>
  </div>
</section>
</main>
<footer>
  <div class="wrap">
    <a href="/" style="text-decoration:none;font-weight:700;color:var(--ink);">Wanisite</a>
    <span>© 2026 · waniscontact7679@gmail.com · +33 6 24 54 73 42</span>
  </div>
</footer>
</body>
</html>
'''

def hero(eyebrow, h1, lead, cta1, cta2, visual, note, quote_msg):
    return f'''<section class="hero">
  <div class="wrap">
    <div>
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="actions">
        <a class="btn main" href="{cta1[1]}">{cta1[0]}</a>
        <a class="btn ghost" href="{wa(quote_msg)}" target="_blank" rel="noopener">{cta2}</a>
      </div>
      <small>Devis gratuit · prix fixe annoncé avant de commencer</small>
    </div>
    <figure style="margin:0;">{visual}<figcaption class="cap"><b>Maquette</b> · {note}</figcaption></figure>
  </div>
</section>'''

def sec(eyebrow, h2, inner, alt=False, intro=None, sid=None):
    i = f'<p class="sec-intro">{intro}</p>' if intro else ''
    return f'''<section{' class="alt"' if alt else ''}{f' id="{sid}"' if sid else ''}>
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h2>{h2}</h2>
    {i}
    {inner}
  </div>
</section>'''

def cards(items, cols=3):
    return f'<div class="grid g{cols}">' + ''.join(f'<div class="card"><h3>{t}</h3><p>{p}</p></div>' for t, p in items) + '</div>'

def flow(steps):
    return '<ol class="flow">' + ''.join(f'<li>{s}</li>' for s in steps) + '</ol>'

def compare(bad_t, bad, good_t, good):
    li = lambda xs: ''.join(f'<li>{x}</li>' for x in xs)
    return f'<div class="compare"><div class="card bad"><h3>{bad_t}</h3><ul>{li(bad)}</ul></div><div class="card good"><h3>{good_t}</h3><ul>{li(good)}</ul></div></div>'

def mock(title, inner, label):
    return f'<div class="mock" role="img" aria-label="{html.escape(label)}"><div class="bar"><i></i><i></i><i></i><b>{html.escape(title)}</b></div><div class="body">{inner}</div></div>'

def price_block(text):
    return f'<div class="price"><div><h3>Prix fixe, annoncé avant de commencer</h3><p>{text}</p></div><a class="btn main" href="/#rdv">Prendre rendez-vous</a></div>'

# =====================================================================
# SITE VITRINE
# =====================================================================
def vitrine():
    v = mock('Votre-entreprise.fr', '''<div class="m-site"><div class="nav">Mon Atelier<span>Accueil · Services · Contact</span></div>
      <h5>Artisan serrurier à Lyon, disponible 7j/7</h5><p>Dépannage rapide, devis gratuit.</p><span class="m-btn">Appeler maintenant</span>
      <div class="row"><i></i><i></i><i></i></div></div>''', 'Maquette de page d\'accueil d\'un site vitrine')
    h = hero('Site vitrine', 'Un site qui <em class="it">vous ressemble</em> et qui fait venir des clients.',
             'Pas besoin de quinze pages. Il faut un site clair, rapide sur mobile, avec votre numéro bien visible : c\'est ce qui fait appeler.',
             ('Voir les réalisations', '#exemples'), 'Demander un devis', v, 'exemple fictif, pour montrer l\'idée.',
             'Bonjour, je voudrais un devis pour un site vitrine.')
    exs = [
        ('rmserrure', 'RM Serrure', 'Serrurier 24h/24 en Île-de-France', 'https://rmserrure.com'),
        ('streetcarwash', 'Street Car Wash', 'Lavage auto à domicile, avec réservation en ligne', 'https://streetcarwash.com'),
        ('cleanpolish', 'Clean &amp; Polish', 'Lavage auto et remplacement de pare-brise à Aulnay-sous-Bois', 'https://cleanandpolish.fr'),
        ('aestheticmen', 'Aesthetic Men', 'Mésothérapie capillaire à Paris 17', 'https://aestheticmenparis.com'),
        ('123permis', '123permis', 'Auto-école', 'https://123-permis.fr'),
        ('a2d', 'A2D Distribution', 'Sourcing B2B et importation en gros', 'https://a2ddistribution.com'),
        ('xlparebrise', 'XL Pare-Brise', 'Pare-brise', 'https://xlparebrise.fr'),
        ('iliesprod', 'Ilies Prod', 'VFX, 3D et films de marque', 'https://iliesprod.com'),
    ]
    ex_html = '<div class="grid g4">' + ''.join(
        f'<a class="ex" href="{u}" target="_blank" rel="noopener"><img src="/assets/portfolio/{img}.webp" alt="Capture du site {n}" loading="lazy" width="640" height="400"><div><b>{n}</b><span>{d}</span><em>Voir le site →</em></div></a>'
        for img, n, d, u in exs) + '</div>'
    body = ''.join([
        sec('En clair', 'Un site vitrine, c\'est quoi ?',
            '<div class="grid g3">' + ''.join(f'<div class="card"><div class="ico">{i}</div><h3>{t}</h3><p>{p}</p></div>' for i, (t, p) in enumerate([
                ('Être trouvé', 'Quand quelqu\'un cherche votre métier près de chez lui, il tombe sur vous.'),
                ('Rassurer', 'Vos photos, vos horaires, vos réalisations : le client voit à qui il a affaire.'),
                ('Faire contacter', 'Un bouton pour appeler, écrire ou réserver, visible dès l\'arrivée.')], 1)) + '</div>',
            alt=True, intro='C\'est la vitrine de votre activité sur internet : quelques pages simples qui expliquent ce que vous faites, où vous êtes et comment vous joindre.'),
        sec('Pour qui', 'Des sites pour tous les métiers de proximité.',
            '<ul class="chips"><li>Coiffeurs et salons</li><li>Artisans</li><li>Restaurants</li><li>Entreprises locales</li><li>Indépendants</li><li>Commerces</li></ul>'),
        sec('Exemples', 'Des sites réels, livrés.', ex_html + '<p class="sec-intro" style="margin-top:20px;">Chaque site est dessiné pour son activité. Les liens ouvrent les sites en ligne.</p>', alt=True, sid='exemples'),
        sec('Ce que contient un site', 'Les éléments qu\'on assemble.',
            cards([('Pages', 'Accueil, services, à propos, contact : juste ce qu\'il faut.'),
                   ('Formulaire', 'Pour recevoir les demandes directement.'),
                   ('Galerie', 'Vos photos et réalisations, bien présentées.'),
                   ('Avis', 'Les témoignages de clients, quand vous en avez.'),
                   ('Carte', 'Votre adresse et l\'itinéraire en un clic.'),
                   ('Réseaux sociaux', 'Vos comptes reliés au site.'),
                   ('Appel et WhatsApp', 'Un bouton pour vous joindre tout de suite.'),
                   ('Réservation', 'Prise de rendez-vous en ligne, si votre activité s\'y prête.')], 4)),
        sec('Comment ça se passe', 'De votre besoin à la mise en ligne.',
            flow(['Échange sur votre besoin', 'Création de la maquette', 'Validation du design', 'Développement du site', 'Tests sur mobile et ordinateur', 'Mise en ligne']),
            alt=True),
        sec('Avant / après', 'La différence se voit tout de suite.',
            compare('Présence en ligne faible',
                    ['Une page de réseau social, difficile à trouver sur Google.', 'Pas de numéro ni d\'horaires clairs.', 'Peu de photos, aucune preuve de votre travail.', 'Le client hésite et appelle quelqu\'un d\'autre.'],
                    'Site professionnel',
                    ['Vous apparaissez quand on cherche votre métier.', 'Numéro et horaires visibles dès l\'arrivée.', 'Photos et réalisations qui rassurent.', 'Le client vous contacte en un geste.'])),
        sec('Ce que ça change', 'Cinq bénéfices concrets.',
            cards([('Crédibilité', 'Un site soigné donne confiance.'), ('Visibilité', 'On vous trouve en ligne.'), ('Contacts', 'Plus de demandes directes.'), ('Présentation', 'Vous racontez votre métier comme vous le voulez.'), ('Conversion', 'Le visiteur sait quoi faire pour vous contacter.')], 3), alt=True),
        sec('Tarif', 'Un prix clair, avant de commencer.',
            price_block('Le prix dépend du nombre de pages et des fonctions voulues. Vous le connaissez avant le début du travail, sans surprise. L\'hébergement et le nom de domaine sont à votre charge : on vous aide à les choisir.')),
    ])
    faq = [
        ('Combien de temps pour avoir mon site ?', 'Un site simple et bien défini peut être en ligne en environ 7 jours. Pour un site plus complet, le délai exact est annoncé avec le devis.'),
        ('Combien ça coûte ?', 'Le prix dépend du nombre de pages et des fonctions voulues. On vous donne un devis gratuit avec un prix fixe avant de commencer.'),
        ('Pourrai-je modifier mon site après la mise en ligne ?', 'Oui. Les petites modifications (texte, horaires, photos) se font à la demande, et sont chiffrées avant d\'être faites.'),
        ('Qui s\'occupe de l\'hébergement et du nom de domaine ?', 'Ils sont à votre charge, car ils sont à votre nom. On vous aide à les choisir et à tout mettre en place.'),
        ('Mon site sera-t-il lisible sur téléphone ?', 'Oui. Chaque site est testé sur téléphone, tablette et ordinateur avant la mise en ligne.'),
    ]
    return page('site-vitrine', 'Site vitrine pour artisans, commerçants et indépendants — Wanisite',
                'Un site clair, rapide sur mobile, avec votre numéro bien visible. Exemples réels, devis gratuit et prix fixe annoncé avant de commencer.',
                'Création de site vitrine', 'Bonjour, je voudrais un devis pour un site vitrine.', 'Bonjour, je voudrais présenter mon projet de site vitrine.', h, body, faq)

# =====================================================================
# E-COMMERCE
# =====================================================================
def ecommerce():
    v = mock('Ma boutique', '''<div class="m-shop"><div class="pic">Photo du produit</div>
      <div><h5>Savon d'Alep artisanal</h5><span class="tag ok">En stock</span><div class="pr">12,90 €</div><p style="margin:0;color:var(--muted);font-size:12.5px;">Livraison offerte dès 40 €.</p><span class="m-btn">Ajouter au panier</span></div></div>''',
        'Maquette de fiche produit d\'une boutique en ligne')
    h = hero('Boutique en ligne', 'Vendez en ligne, <em class="it">sans vous compliquer</em> la vie.',
             'Une boutique claire pour vos clients, un tableau de bord simple pour vous. De l\'idée à la première commande, on vous accompagne.',
             ('Voir les exemples', '#exemples'), 'Demander un devis', v, 'boutique fictive, produit d\'exemple.',
             'Bonjour, je voudrais un devis pour une boutique en ligne.')
    cart = mock('Mon panier', '''<div class="m-line"><b>Savon d'Alep × 2</b><span>25,80 €</span></div><div class="m-line"><b>Huile d'olive × 1</b><span>9,50 €</span></div><div class="m-line"><span>Livraison</span><span>offerte</span></div><div class="m-total"><span>Total</span><span>35,30 €</span></div><span class="m-btn" style="width:100%;">Payer en ligne</span>''', 'Maquette de panier')
    dash = mock('Tableau de bord vendeur', '''<div class="kpis"><div class="kpi"><span>Commandes</span><b>24</b></div><div class="kpi"><span>Ventes</span><b>1 120 €</b></div><div class="kpi"><span>Stock bas</span><b>2</b></div></div>
      <div class="m-order"><span>#1042 · Marie L.</span><span class="tag warn">À préparer</span></div><div class="m-order"><span>#1041 · Karim B.</span><span class="tag ok">Expédiée</span></div>''', 'Maquette de tableau de bord vendeur')
    exemple = '''<div class="grid g3" style="align-items:start;"><figure style="margin:0;">''' + v + '''<figcaption class="cap"><b>Fiche produit</b> · photo, prix, stock, bouton d'achat.</figcaption></figure>
      <figure style="margin:0;">''' + cart + '''<figcaption class="cap"><b>Panier</b> · récapitulatif clair avant le paiement.</figcaption></figure>
      <figure style="margin:0;">''' + dash + '''<figcaption class="cap"><b>Côté vendeur</b> · commandes et stock au même endroit.</figcaption></figure></div>
      <p class="sec-intro" style="margin-top:14px;"><b>Maquettes</b> : produits et chiffres fictifs, pour montrer le type d'écrans.</p>
      <h3 style="margin-top:44px;">Un exemple réel : Equip'Food</h3>
      <p class="sec-intro">Equip'Food fournit en matériel les cafés, hôtels et restaurants. Son catalogue est en ligne : filtres par marque, fiche produit, et demande de devis directement par WhatsApp. Un bon choix quand les prix se discutent plutôt que de s'afficher.</p>
      <div class="shots"><figure><img src="/assets/equipfood/accueil.webp" alt="Accueil du site Equip'Food" loading="lazy"><figcaption>Accueil</figcaption></figure>
      <figure><img src="/assets/equipfood/catalogue.webp" alt="Catalogue du site Equip'Food avec filtres" loading="lazy"><figcaption>Catalogue et filtres</figcaption></figure>
      <figure><img src="/assets/equipfood/produit.webp" alt="Fiche produit du site Equip'Food" loading="lazy"><figcaption>Fiche produit et demande de devis</figcaption></figure></div>'''
    body = ''.join([
        sec('En clair', 'Une boutique en ligne, c\'est quoi ?', '', alt=True,
            intro='C\'est un site où vos clients voient vos produits, les mettent au panier et commandent, à toute heure. Vous, vous suivez les commandes et le stock depuis un tableau de bord simple.'),
        sec('Pourquoi', 'Vendre seulement par téléphone ou messages a ses limites.',
            compare('Sans boutique',
                    ['Les commandes se perdent dans les messages.', 'Pas de catalogue à montrer à vos clients.', 'Vous répondez aux mêmes questions tous les jours.', 'Impossible de vendre quand vous dormez.'],
                    'Avec une boutique',
                    ['Chaque commande est enregistrée et suivie.', 'Vos produits sont visibles, avec photos et prix.', 'Le client trouve seul ce qu\'il cherche.', 'La boutique reste ouverte tout le temps.'])),
        sec('Exemples', 'À quoi ça ressemble.', exemple, alt=True, sid='exemples'),
        sec('Le parcours de votre client', 'De la découverte à la confirmation.',
            flow(['Il découvre un produit', 'Il consulte la fiche produit', 'Il ajoute au panier', 'Il renseigne ses informations', 'Il paie en ligne', 'Il reçoit une confirmation', 'Vous suivez et préparez la commande'])),
        sec('Fonctionnalités', 'Ce que peut contenir votre boutique.',
            cards([('Catalogue', 'Produits, catégories et recherche.'), ('Paiement', 'Un paiement en ligne sécurisé, mis en place selon votre projet.'),
                   ('Commandes', 'Suivi, statut et historique.'), ('Stock', 'Quantités disponibles et alertes.'),
                   ('Livraison', 'Zones, tarifs et frais.'), ('Promotions', 'Codes promo et réductions.'),
                   ('Clients', 'Comptes et historique d\'achats.'), ('Marketing', 'Newsletter et relances.'),
                   ('Statistiques', 'Ventes, chiffre d\'affaires, produits populaires.'), ('Administration', 'Tout se gère depuis un tableau de bord.')], 4),
            alt=True, intro='Toutes ne sont pas utiles à tous. On choisit avec vous ce qui compte pour votre activité.'),
        sec('Comment ça se passe', 'De l\'idée à la boutique en ligne.',
            flow(['Analyse du projet', 'Maquette de la boutique', 'Ajout des produits', 'Mise en place du paiement', 'Configuration de la livraison', 'Tests de commande', 'Mise en ligne'])),
        sec('Tarif', 'Un prix clair, avant de commencer.',
            price_block('Le prix dépend du nombre de produits et des fonctions voulues (paiement, livraison, stock). Vous le connaissez avant le début du travail. Hébergement, nom de domaine et abonnements d\'outils externes restent à votre charge.'), alt=True),
    ])
    faq = [
        ('Comment mes clients paient-ils ?', 'Par un paiement en ligne sécurisé, mis en place selon votre projet. Si vos prix se discutent, une demande de devis (par WhatsApp, par exemple) peut remplacer le paiement : c\'est le choix d\'Equip\'Food.'),
        ('Comment gérer la livraison ?', 'On configure avec vous les zones, les tarifs et les frais. Vous suivez chaque commande depuis votre tableau de bord.'),
        ('Puis-je gérer mes produits moi-même ?', 'Oui. Vous ajoutez et modifiez vos produits, vos prix et votre stock vous-même. On vous forme à la prise en main.'),
        ('Qui s\'occupe de la maintenance ?', 'Nous, si vous le souhaitez : mises à jour, corrections, sauvegardes. Le détail est précisé dans le devis.'),
        ('Combien de temps pour ouvrir ma boutique ?', 'Cela dépend du nombre de produits et des fonctions. Le délai est annoncé avec le devis, avant de commencer.'),
    ]
    return page('ecommerce', 'Boutique en ligne : créer sa boutique e-commerce — Wanisite',
                'Une boutique claire pour vos clients, un tableau de bord simple pour vous. Exemple réel, devis gratuit et prix fixe annoncé avant de commencer.',
                'Création de boutique en ligne', 'Bonjour, je voudrais un devis pour une boutique en ligne.', 'Bonjour, je voudrais présenter mon projet de boutique en ligne.', h, body, faq)

# =====================================================================
# RÉSERVATION
# =====================================================================
def reservation():
    cal = mock('Agenda', '''<div class="m-cal"><span></span><span class="h">Lun.</span><span class="h">Mar.</span><span class="h">Mer.</span>
      <span class="t">9 h</span><span class="c b">Marie L.<br>Coupe</span><span class="c"></span><span class="c x"></span>
      <span class="t">10 h</span><span class="c"></span><span class="c b">Karim B.<br>Barbe</span><span class="c x"></span>
      <span class="t">11 h</span><span class="c b">Sophie D.<br>Soin</span><span class="c"></span><span class="c x"></span>
      <span class="t">14 h</span><span class="c"></span><span class="c"></span><span class="c b">Julien R.<br>Coupe</span></div>''', 'Maquette d\'agenda de rendez-vous')
    page_c = mock('Réserver', '''<p style="margin:0 0 4px;font-weight:700;">Choisissez un créneau</p><p style="margin:0;color:var(--muted);">Mardi 28 octobre</p>
      <div class="m-slots"><span>9 h</span><span class="off">10 h</span><span class="on">11 h</span><span>14 h</span><span>15 h</span><span class="off">16 h</span></div><span class="m-btn" style="width:100%;">Confirmer le rendez-vous</span>''', 'Maquette de page de réservation côté client')
    notifs = mock('Confirmations', '''<div class="m-notif"><i>✓</i><div><b>Rendez-vous confirmé</b><span>Mardi 28 octobre, 11 h. À bientôt !</span></div></div>
      <div class="m-notif"><i>!</i><div><b>Nouvelle réservation</b><span>Sophie D. · mardi 11 h</span></div></div>
      <div class="m-notif"><i>⏰</i><div><b>Rappel</b><span>Votre rendez-vous est demain à 11 h.</span></div></div>''', 'Maquette de notifications de réservation')
    h = hero('Réservation en ligne', 'Vos clients réservent <em class="it">tout seuls</em>, vous gardez la main.',
             'Un agenda en ligne : le client choisit un créneau libre, vous êtes prévenu, il reçoit une confirmation. Plus de messages à rallonge pour caler une heure.',
             ('Voir un exemple', '#exemples'), 'Demander un devis', cal, 'agenda fictif, noms inventés.',
             'Bonjour, je voudrais un devis pour un système de réservation en ligne.')
    exemple = '''<div class="grid g3" style="align-items:start;"><figure style="margin:0;">''' + cal + '''<figcaption class="cap"><b>Côté professionnel</b> · l'agenda et les créneaux pris.</figcaption></figure>
      <figure style="margin:0;">''' + page_c + '''<figcaption class="cap"><b>Côté client</b> · il choisit un créneau libre.</figcaption></figure>
      <figure style="margin:0;">''' + notifs + '''<figcaption class="cap"><b>Confirmations</b> · client et professionnel sont prévenus.</figcaption></figure></div>
      <p class="sec-intro" style="margin-top:14px;"><b>Maquettes</b> : noms et horaires fictifs, pour montrer le type d'écrans.</p>
      <h3 style="margin-top:44px;">Un exemple réel : Street Car Wash</h3>
      <p class="sec-intro">Street Car Wash propose du lavage auto à domicile en Île-de-France. Ses clients réservent leur lavage en ligne, directement depuis le site.</p>
      <div class="shots" style="grid-template-columns:minmax(0,520px);"><figure><a href="https://streetcarwash.com" target="_blank" rel="noopener"><img src="/assets/portfolio/streetcarwash.webp" alt="Page d'accueil du site Street Car Wash avec réservation en ligne" loading="lazy"></a><figcaption>streetcarwash.com</figcaption></figure></div>'''
    body = ''.join([
        sec('Le problème', 'Les réservations à la main prennent du temps.',
            compare('Réservation manuelle',
                    ['Il faut répondre au téléphone ou aux messages, en pleine journée.', 'Les créneaux se calent par aller-retour.', 'Un rendez-vous oublié, c\'est une heure perdue.', 'Les annulations arrivent au dernier moment.'],
                    'Réservation en ligne',
                    ['Le client réserve quand il veut, même la nuit.', 'Seuls les créneaux libres sont proposés.', 'Une confirmation est envoyée au client.', 'Vous voyez tout dans un seul agenda.']), alt=True),
        sec('Comment ça marche', 'Du créneau choisi à la confirmation.',
            flow(['Le client choisit un créneau', 'La réservation est enregistrée', 'Le professionnel est prévenu', 'Le client reçoit une confirmation', 'Un rappel peut être envoyé avant le rendez-vous'])),
        sec('Exemples', 'À quoi ça ressemble.', exemple, alt=True, sid='exemples'),
        sec('Fonctionnalités', 'Ce que contient le système.',
            cards([('Agenda', 'Tous vos rendez-vous au même endroit.'), ('Créneaux', 'Durées et horaires adaptés à chaque prestation.'),
                   ('Confirmations', 'Le client sait que c\'est bien pris.'), ('Rappels', 'Moins d\'oublis, en option.'),
                   ('Annulations', 'Le client peut annuler ou déplacer.'), ('Disponibilités', 'Vous bloquez vos congés et vos pauses.')], 3)),
        sec('Pour qui', 'Tous ceux qui travaillent sur rendez-vous.',
            '<ul class="chips"><li>Salons et coiffeurs</li><li>Indépendants</li><li>Commerces</li><li>Entreprises de services</li></ul>', alt=True),
        sec('Ce que ça change', 'Quatre avantages.',
            cards([('Gain de temps', 'Moins de messages, moins d\'appels pour caler une heure.'), ('Moins d\'oublis', 'Le client est prévenu, vous aussi.'),
                   ('Meilleure organisation', 'Un agenda lisible, des créneaux maîtrisés.'), ('Plus de réservations', 'Le client réserve à toute heure, sans attendre.')], 4)),
        sec('Mise en place', 'Comment on s\'y prend.',
            flow(['On définit vos prestations et horaires', 'On dessine l\'agenda', 'Vous validez', 'On le met en ligne', 'On vous forme à l\'utiliser']), alt=True),
        sec('Tarif', 'Un prix clair, avant de commencer.',
            price_block('Le prix dépend de ce que le système doit faire (une ou plusieurs prestations, plusieurs personnes, paiement à la réservation). Vous le connaissez avant le début du travail.')),
    ])
    faq = [
        ('Mes clients doivent-ils créer un compte ?', 'Pas forcément. On peut proposer une réservation simple, avec juste un nom et un moyen de vous joindre. Un compte client est possible si votre activité le demande.'),
        ('Peut-on faire payer à la réservation ?', 'C\'est possible, mais c\'est une fonction en plus, chiffrée dans le devis.'),
        ('Et si un client veut annuler ?', 'On prévoit une règle claire : le client peut annuler ou déplacer son rendez-vous, selon le délai que vous choisissez.'),
        ('Puis-je bloquer mes jours de congé ?', 'Oui. Vous gérez vos disponibilités, vos pauses et vos congés depuis l\'agenda.'),
        ('Combien de temps pour être en place ?', 'Cela dépend de ce que le système doit faire. Le délai est annoncé avec le devis, avant de commencer.'),
    ]
    return page('reservation', 'Réservation en ligne : agenda et prise de rendez-vous — Wanisite',
                'Vos clients choisissent un créneau libre, vous êtes prévenu, ils reçoivent une confirmation. Exemple réel, devis gratuit et prix fixe annoncé avant de commencer.',
                'Système de réservation en ligne', 'Bonjour, je voudrais un devis pour un système de réservation en ligne.', 'Bonjour, je voudrais présenter mon projet de réservation en ligne.', h, body, faq)

for name, fn in (('site-vitrine', vitrine), ('ecommerce', ecommerce), ('reservation', reservation)):
    with open(f'{OUT}/{name}.html', 'w') as f:
        f.write(fn())
    print('écrit', name)
