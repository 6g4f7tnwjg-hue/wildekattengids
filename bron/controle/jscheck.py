# Controleert alle inline scripts van een gids of pagina met node --check.
# Gebruik: python3 jscheck.py bron/gidsen/ro.html [roemenie/index.html ...]
import re, subprocess, sys, tempfile
bad = 0
for f in sys.argv[1:]:
    s = open(f, encoding="utf8").read()
    for i, m in enumerate(re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", s, re.S)):
        t = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False); t.write(m.group(1)); t.close()
        r = subprocess.run(["node", "--check", t.name], capture_output=True, text=True)
        if r.returncode: bad += 1; print(f, "script", i, r.stderr.strip().split("\n")[:4])
print("JS-fouten:", bad)
