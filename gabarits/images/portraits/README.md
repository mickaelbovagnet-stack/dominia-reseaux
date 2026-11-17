# Portraits de Mickaël Bovagnet

Règle validée par Mick le 17 novembre 2026. Elle complète la charte des réseaux (`CLAUDE.md`, section 4).

## La règle

### Ce qui est autorisé
- Des variantes de portrait réalisées avec l'IA à partir d'une **vraie photo de Mickaël**, la photo de référence de ce dossier.
- Uniquement sur les **réseaux sociaux de Cimeria** (Instagram, LinkedIn, Facebook), dans les gabarits `point_de_vue` et `cas_fin`.
- Ce qui peut varier :
  - la pose ;
  - le cadrage, du gros plan au mi-corps ;
  - l'expression ;
  - la tenue, dans le style réel de Mickaël (chemise et veste bleu marine, chemise blanche) ;
  - la lumière de studio.

### Ce qui est interdit
- Toute mise en scène inventée : lieu, décor, événement, scène de conférence, bureau, poignée de main, public.
- Tout objet qui raconte une situation : micro, écran, livre, tasse, ordinateur.
- Toute autre personne, même floue.
- Toute modification de l'apparence de Mickaël :
  - visage, âge, poids, carrure ;
  - coupe de cheveux, barbe ;
  - lunettes ;
  - peau lissée.
- Un logo de marque sur les vêtements, du texte, un accessoire absent de la photo d'origine.
- Une variante tirée d'une autre variante. On repart toujours de la photo de référence pour éviter que la ressemblance dérive.
- La photo de profil des comptes, le site cimeria.ch et le profil LinkedIn personnel de Mickaël. Ils gardent une vraie photo.

### Ressemblance stricte
Une variante n'est retenue que si elle passe **chaque** point ci-dessous, en comparaison côte à côte avec la photo de référence, à taille réelle. Au moindre doute, elle est rejetée.

1. La forme du visage, du nez, des oreilles et de la mâchoire est identique.
2. Les lunettes sont rondes, à fine monture métallique, de même taille sur le visage.
3. Les cheveux bruns courts sont coiffés vers l'arrière, avec la même implantation et le même volume.
4. Les yeux sont bruns, les sourcils ont la même forme et le sourire garde la même légère asymétrie.
5. La carnation et le grain de peau sont naturels, sans effet de peau de cire.
6. Les mains ont cinq doigts, des articulations crédibles et aucune déformation.
7. Les vêtements sont cohérents : boutons alignés, col symétrique, aucun logo.
8. Le fond est uni, sans tache, sans motif et sans artefact.
9. Mickaël valide lui-même. Idéalement, un proche confirme qu'il le reconnaît sans hésiter.

### Transparence
- Le texte alternatif de chaque image qui contient une variante mentionne « Portrait réalisé avec l'IA à partir d'une photo de Mickaël Bovagnet ».
- Le visuel porte la mention discrète « Portrait réalisé avec l'IA » au bas de la photo. Les gabarits l'ajoutent quand le champ `photo_ia` vaut `true`.
- À la publication sur Instagram, Mickaël active l'étiquette IA dans les paramètres avancés du post.
- Les variantes ne sont jamais présentées comme des photos prises sur le vif.

### Rangement
- Photo de référence : `reference-bras-croises.jpg`, vraie photo, sans métadonnées.
- Variantes validées : `ia-NN-pose.jpg` (par exemple `ia-01-explique-assis.jpg`), en 1'500 pixels de large au moins.
- Chaque variante est inscrite dans `registre.md` avec la pose, l'outil, la date et la validation.
- Les métadonnées des fichiers sont retirées avant d'entrer dans ce dépôt, qui est public.

## Le modèle de prompt

Il suit la méthode des 4 C de Cimeria. Joindre la photo de référence, coller le prompt, remplacer la ligne « Pose » par une pose du catalogue ci-dessous. Une seule variante par demande, en repartant toujours de la photo de référence.

