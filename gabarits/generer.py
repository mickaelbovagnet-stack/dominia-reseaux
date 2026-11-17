"""Génère les visuels Cimeria pour les réseaux sociaux à partir d'une description JSON.

Usage : python3 gabarits/generer.py visuels.json dossier/de/sortie

Le JSON contient "visuels", une liste. Chaque visuel a un "gabarit" et ses champs.
- couverture : rubrique, titre (accroche, pas le titre du site), accroche, image (graphisme de l'article), total
- etape      : rubrique, numero, total, titre, texte, capture (facultatif, chemin d'une capture d'écran)
- fait       : numero, total, titre, impact, source      (carrousel hebdomadaire d'actualité)
- fin        : titre, texte, total
- cas        : titre, accroche, photo                     (couverture de Reel, univers anthracite)
- agenda     : titre, evenements [{date, lieu, titre}]
- actualite  : date, titre, resume, source                (carte seule, LinkedIn et Facebook)
- chiffre, liste, point_de_vue, cas_couverture, cas_etape, cas_fin : gabarits éditoriaux du 17 novembre 2026 (voir chaque fonction)
- couverture_ia, lecon, etape_methode, capture, fin : anciens gabarits, conservés pour l'archive
Champ commun facultatif : "fichier". Les chemins d'image sont absolus ou relatifs au fichier JSON.
Règles : textes courts et gros (lecture sur téléphone), rouge réservé à l'étiquette, au filet et au logo.
"""
import asyncio, json, pathlib, sys, html
from playwright.async_api import async_playwright

ICI = pathlib.Path(__file__).resolve().parent
def police(nom): return (ICI / f"polices/{nom}.woff2").as_uri()
POLICES = "".join(
    f"@font-face {{ font-family:'{fam}'; font-weight:{poids}; src:url('{police(f'{fam}-{poids}')}') format('woff2'); }}"
    f"@font-face {{ font-family:'{fam}'; font-weight:{poids}; src:url('{police(f'{fam}-{poids}-ext')}') format('woff2'); unicode-range:U+0100-024F,U+1E00-1EFF; }}"
    for fam, poids in [("Jost", 400), ("Jost", 500), ("Figtree", 400), ("Figtree", 500), ("Figtree", 600)])
# Logotype Cimeria, tracés repris de dominia-site/scripts/marque.mjs (charte Cimeria). Le mot reste d'un seul bloc.
LETTRES = "M33.2 -70Q33.2 -85 39.9 -96.1Q46.6 -107.2 57.4 -113.3Q68.2 -119.4 81 -119.4Q91 -119.4 99.1 -116.8Q107.2 -114.2 113.6 -109.7Q120 -105.2 124.8 -99.6V-127.6Q116.2 -135 105.9 -138.8Q95.6 -142.6 80.2 -142.6Q64.8 -142.6 51.5 -137.3Q38.2 -132 28.4 -122.3Q18.6 -112.6 13.1 -99.3Q7.6 -86 7.6 -70Q7.6 -54.2 13.1 -40.9Q18.6 -27.6 28.4 -17.8Q38.2 -8 51.5 -2.8Q64.8 2.4 80.2 2.4Q95.6 2.4 105.9 -1.4Q116.2 -5.2 124.8 -12.4V-40.6Q120 -34.8 113.6 -30.3Q107.2 -25.8 99.1 -23.2Q91 -20.6 81 -20.6Q68.2 -20.6 57.4 -26.8Q46.6 -33 39.9 -44.1Q33.2 -55.2 33.2 -70ZM181.8 -140V0H205.8V-140ZM290.8 -85.2 333.4 -13 376.2 -85.2 385.8 0H410.2L391 -147L333.4 -52L276 -147L256.8 0H281.2ZM476 0H546.6V-20.8H476ZM476 -119.2H546.6V-140H476ZM476 -64.8H542.6V-85.2H476ZM461.4 -140V0H484.6V-140ZM632.6 -66.8 677 0H705.6L658 -66.8ZM603.6 -140V0H627.2V-140ZM617.6 -119.6H645.8Q654 -119.6 660 -116.8Q666 -114 669.4 -108.8Q672.8 -103.6 672.8 -96Q672.8 -88.6 669.4 -83.3Q666 -78 660 -75.3Q654 -72.6 645.8 -72.6H617.6V-53H646.8Q662.2 -53 673.4 -58.4Q684.6 -63.8 690.9 -73.6Q697.2 -83.4 697.2 -96.6Q697.2 -109.8 690.9 -119.5Q684.6 -129.2 673.4 -134.6Q662.2 -140 646.8 -140H617.6ZM750.6 -140V0H774.6V-140ZM850.4 -36H924.4L920 -56H855ZM887 -100.4 909.4 -48.4 909.8 -42.6 928.8 0H955.6L887 -147.8L818.6 0H845.2L864.6 -43.8L865 -49Z"
def logotype(encre, rouge, largeur=250):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='7.6 -147.8 993 150.2' style='width:{largeur}px;height:auto;display:block' role='img' aria-label='Cimeria'>"
            f"<path d='{LETTRES}' fill='{encre}'/><rect x='972.6' y='-140' width='28' height='28' fill='{rouge}'/></svg>")
CLAIR = dict(fond="#F6F5F2", carte="#FFFFFF", encre="#2B2B2D", douce="#5A5A5C", rouge="#DA291C", rougeTexte="#C42518", filet="#E2E0DA")
SOMBRE = dict(fond="#2B2B2D", carte="#36363A", encre="#F6F5F2", douce="#BEBDB8", rouge="#F04A3B", rougeTexte="#FF6B5C", filet="#4A4A4E")
RACINE = pathlib.Path(".")

def e(t):
    """Échappe le texte et pose les espaces insécables de la typographie française (CHF 500, 4 %, « »)."""
    t = html.escape(str(t or ""))
    for a, b in (("CHF ", "CHF\u00a0"), (" %", "\u00a0%"), ("« ", "«\u00a0"), (" »", "\u00a0»"), (" ?", "\u202f?"), (" !", "\u202f!")):
        t = t.replace(a, b)
    return t
def img(chemin):
    p = pathlib.Path(chemin)
    return (p if p.is_absolute() else (RACINE / p)).resolve().as_uri()

def base(c, w, h):
    return f"""
{POLICES}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{w}px; height:{h}px; }}
body {{ background:{c['fond']}; color:{c['encre']}; font-family:'Figtree',sans-serif; overflow:hidden; position:relative; }}
.cadre {{ position:absolute; inset:80px; display:flex; flex-direction:column; }}
.tete {{ display:flex; justify-content:space-between; align-items:baseline; }}
.etiquette {{ color:{c['rougeTexte']}; font-family:'Jost',sans-serif; font-weight:500; font-size:32px; letter-spacing:.16em; text-transform:uppercase; }}
.compteur {{ font-family:'Jost',sans-serif; font-size:32px; font-weight:500; color:{c['douce']}; }}
.accent {{ width:80px; height:8px; background:{c['rouge']}; }}
.titre {{ font-family:'Jost',sans-serif; font-weight:500; letter-spacing:-.015em; line-height:1.08; }}
.texte {{ font-weight:400; color:{c['douce']}; letter-spacing:-.01em; line-height:1.3; font-size:46px; }}
.milieu {{ flex:1; display:flex; flex-direction:column; justify-content:center; min-height:0; }}
.pied {{ padding-top:32px; border-top:2px solid {c['filet']}; display:flex; justify-content:space-between; align-items:baseline; }}
.logo {{ display:flex; align-items:center; }}
.site {{ font-family:'Jost',sans-serif; font-size:30px; font-weight:400; letter-spacing:.02em; color:{c['douce']}; }}
"""
def pied(c, droite="cimeria.ch"):
    return f"<div class='pied'><div class='logo'>{logotype(c['encre'], c['rouge'])}</div><div class='site'>{e(droite)}</div></div>"
