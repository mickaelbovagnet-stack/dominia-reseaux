"""Maquettes v2 du 17 novembre 2026 : grille éditoriale fixe, une seule image forte par visuel, rouge réservé à la rubrique.
Inspiration : The Economist et Harvard Business Review sur Instagram. Pas de capture d'écran.
Usage : python3 maquettes/2026-11-17/maquettes-v2.py
"""
import asyncio, math, pathlib, sys
from PIL import Image
ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent.parent / "gabarits"))
import generer as g
from playwright.async_api import async_playwright

ENCRE, FOND, ROUGE, ROUGE_T, DOUCE, FILET, BLANC = "#2B2B2D", "#F6F5F2", "#DA291C", "#C42518", "#5A5A5C", "#E2E0DA", "#FFFFFF"
PORTRAIT = ICI.parent.parent / "gabarits/images/mickael-bovagnet.jpg"
e = g.e

CSS = g.POLICES + f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1350px; overflow:hidden; }}
body {{ background:{FOND}; color:{ENCRE}; font-family:'Figtree',sans-serif; position:relative; }}
.rub {{ position:absolute; left:80px; top:84px; font-family:'Jost',sans-serif; font-weight:500; font-size:28px; letter-spacing:.16em; text-transform:uppercase; color:{ROUGE_T}; }}
.cpt {{ position:absolute; right:80px; top:84px; font-family:'Jost',sans-serif; font-weight:500; font-size:28px; color:{DOUCE}; }}
.titre {{ position:absolute; left:80px; right:80px; top:146px; font-family:'Jost',sans-serif; font-weight:500; letter-spacing:-.015em; line-height:1.08; }}
.sous {{ font-family:'Figtree',sans-serif; font-weight:400; font-size:36px; line-height:1.3; color:{DOUCE}; letter-spacing:0; margin-top:26px; }}
.pied {{ position:absolute; left:80px; right:80px; bottom:60px; padding-top:28px; border-top:2px solid {FILET}; display:flex; justify-content:space-between; align-items:center; }}
.site {{ font-family:'Jost',sans-serif; font-size:28px; letter-spacing:.02em; color:{DOUCE}; }}
"""
def page(corps): return f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{corps}</body></html>"
def pied(droite="cimeria.ch", encre=ENCRE): return f"<div class='pied'>{g.logotype(encre, ROUGE, 210)}<div class='site'>{e(droite)}</div></div>"
def tete(rubrique, titre, sous="", taille=76, cpt=""):
    c = f"<div class='cpt'>{cpt}</div>" if cpt else ""
    return f"<div class='rub'>{e(rubrique)}</div>{c}<div class='titre' style='font-size:{taille}px'>{e(titre)}<div class='sous'>{e(sous)}</div></div>"

# 1. Chiffre clé : une PME sur trois (étude AXA 2025, citée dans l'article ia-pour-pme-usages-concrets)
def chiffre():
    rond = lambda plein: f"<div style='width:250px;height:250px;border-radius:50%;{'background:'+ENCRE if plein else 'border:6px solid '+ENCRE}'></div>"
    corps = f"""{tete('Le chiffre', 'Une PME sur trois s’est fixé des règles.', 'Parmi les PME suisses qui utilisent l’IA, seul un tiers a des règles claires de protection des données.', 72)}
    <div style='position:absolute;left:80px;right:80px;top:600px;display:flex;justify-content:space-between'>{rond(True)}{rond(False)}{rond(False)}</div>
    <div style='position:absolute;left:80px;right:80px;top:900px;display:flex;justify-content:space-between;font-size:32px;line-height:1.3;text-align:center'>
      <div style='width:250px;font-weight:600'>Avec des règles claires</div><div style='width:250px;color:{DOUCE}'>Sans règles claires</div><div style='width:250px;color:{DOUCE}'>Sans règles claires</div></div>
    <div style='position:absolute;left:80px;right:80px;top:1130px;font-size:26px;color:{DOUCE}'>Source · AXA, étude sur le marché du travail des PME, édition 2025.</div>
    {pied()}"""
    return page(corps)

# 2. La carte à enregistrer, version sobre : liste numérotée en deux colonnes, pas de rouge hors rubrique
USAGES = [("Relire un courrier délicat", "d"), ("Résumer un contrat", "d"), ("Préparer un comité", "d"), ("Analyser les ventes", "i"),
          ("Tester un budget", "i"), ("Étudier un marché", "i"), ("Décrire le client idéal", "d"), ("Relancer un impayé", "d"),
          ("Répéter une négociation", "i"), ("Traduire pour Zurich", "d")]
def usages():
    ligne = lambda k, lib, niv: (f"<div style='display:flex;align-items:center;gap:30px;padding:9px 0;border-top:2px solid {FILET}'>"
        f"<div style='font-family:Jost;font-weight:500;font-size:36px;width:56px;flex:none'>{k:02d}</div>"
        f"<div style='font-size:35px;line-height:1.2;flex:1'>{e(lib)}</div>"
        f"<div style='width:16px;height:16px;border-radius:50%;flex:none;{'background:'+ENCRE if niv=='d' else 'border:3px solid '+ENCRE}'></div></div>")
    col = lambda a, b: "".join(ligne(k + 1, *USAGES[k]) for k in range(a, b))
    corps = f"""{tete('À garder', '10 usages de l’IA pour diriger une PME', 'Sans développeur ni budget, version gratuite comprise.', 72)}
    <div style='position:absolute;left:80px;right:80px;top:420px'>{col(0, 10)}</div>
    <div style='position:absolute;left:80px;right:80px;top:1172px;display:flex;justify-content:space-between;font-size:26px;color:{DOUCE}'>
      <div><span style='display:inline-block;width:16px;height:16px;border-radius:50%;background:{ENCRE}'></span>&nbsp; Débutant &nbsp;&nbsp;&nbsp;<span style='display:inline-block;width:16px;height:16px;border-radius:50%;border:3px solid {ENCRE}'></span>&nbsp; Intermédiaire</div>
      <div>Les 10 prompts sont dans l’article.</div></div>
    {pied('Lien en bio')}"""
    return page(corps)

# 3. Point de vue, portrait (citation de Mickaël tirée de l'article comment-ecrire-un-bon-prompt)
def point_de_vue():
    corps = f"""<div style='position:absolute;left:0;right:0;top:0;height:640px;background:{FOND}'></div>
    {tete('Point de vue', '« La consigne a fait la différence, pas la formulation. »', '', 70)}
    <div style='position:absolute;left:80px;top:470px;font-size:30px;color:{DOUCE}'>Mickaël Bovagnet, auteur du guide</div>
    <div style='position:absolute;left:0;right:0;top:600px;bottom:0;background:url({PORTRAIT.resolve().as_uri()}) center 18%/cover'></div>
    <div style='position:absolute;left:0;right:0;bottom:0;height:220px;background:linear-gradient(rgba(20,20,22,0),rgba(20,20,22,.85))'></div>
    <div class='pied' style='border-top-color:rgba(246,245,242,.25)'>{g.logotype('#F6F5F2', ROUGE, 210)}<div class='site' style='color:#BEBDB8'>cimeria.ch</div></div>"""
    return page(corps)

# 4. Cas pratique, couverture illustrée (dessin au trait, un seul détail rouge)
def illustration_email():
    return f"""<svg viewBox='0 0 600 420' width='600' height='420' fill='none' stroke='{ENCRE}' stroke-width='6' stroke-linejoin='round' stroke-linecap='round'>
      <rect x='40' y='70' width='440' height='300' rx='14' fill='{BLANC}'/>
      <path d='M40 84 L260 240 L480 84'/>
      <path d='M40 356 L200 210 M480 356 L320 210'/>
      <g transform='translate(400 20) rotate(12)'>
        <path d='M0 30 L30 0 L170 0 L170 120 L30 120 L0 90 Z' fill='{FOND}'/>
        <circle cx='26' cy='60' r='9' fill='{ROUGE}' stroke='none'/>
        <text x='100' y='78' text-anchor='middle' font-family='Jost' font-weight='500' font-size='54' fill='{ENCRE}' stroke='none'>+4 %</text>
      </g></svg>"""
def couverture_cas():
    corps = f"""{tete('Cas pratique', 'Annoncer une hausse de prix avec l’IA', 'Un e-mail prêt à relire en 4 étapes. Exemple fictif d’une PME genevoise.', 80, '1 / 6')}
    <div style='position:absolute;left:0;right:0;top:600px;display:flex;justify-content:center'>{illustration_email()}</div>
    {pied('Faites défiler →')}"""
    return page(corps)

# 5. Cas pratique, une étape : un seul bloc, peu de mots
def etape():
    corps = f"""<div class='rub'>Étape 1 sur 4</div><div class='cpt'>2 / 6</div>
    <div style='position:absolute;left:80px;top:150px;font-family:Jost;font-weight:500;font-size:200px;line-height:1'>Contexte</div>
    <div style='position:absolute;left:80px;right:80px;top:400px;font-size:44px;line-height:1.3'>Dites qui vous êtes et où vous en êtes, comme à un nouveau collaborateur.</div>
    <div style='position:absolute;left:80px;right:80px;top:640px;background:{BLANC};border-radius:16px;padding:48px 52px;border:2px solid {FILET}'>
      <div style='font-family:Jost;font-weight:500;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:{DOUCE};margin-bottom:22px'>Vous écrivez</div>
      <div style='font-size:40px;line-height:1.35'>Je dirige une PME genevoise de 18 collaborateurs, spécialisée dans l’entretien de chauffages. Nous augmentons le contrat annuel de 4 %.</div></div>
    <div style='position:absolute;left:80px;right:80px;top:1060px;font-size:34px;line-height:1.3;color:{DOUCE}'>L’e-mail parle enfin de vos clients. Il reste vague sur le montant.</div>
    {pied()}"""
    return page(corps)

RENDUS = [("v2-1-chiffre.png", chiffre), ("v2-2-usages.png", usages), ("v2-3-point-de-vue.png", point_de_vue),
          ("v2-4-cas-couverture.png", couverture_cas), ("v2-5-cas-etape.png", etape)]

async def main():
    async with async_playwright() as p:
        nav = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        for nom, f in RENDUS:
            tmp = ICI / ".rendu.html"; tmp.write_text(f())
            pg = await nav.new_page(viewport={"width": 1080, "height": 1350})
            await pg.goto(tmp.as_uri()); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(ICI / nom)); await pg.close()
        await nav.close()
    (ICI / ".rendu.html").unlink(missing_ok=True)
    ims = [Image.open(ICI / n) for n, _ in RENDUS]
    W, H = 432, 540; pl = Image.new("RGB", (len(ims) * (W + 16) + 16, H + 32), "white")
    for i, im in enumerate(ims): pl.paste(im.resize((W, H)), (16 + i * (W + 16), 16))
    pl.save(ICI / "v2-planche.png")

asyncio.run(main())
