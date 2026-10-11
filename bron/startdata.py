# Berekent de gegevens voor de startpagina (kaartstippen, aantallen, recente geboortes) uit de gidsen.
import json, re, datetime, unicodedata

PRIO = "grybnpw"   # welke status telt als er meerdere zijn: aanwezig gaat voor
CONF = set("gybr")  # deze statussen tellen als "bevestigd"

def slug(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def _young(o, sp_en, fr, today, pre):
    SP = {a[0]: a for a in o["SPECIES"]}
    out = []
    for y in o["YOUNG"]:
        p = list(map(int, y["born"].split("-")))
        d = datetime.date(p[0], p[1], p[2] if len(p) > 2 else 15)
        m = (today.year - d.year) * 12 + today.month - d.month - (1 if today.day < d.day else 0)
        if m >= (24 if SP[y["sp"]][3] in o["PANTH"] else 12):
            continue
        en = sp_en(y["sp"])
        nen = y["n"][1] or re.sub(r"\bwelpen\b", "cubs", re.sub(r"\bwelp\b", "cub", re.sub(r"\bjongen\b", "young", re.sub(r"\bjong\b", "young", y["n"][0]))))
        e = {"sp": [y["sp"], en, fr(y["sp"], en)], "spslug": slug(y["sp"]), "loc": y["loc"], "born": y["born"],
             "approx": bool(y.get("approx", False)), "n": [y["n"][0], nen] + list(y["n"][2:])}
        if pre:
            e["pre"] = pre
        out.append((d, e))
    return out

def bereken(parts, oud, today, frnames):
    """parts: {deel: extract-uitvoer}; oud: huidige D-invoer van dit land (kaartvorm, notitie blijven)."""
    locs, conf, ys = [], set(), []
    for deel, o in parts.items():
        pre = None if deel == "main" else deel + "/"
        spen = o.get("SPEN") or {}
        sp_en = lambda n: ((spen.get(n) or [n])[0] or n)
        fr = (lambda n, en: en) if pre else (lambda n, en: frnames.get(n, en))
        for r in o["R"]:
            if any(c in CONF for c in r[4].split("+")):
                conf.add(r[0])
        for l in o["LOCS"]:
            bysp = {}
            for r in o["R"]:
                if r[2] in l[4]:
                    bysp.setdefault(r[0], set()).update(r[4].split("+"))
            sps = [[sp, sp_en(sp), fr(sp, sp_en(sp)), next(c for c in PRIO if c in codes), slug(sp)] for sp, codes in bysp.items()]
            e = [l[0], l[1], l[2], l[3], slug(l[0]), sps]
            if pre:
                e.append(pre)
            locs.append(e)
        ys += _young(o, sp_en, fr, today, pre)
    seen, young = set(), []
    for d, y in sorted(ys, key=lambda t: t[0], reverse=True):
        k = (y["sp"][0], y["loc"])
        if k in seen:
            continue
        seen.add(k)
        young.append(y)
        if len(young) == 3:
            break
    nieuw = dict(oud)
    nieuw.update({"counts": [len(conf), len(locs)], "locs": locs, "young": young})
    return nieuw
