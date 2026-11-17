# Charte des réseaux sociaux Cimeria

Ce dépôt héberge les visuels publics des réseaux sociaux de Cimeria (Dominia jusqu'au 16 novembre 2026, le dépôt garde son nom dominia-reseaux). Comptes : Instagram @cimeria.ch, LinkedIn linkedin.com/company/cimeria-ch, Facebook facebook.com/cimeria.ch. Ces consignes s'appliquent à toute conversation du projet et à toute tâche planifiée qui prépare un post. Processus validé par Mick le 12 novembre 2026, passé aux couleurs de Cimeria et à la grille éditoriale le 17 novembre 2026.

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

### 3. Construire le carrousel Instagram en 6 diapositives (1080 x 1350)

Direction validée par Mick le 17 novembre 2026, sur le modèle de The Economist et de la Harvard Business Review. La cible est faite de cadres et de dirigeants, des lecteurs ordonnés et souvent expérimentés. La grille reste fixe, peu de texte, une seule image forte par visuel. Pas de capture d'écran, pas de mise en page qui part dans tous les sens.

| N° | Gabarit | Contenu |
|---|---|---|
| 1 | `cas_couverture` | Bandeau anthracite avec le titre (50 signes au plus) et un sous-titre concret. En partie claire, une illustration au trait tirée de `gabarits/illustrations/`. « Exemple fictif » en note quand c'est le cas. |
| 2 à 5 | `cas_etape` | Une étape par diapositive. Bandeau anthracite avec la barre de progression et le mot de l'étape (Contexte, Consigne, Contenu, Cadre). Carte « Vous ajoutez » de 25 mots au plus, le script prévient au-delà. Puis « L'IA vous rend » (une ou deux lignes courtes) et « Ce qui manque encore », qui devient « Votre part » à la dernière étape. Les termes techniques sont traduits et les sigles écrits en toutes lettres. |
| 6 | `cas_fin` | « Enregistrez ce post pour le retrouver. » Le prompt complet annoncé en commentaire, l'article en lien dans la bio. Portrait de Mickaël en moitié basse avec la signature « Mickaël Bovagnet, Auteur du guide, Cimeria ». |

Le nombre d'étapes suit l'article. La structure reste la même.

Formats d'image unique, à alterner avec les carrousels dans la grille du profil :
- `chiffre` : un chiffre clé d'une source officielle, sur fond anthracite. La partie `accent` du chiffre est en rouge. Une phrase qui l'explique, une ligne qui dit quoi faire, la source.
- `liste` : une liste numérotée à garder (10 éléments au plus), par exemple les usages d'un article.
- `point_de_vue` : une phrase de Mickaël tirée d'un article publié, avec son portrait en moitié basse.
- Décryptage : un carrousel `cas_couverture`, puis une diapositive `fait_cle` par élément comparé (fonds en alternance), puis `cas_fin`.

### 4. Respecter la charte visuelle
- Charte Cimeria (artifact « Cimeria, identité », https://claude.ai/artifact/WV2b8yPKi2L1bGXnSqTtfR).
- Fond clair #F6F5F2, cartes #FFFFFF, encre #2B2B2D. L'anthracite sert de bandeau (couverture et étapes) ou de fond plein (chiffre). Dans la grille du profil, les visuels anthracite et clairs alternent.
- Le rouge (#DA291C, #F04A3B sur anthracite) est réservé à la rubrique, au carré du logo, à la barre de progression et à la partie `accent` d'un chiffre clé. Jamais de surlignage, de cadre ni d'aplat rouge.
- Jost pour les titres, étiquettes et chiffres, Figtree pour les textes.
- Logotype Cimeria en pied de chaque visuel, d'un seul bloc, sans jamais isoler « ia ». Aucun quadrillage sur les visuels des réseaux.
- Les illustrations sont des dessins au trait anthracite, un seul détail rouge, rangés dans `gabarits/illustrations/` (SVG 600 x 420). Jamais de photo de banque d'images ni de logo d'un éditeur.
- Les photos sont celles de Mickaël. Les seules images générées par IA autorisées sont des variantes de son portrait, tirées de sa vraie photo de référence, selon la règle de `gabarits/images/portraits/README.md` (validée le 17 novembre 2026) :
  - ressemblance stricte ;
  - aucune mise en scène inventée ;
  - mention « Portrait réalisé avec l'IA » sur le visuel (`photo_ia: true`) et dans le texte alternatif ;
  - étiquette IA activée par Mick sur Instagram.

  Les variantes servent sur les réseaux seulement, jamais en photo de profil ni sur le site.
- Lisibilité sur téléphone (demande de Mick du 17 novembre 2026). Un visuel de 1080 px s'affiche sur environ 390 points d'écran.
  - Aucun texte sous 30 px, textes courants à 44 px au moins. Le script signale tout texte plus petit.
  - Les gabarits remplissent la hauteur disponible. Un texte trop long se raccourcit, il ne se réduit pas.
  - `fait_cle` : titre de 70 signes au plus, résumé de 25 mots au plus. L'élément clé s'ajuste seul à la largeur.
- Uniquement les gabarits de `gabarits/generer.py`, sans mise en page improvisée. `apercus/` montre chaque gabarit. Les gabarits `couverture_ia`, `lecon`, `etape_methode`, `capture` et `fin` sont conservés pour l'archive et ne servent plus.

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
  - Le premier commentaire n'est pas programmable sur l'offre gratuite de Buffer (refus vérifié le 17 novembre 2026). Il est écrit dans `premier-commentaire.txt` et recopié dans le document du projet Claude `claude/premiers-commentaires-instagram.md`, où Mick le copie depuis son téléphone pour le poster à la main juste après la publication.
- **LinkedIn** (6afb14e7ece6dfde5fe50e82, page cimeria-ch) : le même carrousel en document PDF, avec une légende plus développée et un lien direct vers l'article.
- **Facebook** (6afb1540ece6dfde5fe51193, page cimeria.ch) : les mêmes images en album, avec une légende proche d'Instagram et un lien direct vers l'article.

### 8. Soumettre à Mick
Envoyer la planche, le premier commentaire et un court récapitulatif. Mick valide, publie et poste le commentaire. Quand un visuel contient un portrait généré, le récapitulatif le signale pour qu'il active l'étiquette IA d'Instagram.

## Version allégée pour l'actualité

1. Partir d'une source officielle vérifiée, liée dans le post, ou de l'article hebdomadaire « L'IA cette semaine » publié le lundi sur cimeria.ch.
2. Un visuel unique (gabarit `fait_cle`) pour LinkedIn et Facebook. Le carrousel hebdomadaire d'Instagram enchaîne un sommaire (`liste`, rubrique « L'IA cette semaine »), une diapositive `fait_cle` par fait (5 au plus), fonds anthracite et clair en alternance, chacune ancrée par un élément clé en très grand (date, chiffre, mot), avec la section de l'article en rubrique (À la une, En Suisse, Tech et outils, Économie de l'IA), et une fin (`cas_fin`, « Abonnez-vous pour suivre l'actualité IA. »).
3. L'agenda des événements (gabarit `agenda`, 5 événements au plus par visuel, au-delà un carrousel de deux visuels) part des fichiers de `dominia-site/src/content/evenements`. Seuls les organisateurs de `organisateurs.json` sont nommés.
4. Une seule relecture, celle du client type.
5. Brouillons LinkedIn et Facebook déposés dans Buffer avant 8 h.

## Arborescence

- `gabarits/` : générateur, polices Jost et Figtree, illustrations au trait.
- `gabarits/images/portraits/` : photo de référence, variantes validées, règle, modèle de prompt et registre.
- `maquettes/2026-11-17/` : les maquettes qui ont mené à la grille éditoriale.
- `publications/2026-11-12/` : archive de l'époque Dominia, à ne pas republier telle quelle.
- `publications/AAAA-MM-JJ/sujet/` : `sources/`, fichiers JSON de chaque version, images, `planche.png`, `premier-commentaire.txt`.
- `apercus/` : un exemple de chaque gabarit, régénéré par `python3 gabarits/generer.py apercus/source/apercus.json apercus`.
