# Stap 1: hu_basis.html -> ro_basis_raw.html (code hu -> ro) en ro_todo.json (alle Hongaarse teksten om te vertalen).
# Stap 2 (met --invoegen): ro_vast.json (zelfde sleutels, Roemeense tekst) -> ro_basis.html.
import json, re, sys, os
D = os.path.dirname(os.path.abspath(__file__)) + "/../"
def code():
    s = open(D + "../hu/hu_basis.html", encoding="utf8").read()
    s = re.sub(r"\b(SP|R1|R5|R6|R7)HU\b", r"\1RO", s)
    s = re.sub(r"\bHU(D|M)\b", r"RO\1", s)
    s = re.sub(r"\b(RP_TYPE|ROUTENOTE|EARLIER|LBL|TITLE|MND)_HU(1?)\b", r"\1_RO\2", s)
    s = s.replace("html:not(.hu)", "html:not(.ro)").replace('"hu"', '"ro"').replace("l-hu", "l-ro").replace("html.hu", "html.ro").replace('-hu"', '-ro"')
    s = re.sub(r"\bhu:\[", "ro:[", s); s = s.replace("hu:{get SP", "ro:{get SP")
    a = 'lang="ro">HU<'; assert s.count(a) == 1; s = s.replace(a, 'lang="ro">RO<')
    # datum: Roemeens "30 octombrie 2026", alleen maand: "octombrie 2026" (standaardtak)
    a = 'return D?(LANG==="de"?`${D}. ${mn} ${Y}`:LANG==="ro"?`${Y}. ${mn} ${D}.`:`${d} ${mn} ${Y}`):(LANG==="ro"?`${Y}. ${MND_RO1[M-1]}`:`${mn} ${Y}`);}'
    assert s.count(a) == 1, "yDate"
    s = s.replace(a, 'return D?(LANG==="de"?`${D}. ${mn} ${Y}`:`${d} ${mn} ${Y}`):`${mn} ${Y}`;}')
    a = 'LANG==="ro"?x.replace(/\\./g,"\\u00a0").replace("ca\\u00a0 ","kb. ")'; assert s.count(a) == 1, "wildL"; s = s.replace(a, 'LANG==="ro"?x.replace("ca. ","aprox. ")')
    for x, y in [('ro:["dátum nélkül","változat","holland Wikipédia"]', 'ro:["fără dată","versiunea","Wikipedia în neerlandeză"]'), ('ro:["Kb. ","év","Ismeretlen"]', 'ro:["Aprox. ","ani","Necunoscută"]')]:
        assert s.count(x) == 1, x; s = s.replace(x, y)
    s = re.sub(r"const MND_RO1=\[.*?\];\n?", "", s)
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
    for m in re.finditer(r'<(\w+)([^>]*\bclass="[^"]*\bl-ro\b[^"]*"[^>]*)>', s):
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
    for name in ["SPRO", "ROD", "LBL_RO", "RP_TYPE_RO", "TITLE_RO", "MND_RO"]:
        m = re.search(r"const " + name + r"=(.*?);\n", s, re.S)
        out.append((m.start(1), m.end(1), m.group(1), "const:" + name, ""))
    out.sort()
    # geen overlap (T binnen l-sv-element bestaat niet in html)
    return out
if "--invoegen" not in sys.argv:
    s = code()
    open(D + "tools/ro_basis_raw.html", "w", encoding="utf8").write(s)
    V = vind(s)
    todo = {f"{n:04d}": {"soort": v[3], "hu": v[2], **({"en": v[4]} if v[4] else {})} for n, v in enumerate(V)}
    json.dump(todo, open(D + "tools/ro_todo.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
    rest = s
    for a, b, *_ in reversed(V): rest = rest[:a] + rest[b:]
    left = [ln.strip()[:160] for ln in rest.split("\n") if re.search(r"[őűŐŰ]|\b(és|nem|faj\w*|hely\w*|Magyarország\w*|állat\w*)\b", ln)]
    print(len(V), "stukken;", len(left), "regels met Hongaarse woorden over:"); [print("  ", x) for x in left[:40]]
else:
    s = open(D + "tools/ro_basis_raw.html", encoding="utf8").read()
    V = vind(s); SV = json.load(open(D + "tools/ro_vast.json", encoding="utf8"))
    for n, (a, b, t, k, _) in reversed(list(enumerate(V))):
        x = SV[f"{n:04d}"]
        if not isinstance(x, str): x = json.dumps(x, ensure_ascii=False)
        s = s[:a] + x + s[b:]
    open(D + "ro_basis.html", "w", encoding="utf8").write(s)
    print("ro_basis.html geschreven")
