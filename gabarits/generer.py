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
    c = SOMBRE; w, h = 1080, 1350
    corps = f"""<div class='cadre'>
      {tete(v, v.get('rubrique','Dominia'), v.get('total'))}
      <div class='milieu'>
        <div class='accent' style='margin-bottom:44px'></div>
        <div class='titre' style='font-size:96px'>{e(v.get('titre','Enregistrez ce post pour le retrouver.'))}</div>
        <div class='texte' style='margin-top:44px'>{e(v.get('texte','Une question sur votre cas ? Écrivez-nous en message privé. L’article complet est en lien dans la bio.'))}</div>
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

GABARITS = dict(demo=demo, couverture=couverture, etape=etape, fait=fait, fin=fin, cas=cas, agenda=agenda, actualite=actualite)

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
