# Stap 1: se_basis.html -> no_basis_raw.html (code sv -> nb) en nb_todo.json (alle Zweedse teksten om te vertalen).
# Stap 2 (met --invoegen): nb_vast.json (zelfde sleutels, Noorse tekst) -> no_basis.html.
import json, re, sys, os
D = os.path.dirname(os.path.abspath(__file__)) + "/../"
def code():
    s = open(D + "../se/se_basis.html", encoding="utf8").read()
    s = re.sub(r"\b(SP|R1|R5|R6|R7)SV\b", r"\1NB", s)
    s = re.sub(r"\bSV(D|M)\b", r"NB\1", s)
    s = re.sub(r"\b(RP_TYPE|ROUTENOTE|EARLIER|LBL|TITLE|MND)_SV(1?)\b", r"\1_NB\2", s)
    s = s.replace("html:not(.sv)", "html:not(.nb)").replace('"sv"', '"nb"').replace("l-sv", "l-nb").replace("html.sv", "html.nb").replace('-sv"', '-nb"')
    s = re.sub(r"\bsv:", "nb:", s)
    s = s.replace('lang="sv">SV<', 'lang="nb">NB<')
    # datum: Noors "22. oktober 2026"
    a = 'return D?(LANG==="de"?`${D}. ${mn} ${Y}`'; assert s.count(a) == 1; s = s.replace(a, 'return D?((LANG==="de"||LANG==="nb")?`${D}. ${mn} ${Y}`')
    a = 'LANG==="nb"?x.replace("ca. ","ca ")'; assert s.count(a) == 1; s = s.replace(a, 'LANG==="nb"?x.replace("ca. ","ca. ")')
    for x, y in [('nb:["odaterad","version","nederländska Wikipedia"]', 'nb:["udatert","versjon","nederlandsk Wikipedia"]'), ('nb:["Cirka ","år","Okänd"]', 'nb:["Cirka ","år","Ukjent"]')]:
        assert s.count(x) == 1, x; s = s.replace(x, y)
    s = re.sub(r"const MND_NB1=\[.*?\];", 'const MND_NB1=["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"];', s)
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
    for m in re.finditer(r'<(\w+)([^>]*\bclass="[^"]*\bl-nb\b[^"]*"[^>]*)>', s):
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
    for name in ["SPNB", "NBD", "LBL_NB", "RP_TYPE_NB", "TITLE_NB", "MND_NB"]:
        m = re.search(r"const " + name + r"=(.*?);\n", s, re.S)
        out.append((m.start(1), m.end(1), m.group(1), "const:" + name, ""))
    out.sort()
    # geen overlap (T binnen l-sv-element bestaat niet in html)
    return out
if "--invoegen" not in sys.argv:
    s = code()
    open(D + "tools/no_basis_raw.html", "w", encoding="utf8").write(s)
    V = vind(s)
    todo = {f"{n:04d}": {"soort": v[3], "sv": v[2], **({"en": v[4]} if v[4] else {})} for n, v in enumerate(V)}
    json.dump(todo, open(D + "tools/nb_todo.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
    rest = s
    for a, b, *_ in reversed(V): rest = rest[:a] + rest[b:]
    left = [ln.strip()[:160] for ln in rest.split("\n") if re.search(r"[äöÄÖ]|\b(och|inte|eller|finns|katter|arter|platser)\b", ln)]
    print(len(V), "stukken;", len(left), "regels met Zweedse woorden over:"); [print("  ", x) for x in left[:40]]
else:
    s = open(D + "tools/no_basis_raw.html", encoding="utf8").read()
    V = vind(s); SV = json.load(open(D + "tools/nb_vast.json", encoding="utf8"))
    for n, (a, b, t, k, _) in reversed(list(enumerate(V))):
        x = SV[f"{n:04d}"]
        if not isinstance(x, str): x = json.dumps(x, ensure_ascii=False)
        s = s[:a] + x + s[b:]
    open(D + "no_basis.html", "w", encoding="utf8").write(s)
    print("se_basis.html geschreven")