def tete(v, etiquette, n=None):
    cpt = f"<div class='compteur'>{e(n)} / {e(v['total'])}</div>" if v.get("total") and n else ""
    return f"<div class='tete'><div class='etiquette'>{e(etiquette)}</div>{cpt}</div>"
def page(css, corps):
    return f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><style>{css}</style></head><body>{corps}</body></html>"
def tt(t, a, b, c_): return a if len(t) <= 45 else b if len(t) <= 80 else c_

def couverture(v):
    c = SOMBRE; w, h = 1080, 1350
    fond = f"<div style='position:absolute;inset:0 0 auto 0;height:620px;background:url({img(v['image'])}) center/cover'></div><div style='position:absolute;left:0;right:0;top:420px;height:200px;background:linear-gradient(transparent,{c['fond']})'></div>" if v.get("image") else ""
    corps = f"""{fond}<div class='cadre' style='top:{600 if v.get('image') else 80}px'>
      {tete(v, v['rubrique'], 1)}
      <div class='milieu'>
        <div class='titre' style='font-size:{tt(v['titre'],108,92,78)}px'>{e(v['titre'])}</div>
        <div class='texte' style='margin-top:36px'>{e(v.get('accroche',''))}</div>
      </div>
      {pied(c, 'Faites défiler →')}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def etape(v):
    c = CLAIR; w, h = 1080, 1350
    cap = f"<div style='margin-top:40px;flex:1;min-height:0;border:2px solid {c['filet']};border-radius:8px;background:{c['carte']} url({img(v['capture'])}) top left/cover no-repeat'></div>" if v.get("capture") else ""
    corps = f"""<div class='cadre'>
      {tete(v, v['rubrique'], v.get('position'))}
      <div class='{'' if cap else 'milieu'}' style='{'margin-top:48px;display:flex;flex-direction:column;flex:1;min-height:0' if cap else ''}'>
        <div style='display:flex;align-items:baseline;gap:32px'>
          <div class='titre' style='font-size:{150 if cap else 220}px;line-height:.9'>{e(v['numero'])}</div>
          <div class='accent' style='flex:none'></div>
        </div>
        <div class='titre' style='font-size:{tt(v['titre'],76,66,58)}px;margin-top:36px'>{e(v['titre'])}</div>
        <div class='texte' style='margin-top:28px'>{e(v['texte'])}</div>
        {cap}
      </div>
      <div style='height:40px'></div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def fait(v):
    c = CLAIR; w, h = 1080, 1350
    corps = f"""<div class='cadre'>
      {tete(v, v.get('etiquette','L’IA cette semaine'), v.get('position'))}
      <div class='milieu'>
        <div class='titre' style='font-size:{tt(v['titre'],88,76,66)}px'>{e(v['titre'])}</div>
        <div style='margin-top:56px;padding-left:36px;border-left:8px solid {c['rouge']}'>
          <div class='etiquette' style='color:{c['encre']};font-size:28px'>Ce que cela change pour vous</div>
          <div class='texte' style='margin-top:18px;color:{c['encre']}'>{e(v['impact'])}</div>
        </div>
        <div class='site' style='margin-top:44px'>Source · {e(v['source'])}</div>
      </div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def fin(v):
    c = CLAIR; w, h = 1080, 1350
    corps = f"""<div class='cadre'>
      {tete(v, v.get('rubrique','Cimeria'), v.get('total'))}
      <div class='milieu'>
        <div class='accent' style='margin-bottom:44px'></div>
        <div class='titre' style='font-size:96px'>{e(v.get('titre','Enregistrez ce post pour le retrouver.'))}</div>
        <div class='texte' style='margin-top:44px'>{e(v.get('texte','Une question sur votre cas ? Écrivez-nous en message privé. L’article complet est en lien dans la bio.'))}</div>
        {f"<div style='display:flex;align-items:center;gap:28px;margin-top:56px'><div style='width:120px;height:120px;border-radius:50%;background:url({img(v['photo'])}) center 20%/cover'></div><div style='font-size:34px;line-height:1.3'><div style='font-weight:600'>{e(v['auteur'])}</div><div style='color:{c['douce']}'>{e(v.get('fonction',''))}</div></div></div>" if v.get('auteur') else ""}
      </div>
      {pied(c, '@cimeria.ch')}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def cas(v):
    c = SOMBRE; w, h = 1080, 1920   # la grille Instagram ne montre que le centre 1080 x 1440
    photo = v.get("photo", str(ICI / "images/mickael-bovagnet.jpg"))
    corps = f"""<div style='position:absolute;inset:0;background:#000'></div>
    <div style='position:absolute;left:0;right:0;top:250px;height:900px;background:url({img(photo)}) center top/cover'></div>
    <div style='position:absolute;left:0;right:0;top:250px;height:160px;background:linear-gradient(#000,transparent)'></div>
    <div style='position:absolute;left:0;right:0;top:760px;height:400px;background:linear-gradient(transparent,#000)'></div>
    <div class='cadre' style='top:960px;bottom:270px'>
      <div class='etiquette'>Cas pratique</div>
      <div class='titre' style='font-size:{tt(v['titre'],104,88,74)}px;margin-top:28px'>{e(v['titre'])}</div>
      <div class='texte' style='margin-top:28px;font-size:42px'>{e(v.get('accroche',''))}</div>
      <div style='flex:1'></div>
      <div class='pied' style='border-color:#3a3a3e'><div class='logo'>{logotype(c['encre'], c['rouge'])}</div><div class='site'>{e(v.get('signature','Mickaël Bovagnet'))}</div></div>
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def agenda_ancien(v):
    c = CLAIR; w, h = 1080, 1350
    lignes = "".join(
        f"<div style='padding:30px 0;border-top:2px solid {c['filet']}'>"
        f"<div class='etiquette' style='font-size:28px;color:{c['douce']}'>{e(x['date'])} · {e(x['lieu'])}</div>"
        f"<div class='titre' style='font-size:46px;margin-top:12px;letter-spacing:-.02em;line-height:1.12'>{e(x['titre'])}</div></div>"
        for x in v["evenements"][:3])
    corps = f"""<div class='cadre'>
      {tete(v, 'Agenda IA')}
      <div class='milieu'>
        <div class='titre' style='font-size:84px;margin-bottom:40px'>{e(v.get('titre','Cette semaine en Suisse romande'))}</div>
        {lignes}
      </div>
      {pied(c, 'cimeria.ch/agenda')}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def actualite_ancien(v):
    c = CLAIR; w, h = 1080, 1350
    corps = f"""<div class='cadre'>
      {tete(v, 'Actualité IA · ' + v['date'])}
      <div class='milieu'>
        <div class='accent' style='margin-bottom:40px'></div>
        <div class='titre' style='font-size:{tt(v['titre'],104,88,74)}px'>{e(v['titre'])}</div>
        <div class='texte' style='margin-top:40px'>{e(v.get('resume',''))}</div>
        <div class='site' style='margin-top:36px'>Source · {e(v['source'])}</div>
      </div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def demo(v):
    """Étape illustrée par une carte claire qui montre ce que produit l'IA (univers sombre).
    Champs : rubrique, position, total, numero, titre, carte {type, etiquette, ...}
    carte.type : citation (texte) | liste (elements [{fort, texte}]) | chiffre (valeur, legende, detail) | image (chemin, recadrage [x0,y0,x1,y1])"""
    c = SOMBRE; w, h = 1080, 1350
    k = v["carte"]; t = k["type"]
    if t == "citation":
        contenu = f"<div style='font-size:60px;line-height:1.22;font-weight:600;letter-spacing:-.02em'>« {e(k['texte'])} »</div>"
    elif t == "liste":
        contenu = "".join(f"<div style='display:flex;gap:24px;padding:30px 0;border-top:2px solid #ECEBE7'><div style='width:18px;height:18px;margin-top:22px;flex:none;background:#DA291C'></div><div style='font-size:48px;line-height:1.2'><b style='font-weight:600'>{e(x['fort'])}</b> {e(x.get('texte',''))}</div></div>" for x in k["elements"])
    elif t == "chiffre":
        contenu = f"<div style='font-size:230px;font-family:Jost;font-weight:500;letter-spacing:-.02em;line-height:1'>{e(k['valeur'])}</div><div style='font-size:54px;font-weight:600;margin-top:24px;line-height:1.15;letter-spacing:-.015em'>{e(k['legende'])}</div><div style='font-size:38px;color:#5A5A5C;margin-top:28px;line-height:1.3'>{e(k.get('detail',''))}</div>"
    else:
        contenu = f"<img src='{img(k['chemin_recadre'])}' style='display:block;width:100%;border-radius:4px'>"
    corps = f"""<div class='cadre'>
      {tete(v, v['rubrique'], v.get('position'))}
      <div style='display:flex;align-items:baseline;gap:32px;margin-top:56px'>
        <div class='titre' style='font-size:120px;line-height:.9;color:{c['rouge']}'>{e(v['numero'])}</div>
        <div class='titre' style='font-size:{tt(v['titre'],84,72,60)}px'>{e(v['titre'])}</div>
      </div>
      <div class='milieu'>
        <div style='background:#FFFFFF;color:#2B2B2D;border-radius:12px;padding:56px 56px;box-shadow:0 24px 60px rgba(0,0,0,.45)'>
          <div style='font-size:30px;font-family:Jost;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:#C42518;margin-bottom:32px'>{e(k['etiquette'])}</div>
          {contenu}
        </div>
      </div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def bulle_vous(texte, joint=None, taille=40):
    pj = f"<div style='display:inline-block;margin-bottom:18px;padding:10px 18px;border:2px solid #5A5A5C;border-radius:8px;font-size:28px;font-weight:600;color:#F6F5F2'>Fichiers joints · {e(joint)}</div><br>" if joint else ""
    return f"""<div style='display:flex;justify-content:flex-end'>
      <div style='max-width:86%;background:#2B2B2D;color:#F6F5F2;border-radius:28px 28px 6px 28px;padding:32px 38px'>
        <div style='font-size:24px;font-family:Jost;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:#BEBDB8;margin-bottom:14px'>Vous demandez</div>
        {pj}<div style='font-size:{taille}px;line-height:1.25;font-weight:500'>{e(texte)}</div></div></div>"""

