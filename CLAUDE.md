# Charte des réseaux sociaux Cimeria

Ce dépôt héberge les visuels publics des réseaux sociaux de Cimeria (Dominia jusqu'au 16 novembre 2026, le dépôt garde son nom dominia-reseaux). Comptes : Instagram @cimeria.ch, LinkedIn linkedin.com/company/cimeria-ch, Facebook facebook.com/cimeria.ch. Ces consignes s'appliquent à toute conversation du projet et à toute tâche planifiée qui prépare un post. Processus validé par Mick le 12 novembre 2026, passé aux couleurs de Cimeria le 17 novembre 2026.

## Règles absolues

- Échanger avec Mick en français. Il s'appelle Mickaël Bovagnet dans tout contenu public.
- Rien n'est jamais publié par Claude. Tout part en brouillon dans Buffer et Mick publie lui-même.
- Tout ce qui est dans ce dépôt est public. Aucune donnée confidentielle.
- Les règles de contenu du site s'appliquent aussi aux réseaux (voir le CLAUDE.md de dominia-site). Aucun prix du coaching, aucun montant en dollars ou en euros, aucune organisation privée romande nommée sans l'accord de Mick.
- Typographie de chaque texte (visuels, légendes, textes alternatifs, commentaires) :
  - aucun tiret long ;
  - jamais de virgule avant « et » ni avant « mais » ;
  - pas de phrase coupée par deux-points en son milieu ;
  - formulations affirmatives ;
  - guillemets « » ;
  - montants en CHF avec apostrophe des milliers (5'100).

## Deux formats

1. **Cas pratique**, 1 à 2 par semaine. Processus complet ci-dessous.
2. **Actualité**, quotidienne et automatisée. Version allégée décrite en fin de fichier.

## Processus complet d'un cas pratique

### 1. Partir d'un article en ligne
Relire l'article publié sur cimeria.ch en entier. Tous les chiffres, consignes et vérifications du post en viennent, sans aucun ajout. Un exemple fictif est signalé comme tel.

### 2. Choisir l'angle
- Mettre en avant la méthode IA, jamais la méthode métier.
- Montrer la vraie consigne en 4 C (Contexte, Consigne, Contenu, Cadre) et les vérifications.
- Ne jamais laisser croire qu'une question suffit. Le post n'est pas réducteur.

### 3. Construire le carrousel Instagram en 8 diapositives (1080 x 1350)

| N° | Gabarit | Étiquette | Contenu |
|---|---|---|---|
| 1 | `couverture_ia` | Pratique | Le titre en haut, gros et lisible en vignette (45 signes au plus), sans mot répété. Une accroche concrète (durée, nombre d'étapes, exemple). En dessous, la demande naïve, la réponse vague de l'IA et le tampon « Trop vague ». |
| 2 | `lecon` | Aperçu du guide | « Ce qui fait la différence ». Les 4 C nommés, vos sources, votre contrôle. |
| 3 à 6 | `etape_methode` | Aperçu du guide | Une étape par diapositive : le bloc « Ce que vous écrivez, en 4 C » (consignes courtes), puis deux lignes, « L'IA vous rend » et « Vous vérifiez ». 60 mots au plus par diapositive, le script prévient au-delà. Une étape plus riche se répartit sur deux diapositives. Les termes techniques sont traduits (« un rapport à ouvrir dans le navigateur » plutôt que « HTML »). Les sigles sont écrits en toutes lettres. |
| 7 | `capture` | Aperçu du guide | Le résultat réel. Une vraie capture tirée de l'article (outil et date en légende), recadrée pour rester lisible sur téléphone, le bas effacé avec « La suite dans l'article ». Jamais d'image générée par IA ni de photo de banque d'images. |
| 8 | `fin` | Pratique | « Enregistrez ce post pour le retrouver. » La consigne complète de l'étape 1 annoncée en commentaire, le renvoi à l'article en lien dans la bio. Signature « Mickaël Bovagnet, Auteur du guide, Cimeria » avec le portrait. |

Le nombre d'étapes peut varier selon l'article. La structure reste la même.

### 4. Respecter la charte visuelle
- Charte Cimeria (artifact « Cimeria, identité », https://claude.ai/artifact/WV2b8yPKi2L1bGXnSqTtfR).
- Univers clair (fond #F6F5F2, cartes #FFFFFF, encre #2B2B2D). L'univers anthracite reste réservé aux couvertures de cas pratique avec portrait.
- Le rouge (#DA291C) est réservé aux accents et au carré du logo, jamais en aplat.
- Jost pour les titres, étiquettes et chiffres, Figtree pour les textes.
- Logotype Cimeria en pied de chaque visuel, d'un seul bloc, sans jamais isoler « ia ». Aucun quadrillage sur les visuels des réseaux.
- Uniquement les gabarits de `gabarits/generer.py`, sans mise en page improvisée. `apercus/` montre chaque gabarit.

### 5. Relire deux fois avant d'envoyer à Mick
1. En expert des réseaux sociaux : accroche, rythme, lisibilité sur téléphone, appel à l'action.
2. Dans la peau du client type, un dirigeant de PME romand qui fait défiler Instagram : est-ce clair, crédible, utile et sans jargon ?

Appliquer les corrections avant tout envoi.

### 6. Produire les images
1. Lancer `python3 gabarits/generer.py publications/AAAA-MM-JJ/sujet/carrousel-vN.json publications/AAAA-MM-JJ/sujet`. Le script signale tout texte qui déborde.
2. Contrôler visuellement la planche complète (`planche.png`).
3. Donner un nouveau nom de fichier à chaque version (v1, v2…), car raw.githubusercontent.com garde l'ancienne image en cache.
4. Pousser sur `main` (autorisé dans ce dépôt), puis vérifier que chaque URL raw répond 200.

### 7. Préparer les brouillons Buffer
Organisation 6af56cc922ccef12afddbdf0 (« My organization », offre gratuite : 3 comptes, 10 publications programmées au plus). Toujours `saveToDraft: true`.

- **Instagram** (6afb1db8ece6dfde5fe5a18f, @cimeria.ch) : metadata `{type: "post", shouldShareToFeed: true}`, un texte alternatif par image.
  - Légende dans cet ordre : accroche, conditions de réussite, exemple, nuance (« le jugement reste le vôtre »), appel à enregistrer, renvoi au premier commentaire et à la bio, 5 hashtags.
  - Le premier commentaire n'est pas programmable sur l'offre gratuite de Buffer. Il est écrit dans `premier-commentaire.txt` et Mick le poste à la main juste après la publication.
- **LinkedIn** (6afb14e7ece6dfde5fe50e82, page cimeria-ch) : le même carrousel en document PDF, avec une légende plus développée et un lien direct vers l'article.
- **Facebook** (6afb1540ece6dfde5fe51193, page cimeria.ch) : les mêmes images en album, avec une légende proche d'Instagram et un lien direct vers l'article.

### 8. Soumettre à Mick
Envoyer la planche, le premier commentaire et un court récapitulatif. Mick valide, publie et poste le commentaire.

## Version allégée pour l'actualité

1. Partir d'une source officielle vérifiée, liée dans le post.
2. Un visuel unique (gabarit `actualite`).
3. Une seule relecture, celle du client type.
4. Brouillons LinkedIn et Facebook déposés dans Buffer avant 8 h.
5. Un carrousel d'actualité hebdomadaire pour Instagram.

## Arborescence

- `gabarits/` : générateur, polices Jost et Figtree, portrait.
- `publications/2026-11-12/` : archive de l'époque Dominia, à ne pas republier telle quelle.
- `publications/AAAA-MM-JJ/sujet/` : `sources/`, fichiers JSON de chaque version, images, `planche.png`, `premier-commentaire.txt`.
- `apercus/` : un exemple de chaque gabarit, régénéré par `python3 gabarits/generer.py apercus/source/apercus.json apercus`.
