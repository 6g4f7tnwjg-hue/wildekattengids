import asyncio, os, sys, json, re
from playwright.async_api import async_playwright
# Vergelijkt de tekst van elke pagina (390 px) tussen oud (poort 8101, = main) en nieuw (poort 8102, = werkmap). Zie servers.sh.
# Gebruik: python3 vergelijk.py <nieuw-land-map> [--opnieuw] [--alle]   (de nieuwe landpagina wordt overgeslagen)
R = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../.."); S = os.path.dirname(os.path.abspath(__file__)) + "/uit"; os.makedirs(S, exist_ok=True)
NIEUW = [a for a in sys.argv[1:] if not a.startswith("--")]
SKIP = re.compile(r"^(" + "".join(re.escape(n) + "|" for n in NIEUW) + r"spottersgids|voorbeeld-jungle|[a-z-]+-oud)(/|$)")
LG = {"nederland": ["nl","en"], "belgie": ["nl","en","fr"], "luxemburg": ["nl","en","fr","de"], "duitsland": ["nl","en","de"], "frankrijk": ["nl","en","fr"],
      "oostenrijk": ["nl","en","de"], "zwitserland": ["nl","en","de","fr","it"], "verenigd-koninkrijk": ["nl","en"], "italie": ["nl","en","it"], "spanje": ["nl","en","es"],
      "ierland": ["nl","en"], "portugal": ["nl","en","pt"], "denemarken": ["nl","en","da"], "tsjechie": ["nl","en","cs"], "zweden": ["nl","en","sv"], "noorwegen": ["nl","en","nb"], "finland": ["nl","en","fi"], "polen": ["nl","en","pl"], "hongarije": ["nl","en","hu"], "roemenie": ["nl","en","ro"]}   # nieuw land hier toevoegen
pages = []
for d, _, fs in os.walk(R):
    rel = os.path.relpath(d, R)
    if "index.html" not in fs or rel.startswith(".") or "/." in rel: continue
    rel = "" if rel == "." else rel
    if SKIP.match(rel) or rel.startswith("bron") or rel.startswith("_"): continue
    land = rel.split("/")[0]
    if rel in LG: langs = LG[rel]
    elif land in LG: langs = ["nl", LG[land][-1]] if "--alle" in sys.argv else ["nl"]
    else: langs = ["nl", "en"]
    for l in langs: pages.append((rel, l))
if "--opnieuw" in sys.argv:
    oud = json.load(open(S + "/verschillen.json")); pages = [(r, l) for r, l, _ in oud]
print(len(pages), "pagina×taal")
async def tekst(b, port, rel, lang):
    ctx = await b.new_context(viewport={"width": 390, "height": 800})
    await ctx.route(re.compile(r"^https?://(?!localhost)"), lambda r: r.abort())
    p = await ctx.new_page()
    await p.add_init_script(f"try{{localStorage.setItem('lang','{lang}')}}catch(e){{}}")
    await p.goto(f"http://localhost:{port}/wildekattengids/{rel}{'/' if rel else ''}", wait_until="load")
    await p.wait_for_timeout(600)
    t = await p.evaluate("document.body.innerText")
    await ctx.close(); return t
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        ctx = await b.new_context(viewport={"width": 390, "height": 800})
        await ctx.route(re.compile(r"^https?://(?!localhost)"), lambda r: r.abort())
        sem = asyncio.Semaphore(10); diffs = []
        async def one(rel, lang):
            async with sem:
                try:
                    a = await tekst(b, 8101, rel, lang); n = await tekst(b, 8102, rel, lang)
                except Exception as e:
                    diffs.append((rel, lang, "FOUT " + str(e)[:100])); return
                if a != n:
                    import difflib
                    d = [x for x in difflib.unified_diff(a.split("\n"), n.split("\n"), lineterm="", n=0) if x[:1] in "+-" and x[:3] not in ("+++", "---")]
                    diffs.append((rel, lang, d[:12]))
        await asyncio.gather(*(one(r, l) for r, l in pages))
        await b.close()
    json.dump(diffs, open(S + "/verschillen.json", "w"), ensure_ascii=False, indent=1)
    print(len(diffs), "verschillend")
    for r, l, d in sorted(diffs)[:400]: print(r, l, (d if isinstance(d, str) else len(d)))
asyncio.run(main())