def bulle_ia(contenu):
    return f"""<div style='display:flex;margin-top:30px'>
      <div style='width:92%;background:#FFFFFF;border:2px solid #E2E0DA;border-radius:28px 28px 28px 6px;padding:34px 38px;box-shadow:0 18px 40px rgba(43,43,45,.10)'>
        <div style='font-size:24px;font-family:Jost;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:#C42518;margin-bottom:18px'>L’IA vous rend</div>
        {contenu}</div></div>"""

def reponse(k):
    t = k["type"]
    if t == "texte":
        return f"<div style='font-size:42px;line-height:1.25;font-weight:600;letter-spacing:-.01em'>{e(k['texte'])}</div>" + (f"<div style='font-size:32px;color:#5A5A5C;margin-top:18px;line-height:1.3'>{e(k['note'])}</div>" if k.get('note') else "")
    if t == "tableau":
        lignes = "".join(f"<div style='display:flex;justify-content:space-between;gap:20px;padding:18px 0;border-top:2px solid #ECEBE7;font-size:36px'><span style='font-weight:600'>{e(a)}</span><span style='color:{'#C42518' if b=='non trouvé' else '#5A5A5C'};text-decoration:{'none' if b=='non trouvé' else 'underline'}'>{e(b)}</span></div>" for a, b in k["lignes"])
        return f"<div style='display:flex;justify-content:space-between;font-size:24px;font-family:Jost;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:#5A5A5C;padding-bottom:12px'><span>{e(k['colonnes'][0])}</span><span>{e(k['colonnes'][1])}</span></div>{lignes}"
    if t == "chiffre":
        return f"<div style='font-size:150px;font-family:Jost;font-weight:500;letter-spacing:-.02em;line-height:1'>{e(k['valeur'])}</div><div style='font-size:42px;font-weight:600;margin-top:14px;line-height:1.15'>{e(k['legende'])}</div><div style='font-size:32px;color:#5A5A5C;margin-top:16px;line-height:1.3'>{e(k.get('detail',''))}</div>"
    if t == "image":
        return f"<div style='font-size:26px;color:#5A5A5C;margin-bottom:14px'>{e(k.get('legende',''))}</div><img src='{img(k['chemin_recadre'])}' style='display:block;width:100%;border:2px solid #ECEBE7;border-radius:6px'>"
    return ""

