---
titre: Site lent sur mobile : les causes fréquentes et les solutions
description: Images trop lourdes, extensions en trop, polices, vidéos, hébergement : les causes les plus courantes d'un site lent sur téléphone, et comment les corriger.
date: 2026-11-18
slug: site-lent-sur-mobile-causes-solutions
service: /services/site-vitrine | Site vitrine
mots_cles: site lent sur mobile, accélérer site internet, vitesse site mobile, site qui charge lentement, PageSpeed Insights, optimiser images site
---
Vos clients vous cherchent surtout depuis leur téléphone, souvent dehors, avec une connexion pas toujours bonne. Si votre site met du temps à s'afficher, une partie d'entre eux repart vers le résultat suivant sans jamais voir vos horaires ou votre numéro. La bonne nouvelle : la lenteur vient presque toujours des mêmes causes, et beaucoup se corrigent sans tout refaire.

## Commencez par mesurer, pas par deviner

Avant de changer quoi que ce soit, regardez ce qui se passe vraiment. Deux réflexes simples :

- **Testez vous-même sur votre téléphone**, en 4G et pas seulement sur le Wi-Fi du bureau. Ouvrez le site en navigation privée, pour ne pas profiter de ce qui est déjà en mémoire.
- **Passez l'adresse dans PageSpeed Insights**, l'outil gratuit de Google (pagespeed.web.dev). Il donne une note pour mobile et, surtout, une liste de problèmes classés par importance.

Ne vous focalisez pas sur la note elle-même. Ce qui compte, c'est la partie « Diagnostics » : elle vous dit quelles images sont trop lourdes, quels fichiers bloquent l'affichage, ce qui prend du temps côté serveur. C'est votre liste de travail.

Notez aussi la page que vous testez. La page d'accueil n'est pas forcément la plus lente : une page produit avec beaucoup de photos ou une page « Réalisations » avec une galerie peuvent être bien pires.

## Cause n°1 : des images trop lourdes

C'est un cas très courant sur les sites de commerces et d'artisans. Une photo prise au téléphone ou fournie par un photographe est souvent envoyée telle quelle sur le site, en très grande taille, alors qu'elle s'affiche sur un écran de quelques centimètres.

Ce qu'il faut faire :

- **Redimensionner** chaque image à la taille où elle est réellement affichée. Inutile d'envoyer une photo plus large que l'écran le plus grand qui la montrera.
- **Compresser** les images. Des outils gratuits comme Squoosh (squoosh.app) permettent de réduire fortement le poids sans différence visible à l'œil.
- **Utiliser un format moderne** comme le WebP ou l'AVIF, plus légers que le JPEG ou le PNG à qualité égale. La plupart des outils de création de site savent les produire.
- **Activer le chargement différé** (« lazy loading ») : les images en bas de page ne se chargent que quand le visiteur fait défiler. En revanche, l'image tout en haut de la page doit se charger tout de suite, sinon l'effet est inverse.

Si votre site est sur WordPress, une extension d'optimisation d'images peut traiter toute la médiathèque d'un coup. Pensez simplement à garder une copie des originaux.

## Cause n°2 : trop d'extensions et de scripts

Chaque extension, chaque widget, chaque outil ajouté « pour essayer » charge ses propres fichiers. Pris un par un, c'est peu. Accumulés au fil des années, ils finissent par peser lourd : un module de chat que personne n'utilise, un carrousel d'avis, deux outils de statistiques qui font la même chose, un bouton de partage, un pop-up d'inscription.

Faites l'inventaire :

