"""Génère les visuels Dominia pour les réseaux sociaux à partir d'une description JSON.

Usage : python3 gabarits/generer.py chemin/vers/visuel.json dossier/de/sortie

Le JSON contient une liste "visuels". Chaque visuel a un "gabarit" et ses champs :
- actualite : etiquette, date, titre, resume, source
- couverture : rubrique, titre, accroche            (première diapositive d'un carrousel)
- etape : rubrique, numero, titre, texte             (diapositive intérieure)
- fin : titre, texte                                 (dernière diapositive, renvoi au lien en bio)
- cas : titre, accroche, signature                   (couverture de Reel ou de carrousel Cas pratique, univers anthracite)
- agenda : titre, evenements [{date, titre, lieu}]
Champ commun facultatif : "fichier" (nom du PNG produit).
Couleurs, police et règles d'usage du rouge reprises du système de design DominIA.
"""
import asyncio, json, pathlib, sys, html
from playwright.async_api import async_playwright

ICI = pathlib.Path(__file__).resolve().parent
POLICE = (ICI / "polices/archivo-latin-wght-normal.woff2").as_uri()
POLICE_EXT = (ICI / "polices/archivo-latin-ext-wght-normal.woff2").as_uri()

CLAIR = dict(fond="#F6F5F2", encre="#2B2B2D", douce="#5A5A5C", rouge="#DA291C", rougeTexte="#C42518", filet="#E2E0DA")
SOMBRE = dict(fond="#2B2B2D", encre="#F6F5F2", douce="#BEBDB8", rouge="#F04A3B", rougeTexte="#FF6B5C", filet="#4A4A4E")

def e(t):
    return html.escape(str(t or ""))

def base(c, w, h):
    return f"""
@font-face {{ font-family:'Archivo'; font-weight:100 900; src:url('{POLICE}') format('woff2'); }}
@font-face {{ font-family:'Archivo'; font-weight:100 900; src:url('{POLICE_EXT}') format('woff2'); unicode-range:U+0100-024F; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{w}px; height:{h}px; }}
body {{ background:{c['fond']}; color:{c['encre']}; font-family:'Archivo',sans-serif; overflow:hidden; position:relative; }}
.cadre {{ position:absolute; inset:96px 96px 96px 96px; display:flex; flex-direction:column; }}
.etiquette {{ color:{c['rougeTexte']}; font-weight:700; font-size:30px; letter-spacing:.16em; text-transform:uppercase; }}
.accent {{ width:72px; height:6px; background:{c['rouge']}; margin-bottom:40px; }}
.titre {{ font-weight:700; letter-spacing:-.03em; line-height:1.06; }}
.texte {{ font-weight:500; color:{c['douce']}; letter-spacing:-.01em; line-height:1.35; }}
.milieu {{ flex:1; display:flex; flex-direction:column; justify-content:center; }}
.pied {{ margin-top:auto; padding-top:36px; border-top:2px solid {c['filet']}; display:flex; justify-content:space-between; align-items:baseline; }}
.logo {{ font-weight:700; font-size:46px; letter-spacing:-.035em; }}
.logo span {{ color:{c['rouge']}; }}
.site {{ font-size:28px; font-weight:500; color:{c['douce']}; }}
.source {{ font-size:26px; color:{c['douce']}; font-weight:500; margin-top:28px; }}
"""

def pied(c, droite="dominia.ch"):
    return f"<div class='pied'><div class='logo'>Domin<span>IA</span></div><div class='site'>{e(droite)}</div></div>"

def page(css, corps):
    return f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><style>{css}</style></head><body>{corps}</body></html>"

def taille_titre(t, grand, moyen, petit):
    n = len(t)
    return grand if n <= 60 else moyen if n <= 100 else petit

