# Consignes de rédaction — blog Wanisite

Lecteur : gérant de commerce, artisan, indépendant ou petite marque en France. Pas technicien.
But : l'aider vraiment (conseils applicables tout de suite) et l'amener vers le service Wanisite qui correspond.

## Forme
- Français simple, phrases courtes, « vous ». Pas de jargon sans explication.
- 900 à 1 400 mots. Un titre clair qui contient la recherche Google visée (60 caractères max si possible).
- Description (meta) : 140 à 160 caractères, concrète, sans point d'exclamation.
- Structure : une intro de 2-3 phrases qui pose le problème, puis des intertitres `##` (et `###` si besoin), listes quand c'est utile, une conclusion courte.
- 1 à 3 liens internes vers les pages du site (services, réalisations, autres articles du blog), écrits en Markdown `[texte](/services/…)`.
- Pas d'emoji, pas de point d'exclamation en série, pas de formules creuses (« dans un monde en constante évolution », « boostez », « révolutionnez »).

## Vérité (règle absolue)
- **Aucun chiffre, statistique, témoignage, client ou cas inventé.** Pas de « 87 % des clients… ».
- Seuls exemples réels utilisables (publiés sur le site) :
  - Clean & Polish (lavage auto, Aulnay-sous-Bois) : campagne Meta Ads, 108 appels en 6 jours, 1,49 € par appel → /realisations/clean-and-polish
  - Aesthetic Men (mésothérapie capillaire, Paris 17) : campagne Meta Ads, 51 appels en 9 jours, 2,39 € par appel → /realisations/aesthetic-men
  - Equip'Food : catalogue en ligne pour cafés, hôtels, restaurants, demande de devis par WhatsApp (pas de chiffre de références)
  - Street Car Wash : lavage auto à domicile, réservation en ligne depuis le site
  - Sites vitrines livrés : RM Serrure (serrurier), 123permis (auto-école), A2D Distribution, XL Pare-Brise, Ilies Prod (VFX/3D)
- Ne jamais citer Thom Cut / Thomcut.
- Ne présenter comme fonction Wanisite que ce qui est livré : sites vitrines, boutiques, réservation, CRM/tableaux de bord sur mesure, campagnes Meta/Google Ads, sourcing en Chine. Pas de « relances automatiques » ni de promesse de résultat chiffré.
- Prix Wanisite : toujours « sur devis, prix fixe annoncé avant de commencer ». Ne pas donner de tarif.
- Règles légales, fiscales, douanières : rester général et exact (ex. « la TVA à l'import s'applique », « le taux de droits dépend du code douanier du produit »), renvoyer vers la source officielle (douane.gouv.fr, service-public.fr, economie.gouv.fr) au lieu d'affirmer un chiffre précis dont on n'est pas sûr.

## Fichier
`_blog/articles/AAAA-MM-JJ-slug.md`, avec cet en-tête :

```
---
titre: …
description: …
date: AAAA-MM-JJ
slug: mots-cles-en-minuscules-avec-tirets
service: /services/xxx.html | Nom du service mis en avant
mots_cles: mot 1, mot 2, mot 3
---
```
Puis le texte en Markdown (`##`, `###`, listes `-` ou `1.`, `**gras**`, `[lien](url)`, `> citation`). Pas de `#` simple (le titre vient de l'en-tête).