def echange(v):
    """Une demande à l'IA et ce qu'elle rend (univers clair).
    Champs : rubrique, position, total, numero, titre, demande, joint (facultatif), carte {type...}"""
    c = CLAIR; w, h = 1080, 1350
    corps = f"""<div class='cadre'>
      {tete(v, v['rubrique'], v.get('position'))}
      <div style='display:flex;align-items:baseline;gap:28px;margin-top:40px'>
        <div class='titre' style='font-size:84px;line-height:.9;color:{c['rouge']}'>{e(v['numero'])}</div>
        <div class='titre' style='font-size:{tt(v['titre'],64,56,50)}px'>{e(v['titre'])}</div>
      </div>
      <div class='milieu'>
        {bulle_vous(v['demande'], v.get('joint'), v.get('taille_demande', 36))}
        {bulle_ia(reponse(v['carte']))}
      </div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def couverture_ia(v):
    """Couverture de cas pratique : le titre en haut, gros, lisible en vignette. L'échange naïf en dessous sert d'illustration.
    Champs : rubrique, total, titre (45 signes au plus de préférence), accroche, demande, reponse_vague, verdict"""
    c = CLAIR; w, h = 1080, 1350
    vague = (f"<div style='display:flex;margin-top:18px'><div style='max-width:86%;background:#FFFFFF;border:2px solid #E2E0DA;border-radius:24px 24px 24px 6px;padding:20px 30px;font-size:28px;color:#5A5A5C;line-height:1.3'>{e(v['reponse_vague'])}</div></div>"
             f"<div style='position:absolute;right:10px;bottom:-34px;border:4px solid #DA291C;background:{c['fond']};color:#C42518;font-family:Jost;font-weight:500;font-size:34px;letter-spacing:.12em;text-transform:uppercase;padding:10px 22px;transform:rotate(-4deg)'>{e(v['verdict'])}</div>") if v.get('verdict') else ""
    corps = f"""<div class='cadre'>
      {tete(v, v['rubrique'], 1)}
      <div class='titre' style='font-size:{tt(v['titre'],124,104,88)}px;line-height:1.02;margin-top:56px'>{e(v['titre'])}</div>
      <div class='texte' style='margin-top:30px;font-size:40px'>{e(v.get('accroche',''))}</div>
      <div class='milieu'>
        <div style='position:relative;opacity:.96'>
          <div style='display:flex;justify-content:flex-end'>
            <div style='max-width:86%;background:#2B2B2D;color:#F6F5F2;border-radius:24px 24px 6px 24px;padding:22px 30px'>
              <div style='font-size:22px;font-family:Jost;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:#BEBDB8;margin-bottom:10px'>Vous demandez</div>
              <div style='font-size:30px;line-height:1.25;font-weight:500'>{e(v['demande'])}</div></div></div>
          {vague}
        </div>
      </div>
      {pied(c, 'Faites défiler →')}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def lecon(v):
    c = CLAIR; w, h = 1080, 1350
    lignes = "".join(f"<div style='display:flex;gap:28px;padding:30px 0;border-top:2px solid {c['filet']}'><div class='titre' style='font-size:44px;width:260px;flex:none;color:{c['rougeTexte'] if i else c['encre']}'>{e(a)}</div><div class='texte' style='font-size:42px;color:{c['encre']}'>{e(b)}</div></div>" for i, (a, b) in enumerate(v["lignes"]))
    corps = f"""<div class='cadre'>
      {tete(v, v['rubrique'], v.get('position'))}
      <div class='milieu'>
        <div class='titre' style='font-size:{tt(v['titre'],84,72,62)}px;margin-bottom:44px'>{e(v['titre'])}</div>
        {lignes}
      </div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def mots(*textes): return sum(len(str(t).split()) for t in textes)

def etape_methode(v):
    """Étape de méthode IA, version allégée : la consigne en 4 C, puis deux lignes, ce que l'IA rend et ce que vous vérifiez.
    Champs : rubrique, position, total, numero, titre, consigne [[label, texte]x4], rend, verifie
    Budget : 60 mots au plus pour consigne, rend et verifie réunis. Au-delà, le script prévient.
    Une étape plus riche se répartit sur deux diapositives."""
    c = CLAIR; w, h = 1080, 1350
    lignes = "".join(f"<div style='display:flex;gap:24px;padding:20px 0;border-top:1px solid #4A4A4E'><div style='width:200px;flex:none;font-size:28px;font-family:Jost;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:#FF6B5C;padding-top:6px'>{e(a)}</div><div style='font-size:38px;line-height:1.22'>{e(b)}</div></div>" for a, b in v["consigne"])
    ligne = lambda lab, txt, coul: f"<div style='display:flex;gap:24px;padding:22px 0;border-top:2px solid {c['filet']}'><div style='width:200px;flex:none;font-size:26px;font-family:Jost;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:{coul};padding-top:6px;line-height:1.3'>{lab}</div><div style='font-size:36px;line-height:1.25'>{e(txt)}</div></div>"
    corps = f"""<div class='cadre'>
      {tete(v, v['rubrique'], v.get('position'))}
      <div style='display:flex;align-items:baseline;gap:26px;margin-top:40px'>
        <div class='titre' style='font-size:96px;line-height:.9;color:{c['rouge']}'>{e(v['numero'])}</div>
        <div class='titre' style='font-size:{tt(v['titre'],68,60,52)}px'>{e(v['titre'])}</div>
      </div>
      <div class='milieu' style='padding-top:28px'>
        <div style='background:#2B2B2D;color:#F6F5F2;border-radius:20px;padding:30px 36px 14px'>
          <div style='font-size:24px;font-family:Jost;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:#BEBDB8;margin-bottom:12px'>Ce que vous écrivez, en 4 C</div>
          {lignes}
        </div>
        <div style='margin-top:40px'>
          {ligne('L’IA vous rend', v['rend'], c['rougeTexte'])}
          {ligne('Vous vérifiez', v['verifie'], c['encre'])}
        </div>
      </div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def capture(v):
    """Le résultat réel : une vraie capture d'écran, dont le bas s'efface pour renvoyer à l'article. Univers clair.
    Champs : rubrique, position, total, numero (facultatif), titre, capture, recadrage [x0,y0,x1,y1] (facultatif),
    masque (part effacée en bas, 0,35 par défaut), legende (outil et date de la capture), suite (facultatif)"""
    c = CLAIR; w, h = 1080, 1350
    m = float(v.get("masque", .35))
    num = f"<div class='titre' style='font-size:84px;line-height:.9;color:{c['rouge']}'>{e(v['numero'])}</div>" if v.get("numero") else ""
    corps = f"""<div class='cadre'>
      {tete(v, v['rubrique'], v.get('position'))}
      <div style='display:flex;align-items:baseline;gap:26px;margin-top:40px'>
        {num}<div class='titre' style='font-size:{tt(v['titre'],68,60,52)}px'>{e(v['titre'])}</div>
      </div>
      <div style='margin-top:40px;margin-right:-80px;flex:1;min-height:0;position:relative;border-radius:16px 0 0 16px;overflow:hidden;background:#FFFFFF;border:2px solid {c['filet']};border-right:none;box-shadow:0 24px 60px rgba(43,43,45,.12)'>
        <img src='{img(v['chemin_recadre'])}' style='display:block;width:100%'>
        <div style='position:absolute;left:0;right:0;bottom:0;height:{m*100:.0f}%;background:linear-gradient(rgba(255,255,255,0),#FFFFFF 70%)'></div>
        <div style='position:absolute;left:0;right:80px;bottom:36px;text-align:center'>
          <span style='display:inline-block;background:#2B2B2D;color:#F6F5F2;font-family:Jost;font-weight:500;font-size:28px;letter-spacing:.12em;text-transform:uppercase;padding:16px 30px;border-radius:999px'>{e(v.get('suite','La suite dans l’article'))}</span>
        </div>
      </div>
      <div class='site' style='margin-top:22px;font-size:26px'>{e(v.get('legende',''))}</div>
      <div style='height:28px'></div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)


# =====================================================================
# Gabarits éditoriaux, validés par Mick le 17 novembre 2026.
# Grille fixe : rubrique en haut, titre, une seule image forte, logotype en pied.
# Le rouge ne sert qu'à la rubrique, au logo, à la barre de progression et à un chiffre clé.
# L'anthracite sert de bandeau (couverture, étapes) ou de fond plein (chiffre, point de vue).
# =====================================================================
ED_BLANC_C, ED_DOUCE_S, ED_ROUGE_S, ED_ROUGE_TS, ED_FILET_S = "#F6F5F2", "#BEBDB8", "#F04A3B", "#FF6B5C", "#4A4A4E"
# Lisibilité sur téléphone (règle du 17 novembre 2026). Un visuel de 1080 px s'affiche sur environ 390 points d'écran,
# soit un facteur 0,36. Aucun texte sous 30 px (11 points à l'écran), textes courants à 44 px au moins. Le script prévient.
ED_MIN, ED_PETIT, ED_ETIQ, ED_TEXTE = 30, 32, 30, 44
def ed_css(fond):
    c = CLAIR
    return POLICES + f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1350px; overflow:hidden; }}
body {{ background:{fond}; color:{c['encre']}; font-family:'Figtree',sans-serif; position:relative; }}
.cadre {{ position:absolute; inset:0; }}
.rub {{ position:absolute; left:80px; top:76px; font-family:'Jost',sans-serif; font-weight:500; font-size:{ED_PETIT}px; letter-spacing:.14em; text-transform:uppercase; color:{c['rougeTexte']}; }}
.cpt {{ position:absolute; right:80px; top:76px; font-family:'Jost',sans-serif; font-weight:500; font-size:{ED_PETIT}px; color:{c['douce']}; }}
.ed-titre {{ font-family:'Jost',sans-serif; font-weight:500; letter-spacing:-.015em; line-height:1.06; }}
.etiq {{ font-family:'Jost',sans-serif; font-weight:500; font-size:{ED_ETIQ}px; letter-spacing:.12em; text-transform:uppercase; color:{c['douce']}; }}
.pied {{ position:absolute; left:80px; right:80px; bottom:56px; padding-top:26px; border-top:2px solid {c['filet']}; display:flex; justify-content:space-between; align-items:center; }}
.site {{ font-family:'Jost',sans-serif; font-size:{ED_MIN}px; letter-spacing:.02em; color:{c['douce']}; }}
.ajuste {{ display:inline-block; white-space:nowrap; }}
"""
def ed_pied(droite="cimeria.ch", sombre=False):
    if sombre:
        return f"<div class='pied' style='border-top-color:{ED_FILET_S}'>{logotype(ED_BLANC_C, CLAIR['rouge'], 230)}<div class='site' style='color:{ED_DOUCE_S}'>{e(droite)}</div></div>"
    return f"<div class='pied'>{logotype(CLAIR['encre'], CLAIR['rouge'], 230)}<div class='site'>{e(droite)}</div></div>"