def actualite(v):
    c = CLAIR; w, h = 1080, 1350
    fs = taille_titre(v["titre"], 96, 80, 66)
    corps = f"""<div class='cadre'>
      <div class='accent'></div>
      <div class='etiquette'>{e(v.get('etiquette','Actualité IA'))} · {e(v['date'])}</div>
      <div class='milieu'>
      <div class='titre' style='font-size:{fs}px'>{e(v['titre'])}</div>
      <div class='texte' style='font-size:40px;margin-top:48px'>{e(v.get('resume',''))}</div>
      <div class='source'>Source · {e(v['source'])}</div>
      </div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def couverture(v):
    c = CLAIR; w, h = 1080, 1350
    fs = taille_titre(v["titre"], 104, 88, 72)
    corps = f"""<div class='cadre'>
      <div class='accent'></div>
      <div class='etiquette'>{e(v['rubrique'])}</div>
      <div class='milieu'>
      <div class='titre' style='font-size:{fs}px'>{e(v['titre'])}</div>
      <div class='texte' style='font-size:40px;margin-top:48px'>{e(v.get('accroche',''))}</div>
      </div>
      <div class='texte' style='font-size:30px;padding-bottom:40px;color:{c['encre']};font-weight:600'>Faites défiler →</div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def etape(v):
    c = CLAIR; w, h = 1080, 1350
    corps = f"""<div class='cadre'>
      <div class='etiquette'>{e(v['rubrique'])}</div>
      <div class='milieu'>
      <div class='titre' style='font-size:200px;color:{c['encre']};line-height:1'>{e(v['numero'])}</div>
      <div style='width:72px;height:6px;background:{c['rouge']};margin:36px 0 44px'></div>
      <div class='titre' style='font-size:{taille_titre(v['titre'],68,58,50)}px'>{e(v['titre'])}</div>
      <div class='texte' style='font-size:40px;margin-top:40px'>{e(v['texte'])}</div>
      </div>
      {pied(c)}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def fin(v):
    c = CLAIR; w, h = 1080, 1350
    corps = f"""<div class='cadre'>
      <div class='milieu'>
      <div class='accent'></div>
      <div class='titre' style='font-size:88px'>{e(v.get('titre','L’article complet est sur dominia.ch'))}</div>
      <div class='texte' style='font-size:40px;margin-top:48px'>{e(v.get('texte','Lien en bio. Prompts prêts à copier, sources vérifiées.'))}</div>
      </div>
      {pied(c, '@dominiamedia')}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def cas(v):
    c = SOMBRE; w, h = v.get("largeur", 1080), v.get("hauteur", 1920)
    marge = 300 if h > 1500 else 96  # zone sûre du Reel, recadré en 3:4 dans la grille
    corps = f"""<div class='cadre' style='inset:{marge}px 96px {marge}px 96px'>
      <div class='accent'></div>
      <div class='etiquette'>Cas pratique</div>
      <div class='milieu'>
      <div class='titre' style='font-size:{taille_titre(v['titre'],100,86,72)}px'>{e(v['titre'])}</div>
      <div class='texte' style='font-size:42px;margin-top:48px'>{e(v.get('accroche',''))}</div>
      <div class='texte' style='font-size:32px;margin-top:56px;color:{c['encre']};font-weight:600'>{e(v.get('signature','Par Mickaël Bovagnet'))}</div>
      </div>
      {pied(c, 'Coaching IA privé')}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

def agenda(v):
    c = CLAIR; w, h = 1080, 1350
    lignes = "".join(
        f"<div style='padding:30px 0;border-bottom:2px solid {c['filet']}'>"
        f"<div class='etiquette' style='font-size:24px;color:{c['douce']}'>{e(x['date'])} · {e(x['lieu'])}</div>"
        f"<div class='titre' style='font-size:40px;margin-top:12px;letter-spacing:-.02em;line-height:1.15'>{e(x['titre'])}</div></div>"
        for x in v["evenements"][:4])
    corps = f"""<div class='cadre'>
      <div class='accent'></div>
      <div class='etiquette'>Agenda IA</div>
      <div class='titre' style='font-size:72px;margin-top:40px;margin-bottom:24px'>{e(v.get('titre','Les rendez-vous IA de la semaine en Suisse romande'))}</div>
      {lignes}
      {pied(c, 'dominia.ch/agenda')}
    </div>"""
    return page(base(c, w, h), corps), (w, h)

GABARITS = dict(actualite=actualite, couverture=couverture, etape=etape, fin=fin, cas=cas, agenda=agenda)

async def main(spec, sortie):
    sortie.mkdir(parents=True, exist_ok=True)
    visuels = json.loads(spec.read_text())["visuels"]
    async with async_playwright() as p:
        nav = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for i, v in enumerate(visuels, 1):
            doc, (w, h) = GABARITS[v["gabarit"]](v)
            tmp = ICI / f".rendu-{i}.html"; tmp.write_text(doc)
            pg = await nav.new_page(viewport={"width": w, "height": h})
            await pg.goto(tmp.as_uri()); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
            nom = v.get("fichier", f"{i:02d}-{v['gabarit']}.png")
            await pg.screenshot(path=str(sortie / nom))
            deborde = await pg.evaluate("(() => { const c=document.querySelector('.cadre'); return c.scrollHeight > c.clientHeight + 2; })()")
            if deborde: print(f"ATTENTION {nom} : le texte déborde, raccourcir")
            print(sortie / nom)
            await pg.close(); tmp.unlink()
        await nav.close()

if __name__ == "__main__":
    asyncio.run(main(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])))