```text
Contexte
Voici une vraie photo de moi, Mickaël Bovagnet, prise en studio. Je publie un média sur l'intelligence artificielle pour des dirigeants de PME en Suisse romande. J'ai besoin de variantes de ce portrait pour mes réseaux sociaux, sans repasser par le studio.

Consigne
Crée une nouvelle photo de moi, avec une autre pose, en gardant exactement mon visage et mon apparence. La personne sur l'image doit être reconnaissable sans hésitation par quelqu'un qui me connaît.

Contenu
Pose : [coller une pose du catalogue]
Garde à l'identique : la forme du visage, du nez, des oreilles et de la mâchoire, mes yeux bruns et mes sourcils, mes cheveux bruns courts coiffés vers l'arrière, mes lunettes rondes à fine monture métallique, ma carnation et le grain naturel de ma peau, mon âge et ma carrure, mon sourire légèrement asymétrique.
Tenue : chemise bleu marine unie comme sur la photo, sans aucun logo. [ou : veste bleu marine sur chemise blanche unie]

Cadre
Photo de studio réaliste, fond uni anthracite très sombre et sans motif, lumière douce venant de la gauche comme sur la photo d'origine, rendu d'un objectif de 85 mm. Format vertical 4:5, haute définition, au moins 1'500 pixels de large. Laisse de l'espace au-dessus de la tête.
N'ajoute aucun décor, aucun objet, aucune autre personne, aucun texte, aucun logo, aucun accessoire. Ne lisse pas la peau, ne me rajeunis pas, ne m'amincis pas, ne change pas mes lunettes ni ma coiffure.
Si une consigne t'oblige à modifier mon visage, garde le visage et simplifie la pose.
```

Une version anglaise donne parfois un meilleur résultat selon l'outil. Elle reprend les mêmes blocs : « Keep my face and appearance exactly as in the attached photo… ».

## Outils

Situation en novembre 2026. Les modèles changent vite, le test ci-dessous tranche.

- **ChatGPT, générateur d'images.** C'est le premier essai. L'éditeur mis à jour en septembre 2026 met en avant la fidélité à la personne, et les images portent les métadonnées de provenance C2PA, ce qui sert notre règle de transparence.
- **Gemini, modèle Nano Banana.** C'est le second essai. Il garde bien ce qui doit rester fixe, mais le visage peut dériver d'une génération à l'autre.
- **À éviter.** Les applications de portraits professionnels qui demandent une série de selfies pour entraîner un modèle à votre visage, Midjourney (trop stylisé) et les outils d'IA de Canva (moins fidèles au visage).

Avant tout envoi, désactiver dans l'outil l'option qui autorise l'éditeur à entraîner ses modèles sur vos contenus.

### Test de départ
1. Même photo de référence, même prompt, pose `explique-assis`, trois essais dans chaque outil.
2. Passer les six images à la grille de ressemblance.
3. Garder l'outil qui réussit le plus d'essais sans retouche, l'inscrire dans `registre.md` et s'y tenir jusqu'au prochain test.

## Catalogue de poses

Chaque pose est pensée pour la moitié basse des gabarits `point_de_vue` et `cas_fin`, une zone horizontale de 1'080 x 750 pixels. Le visage doit se trouver dans le tiers haut de l'image.

| Code | Pose à coller dans le prompt | Usage |
|---|---|---|
| `explique-assis` | Assis derrière une table nue et sombre, avant-bras posés, mains ouvertes vers l'avant comme en train d'expliquer, regard légèrement hors cadre vers la droite, bouche détendue. Cadrage à mi-corps. | Point de vue, fin de cas pratique |
| `ecoute-assis` | Assis derrière une table nue et sombre, mains croisées posées à plat, buste penché vers l'avant, regard attentif vers l'objectif. Cadrage à mi-corps. | Fin de cas pratique |
| `accueil-debout` | Debout, face à l'objectif, mains jointes devant lui à hauteur de la taille, sourire chaleureux, regard caméra. Cadrage à mi-corps. | Présentation de Cimeria |
| `gros-plan` | Gros plan du visage et des épaules, de face, regard caméra, sourire léger. | Point de vue court, vignette |
| `trois-quarts-pensif` | Buste de trois quarts tourné vers la gauche, regard au loin, expression pensive et calme, bras le long du corps. | Point de vue sur un sujet de fond |
| `main-menton` | Buste de face, une main près du menton, index le long de la joue, regard caméra, expression réfléchie. | Point de vue, question de fond |
| `bras-croises` | La photo de référence elle-même, sans génération. | Tous usages |

## Ce que cette règle permet aussi

Le procédé peut devenir un cas pratique, « Des portraits variés à partir d'une seule photo ». Le post montrera la photo de référence, le prompt et la grille de vérification. Comme tout cas pratique, il part d'un article publié sur cimeria.ch, à écrire d'abord.