def ed_cpt(v, sombre=False):
    return f"<div class='cpt' style='color:{ED_DOUCE_S if sombre else CLAIR['douce']}'>{e(v['position'])} / {e(v['total'])}</div>" if v.get("position") and v.get("total") else ""
def ed_page(fond, corps): return page(ed_css(fond), f"<div class='cadre'>{corps}</div>"), (1080, 1350)
def ed_mention_ia(v):
    return f"<div style='position:absolute;right:80px;bottom:160px;font-size:{ED_MIN}px;color:rgba(246,245,242,.8)'>Portrait réalisé avec l’IA</div>" if v.get('photo_ia') else ''

def chiffre(v):
    """Chiffre clé, fond anthracite. Champs : rubrique, accent (partie rouge du chiffre), nombre (suite du chiffre), phrase, action, source.
    Exemple : accent "1", nombre " sur 3". Le chiffre est ajusté à la largeur, 8 signes au plus."""
    c = CLAIR
    corps = f"""<div class='rub' style='color:{ED_ROUGE_TS}'>{e(v.get('rubrique','Le chiffre'))}</div>
    <div id='corps' style='position:absolute;left:80px;right:80px;top:130px;bottom:160px;display:flex;flex-direction:column;overflow:hidden'>
      <div style='margin-left:-14px;font-family:Jost;font-weight:500;line-height:1;letter-spacing:-.045em;color:{ED_BLANC_C}'><span class='ajuste' data-max='{v.get('taille',360)}' data-max0='{v.get('taille',360)}'><span style='color:{ED_ROUGE_S}'>{e(v.get('accent',''))}</span>{e(v.get('nombre',''))}</span></div>
      <div class='ed-titre' data-gonfle='{v.get('taille_phrase', 64)}' style='margin-top:40px;font-size:{v.get('taille_phrase', 64)}px;line-height:1.12;color:{ED_BLANC_C}'>{e(v['phrase'])}</div>
      <div style='flex:1;min-height:56px'></div>
      <div data-gonfle='46' style='padding-top:36px;border-top:2px solid {ED_FILET_S};font-size:46px;line-height:1.3;color:{ED_BLANC_C}'>{e(v.get('action',''))}</div>
      <div style='margin-top:36px;font-size:{ED_PETIT}px;line-height:1.3;color:{ED_DOUCE_S}'>Source · {e(v['source'])}</div>
    </div>
    {ed_pied(v.get('droite','cimeria.ch'), True)}"""
    return ed_page(c['encre'], corps)

def liste(v):
    """Liste à garder, fond clair. Champs : rubrique, titre, sous, elements [[libellé, "d" ou "i"]] (10 au plus), legende (true pour Débutant / Intermédiaire), note, droite.
    Le niveau est facultatif : sans lui, pas de pastille. Les lignes se répartissent sur toute la hauteur disponible."""
    c = CLAIR
    pastille = lambda n, t=22: "" if not n else f"<div style='width:{t}px;height:{t}px;border-radius:50%;flex:none;{'background:'+c['encre'] if n=='d' else 'border:4px solid '+c['encre']}'></div>"
    n = len(v["elements"]); fs = 56 if n <= 5 else 50 if n <= 7 else 40; serre = n > 7
    if max(len(x[0]) for x in v['elements']) > 40: fs -= 8
    lignes = "".join(f"<div style='flex:1;display:flex;align-items:center;gap:30px;border-top:2px solid {c['filet']}'><div style='font-family:Jost;font-weight:500;font-size:{fs}px;width:{int(fs*1.45)}px;flex:none;color:{c['douce']}'>{k:02d}</div><div style='font-size:{fs}px;line-height:1.15;flex:1'>{e(x[0])}</div>{pastille(x[1] if len(x) > 1 else '')}</div>" for k, x in enumerate(v["elements"], 1))
    leg = f"<div style='display:flex;align-items:center;gap:14px;white-space:nowrap'>{pastille('d',20)}Débutant<span style='width:16px'></span>{pastille('i',20)}Intermédiaire</div>" if v.get("legende") else "<div></div>"
    corps = f"""<div class='rub'>{e(v.get('rubrique','À garder'))}</div>{ed_cpt(v)}
    <div id='corps' style='position:absolute;left:80px;right:80px;top:136px;bottom:160px;display:flex;flex-direction:column;overflow:hidden'>
      <div class='ed-titre' style='font-size:{tt(v['titre'],72,64,58) if serre else tt(v['titre'],80,72,64)}px'>{e(v['titre'])}</div>
      {f"<div style='font-size:{40 if serre else ED_TEXTE}px;line-height:1.25;color:{c['douce']};margin-top:18px'>{e(v['sous'])}</div>" if v.get('sous') else ''}
      <div style='flex:1;display:flex;flex-direction:column;margin-top:{24 if serre else 34}px;border-bottom:2px solid {c['filet']}'>{lignes}</div>
      <div style='display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px 30px;margin-top:22px;font-size:{ED_PETIT}px;color:{c['douce']}'>{leg}<div style='white-space:nowrap'>{e(v.get('note',''))}</div></div>
    </div>
    {ed_pied(v.get('droite','cimeria.ch'))}"""
    return ed_page(c['fond'], corps)

def point_de_vue(v):
    """Citation de Mickaël et portrait en moitié basse. Champs : rubrique, citation (sans guillemets), auteur, photo (facultatif), photo_ia (true pour une variante générée, voir images/portraits/README.md)."""
    c = CLAIR; photo = v.get("photo", str(ICI / "images/mickael-bovagnet.jpg"))
    corps = f"""<div class='rub'>{e(v.get('rubrique','Point de vue'))}</div>
    <div id='corps' style='position:absolute;left:80px;right:80px;top:136px;height:470px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden'>
      <div class='ed-titre' style='font-size:{tt(v['citation'],88,80,68)}px;line-height:1.06'>{e('« ' + v['citation'] + ' »')}</div>
      <div style='font-size:{ED_TEXTE}px;color:{c['douce']}'>{e(v.get('auteur','Mickaël Bovagnet, auteur du guide'))}</div>
    </div>
    <div style='position:absolute;left:0;right:0;top:640px;bottom:0;background:url({img(photo)}) center 18%/cover'></div>
    <div style='position:absolute;left:0;right:0;bottom:0;height:240px;background:linear-gradient(rgba(20,20,22,0),rgba(20,20,22,.88))'></div>
    {ed_mention_ia(v)}
    <div class='pied' style='border-top-color:rgba(246,245,242,.25)'>{logotype(ED_BLANC_C, c['rouge'], 230)}<div class='site' style='color:{ED_DOUCE_S}'>{e(v.get('droite','cimeria.ch'))}</div></div>"""
    return ed_page(c['fond'], corps)

