"""Génère les visuels Dominia pour les réseaux sociaux à partir d'une description JSON.

Usage : python3 gabarits/generer.py visuels.json dossier/de/sortie

Le JSON contient "visuels", une liste. Chaque visuel a un "gabarit" et ses champs.
- couverture : rubrique, titre (accroche, pas le titre du site), accroche, image (graphisme de l'article), total
- etape      : rubrique, numero, total, titre, texte, capture (facultatif, chemin d'une capture d'écran)
- fait       : numero, total, titre, impact, source      (carrousel hebdomadaire d'actualité)
- fin        : titre, texte, total
- cas        : titre, accroche, photo                     (couverture de Reel, univers anthracite)
- agenda     : titre, evenements [{date, lieu, titre}]
- actualite  : date, titre, resume, source                (carte seule, LinkedIn et Facebook)
Champ commun facultatif : "fichier". Les chemins d'image sont absolus ou relatifs au fichier JSON.
Règles : textes courts et gros (lecture sur téléphone), rouge réservé à l'étiquette, au filet et au logo.
"""
import asyncio, json, pathlib, sys, html
from playwright.async_api import async_playwright

ICI = pathlib.Path(__file__).resolve().parent
POLICE = (ICI / "polices/archivo-latin-wght-normal.woff2").as_uri()
POLICE_EXT = (ICI / "polices/archivo-latin-ext-wght-normal.woff2").as_uri()
CLAIR = dict(fond="#F6F5F2", carte="#FFFFFF", encre="#2B2B2D", douce="#5A5A5C", rouge="#DA291C", rougeTexte="#C42518", filet="#E2E0DA")
SOMBRE = dict(fond="#2B2B2D", carte="#36363A", encre="#F6F5F2", douce="#BEBDB8", rouge="#F04A3B", rougeTexte="#FF6B5C", filet="#4A4A4E")
RACINE = pathlib.Path(".")

def e(t): return html.escape(str(t or ""))
def img(chemin):
    p = pathlib.Path(chemin)
    return (p if p.is_absolute() else (RACINE / p)).resolve().as_uri()

