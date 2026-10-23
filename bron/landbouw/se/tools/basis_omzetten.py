# Stap 1: cz_basis.html -> se_basis_raw.html (code cs -> sv) en sv_todo.json (alle Tsjechische teksten om te vertalen).
# Stap 2 (met --invoegen): sv_vast.json (zelfde sleutels, Zweedse tekst) -> se_basis.html.
import json, re, sys, os
D = os.path.dirname(os.path.abspath(__file__)) + "/../"
def code():
    s = open(D + "../cz/cz_basis.html", encoding="utf8").read()
    s = re.sub(r"\b(SP|R1|R5|R6|R7)CS\b", r"\1SV", s)
    s = re.sub(r"\bCS(D|M)\b", r"SV\1", s)
    s = re.sub(r"\b(RP_TYPE|ROUTENOTE|EARLIER|LBL|TITLE|MND)_CS(1?)\b", r"\1_SV\2", s)
    s = s.replace("html:not(.cs)", "html:not(.sv)").replace('"cs"', '"sv"').replace("l-cs", "l-sv").replace("html.cs", "html.sv").replace('-cs"', '-sv"')
    s = re.sub(r"\bcs:", "sv:", s)
    s = s.replace('lang="cs">CS<', 'lang="sv">SV<')
    # datum: Zweeds "22 oktober 2026" en "oktober 2026"
    s = s.replace('return LANG==="sv"?(D?`${D}. ${mn} ${Y}`:`${MND_SV1[M-1]} ${Y}`):', "return ")
    s = s.replace('LANG==="sv"?x.replace("ca. ","asi "):x', 'LANG==="sv"?x.replace("ca. ","ca ").replace(/\\./g,"\\u00a0"):x')
    for a, b in [
                 ('T("soorten","species",bySp.size<5?"druhy":"druhů")', 'T("soorten","species","arter")'),
                 ('T("soorten katachtigen","cat species",nb<5?"druhy kočkovitých šelem":"druhů kočkovitých šelem")', 'T("soorten katachtigen","cat species","kattarter")')]:
        assert s.count(a) >= 1, a; s = s.replace(a, b)
    for x, y in [('sv:["bez data","revize","nizozemská Wikipedie"]', 'sv:["odaterad","version","nederländska Wikipedia"]'), ('sv:["Asi ","let","Neznámé"]', 'sv:["Cirka ","år","Okänd"]')]:
        assert s.count(x) == 1, x; s = s.replace(x, y)
    s = re.sub(r"const MND_SV1=\[.*?\];", 'const MND_SV1=["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"];', s)
    return s
def strlit(s, i):
    """lees JS-string vanaf s[i] (quote); geef (eind_excl, inhoud)"""
    q = s[i]; j = i + 1; depth = 0
    while True:
        c = s[j]
        if c == "\\": j += 2; continue
        if q == "`" and c == "$" and s[j+1] == "{": depth += 1; j += 2; continue
        if q == "`" and depth and c == "}": depth -= 1; j += 1; continue
        if c == q and not depth: return j + 1, s[i+1:j]
        j += 1
def vind(s):
    """alle Tsjechische stukken: lijst (start, eind, tekst, soort, context)"""
    out = []
    # 1. elementen met class l-sv
    for m in re.finditer(r'<(\w+)([^>]*\bclass="[^"]*\bl-sv\b[^"]*"[^>]*)>', s):
        tag = m.group(1); a = m.end(); depth = 1; k = a
        while depth:
            o = re.compile(r"<(/?)" + tag + r"\b[^>]*>").search(s, k)
            depth += -1 if o.group(1) else 1; k = o.end()
        b = o.start()
        out.append((a, b, s[a:b], "html", ""))
    # 2. T("nl","en","cs") derde argument
    for m in re.finditer(r"(?<![\w.$])T\(", s):
        i = m.end(); args = []
        try:
            for n in range(3):
                while s[i] in " \n": i += 1
                if s[i] not in "\"'`": break
                e, t = strlit(s, i); args.append((i, e, t)); i = e
                while s[i] in " \n": i += 1
                if s[i] == ",": i += 1
                elif s[i] == ")": break
        except IndexError: continue
        if len(args) == 3:
            a, e, t = args[2]
            out.append((a + 1, e - 1, t, "T" + s[a], args[1][2]))
    # 3. constanten
    for name in ["SPSV", "SVD", "LBL_SV", "RP_TYPE_SV", "TITLE_SV", "MND_SV"]:
        m = re.search(r"const " + name + r"=(.*?);\n", s, re.S)
        out.append((m.start(1), m.end(1), m.group(1), "const:" + name, ""))
    out.sort()
    # geen overlap (T binnen l-sv-element bestaat niet in html)
    return out
if "--invoegen" not in sys.argv:
    s = code()
    open(D + "tools/se_basis_raw.html", "w", encoding="utf8").write(s)
    V = vind(s)
    todo = {f"{n:04d}": {"soort": v[3], "cs": v[2], **({"en": v[4]} if v[4] else {})} for n, v in enumerate(V)}
    json.dump(todo, open(D + "tools/sv_todo.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
    rest = s
    for a, b, *_ in reversed(V): rest = rest[:a] + rest[b:]
    left = [ln.strip()[:160] for ln in rest.split("\n") if re.search(r"[ěščřžůňťďĚŠČŘŽ]", ln)]
    print(len(V), "stukken;", len(left), "regels met Tsjechische letters over:"); [print("  ", x) for x in left[:40]]
else:
    s = open(D + "tools/se_basis_raw.html", encoding="utf8").read()
    V = vind(s); SV = json.load(open(D + "tools/sv_vast.json", encoding="utf8"))
    for n, (a, b, t, k, _) in reversed(list(enumerate(V))):
        x = SV[f"{n:04d}"]
        if not isinstance(x, str): x = json.dumps(x, ensure_ascii=False)
        s = s[:a] + x + s[b:]
    # pas na het invoegen: een nieuwe letterlijke tekst zou de nummering van de stukken verschuiven
    x = 'chosen.length<5?"vybrané lokality":"vybraných lokalit"'; assert s.count(x) == 1; s = s.replace(x, '"valda platser"')
    open(D + "se_basis.html", "w", encoding="utf8").write(s)
    print("se_basis.html geschreven")
