# Stap 1: se_basis.html -> pl_basis_raw.html (code sv -> nb) en nb_todo.json (alle Zweedse teksten om te vertalen).
# Stap 2 (met --invoegen): pl_vast.json (zelfde sleutels, Poolse tekst) -> pl_basis.html.
import json, re, sys, os
D = os.path.dirname(os.path.abspath(__file__)) + "/../"
def code():
    s = open(D + "../fi/fi_basis.html", encoding="utf8").read()
    s = re.sub(r"\b(SP|R1|R5|R6|R7)FI\b", r"\1PL", s)
    s = re.sub(r"\bFI(D|M)\b", r"PL\1", s)
    s = re.sub(r"\b(RP_TYPE|ROUTENOTE|EARLIER|LBL|TITLE|MND)_FI(1?)\b", r"\1_PL\2", s)
    s = s.replace("html:not(.fi)", "html:not(.pl)").replace('"fi"', '"pl"').replace("l-fi", "l-pl").replace("html.fi", "html.pl").replace('-fi"', '-pl"')
    s = re.sub(r"\bfi:\[", "pl:[", s); s = s.replace("fi:{get SP", "pl:{get SP")
    a = 'lang="pl">DA<'; assert s.count(a) == 1; s = s.replace(a, 'lang="pl">PL<')
    # datum: Pools "23 października 2026" (zonder punt), alleen maand: "październik 2026"
    a = '(LANG==="de"||LANG==="pl")?'; assert s.count(a) == 1; s = s.replace(a, 'LANG==="de"?')
    a = 'LANG==="pl"?x.replace(/\\./g,"\\u00a0").replace("ca\\u00a0 ","n. ")'; assert s.count(a) == 1, "wildL"; s = s.replace(a, 'LANG==="pl"?x.replace(/\\./g,"\\u00a0").replace("ca\\u00a0 ","ok. ")')
    for x, y in [('pl:["päiväämätön","versio","hollanninkielinen Wikipedia"]', 'pl:["bez daty","wersja","niderlandzka Wikipedia"]'), ('pl:["Noin ","vuotta","Tuntematon"]', 'pl:["Około ","lat","Nieznana"]')]:
        assert s.count(x) == 1, x; s = s.replace(x, y)
    a = 'const slug=s=>s.replace(/æ/g,"ae")'; assert s.count(a) == 1; s = s.replace(a, 'const slug=s=>s.replace(/ł/g,"l").replace(/Ł/g,"L").replace(/æ/g,"ae")')
    s = re.sub(r"const MND_PL1=\[.*?\];", 'const MND_PL1=["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"];', s)
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
    for m in re.finditer(r'<(\w+)([^>]*\bclass="[^"]*\bl-pl\b[^"]*"[^>]*)>', s):
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
    for name in ["SPPL", "PLD", "LBL_PL", "RP_TYPE_PL", "TITLE_PL", "MND_PL"]:
        m = re.search(r"const " + name + r"=(.*?);\n", s, re.S)
        out.append((m.start(1), m.end(1), m.group(1), "const:" + name, ""))
    out.sort()
    # geen overlap (T binnen l-sv-element bestaat niet in html)
    return out
if "--invoegen" not in sys.argv:
    s = code()
    open(D + "tools/pl_basis_raw.html", "w", encoding="utf8").write(s)
    V = vind(s)
    todo = {f"{n:04d}": {"soort": v[3], "fi": v[2], **({"en": v[4]} if v[4] else {})} for n, v in enumerate(V)}
    json.dump(todo, open(D + "tools/pl_todo.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
    rest = s
    for a, b, *_ in reversed(V): rest = rest[:a] + rest[b:]
    left = [ln.strip()[:160] for ln in rest.split("\n") if re.search(r"[äÄ]|\b(ja|tai|ei|lajia|paikkaa|eläintarha\w*|Suomessa)\b", ln)]
    print(len(V), "stukken;", len(left), "regels met Finse woorden over:"); [print("  ", x) for x in left[:40]]
else:
    s = open(D + "tools/pl_basis_raw.html", encoding="utf8").read()
    V = vind(s); SV = json.load(open(D + "tools/pl_vast.json", encoding="utf8"))
    for n, (a, b, t, k, _) in reversed(list(enumerate(V))):
        x = SV[f"{n:04d}"]
        if not isinstance(x, str): x = json.dumps(x, ensure_ascii=False)
        s = s[:a] + x + s[b:]
    open(D + "pl_basis.html", "w", encoding="utf8").write(s)
    print("pl_basis.html geschreven")