def base(c, w, h):
    return f"""
@font-face {{ font-family:'Archivo'; font-weight:100 900; src:url('{POLICE}') format('woff2'); }}
@font-face {{ font-family:'Archivo'; font-weight:100 900; src:url('{POLICE_EXT}') format('woff2'); unicode-range:U+0100-024F; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{w}px; height:{h}px; }}
body {{ background:{c['fond']}; color:{c['encre']}; font-family:'Archivo',sans-serif; overflow:hidden; position:relative; }}
.cadre {{ position:absolute; inset:80px; display:flex; flex-direction:column; }}
.tete {{ display:flex; justify-content:space-between; align-items:baseline; }}
.etiquette {{ color:{c['rougeTexte']}; font-weight:700; font-size:32px; letter-spacing:.16em; text-transform:uppercase; }}
.compteur {{ font-size:32px; font-weight:600; color:{c['douce']}; }}
.accent {{ width:80px; height:8px; background:{c['rouge']}; }}
.titre {{ font-weight:700; letter-spacing:-.03em; line-height:1.05; }}
.texte {{ font-weight:500; color:{c['douce']}; letter-spacing:-.01em; line-height:1.3; font-size:46px; }}
.milieu {{ flex:1; display:flex; flex-direction:column; justify-content:center; min-height:0; }}
.pied {{ padding-top:32px; border-top:2px solid {c['filet']}; display:flex; justify-content:space-between; align-items:baseline; }}
.logo {{ font-weight:700; font-size:50px; letter-spacing:-.035em; }}
.logo span {{ color:{c['rouge']}; }}
.site {{ font-size:32px; font-weight:500; color:{c['douce']}; }}
"""
def pied(c, droite="dominia.ch"):
    return f"<div class='pied'><div class='logo'>Domin<span>IA</span></div><div class='site'>{e(droite)}</div></div>"
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
      {tete(v, v.get('rubrique','Dominia'), v.get('total'))}
      <div class='milieu'>
        <div class='accent' style='margin-bottom:44px'></div>
        <div class='titre' style='font-size:96px'>{e(v.get('titre','Enregistrez ce post pour le retrouver.'))}</div>
        <div class='texte' style='margin-top:44px'>{e(v.get('texte','Une question sur votre cas ? Écrivez-nous en message privé. L’article complet est en lien dans la bio.'))}</div>
        {f"<div style='display:flex;align-items:center;gap:28px;margin-top:56px'><div style='width:120px;height:120px;border-radius:50%;background:url({img(v['photo'])}) center 20%/cover'></div><div style='font-size:34px;line-height:1.3'><div style='font-weight:700'>{e(v['auteur'])}</div><div style='color:{c['douce']}'>{e(v.get('fonction',''))}</div></div></div>" if v.get('auteur') else ""}
      </div>
      {pied(c, '@dominiamedia')}
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
      <div class='pied' style='border-color:#3a3a3e'><div class='logo'>Domin<span>IA</span></div><div class='site'>{e(v.get('signature','Mickaël Bovagnet'))}</div></div>
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def agenda(v):
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
      {pied(c, 'dominia.ch/agenda')}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def actualite(v):
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
        contenu = f"<div style='font-size:60px;line-height:1.22;font-weight:700;letter-spacing:-.02em'>« {e(k['texte'])} »</div>"
    elif t == "liste":
        contenu = "".join(f"<div style='display:flex;gap:24px;padding:30px 0;border-top:2px solid #ECEBE7'><div style='width:18px;height:18px;margin-top:22px;flex:none;background:#DA291C'></div><div style='font-size:48px;line-height:1.2'><b style='font-weight:700'>{e(x['fort'])}</b> {e(x.get('texte',''))}</div></div>" for x in k["elements"])
    elif t == "chiffre":
        contenu = f"<div style='font-size:230px;font-weight:800;letter-spacing:-.04em;line-height:1'>{e(k['valeur'])}</div><div style='font-size:54px;font-weight:700;margin-top:24px;line-height:1.15;letter-spacing:-.015em'>{e(k['legende'])}</div><div style='font-size:38px;color:#5A5A5C;margin-top:28px;line-height:1.3'>{e(k.get('detail',''))}</div>"
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
          <div style='font-size:30px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#C42518;margin-bottom:32px'>{e(k['etiquette'])}</div>
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
        <div style='font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#BEBDB8;margin-bottom:14px'>Vous demandez</div>
        {pj}<div style='font-size:{taille}px;line-height:1.25;font-weight:500'>{e(texte)}</div></div></div>"""

def bulle_ia(contenu):
    return f"""<div style='display:flex;margin-top:30px'>
      <div style='width:92%;background:#FFFFFF;border:2px solid #E2E0DA;border-radius:28px 28px 28px 6px;padding:34px 38px;box-shadow:0 18px 40px rgba(43,43,45,.10)'>
        <div style='font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#C42518;margin-bottom:18px'>L’IA vous rend</div>
        {contenu}</div></div>"""

def reponse(k):
    t = k["type"]
    if t == "texte":
        return f"<div style='font-size:42px;line-height:1.25;font-weight:600;letter-spacing:-.01em'>{e(k['texte'])}</div>" + (f"<div style='font-size:32px;color:#5A5A5C;margin-top:18px;line-height:1.3'>{e(k['note'])}</div>" if k.get('note') else "")
    if t == "tableau":
        lignes = "".join(f"<div style='display:flex;justify-content:space-between;gap:20px;padding:18px 0;border-top:2px solid #ECEBE7;font-size:36px'><span style='font-weight:600'>{e(a)}</span><span style='color:{'#C42518' if b=='non trouvé' else '#5A5A5C'};text-decoration:{'none' if b=='non trouvé' else 'underline'}'>{e(b)}</span></div>" for a, b in k["lignes"])
        return f"<div style='display:flex;justify-content:space-between;font-size:24px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#5A5A5C;padding-bottom:12px'><span>{e(k['colonnes'][0])}</span><span>{e(k['colonnes'][1])}</span></div>{lignes}"
    if t == "chiffre":
        return f"<div style='font-size:150px;font-weight:800;letter-spacing:-.04em;line-height:1'>{e(k['valeur'])}</div><div style='font-size:42px;font-weight:700;margin-top:14px;line-height:1.15'>{e(k['legende'])}</div><div style='font-size:32px;color:#5A5A5C;margin-top:16px;line-height:1.3'>{e(k.get('detail',''))}</div>"
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
    c = CLAIR; w, h = 1080, 1350
    corps = f"""<div class='cadre'>
      {tete(v, v['rubrique'], 1)}
      <div style='margin-top:48px;display:flex;flex-direction:column'>
        {bulle_vous(v['demande'], None, 34)}
        {f"<div style='display:flex;margin-top:22px'><div style='background:#FFFFFF;border:2px solid #E2E0DA;border-radius:28px 28px 28px 6px;padding:24px 34px;font-size:32px;color:#5A5A5C;line-height:1.3'>{e(v['reponse_vague'])}</div></div><div style='margin-top:22px;display:inline-block;align-self:flex-start;border:4px solid #DA291C;color:#C42518;font-weight:800;font-size:34px;letter-spacing:.12em;text-transform:uppercase;padding:10px 22px;transform:rotate(-3deg)'>{e(v['verdict'])}</div>" if v.get('verdict') else "<div style='display:flex;margin-top:22px'><div style='background:#FFFFFF;border:2px solid #E2E0DA;border-radius:28px 28px 28px 6px;padding:26px 34px;display:flex;gap:14px'><div style='width:18px;height:18px;border-radius:50%;background:#C42518'></div><div style='width:18px;height:18px;border-radius:50%;background:#BEBDB8'></div><div style='width:18px;height:18px;border-radius:50%;background:#BEBDB8'></div></div></div>"}
      </div>
      <div class='milieu'>
        <div class='titre' style='font-size:{tt(v['titre'],96,84,72)}px'>{e(v['titre'])}</div>
        <div class='texte' style='margin-top:32px'>{e(v.get('accroche',''))}</div>
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