def cas_couverture(v):
    """Couverture de cas pratique : bandeau anthracite avec le titre, illustration au trait en partie claire.
    Champs : rubrique, position, total, titre (50 signes au plus), sous, graphisme (image de l'article sans quadrillage, dans gabarits/graphismes, sans .png, prioritaire et toute anthracite), illustration (nom d'un fichier de gabarits/illustrations, sans .svg), note, droite."""
    c = CLAIR
    if v.get("graphisme"):
        g = (ICI / f"graphismes/{v['graphisme']}.png").as_uri()
        corps = f"""<div class='rub' style='color:{ED_ROUGE_TS}'>{e(v.get('rubrique','Cas pratique'))}</div>{ed_cpt(v, True)}
    <div id='corps' style='position:absolute;left:80px;right:80px;top:136px;height:470px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden'>
      <div class='ed-titre' style='font-size:{tt(v['titre'],104,94,88)}px;line-height:1.0;color:{ED_BLANC_C}'>{e(v['titre'])}</div>
      <div style='font-size:44px;line-height:1.25;color:{ED_DOUCE_S}'>{e(v.get('sous',''))}</div>
    </div>
    <div style='position:absolute;left:0;right:0;top:625px;height:520px;background:url({g}) center/cover no-repeat'></div>
    <div style='position:absolute;left:80px;right:80px;bottom:150px;font-size:{ED_PETIT}px;color:{ED_DOUCE_S};text-align:center'>{e(v.get('note',''))}</div>
    {ed_pied(v.get('droite','Faites défiler →'), True)}"""
        return ed_page(c['encre'], corps)
    ill = (ICI / f"illustrations/{v['illustration']}.svg").read_text() if v.get("illustration") else ""
    ill = ill.replace("<svg ", "<svg width='600' height='420' ", 1)
    corps = f"""<div style='position:absolute;left:0;right:0;top:0;height:720px;background:{c['encre']}'></div>
    <div class='rub' style='color:{ED_ROUGE_TS}'>{e(v.get('rubrique','Cas pratique'))}</div>{ed_cpt(v, True)}
    <div id='corps' style='position:absolute;left:80px;right:80px;top:136px;height:550px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden'>
      <div class='ed-titre' style='font-size:{tt(v['titre'],124,110,96)}px;line-height:1.0;color:{ED_BLANC_C}'>{e(v['titre'])}</div>
      <div style='font-size:48px;line-height:1.25;color:{ED_DOUCE_S}'>{e(v.get('sous',''))}</div>
    </div>
    <div style='position:absolute;left:0;right:0;top:740px;display:flex;justify-content:center'>{ill}</div>
    <div style='position:absolute;left:80px;right:80px;bottom:150px;font-size:{ED_PETIT}px;color:{c['douce']};text-align:center'>{e(v.get('note',''))}</div>
    {ed_pied(v.get('droite','Faites défiler →'))}"""
    return ed_page(c['fond'], corps)

def cas_etape(v):
    """Étape de cas pratique : bandeau anthracite avec la progression et le mot de l'étape, carte « Vous ajoutez », puis ce que l'IA rend et ce qui reste.
    Champs : etape, etapes (nombre total d'étapes), mot (12 signes au plus), ajout (25 mots au plus, sans guillemets), rend [1 ou 2 lignes courtes],
    reste, lib_reste (« Ce qui manque encore » par défaut, « Votre part » à la dernière étape), position, total."""
    c = CLAIR; n, tot = int(v["etape"]), int(v.get("etapes", 4))
    long = mots(v['ajout']) > 18 or sum(len(x) for x in v['rend']) + len(v['reste']) > 90; fa, fr = (46, 46) if long else (52, 50)
    barre = "<div style='display:flex;gap:12px'>" + "".join(f"<div style='flex:1;height:12px;border-radius:6px;background:{ED_ROUGE_S if i < n else ED_FILET_S}'></div>" for i in range(tot)) + "</div>"
    puce = lambda plein: f"<div style='width:30px;height:30px;border-radius:50%;flex:none;margin-top:16px;{'background:'+c['encre'] if plein else 'border:5px solid '+c['encre']}'></div>"
    rend = "".join(f"<div style='display:flex;gap:26px;font-size:{fr}px;line-height:1.25;margin-top:16px'>{puce(True)}<div>{e(x)}</div></div>" for x in v["rend"])
    lib = v.get("lib_reste", "Votre part" if n == tot else "Ce qui manque encore")
    corps = f"""<div style='position:absolute;left:0;right:0;top:0;height:500px;background:{c['encre']}'></div>
    <div class='rub' style='color:{ED_ROUGE_TS}'>Étape {n} sur {tot}</div>{ed_cpt(v, True)}
    <div style='position:absolute;left:80px;right:80px;top:140px'>{barre}</div>
    <div style='position:absolute;left:72px;top:192px;white-space:nowrap;font-family:Jost;font-weight:500;font-size:{210 if len(v['mot']) <= 9 else 168}px;line-height:1;letter-spacing:-.035em;color:{ED_BLANC_C}'>{e(v['mot'])}</div>
    <div id='corps' style='position:absolute;left:80px;right:80px;top:430px;bottom:160px;display:flex;flex-direction:column'>
      <div style='background:#FFFFFF;border-radius:18px;padding:42px 50px;box-shadow:0 20px 50px rgba(43,43,45,.12)'>
        <div class='etiq'>Vous ajoutez</div>
        <div style='font-size:{fa}px;line-height:1.25;margin-top:16px'>{e('« ' + v['ajout'] + ' »')}</div></div>
      <div style='flex:1;display:flex;flex-direction:column;justify-content:space-evenly;padding-top:20px'>
        <div><div class='etiq'>L’IA vous rend</div>{rend}</div>
        <div><div class='etiq'>{e(lib)}</div>
        <div style='display:flex;gap:26px;font-size:{fr}px;line-height:1.25;margin-top:16px;color:{c['douce']}'>{puce(False)}<div>{e(v['reste'])}</div></div></div></div></div>
    {ed_pied(v.get('droite','cimeria.ch'))}"""
    return ed_page(c['fond'], corps)

def cas_fin(v):
    """Dernière diapositive d'un carrousel : appel à l'action en partie claire, portrait de Mickaël en moitié basse.
    Champs : rubrique, titre, texte, auteur, fonction, photo (facultatif), photo_ia (true pour une variante générée), position, total."""
    c = CLAIR; photo = v.get("photo", str(ICI / "images/mickael-bovagnet.jpg"))
    corps = f"""<div class='rub'>{e(v.get('rubrique','À retenir'))}</div>{ed_cpt(v)}
    <div id='corps' style='position:absolute;left:80px;right:80px;top:136px;height:470px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden'>
      <div class='ed-titre' style='font-size:{(100 if len(v.get('titre','Enregistrez ce post pour le retrouver.')) <= 40 else 86)}px;line-height:1.04'>{e(v.get('titre','Enregistrez ce post pour le retrouver.'))}</div>
      <div style='font-size:46px;line-height:1.25;color:{c['douce']}'>{e(v.get('texte','Le prompt complet est en commentaire. L’article détaillé est en lien dans la bio.'))}</div>
    </div>
    <div style='position:absolute;left:0;right:0;top:640px;bottom:0;background:url({img(photo)}) center 18%/cover'></div>
    <div style='position:absolute;left:0;right:0;bottom:0;height:300px;background:linear-gradient(rgba(20,20,22,0),rgba(20,20,22,.9))'></div>
    <div style='position:absolute;left:80px;right:80px;bottom:{205 if v.get('photo_ia') else 160}px;font-size:38px;line-height:1.25;color:{ED_BLANC_C}'><b style='font-weight:600'>{e(v.get('auteur','Mickaël Bovagnet'))}</b><br>{e(v.get('fonction','Auteur du guide, Cimeria'))}</div>
    {ed_mention_ia(v)}
    <div class='pied' style='border-top-color:rgba(246,245,242,.25)'>{logotype(ED_BLANC_C, c['rouge'], 230)}<div class='site' style='color:{ED_DOUCE_S}'>{e(v.get('droite','@cimeria.ch'))}</div></div>"""
    return ed_page(c['fond'], corps)


