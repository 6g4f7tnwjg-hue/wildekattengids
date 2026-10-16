# Berekent de gegevens voor de startpagina (kaartstippen, aantallen, recente geboortes) uit de gidsen.
import json, re, datetime, unicodedata

PRIO = "grybnpw"   # welke status telt als er meerdere zijn: aanwezig gaat voor
CONF = set("gybr")  # deze statussen tellen als "bevestigd"

def slug(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

# aantal jongen in het Frans en Duits, als de gids het niet zelf heeft (Nederlandse gids)
_N_FR = [(r"^Drieling$", "Triplés"), (r"\bin twee nesten\b", "en deux portées"), (r"\b(\d+) in leven\b", r"\1 en vie"),
         (r"^1 zwarte welp\b", "1 petit noir"), (r"^1 (?:welp|jong|kitten)\b", "1 petit"), (r"^(\d+) (?:welpen|jongen|kittens)\b", r"\1 petits")]
_N_DE = [(r"^Drieling$", "Drillinge"), (r"\bin twee nesten\b", "in zwei Würfen"), (r"\b(\d+) in leven\b", r"\1 leben"),
         (r"^1 zwarte welp\b", "1 schwarzes Jungtier"), (r"^1 (?:welp|jong|kitten)\b", "1 Jungtier"), (r"^(\d+) (?:welpen|jongen|kittens)\b", r"\1 Jungtiere")]
_N_IT = [(r"^Drieling$", "Tre gemelli"), (r"\bin twee nesten\b", "in due cucciolate"), (r"\b(\d+) in leven\b", r"\1 in vita"),
         (r"^1 zwarte welp\b", "1 cucciolo nero"), (r"^1 (?:welp|jong|kitten)\b", "1 cucciolo"), (r"^(\d+) (?:welpen|jongen|kittens)\b", r"\1 cuccioli")]
_N_ES = [(r"^Drieling$", "Trillizos"), (r"\bin twee nesten\b", "en dos camadas"), (r"\b(\d+) in leven\b", r"\1 con vida"),
         (r"^1 zwarte welp\b", "1 cría negra"), (r"^1 (?:welp|jong|kitten)\b", "1 cría"), (r"^(\d+) (?:welpen|jongen|kittens)\b", r"\1 crías")]
def _vert(nl, regels):
    for a, b in regels:
        nl = re.sub(a, b, nl)
    return nl
# talen van elke gids na Nederlands en Engels (zelfde volgorde als de vakken in de gids)
GTAAL = {"nl": [], "be": ["fr"], "lu": ["fr", "de"], "de": ["de"], "fr": ["fr"], "at": ["de"], "ch": ["de", "fr", "it"], "uk": [], "it": ["it"], "es": ["es"], "ie": [], "pt": ["pt"]}
def n4(n, land):
    """[nl, en, fr, de, it, es] voor 'aantal jongen': uit de gids zelf als die de taal heeft, anders vertaald met vaste regels."""
    vak = lambda l: (n[2 + GTAAL.get(land, []).index(l)] if l in GTAAL.get(land, []) and len(n) > 2 + GTAAL[land].index(l) else "")
    fr = vak("fr") or _vert(n[0], _N_FR)
    de = vak("de") or _vert(n[0], _N_DE)
    it = vak("it") or _vert(n[0], _N_IT)
    es = vak("es") or _vert(n[0], _N_ES)
    return [n[0], n[1], fr, de, it, es]

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

def bereken(parts, oud, today, frnames, land="", denames=None, itnames=None, esnames=None):
    """parts: {deel: extract-uitvoer}; oud: huidige D-invoer van dit land (kaartvorm, notitie blijven)."""
    locs, conf, ys, lt = [], set(), [], []
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
            sps = [[sp, sp_en(sp), fr(sp, sp_en(sp)), next(c for c in PRIO if c in codes), slug(sp), (denames or {}).get(sp, sp_en(sp)), (itnames or {}).get(sp, sp_en(sp)), (esnames or {}).get(sp, sp_en(sp))] for sp, codes in bysp.items()]
            e = [l[0], l[1], l[2], l[3], slug(l[0]), sps]
            if pre:
                e.append(pre)
            locs.append(e)
            inf = (o.get("LOCINFO") or {}).get(l[0]) or {}
            lt.append([(inf.get("type") or [""])[0], inf.get("labels") or []])
        ys += [(d, dict(y, n=n4(y["n"], land))) for d, y in _young(o, sp_en, fr, today, pre)]
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
    nieuw.update({"counts": [len(conf), len(locs)], "locs": locs, "young": young, "lt": lt})
    return nieuw

def soorten(DATA, frnames, today, denames=None, itnames=None, esnames=None):
    """Eén lijst van alle soorten over alle landen heen (sleutel: wetenschappelijke naam).
    Per soort: [slug, nl, en, fr, wetenschappelijk, aliassen, fotonummer, foto-info, recente geboortes, de, it, es]."""
    nl = DATA["nl"]["main"]
    spen = nl.get("SPEN") or {}
    out, bysci = [], {}
    for s in nl["SPECIES"]:
        en = (spen.get(s[0]) or [s[0]])[0] or s[0]
        e = {"slug": slug(s[0]), "nl": s[0], "en": en, "fr": frnames.get(s[0], ""), "sci": s[2], "de": (denames or {}).get(s[0], ""), "it": (itnames or {}).get(s[0], ""), "es": (esnames or {}).get(s[0], ""), "al": [], "img": None, "foto": None, "young": []}
        bysci[s[2]] = e
        out.append(e)
    for c, parts in DATA.items():
        for deel, o in parts.items():
            pre = None if deel == "main" else deel + "/"
            loc2sci = {s[0]: s[2] for s in o["SPECIES"]}
            for s in o["SPECIES"]:
                e = bysci.get(s[2])
                if e and slug(s[0]) != e["slug"] and slug(s[0]) not in e["al"]:
                    e["al"].append(slug(s[0]))
            for naam, p in (o.get("PHOTOS") or {}).items():
                e = bysci.get(loc2sci.get(naam))
                m = re.match(r"@@IMG(\d+)@@", p.get("src", ""))
                if e and m and e["img"] is None:
                    e["img"] = int(m.group(1))
                    e["foto"] = {k: p[k] for k in ("who", "lic", "url", "cap", "site", "zoo") if p.get(k)}
            sp_en = lambda n: n
            for d, y in _young(o, sp_en, lambda n, en: en, today, pre):
                e = bysci.get(loc2sci.get(y["sp"][0]))
                if e:
                    e["young"].append((d, {"c": c, "pre": pre or "", "loc": y["loc"], "born": y["born"], "approx": y["approx"], "n": n4(y["n"], c)}))
    res = []
    for e in out:
        ys = [y for d, y in sorted(e["young"], key=lambda t: t[0], reverse=True)]
        res.append([e["slug"], e["nl"], e["en"], e["fr"], e["sci"], e["al"], e["img"], e["foto"] or {}, ys, e["de"], e["it"], e["es"]])
    return res
