# Test een landpagina in alle talen op 390 px: JS-fouten, horizontaal scrollen, resten van de vorige taal.
# Gebruik: python3 landtest.py <land-map> <talen,komma> <url-delen,komma> [resten-regex]
# Voorbeeld: python3 landtest.py roemenie nl,en,ro "#locatie/zoo-bucuresti,#soort/caracal" "Magyar\w*|faj|hely"
# Vaste onderdelen (#locaties, #soorten, #meer, #route, #actueel, #kleur, #uitleg, #rapporteer, #tabel, #tldr) worden altijd getest.
# Uitvoer: alleen afwijkingen; schermafdrukken in uit/shots/.
import asyncio, re, os, sys
from playwright.async_api import async_playwright
S = os.path.dirname(os.path.abspath(__file__)) + "/uit/shots"; os.makedirs(S, exist_ok=True)
B = "http://localhost:8102/wildekattengids/"
land, talen = sys.argv[1], sys.argv[2].split(",")
extra = [x for x in (sys.argv[3].split(",") if len(sys.argv) > 3 and sys.argv[3] else [])]
REST = re.compile(r"\b(undefined|null|NaN" + ("|" + sys.argv[4] if len(sys.argv) > 4 else "") + r")\b")
URLS = [f"{land}/"] + [f"{land}/{h}" for h in ["#locaties", "#soorten", "#meer", "#soort/tijger", "#route", "#actueel", "#kleur", "#uitleg", "#rapporteer", "#tabel", "#tldr"] + extra] + [f"{land}-oud/"]
async def main():
    fout = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        for lang in talen:
            for u in URLS:
                ctx = await b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
                await ctx.route(re.compile(r"^https?://(?!localhost)"), lambda r: r.abort())
                p = await ctx.new_page(); errs = []
                p.on("pageerror", lambda e: errs.append(str(e)[:150]))
                await p.add_init_script(f"try{{localStorage.setItem('lang','{lang}')}}catch(e){{}}")
                await p.goto(B + u, wait_until="load"); await p.wait_for_timeout(1500)
                w = await p.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
                t = await p.evaluate("document.body.innerText")
                rest = sorted(set(REST.findall(t)))
                await p.screenshot(path=f"{S}/{re.sub(r'[^a-z0-9]+', '_', u)}_{lang}.png")
                if errs or rest or w[0] > w[1] or len(t) < 400:
                    fout += 1; print(u, lang, "breedte", w, "fouten", errs, "resten", rest, "tekst", len(t))
                await ctx.close()
        await b.close()
    print("klaar;", fout, "afwijkingen")
asyncio.run(main())