def actualite(v):
    """Une actualité vérifiée, sur la grille éditoriale. Bandeau anthracite avec la date et le titre, puis le résumé, qui est concerné et la source.
    Champs : date, titre (90 signes au plus), resume (35 mots au plus), concerne (facultatif), source, rubrique, position et total, droite.
    Pour un carrousel, préférer fait_cle, plus rythmé."""
    c = CLAIR
    conc = f"<div class='etiq' style='margin-top:40px'>Qui est concerné</div><div style='font-size:{ED_TEXTE}px;line-height:1.3;margin-top:12px'>{e(v['concerne'])}</div>" if v.get("concerne") else ""
    corps = f"""<div style='position:absolute;left:0;right:0;top:0;height:620px;background:{c['encre']}'></div>
    <div class='rub' style='color:{ED_ROUGE_TS}'>{e(v.get('rubrique','Actualité IA'))}</div>{ed_cpt(v, True)}
    <div style='position:absolute;left:80px;right:80px;top:136px;font-family:Jost;font-weight:500;font-size:36px;color:{ED_DOUCE_S}'>{e(v['date'])}</div>
    <div class='ed-titre' style='position:absolute;left:80px;right:80px;top:196px;font-size:{tt(v['titre'],92,80,70)}px;line-height:1.06;color:{ED_BLANC_C}'>{e(v['titre'])}</div>
    <div id='corps' style='position:absolute;left:80px;right:80px;top:670px;bottom:160px;display:flex;flex-direction:column;overflow:hidden'>
      <div style='font-size:48px;line-height:1.28'>{e(v.get('resume',''))}</div>{conc}
      <div style='flex:1;min-height:24px'></div>
      <div style='font-size:{ED_PETIT}px;color:{c['douce']}'>Source · {e(v['source'])}</div></div>
    {ed_pied(v.get('droite','cimeria.ch'))}"""
    return ed_page(c['fond'], corps)

def agenda(v):
    """Agenda des événements IA, fond anthracite ou clair (sombre, alterné automatiquement dans un carrousel). Champs : titre, sous (facultatif), evenements [{date, titre, lieu}] (5 au plus, au-delà un carrousel de deux visuels), rubrique, position, total, note, droite.
    Les lignes se répartissent sur toute la hauteur. Seuls les organisateurs de dominia-site/src/content/organisateurs.json sont nommés."""
    c = CLAIR; sb = v.get('sombre', True)
    BL, DO, FI, RO = (ED_BLANC_C, ED_DOUCE_S, ED_FILET_S, ED_ROUGE_TS) if sb else (c['encre'], c['douce'], c['filet'], c['rougeTexte'])
    n = len(v["evenements"]); fd, ft, fl = (52, 54, 38) if n <= 3 else (44, 46, 34)
    lignes = "".join(f"<div style='flex:1;display:flex;align-items:center;gap:36px;border-top:2px solid {FI}'>"
                     f"<div style='width:{int(fd*6.2)}px;flex:none;font-family:Jost;font-weight:500;font-size:{fd}px;line-height:1.1;color:{BL}'>{e(x['date'])}</div>"
                     f"<div style='flex:1'><div style='font-size:{ft}px;line-height:1.15;font-weight:600;color:{BL}'>{e(x['titre'])}</div>"
                     f"<div style='font-size:{fl}px;line-height:1.25;margin-top:6px;color:{DO}'>{e(x['lieu'])}</div></div></div>" for x in v["evenements"])
    corps = f"""<div class='rub' style='color:{RO}'>{e(v.get('rubrique','Agenda'))}</div>{ed_cpt(v, sb)}
    <div id='corps' style='position:absolute;left:80px;right:80px;top:136px;bottom:160px;display:flex;flex-direction:column;overflow:hidden'>
      <div class='ed-titre' style='font-size:80px;color:{BL}'>{e(v.get('titre','À noter en Suisse romande'))}</div>
      {f"<div style='font-size:{ED_TEXTE}px;line-height:1.25;color:{DO};margin-top:18px'>{e(v['sous'])}</div>" if v.get('sous') else ''}
      <div style='flex:1;display:flex;flex-direction:column;margin-top:30px;border-bottom:2px solid {FI}'>{lignes}</div>
      <div style='margin-top:22px;font-size:{ED_PETIT}px;color:{DO}'>{e(v.get('note','Tout l’agenda est sur cimeria.ch/agenda.'))}</div>
    </div>
    {ed_pied(v.get('droite','cimeria.ch/agenda'), sb)}"""
    return ed_page(c['encre'] if sb else c['fond'], corps)


def fait_cle(v):
    """Un fait ancré par un élément clé en très grand (date, chiffre, nom, mot), ajusté à la largeur. Alterne fond anthracite et fond clair pour rythmer les carrousels.
    Champs : rubrique, kicker (date et source, facultatif), cle (12 signes au plus), cle_legende (une ligne si possible), titre (70 signes au plus),
    resume (25 mots au plus), pour_label et pour (facultatifs, une ligne d'usage), source, sombre (true ou false), position, total, droite."""
    c = CLAIR; s = bool(v.get("sombre"))
    encre, douce, filet = (ED_BLANC_C, ED_DOUCE_S, ED_FILET_S) if s else (c['encre'], c['douce'], c['filet'])
    kick = f"<div style='font-family:Jost;font-weight:500;font-size:36px;color:{douce};margin-bottom:10px'>{e(v['kicker'])}</div>" if v.get("kicker") else ""
    pour = (f"<div style='margin-top:34px;padding-top:28px;border-top:2px solid {filet}'><div class='etiq' style='color:{douce}'>{e(v.get('pour_label','Pour quel usage'))}</div>"
            f"<div style='font-size:46px;line-height:1.25;margin-top:12px;color:{encre};font-weight:500'>{e(v['pour'])}</div></div>") if v.get("pour") else ""
    corps = f"""<div class='rub' style='color:{ED_ROUGE_TS if s else c['rougeTexte']}'>{e(v.get('rubrique',''))}</div>{ed_cpt(v, s)}
    <div id='corps' style='position:absolute;left:80px;right:80px;top:136px;bottom:160px;display:flex;flex-direction:column;overflow:hidden'>
      {kick}
      <div style='margin-left:-10px;font-family:Jost;font-weight:500;line-height:1;letter-spacing:-.04em;color:{encre}'><span class='ajuste' data-max='{v.get('taille', 330)}' data-max0='{v.get('taille', 330)}'>{e(v['cle'])}</span></div>
      <div data-gonfle='42' style='font-size:42px;line-height:1.25;color:{douce};margin-top:18px'>{e(v.get('cle_legende',''))}</div>
      <div style='flex:1;min-height:56px;display:flex;align-items:center'><div style='width:100%;border-top:2px solid {filet}'></div></div>
      <div class='ed-titre' data-gonfle='{tt(v['titre'],74,66,60)}' style='font-size:{tt(v['titre'],74,66,60)}px;line-height:1.08;color:{encre}'>{e(v['titre'])}</div>
      <div data-gonfle='{ED_TEXTE}' style='font-size:{ED_TEXTE}px;line-height:1.3;color:{douce};margin-top:22px'>{e(v.get('resume',''))}</div>
      {pour}
      {f"<div style='font-size:{ED_PETIT}px;color:{douce};margin-top:28px'>Source · {e(v['source'])}</div>" if v.get('source') else ''}
    </div>
    {ed_pied(v.get('droite','cimeria.ch'), s)}"""
    return ed_page(c['encre'] if s else c['fond'], corps)