def etape_methode(v):
    """Étape de méthode IA : la consigne structurée (4 C), ce que l'IA rend, ce que vous vérifiez. Univers clair.
    Champs : rubrique, position, total, numero, titre, avant (facultatif), consigne [[label, texte]x4], rend, verifie"""
    c = CLAIR; w, h = 1080, 1350
    avant = f"<div style='font-size:30px;font-weight:600;margin-top:26px;color:{c['douce']}'>Avant · {e(v['avant'])}</div>" if v.get("avant") else ""
    lignes = "".join(f"<div style='display:flex;gap:22px;padding:13px 0;border-top:1px solid #4A4A4E'><div style='width:190px;flex:none;font-size:28px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#FF6B5C;padding-top:6px'>{e(a)}</div><div style='font-size:37px;line-height:1.2'>{e(b)}</div></div>" for a, b in v["consigne"])
    corps = f"""<div class='cadre'>
      {tete(v, v['rubrique'], v.get('position'))}
      <div style='display:flex;align-items:baseline;gap:26px;margin-top:34px'>
        <div class='titre' style='font-size:84px;line-height:.9;color:{c['rouge']}'>{e(v['numero'])}</div>
        <div class='titre' style='font-size:{tt(v['titre'],64,56,50)}px'>{e(v['titre'])}</div>
      </div>
      {avant}
      <div class='milieu' style='gap:22px'>
        <div style='background:#2B2B2D;color:#F6F5F2;border-radius:20px;padding:26px 34px 16px'>
          <div style='font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#BEBDB8;margin-bottom:10px'>Ce que vous écrivez, en 4 C</div>
          {lignes}
        </div>
        <div style='background:#FFFFFF;border:2px solid {c['filet']};border-radius:20px;padding:24px 34px'>
          <div style='font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{c['rougeTexte']};margin-bottom:8px'>L’IA vous rend</div>
          <div style='font-size:34px;line-height:1.25;font-weight:600'>{e(v['rend'])}</div>
        </div>
        <div style='border-left:8px solid {c['rouge']};padding:6px 0 6px 28px'>
          <div style='font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{c['encre']};margin-bottom:8px'>Vous vérifiez</div>
          <div style='font-size:34px;line-height:1.25'>{e(v['verifie'])}</div>
        </div>
      </div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

GABARITS = dict(etape_methode=etape_methode, echange=echange, couverture_ia=couverture_ia, lecon=lecon, demo=demo, couverture=couverture, etape=etape, fait=fait, fin=fin, cas=cas, agenda=agenda, actualite=actualite)

async def main(spec, sortie):
    global RACINE
    RACINE = spec.resolve().parent
    sortie.mkdir(parents=True, exist_ok=True)
    visuels = json.loads(spec.read_text())["visuels"]
    from PIL import Image
    for i, v in enumerate(visuels, 1):
        k = v.get("carte", {})
        if k.get("type") == "image":
            src = pathlib.Path(k["chemin"]); src = src if src.is_absolute() else RACINE / src
            im = Image.open(src).convert("RGB")
            if k.get("recadrage"): im = im.crop(tuple(k["recadrage"]))
            dst = ICI / f".recadre-{i}.png"; im.save(dst); k["chemin_recadre"] = str(dst)
    async with async_playwright() as p:
        nav = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        for i, v in enumerate(visuels, 1):
            doc, (w, h) = GABARITS[v["gabarit"]](v)
            tmp = ICI / f".rendu-{i}.html"; tmp.write_text(doc)
            pg = await nav.new_page(viewport={"width": w, "height": h})
            await pg.goto(tmp.as_uri()); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            nom = v.get("fichier", f"{i:02d}-{v['gabarit']}.png")
            await pg.screenshot(path=str(sortie / nom))
            if await pg.evaluate("(() => { const c=document.querySelector('.cadre'); return c.scrollHeight > c.clientHeight + 2; })()"):
                print(f"ATTENTION {nom} : le texte déborde, raccourcir")
            print(sortie / nom)
            await pg.close(); tmp.unlink()
            if v.get('carte',{}).get('chemin_recadre'): pathlib.Path(v['carte']['chemin_recadre']).unlink()
        await nav.close()

if __name__ == "__main__":
    asyncio.run(main(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])))
