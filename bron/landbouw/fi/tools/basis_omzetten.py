# Stap 1: se_basis.html -> fi_basis_raw.html (code sv -> nb) en nb_todo.json (alle Zweedse teksten om te vertalen).
# Stap 2 (met --invoegen): fi_vast.json (zelfde sleutels, Finse tekst) -> fi_basis.html.
import json, re, sys, os
D = os.path.dirname(os.path.abspath(__file__)) + "/../"
def code():
    s = open(D + "../no/no_basis.html", encoding="utf8").read()
    s = re.sub(r"\b(SP|R1|R5|R6|R7)NB\b", r"\1FI", s)
    s = re.sub(r"\bNB(D|M)\b", r"FI\1", s)
    s = re.sub(r"\b(RP_TYPE|ROUTENOTE|EARLIER|LBL|TITLE|MND)_NB(1?)\b", r"\1_FI\2", s)
    s = s.replace("html:not(.nb)", "html:not(.fi)").replace('"nb"', '"fi"').replace("l-nb", "l-fi").replace("html.nb", "html.fi").replace('-nb"', '-fi"')
    s = re.sub(r"\bnb:\[", "fi:[", s); s = s.replace("nb:{get SP", "fi:{get SP")
    s = s.replace('lang="nb">NB<', 'lang="fi">FI<')
    # datum: Fins "23. lokakuuta 2026", maar alleen maand: "lokakuu 2026"
    a = '):`${mn} ${Y}`;}'; assert s.count(a) == 1; s = s.replace(a, '):(LANG==="fi"?`${MND_FI1[M-1]} ${Y}`:`${mn} ${Y}`);}')
    a = 'LANG==="fi"?x.replace(/\\./g,"\\u00a0").replace("ca\\u00a0 ","ca. ")'; assert s.count(a) == 1, "wildL"; s = s.replace(a, 'LANG==="fi"?x.replace(/\\./g,"\\u00a0").replace("ca\\u00a0 ","n. ")')
    for x, y in [('fi:["udatert","versjon","nederlandsk Wikipedia"]', 'fi:["päiväämätön","versio","hollanninkielinen Wikipedia"]'), ('fi:["Cirka ","år","Ukjent"]', 'fi:["Noin ","vuotta","Tuntematon"]')]:
        assert s.count(x) == 1, x; s = s.replace(x, y)
    s = re.sub(r"const MND_FI1=\[.*?\];", 'const MND_FI1=["tammikuu", "helmikuu", "maaliskuu", "huhtikuu", "toukokuu", "kesäkuu", "heinäkuu", "elokuu", "syyskuu", "lokakuu", "marraskuu", "joulukuu"];', s)
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
    for m in re.finditer(r'<(\w+)([^>]*\bclass="[^"]*\bl-fi\b[^"]*"[^>]*)>', s):
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
    for name in ["SPFI", "FID", "LBL_FI", "RP_TYPE_FI", "TITLE_FI", "MND_FI"]:
        m = re.search(r"const " + name + r"=(.*?);\n", s, re.S)
        out.append((m.start(1), m.end(1), m.group(1), "const:" + name, ""))
    out.sort()
    # geen overlap (T binnen l-sv-element bestaat niet in html)
    return out
if "--invoegen" not in sys.argv:
    s = code()
    open(D + "tools/fi_basis_raw.html", "w", encoding="utf8").write(s)
    V = vind(s)
    todo = {f"{n:04d}": {"soort": v[3], "nb": v[2], **({"en": v[4]} if v[4] else {})} for n, v in enumerate(V)}
    json.dump(todo, open(D + "tools/fi_todo.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
    rest = s
    for a, b, *_ in reversed(V): rest = rest[:a] + rest[b:]
    left = [ln.strip()[:160] for ln in rest.split("\n") if re.search(r"[æøÆØ]|\b(og|ikke|eller|finnes|katter|arter|steder|dyrehage)\b", ln)]
    print(len(V), "stukken;", len(left), "regels met Noorse woorden over:"); [print("  ", x) for x in left[:40]]
else:
    s = open(D + "tools/fi_basis_raw.html", encoding="utf8").read()
    V = vind(s); SV = json.load(open(D + "tools/fi_vast.json", encoding="utf8"))
    for n, (a, b, t, k, _) in reversed(list(enumerate(V))):
        x = SV[f"{n:04d}"]
        if not isinstance(x, str): x = json.dumps(x, ensure_ascii=False)
        s = s[:a] + x + s[b:]
    open(D + "fi_basis.html", "w", encoding="utf8").write(s)
    print("fi_basis.html geschreven")