GABARITS = dict(fait_cle=fait_cle, chiffre=chiffre, liste=liste, point_de_vue=point_de_vue, cas_couverture=cas_couverture, cas_etape=cas_etape, cas_fin=cas_fin, capture=capture, etape_methode=etape_methode, echange=echange, couverture_ia=couverture_ia, lecon=lecon, demo=demo, couverture=couverture, etape=etape, fait=fait, fin=fin, cas=cas, agenda=agenda, actualite=actualite)

EDITORIAUX = {"fait_cle", "chiffre", "liste", "point_de_vue", "cas_couverture", "cas_etape", "cas_fin", "actualite", "agenda"}
# Agrandit chaque élément .ajuste jusqu'à la largeur disponible, sans dépasser data-max (en px).
AJUSTE = """(() => { for (const el of document.querySelectorAll('.ajuste')) {
  const max = +el.dataset.max || 300; el.style.fontSize = max + 'px';
  const dispo = el.parentElement.clientWidth; const w = el.getBoundingClientRect().width;
  if (w > dispo) el.style.fontSize = Math.floor(max * dispo / w) + 'px'; } })()"""
# Agrandit les textes marqués data-gonfle (et l'élément clé) jusqu'à remplir #corps, sans vide au milieu (demande de Mick du 17 novembre 2026).
REMPLIR = """(() => { const c = document.getElementById('corps'); if (!c) return;
  const g = [...c.querySelectorAll('[data-gonfle]')], a = [...c.querySelectorAll('.ajuste[data-max0]')]; if (!g.length) return;
  const fixe = f => { g.forEach(el => el.style.fontSize = (+el.dataset.gonfle * f) + 'px');
    a.forEach(el => { const m = +el.dataset.max0 * Math.min(1 + (f - 1) * 1.5, 1.45); el.style.fontSize = m + 'px';
      const d = el.parentElement.clientWidth, w = el.getBoundingClientRect().width; if (w > d) el.style.fontSize = Math.floor(m * d / w) + 'px'; }); };
  const ok = () => c.scrollHeight <= c.clientHeight + 1;
  let lo = 1, hi = 1.45; fixe(hi); if (ok()) return; fixe(lo); if (!ok()) return;
  for (let i = 0; i < 14; i++) { const m = (lo + hi) / 2; fixe(m); if (ok()) lo = m; else hi = m; } fixe(lo); })()"""
# Liste les textes visibles plus petits que le plancher de lisibilité.
PETITS = """(() => { const r = []; for (const el of document.body.querySelectorAll('*')) {
  if (el.closest('svg')) continue;
  const t = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join(' ').trim();
  if (t && parseFloat(getComputedStyle(el).fontSize) < %d) r.push(t.slice(0, 40)); } return r; })()""" % ED_MIN

# Jamais deux visuels anthracite à la suite dans un carrousel (demande de Mick du 17 novembre 2026) : le fond de
# fait_cle et d'agenda est fixé ici en alternance avec le visuel précédent, le champ « sombre » du JSON est ignoré.
FOND_FIXE = {"chiffre": True, "liste": False, "cas_etape": False, "cas_fin": False, "point_de_vue": False}
def alterner(visuels):
    if len(visuels) < 2: return
    prec = None
    for v in visuels:
        g = v["gabarit"]
        if g in ("fait_cle", "agenda"): v["sombre"] = (not prec) if prec is not None else True
        sombre = bool(v.get("graphisme")) if g == "cas_couverture" else v.get("sombre", True) if g in ("fait_cle", "agenda") else FOND_FIXE.get(g, False)
        if prec and sombre: print(f"ATTENTION {v.get('fichier', g)} : deux visuels anthracite à la suite")
        prec = sombre

async def main(spec, sortie):
    global RACINE
    RACINE = spec.resolve().parent
    sortie.mkdir(parents=True, exist_ok=True)
    visuels = json.loads(spec.read_text())["visuels"]
    from PIL import Image
    for i, v in enumerate(visuels, 1):
        k = v.get("carte", {})
        if v.get("gabarit") == "capture": k = v
        if k is v or k.get("type") == "image":
            if k is v: k.setdefault("chemin", v["capture"])
            src = pathlib.Path(k["chemin"]); src = src if src.is_absolute() else RACINE / src
            im = Image.open(src).convert("RGB")
            if k.get("recadrage"): im = im.crop(tuple(k["recadrage"]))
            dst = ICI / f".recadre-{i}.png"; im.save(dst); k["chemin_recadre"] = str(dst)
    async with async_playwright() as p:
        chrome = next((c for c in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser") if pathlib.Path(c).exists()), None)
        # Sans Chrome installé, Playwright prend son propre Chromium (pip install playwright && playwright install chromium).
        nav = await p.chromium.launch(**({"executable_path": chrome} if chrome else {}), args=["--no-sandbox", "--allow-file-access-from-files"])
        alterner(visuels)
        for i, v in enumerate(visuels, 1):
            doc, (w, h) = GABARITS[v["gabarit"]](v)
            tmp = ICI / f".rendu-{i}.html"; tmp.write_text(doc)
            pg = await nav.new_page(viewport={"width": w, "height": h})
            await pg.goto(tmp.as_uri()); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            await pg.evaluate(AJUSTE)
            await pg.evaluate(REMPLIR)
            nom = v.get("fichier", f"{i:02d}-{v['gabarit']}.png")
            await pg.screenshot(path=str(sortie / nom))
            if v["gabarit"] == "cas_etape" and (n := mots(v["ajout"])) > 25:
                print(f"ATTENTION {nom} : « Vous ajoutez » fait {n} mots, 25 au plus")
            if v["gabarit"] == "etape_methode" and (n := mots(*(b for _, b in v["consigne"]), v["rend"], v["verifie"])) > 60:
                print(f"ATTENTION {nom} : {n} mots, 60 au plus, alléger ou répartir sur deux diapositives")
            if await pg.evaluate("(() => { const c=document.getElementById('corps') || document.querySelector('.cadre'); return c.scrollHeight > c.clientHeight + 2; })()"):
                print(f"ATTENTION {nom} : le texte déborde, raccourcir")
            if v["gabarit"] in EDITORIAUX and (petits := await pg.evaluate(PETITS)):
                print(f"ATTENTION {nom} : texte sous {ED_MIN} px, illisible sur téléphone : " + " | ".join(petits[:4]))
            print(sortie / nom)
            await pg.close(); tmp.unlink()
            for k in (v.get('carte', {}), v):
                if k.get('chemin_recadre'): pathlib.Path(k['chemin_recadre']).unlink(missing_ok=True)
        await nav.close()

if __name__ == "__main__":
    asyncio.run(main(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])))