1. Listez tout ce qui est installé sur le site (extensions, codes ajoutés dans l'en-tête, widgets externes).
2. Pour chaque élément, posez-vous une question : est-ce que quelqu'un s'en sert vraiment, et est-ce que ça m'apporte des clients ?
3. Désactivez ce qui ne sert pas, puis retestez la vitesse.

Faites-le de préférence sur une copie du site ou après une sauvegarde, une extension pouvant en dépendre d'une autre.

## Cause n°3 : un thème ou un constructeur de pages trop chargé

Les thèmes « tout-en-un » vendus avec des dizaines de mises en page, d'animations et d'effets chargent souvent tout ce code sur chaque page, même si vous n'utilisez qu'une petite partie des fonctions. Il en va de même pour certains constructeurs de pages visuels, très pratiques pour modifier soi-même, mais qui produisent beaucoup de code.

Quelques pistes, de la plus simple à la plus lourde :

- supprimer les animations à l'apparition, les sliders en plein écran et les effets de parallaxe, qui ralentissent sans aider à vendre ;
- désactiver dans les réglages du thème les modules que vous n'utilisez pas ;
- si le site reste lent malgré tout, envisager un thème plus léger ou une refonte plus sobre.

## Cause n°4 : vidéos et polices mal intégrées

Une vidéo en fond de page d'accueil fait de l'effet sur un grand écran, mais sur mobile elle peut retarder tout le reste. Si vous tenez à une vidéo, préférez une version courte et compressée, ou affichez une image fixe avec un bouton « lecture » qui ne charge la vidéo qu'au clic. Pour les vidéos YouTube intégrées, le même principe s'applique : une simple image en attendant le clic.

Les polices de caractères comptent aussi. Chaque famille de police, et chaque graisse (normal, gras, italique…), est un fichier à télécharger. Limitez-vous à une ou deux polices et aux graisses que vous utilisez réellement.

## Cause n°5 : l'hébergement et l'absence de cache

Parfois, le site lui-même n'est pas en cause : c'est le serveur qui répond lentement. Dans PageSpeed Insights, cela se voit dans la ligne qui mesure le temps de réponse du serveur. Les causes possibles :

- un hébergement très bas de gamme, partagé entre un grand nombre de sites ;
- un serveur situé loin de vos visiteurs ;
- l'absence de **cache**, c'est-à-dire d'une copie toute prête des pages. Sans cache, un site WordPress reconstruit chaque page à chaque visite.

Sur WordPress, une extension de cache bien réglée change souvent beaucoup de choses. Votre hébergeur propose peut-être déjà un cache intégré : vérifiez dans votre espace client avant d'ajouter une extension, pour ne pas en faire tourner deux en même temps.

Pensez aussi aux mises à jour : une version récente de PHP (le langage qui fait tourner WordPress) est généralement plus rapide que les anciennes. Votre hébergeur permet en principe de la changer depuis son panneau, après vérification que vos extensions sont compatibles.

## Ce qui ne sert à rien (ou presque)

Quelques fausses bonnes idées reviennent souvent :

- **Installer plusieurs extensions « d'accélération » en même temps** : elles se gênent et peuvent casser l'affichage.
- **Courir après une note parfaite** : un site qui s'affiche vite et reste agréable à utiliser vaut mieux qu'une note maximale obtenue en retirant tout ce qui rassure le client (photos, avis, plan d'accès).
- **Tester uniquement sur ordinateur** : ce que vous voyez sur votre écran de bureau ne dit rien de ce que vit un client dans la rue.

## Une méthode simple pour avancer

Si vous ne savez pas par où commencer, procédez dans cet ordre :

1. Mesurez la page d'accueil et la page la plus visitée, sur mobile.
2. Traitez les images (redimensionner, compresser, format moderne).
3. Retirez les extensions et scripts inutiles.
4. Activez un cache, si ce n'est pas déjà fait.
5. Retestez, et notez la différence.

Ces étapes règlent une bonne partie des cas. Si le site reste lent après cela, le problème est souvent plus profond : thème trop lourd, hébergement inadapté, ou construction qui n'a pas été pensée pour le mobile au départ. Dans ce cas, un nettoyage ne suffit plus et il vaut mieux repartir sur une base saine.

Le choix de l'outil a aussi un impact sur ce point. Si vous hésitez encore pour une boutique, notre article [Shopify, WooCommerce ou sur mesure](/blog/shopify-woocommerce-ou-sur-mesure) détaille ce que chaque solution implique au quotidien.

## En résumé

Un site lent sur mobile coûte des visites sans que vous le voyiez. Mesurez d'abord, puis attaquez les causes dans l'ordre : images, extensions, thème, médias, hébergement. La plupart des corrections sont accessibles sans être développeur.

Si vous préférez repartir sur un site conçu dès le départ pour le téléphone, léger et facile à mettre à jour, c'est ce que nous faisons avec notre offre [site vitrine](/services/site-vitrine) : sur devis, avec un prix fixe annoncé avant de commencer.
