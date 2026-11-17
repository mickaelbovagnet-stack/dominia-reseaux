"""Maquettes exploratoires du 17 novembre 2026, à valider par Mick avant tout changement de gabarit.
A. Carte unique à enregistrer : les 10 usages de l'IA pour PME (article ia-pour-pme-usages-concrets).
B. Carrousel en captures annotées : le prompt en 4 C (article comment-ecrire-un-bon-prompt).
Usage : python3 maquettes/2026-11-17/maquettes.py
"""
import asyncio, math, pathlib, sys
from PIL import Image
ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent.parent / "gabarits"))
import generer as g
from playwright.async_api import async_playwright

ENCRE, FOND, ROUGE, ROUGE_T, DOUCE, FILET = "#2B2B2D", "#F6F5F2", "#DA291C", "#C42518", "#5A5A5C", "#E2E0DA"
SRC = ICI / "sources"

def css(fond=FOND, encre=ENCRE):
    return g.POLICES + f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1350px; overflow:hidden; }}
body {{ background:{fond}; color:{encre}; font-family:'Figtree',sans-serif; position:relative; }}
.j {{ font-family:'Jost',sans-serif; font-weight:500; letter-spacing:-.02em; }}
.sur {{ background:{ROUGE}; color:#FFFFFF; padding:0 .14em; box-decoration-break:clone; -webkit-box-decoration-break:clone; }}
.trait {{ background:linear-gradient(transparent 68%, rgba(218,41,28,.85) 68%, rgba(218,41,28,.85) 90%, transparent 90%); }}
.pied {{ position:absolute; left:80px; right:80px; bottom:64px; display:flex; justify-content:space-between; align-items:center; }}
.site {{ font-family:'Jost',sans-serif; font-size:28px; letter-spacing:.02em; }}
"""
def pied(encre=ENCRE, droite="cimeria.ch", couleur=DOUCE):
    return f"<div class='pied'>{g.logotype(encre, ROUGE, 220)}<div class='site' style='color:{couleur}'>{droite}</div></div>"
def doc(c, corps): return f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><style>{c}</style></head><body>{corps}</body></html>"
def uri(p): return pathlib.Path(p).resolve().as_uri()
def e(t): return g.e(t)

# ---------- A. La roue des 10 usages ----------
USAGES = [  # (libellé court, niveau) d'après les dix titres de l'article
    ("Relire un courrier délicat", "d"), ("Résumer un contrat", "d"), ("Préparer un comité", "d"),
    ("Analyser les ventes", "i"), ("Tester un budget", "i"), ("Étudier un marché", "i"),
    ("Décrire le client idéal", "d"), ("Relancer un impayé", "d"), ("Répéter une négociation", "i"),
    ("Traduire pour Zurich", "d"),
]
def roue():
    cx, cy, r0, r1 = 540, 810, 120, 228
    n = len(USAGES); traits = []; etiquettes = []
    for k, (lib, niv) in enumerate(USAGES):
        a = -math.pi / 2 + 2 * math.pi * k / n
        x0, y0 = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
        x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        traits.append(f"<line x1='{x0:.0f}' y1='{y0:.0f}' x2='{x1:.0f}' y2='{y1:.0f}' stroke='{ENCRE}' stroke-width='3'/>"
                      f"<circle cx='{x1:.0f}' cy='{y1:.0f}' r='11' fill='{ROUGE if niv == 'i' else ENCRE}'/>")
        lx, ly = cx + (r1 + 34) * math.cos(a), cy + (r1 + 34) * math.sin(a)
        cosa = math.cos(a)
        ancre = "center" if abs(cosa) < .25 else ("left" if cosa > 0 else "right")
        tx = {"center": "-50%", "left": "0", "right": "-100%"}[ancre]
        ty = "-100%" if math.sin(a) < -.9 else ("0" if math.sin(a) > .9 else "-50%")
        num = f"<span class='j' style='color:{ROUGE_T};margin-right:8px'>{k+1}</span>"
        etiquettes.append(f"<div style='position:absolute;left:{lx:.0f}px;top:{ly:.0f}px;transform:translate({tx},{ty});width:230px;text-align:{ancre};font-size:29px;line-height:1.15;font-weight:600'>{num}{e(lib)}</div>")
    corps = f"""
    <div style='position:absolute;left:80px;right:80px;top:84px'>
      <div class='j' style='font-size:30px;letter-spacing:.16em;text-transform:uppercase;color:{ROUGE_T}'>À enregistrer</div>
      <div class='j' style='font-size:84px;line-height:1.02;margin-top:22px'><span class='trait'>10 usages</span> de l’IA pour diriger une PME</div>
      <div style='font-size:34px;color:{DOUCE};margin-top:20px'>Sans développeur ni budget, avec la version gratuite de Claude.</div>
    </div>
    <svg width='1080' height='1350' style='position:absolute;inset:0'>{''.join(traits)}
      <circle cx='{cx}' cy='{cy}' r='{r0 - 6}' fill='{ENCRE}'/></svg>
    <div style='position:absolute;left:{cx}px;top:{cy}px;transform:translate(-50%,-50%);text-align:center;color:#F6F5F2'>
      <div class='j' style='font-size:120px;line-height:.9'>10</div>
      <div style='font-size:24px;letter-spacing:.14em;text-transform:uppercase;font-family:Jost;margin-top:6px'>prompts</div>
    </div>
    {''.join(etiquettes)}
    <div style='position:absolute;left:80px;right:80px;bottom:150px;display:flex;justify-content:space-between;align-items:center;font-size:27px;color:{DOUCE}'>
      <div><span style='display:inline-block;width:20px;height:20px;border-radius:50%;background:{ENCRE};vertical-align:-2px'></span> Débutant &nbsp;&nbsp;
        <span style='display:inline-block;width:20px;height:20px;border-radius:50%;background:{ROUGE};vertical-align:-2px'></span> Intermédiaire</div>
      <div>Les 10 prompts complets sont dans l’article.</div>
    </div>
    <div style='position:absolute;left:80px;right:80px;bottom:128px;border-top:2px solid {FILET}'></div>
    {pied(droite='Lien en bio')}"""
    return doc(css(), corps)

# ---------- B. Carrousel en captures annotées ----------
def recadre(nom, box, sortie):
    Image.open(SRC / nom).convert("RGB").crop(box).save(sortie); return sortie

def capture_annotee(chemin, notes, largeur=1000):
    """notes : (x0, y0, x1, y1, libellé) en pixels de l'image recadrée. Chaque cadre porte un numéro, la légende va sous la capture."""
    im = Image.open(chemin); k = largeur / im.width
    calques = ""
    for i, (x0, y0, x1, y1, lib) in enumerate(notes, 1):
        X0, Y0, W, H = x0 * k - 8, y0 * k - 6, (x1 - x0) * k + 16, (y1 - y0) * k + 12
        calques += f"<div style='position:absolute;left:{X0:.0f}px;top:{Y0:.0f}px;width:{W:.0f}px;height:{H:.0f}px;border:5px solid {ROUGE};border-radius:10px'></div>"
        calques += f"<div class='j' style='position:absolute;left:{X0 + W - 22:.0f}px;top:{Y0 - 22:.0f}px;width:44px;height:44px;border-radius:50%;background:{ROUGE};color:#FFF;font-size:28px;display:flex;align-items:center;justify-content:center'>{i}</div>"
    return (f"<div style='position:relative;width:{largeur}px;height:{im.height * k:.0f}px;background:#FFFFFF'>"
            f"<img src='{uri(chemin)}' style='display:block;width:{largeur}px'>{calques}</div>")

def legende(notes, top):
    items = "".join(f"<div style='display:flex;align-items:center;gap:18px'><div class='j' style='width:48px;height:48px;flex:none;border-radius:50%;background:{ROUGE};color:#FFF;font-size:30px;display:flex;align-items:center;justify-content:center'>{i}</div><div style='font-size:38px;font-weight:600'>{e(n[4])}</div></div>" for i, n in enumerate(notes, 1))
    return f"<div style='position:absolute;left:80px;right:80px;top:{top}px;display:flex;flex-direction:column;gap:18px'>{items}</div>"

def compteur(n, total=5, sombre=False):
    return f"<div class='j' style='position:absolute;right:80px;top:84px;font-size:30px;color:{'#BEBDB8' if sombre else DOUCE}'>{n} / {total}</div>"

def b1():
    c1 = recadre("comment-ecrire-un-bon-prompt-1.webp", (20, 590, 1060, 1000), ICI / ".b-c1.png")
    c4 = recadre("comment-ecrire-un-bon-prompt-4.webp", (20, 280, 1060, 960), ICI / ".b-c4.png")
    carte = lambda p, rot, l, t, tampon, coul: f"""<div style='position:absolute;left:{l}px;top:{t}px;width:640px;transform:rotate({rot}deg);background:#FFF;border-radius:14px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.5)'>
        <img src='{uri(p)}' style='display:block;width:100%;height:330px;object-fit:cover;object-position:top left'>
        <div class='j' style='position:absolute;{"left" if rot < 0 else "right"}:22px;bottom:22px;border:5px solid {coul};color:{coul};background:#FFF;font-size:34px;letter-spacing:.12em;text-transform:uppercase;padding:8px 20px;transform:rotate(-4deg)'>{tampon}</div></div>"""
    corps = f"""{compteur(1, sombre=True)}
    <div style='position:absolute;left:80px;top:84px' class='j'><span style='font-size:30px;letter-spacing:.16em;text-transform:uppercase;color:#FF6B5C'>Pratique</span></div>
    <div class='j' style='position:absolute;left:80px;right:80px;top:160px;font-size:112px;line-height:1.0;color:#F6F5F2'>Même IA.<br>Même e-mail.<br><span class='sur'>Deux résultats.</span></div>
    {carte(c1, -5, 60, 560, 'Générique', '#5A5A5C')}
    {carte(c4, 4, 380, 830, 'Prêt à relire', ROUGE)}
    <div style='position:absolute;left:80px;right:80px;bottom:150px;font-size:38px;color:#F6F5F2;text-align:right'></div>
    {pied('#F6F5F2', 'Faites défiler →', '#BEBDB8')}"""
    return doc(css(ENCRE, "#F6F5F2"), corps)

def b2():
    c1 = ICI / ".b-c1.png"
    notes = [(14, 56, 432, 90, "Des raisons supposées par l’IA"), (14, 352, 146, 386, "Des trous à compléter vous-même")]
    corps = f"""{compteur(2)}
    <div style='position:absolute;left:80px;top:84px' class='j'><span style='font-size:30px;letter-spacing:.16em;text-transform:uppercase;color:{ROUGE_T}'>Avant</span></div>
    <div class='j' style='position:absolute;left:80px;right:80px;top:160px;font-size:80px;line-height:1.04'>Vous donnez le contexte. <span class='trait'>L’IA devine le reste.</span></div>
    <div style='position:absolute;left:80px;right:80px;top:370px;font-size:34px;color:{DOUCE};line-height:1.3'>« Je dirige une PME genevoise d’entretien de chauffages. Hausse de 4 %. Rédige un e-mail. »</div>
    <div style='position:absolute;left:80px;top:520px;box-shadow:0 24px 60px rgba(43,43,45,.14);border-radius:14px 0 0 14px;overflow:hidden'>{capture_annotee(c1, notes)}</div>
    {legende(notes, 960)}
    <div style='position:absolute;left:80px;right:80px;top:1110px;font-size:26px;color:{DOUCE}'>Claude, mode incognito, 6 novembre 2026. Exemple fictif.</div>
    {pied()}"""
    return doc(css(), corps)

def b3():
    lignes = [("Contexte", "Qui vous êtes et la situation."), ("Consigne", "Ce que le lecteur doit faire après lecture."),
              ("Contenu", "Vos chiffres, vos raisons, un exemple."), ("Cadre", "120 mots au plus. Signale ce que tu as supposé.")]
    bloc = "".join(f"<div style='display:flex;gap:36px;align-items:baseline;padding:34px 0;border-top:2px solid #4A4A4E'><div class='j' style='width:300px;flex:none;font-size:64px;color:{'#FF6B5C' if i else '#F6F5F2'}'><span style='color:#FF6B5C'>{l[0]}</span>{l[1:]}</div><div style='font-size:38px;line-height:1.25;color:#F6F5F2'>{e(t)}</div></div>" for i, (l, t) in enumerate(lignes))
    corps = f"""{compteur(3, sombre=True)}
    <div style='position:absolute;left:80px;top:84px' class='j'><span style='font-size:30px;letter-spacing:.16em;text-transform:uppercase;color:#FF6B5C'>La méthode</span></div>
    <div class='j' style='position:absolute;left:80px;right:80px;top:160px;font-size:88px;line-height:1.02;color:#F6F5F2'>Ajoutez <span class='sur'>4 blocs</span> à votre demande.</div>
    <div style='position:absolute;left:80px;right:80px;top:470px'>{bloc}</div>
    {pied('#F6F5F2', 'cimeria.ch', '#BEBDB8')}"""
    return doc(css(ENCRE, "#F6F5F2"), corps)

def b4():
    c4 = ICI / ".b-c4.png"
    notes = [(447, 48, 946, 80, "Vos chiffres, repris tels quels"), (12, 110, 554, 142, "Vos raisons, pas les siennes"), (12, 630, 522, 665, "La liste de ce qu’elle a supposé")]
    corps = f"""{compteur(4)}
    <div style='position:absolute;left:80px;top:84px' class='j'><span style='font-size:30px;letter-spacing:.16em;text-transform:uppercase;color:{ROUGE_T}'>Après</span></div>
    <div class='j' style='position:absolute;left:80px;right:80px;top:160px;font-size:80px;line-height:1.04'>Même IA. <span class='trait'>Prêt à relire.</span></div>
    <div style='position:absolute;left:80px;top:300px;box-shadow:0 24px 60px rgba(43,43,45,.14);border-radius:14px 0 0 14px;overflow:hidden'>{capture_annotee(c4, notes)}</div>
    {legende(notes, 980)}
    <div style='position:absolute;left:80px;right:80px;top:1192px;font-size:26px;color:{DOUCE}'></div>
    {pied(droite='Claude, 6 novembre 2026. Exemple fictif.')}"""
    return doc(css(), corps)

def b5():
    corps = f"""<div style='position:absolute;inset:0 0 auto 0;height:760px;background:url({uri(SRC / "mickael-bovagnet.jpg")}) center 22%/cover'></div>
    <div style='position:absolute;left:0;right:0;top:520px;height:240px;background:linear-gradient(rgba(43,43,45,0),{ENCRE})'></div>
    {compteur(5, sombre=True)}
    <div class='j' style='position:absolute;left:80px;right:80px;top:770px;font-size:80px;line-height:1.1;color:#F6F5F2'>Enregistrez ce post.<br><span class='sur'>Testez-le lundi.</span></div>
    <div style='position:absolute;left:80px;right:80px;top:990px;font-size:36px;line-height:1.3;color:#BEBDB8'>Le prompt complet est en commentaire. L’article détaillé est en lien dans la bio.</div>
    <div style='position:absolute;left:80px;top:1130px;font-size:30px;color:#F6F5F2'><b style='font-weight:600'>Mickaël Bovagnet</b> · Auteur du guide, Cimeria</div>
    {pied('#F6F5F2', '@cimeria.ch', '#BEBDB8')}"""
    return doc(css(ENCRE, "#F6F5F2"), corps)

async def main():
    sortie = ICI
    rendus = [("A-roue-10-usages.png", roue)] + [(f"B{i}-prompt-4c.png", f) for i, f in enumerate([b1, b2, b3, b4, b5], 1)]
    async with async_playwright() as p:
        nav = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        for nom, f in rendus:
            tmp = ICI / ".rendu.html"; tmp.write_text(f())
            pg = await nav.new_page(viewport={"width": 1080, "height": 1350})
            await pg.goto(tmp.as_uri()); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(sortie / nom)); await pg.close(); print(nom)
        await nav.close()
    for t in ICI.glob(".*.png"): t.unlink()
    (ICI / ".rendu.html").unlink(missing_ok=True)
    ims = [Image.open(sortie / n) for n, _ in rendus[1:]]
    W, H = 432, 540; pl = Image.new("RGB", (len(ims) * (W + 16) + 16, H + 32), "white")
    for i, im in enumerate(ims): pl.paste(im.resize((W, H)), (16 + i * (W + 16), 16))
    pl.save(sortie / "B-planche.png")

asyncio.run(main())
