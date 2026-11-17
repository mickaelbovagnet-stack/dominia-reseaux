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
def illustration_email(k=0.0):
    w, h = (600, 420) if not k else (620, 434)
    return f"""<svg viewBox='0 0 600 420' width='{w}' height='{h}' fill='none' stroke='{ENCRE}' stroke-width='6' stroke-linejoin='round' stroke-linecap='round'>
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

# ---------- v3 : chiffre lisible et étape avec plus d'impact ----------
def chiffre_v3():
    corps = f"""<div class='rub'>Le chiffre</div>
    <div style='position:absolute;left:72px;top:150px;font-family:Jost;font-weight:500;font-size:330px;line-height:1;letter-spacing:-.04em'>1 sur 3</div>
    <div style='position:absolute;left:80px;right:80px;top:520px;font-family:Jost;font-weight:500;font-size:58px;line-height:1.15;letter-spacing:-.01em'>Seule une PME suisse sur trois qui utilise l’IA a fixé des règles claires pour protéger ses données.</div>
    <div style='position:absolute;left:80px;right:80px;top:840px;padding-top:40px;border-top:2px solid {FILET};font-size:40px;line-height:1.35'>
      Une page suffit. Elle dit ce qui entre dans l’outil, ce qui n’y entre jamais et qui relit avant l’envoi.</div>
    <div style='position:absolute;left:80px;right:80px;top:1150px;font-size:26px;color:{DOUCE}'>Source · AXA, étude sur le marché du travail des PME, édition 2025.</div>
    {pied()}"""
    return page(corps)

def progression(n, total=4):
    return "<div style='display:flex;gap:12px'>" + "".join(
        f"<div style='flex:1;height:12px;border-radius:6px;{'background:'+ENCRE if i < n else 'border:2px solid '+ENCRE}'></div>" for i in range(total)) + "</div>"

def etape_v3(n, mot, ajout, gains, reste, lib_reste="Ce qui manque encore", cpt=""):
    puce = lambda plein: f"<div style='width:26px;height:26px;border-radius:50%;flex:none;margin-top:12px;{'background:'+ENCRE if plein else 'border:4px solid '+ENCRE}'></div>"
    lignes = "".join(f"<div style='display:flex;gap:24px;font-size:40px;line-height:1.3;margin-top:18px'>{puce(True)}<div>{e(x)}</div></div>" for x in gains)
    corps = f"""<div class='rub'>Étape {n} sur 4</div><div class='cpt'>{cpt}</div>
    <div style='position:absolute;left:80px;right:80px;top:150px'>{progression(n)}</div>
    <div style='position:absolute;left:74px;top:210px;font-family:Jost;font-weight:500;font-size:170px;line-height:1;letter-spacing:-.03em'>{e(mot)}</div>
    <div style='position:absolute;left:80px;right:80px;top:430px;border-left:8px solid {ENCRE};padding:6px 0 6px 40px'>
      <div style='font-family:Jost;font-weight:500;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:{DOUCE}'>Vous ajoutez</div>
      <div style='font-size:46px;line-height:1.3;margin-top:14px'>« {e(ajout)} »</div></div>
    <div style='position:absolute;left:80px;right:80px;top:800px'>
      <div style='font-family:Jost;font-weight:500;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:{DOUCE}'>L’IA vous rend</div>{lignes}
      <div style='font-family:Jost;font-weight:500;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:{DOUCE};margin-top:44px'>{e(lib_reste)}</div>
      <div style='display:flex;gap:24px;font-size:40px;line-height:1.3;margin-top:18px;color:{DOUCE}'>{puce(False)}<div>{e(reste)}</div></div></div>
    {pied()}"""
    return page(corps)

def etape1(): return etape_v3(1, "Contexte", "Je dirige une PME genevoise d’entretien de chauffages. Hausse de 4 % au 1er\u00a0janvier.",
                             ["Un e-mail qui parle de vos clients."], "Le montant et les raisons restent vagues.", cpt="2 / 6")
def etape4(): return etape_v3(4, "Cadre", "120 mots au plus. Signale-moi ce que tu as dû inventer.",
                             ["Un e-mail de 105 mots.", "La liste de ce que l’IA a supposé."],
                             "Vous relisez avant l’envoi.", lib_reste="Votre part", cpt="5 / 6")

RENDUS = [("v3-1-chiffre.png", chiffre_v3), ("v3-5-etape-1.png", etape1), ("v3-5-etape-4.png", etape4)]

# ---------- v4 : plus de présence, par le contraste anthracite et un seul accent rouge ----------
R_SOMBRE, BLANC_C, DOUCE_S = "#F04A3B", "#F6F5F2", "#BEBDB8"
def chiffre_v4():
    corps = f"""<div style='position:absolute;inset:0;background:{ENCRE}'></div>
    <div class='rub' style='color:#FF6B5C'>Le chiffre</div>
    <div style='position:absolute;left:66px;top:140px;white-space:nowrap;font-family:Jost;font-weight:500;font-size:345px;line-height:1;letter-spacing:-.045em;color:{BLANC_C}'><span style='color:{R_SOMBRE}'>1</span> sur 3</div>
    <div style='position:absolute;left:80px;right:80px;top:560px;font-family:Jost;font-weight:500;font-size:62px;line-height:1.14;letter-spacing:-.01em;color:{BLANC_C}'>Seule une PME suisse sur trois qui utilise l’IA a fixé des règles claires pour protéger ses données.</div>
    <div style='position:absolute;left:80px;right:80px;top:850px;padding-top:44px;border-top:2px solid #4A4A4E;font-size:46px;line-height:1.35;color:{DOUCE_S}'>
      Une page suffit. Elle dit ce qui entre dans l’outil, ce qui n’y entre jamais et qui relit avant l’envoi.</div>
    <div style='position:absolute;left:80px;right:80px;top:1168px;font-size:26px;color:{DOUCE_S}'>Source · AXA, étude sur le marché du travail des PME, édition 2025.</div>
    <div class='pied' style='border-top-color:#4A4A4E'>{g.logotype(BLANC_C, ROUGE, 210)}<div class='site' style='color:{DOUCE_S}'>cimeria.ch</div></div>"""
    return page(corps)

def bandeau(hauteur):
    return f"<div style='position:absolute;left:0;right:0;top:0;height:{hauteur}px;background:{ENCRE}'></div>"

def progression_v4(n, total=4):
    return "<div style='display:flex;gap:12px'>" + "".join(
        f"<div style='flex:1;height:12px;border-radius:6px;background:{R_SOMBRE if i < n else '#4A4A4E'}'></div>" for i in range(total)) + "</div>"

def etape_v4(n, mot, ajout, gains, reste, lib_reste="Ce qui manque encore", cpt=""):
    puce = lambda plein: f"<div style='width:30px;height:30px;border-radius:50%;flex:none;margin-top:13px;{'background:'+ENCRE if plein else 'border:5px solid '+ENCRE}'></div>"
    lignes = "".join(f"<div style='display:flex;gap:26px;font-size:46px;line-height:1.28;margin-top:20px'>{puce(True)}<div>{e(x)}</div></div>" for x in gains)
    etiq = lambda t, m=0: f"<div style='font-family:Jost;font-weight:500;font-size:28px;letter-spacing:.14em;text-transform:uppercase;color:{DOUCE};margin-top:{m}px'>{t}</div>"
    corps = f"""{bandeau(500)}
    <div class='rub' style='color:#FF6B5C'>Étape {n} sur 4</div><div class='cpt' style='color:{DOUCE_S}'>{cpt}</div>
    <div style='position:absolute;left:80px;right:80px;top:150px'>{progression_v4(n)}</div>
    <div style='position:absolute;left:72px;top:200px;font-family:Jost;font-weight:500;font-size:200px;line-height:1;letter-spacing:-.035em;color:{BLANC_C}'>{e(mot)}</div>
    <div style='position:absolute;left:80px;right:80px;top:430px;bottom:170px;display:flex;flex-direction:column'>
      <div style='background:{BLANC};border-radius:18px;padding:44px 52px;box-shadow:0 20px 50px rgba(43,43,45,.12)'>
        {etiq('Vous ajoutez')}
        <div style='font-size:50px;line-height:1.28;margin-top:16px'>« {e(ajout)} »</div></div>
      <div style='flex:1;display:flex;flex-direction:column;justify-content:center;padding-top:36px'>
        {etiq('L’IA vous rend')}{lignes}
        {etiq(e(lib_reste), 52)}
        <div style='display:flex;gap:26px;font-size:46px;line-height:1.28;margin-top:20px;color:{DOUCE}'>{puce(False)}<div>{e(reste)}</div></div></div></div>
    {pied()}"""
    return page(corps)

def etape1_v4(): return etape_v4(1, "Contexte", "Je dirige une PME genevoise d’entretien de chauffages. Hausse de 4 % au 1er\u00a0janvier.",
                             ["Un e-mail qui parle de vos clients."], "Le montant et les raisons restent vagues.", cpt="2 / 6")
def etape4_v4(): return etape_v4(4, "Cadre", "120 mots au plus. Signale-moi ce que tu as dû inventer.",
                             ["Un e-mail de 105 mots.", "La liste de ce que l’IA a supposé."],
                             "Vous relisez avant l’envoi.", lib_reste="Votre part", cpt="5 / 6")

def couverture_v4():
    corps = f"""{bandeau(700)}
    <div class='rub' style='color:#FF6B5C'>Cas pratique</div><div class='cpt' style='color:{DOUCE_S}'>1 / 6</div>
    <div class='titre' style='font-size:118px;line-height:1.02;color:{BLANC_C}'>Annoncer une hausse de prix avec l’IA<div class='sous' style='color:{DOUCE_S};font-size:42px;margin-top:30px'>Un e-mail prêt à relire en 4 étapes.</div></div>
    <div style='position:absolute;left:0;right:0;top:730px;display:flex;justify-content:center'>{illustration_email(1.0)}</div>
    <div style='position:absolute;left:80px;right:80px;top:1172px;font-size:26px;color:{DOUCE};text-align:center'>Exemple fictif d’une PME genevoise de 18 collaborateurs.</div>
    {pied('Faites défiler →')}"""
    return page(corps)

RENDUS = [("v4-chiffre.png", chiffre_v4), ("v4-couverture.png", couverture_v4), ("v4-etape-1.png", etape1_v4), ("v4-etape-4.png", etape4_v4)]

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
    pl.save(ICI / "v4-planche.png")

asyncio.run(main())
