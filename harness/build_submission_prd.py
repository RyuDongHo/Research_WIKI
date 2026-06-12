"""Rebuild submission/PRD.md = root PRD + Wiki Agent SPEC appendix (UTF-8 safe)."""
import io
import re

prd = io.open("PRD.md", encoding="utf-8").read()
spec = io.open("specs/agent-spec.md", encoding="utf-8").read()
body = spec.split("\n", 1)[1]
body = re.sub(r"(?m)^## ", "### ", body)
prd = prd.rstrip() + "\n\n---\n\n# Appendix: Wiki Agent SPEC (역할 · 권한 · 허용 기능)\n" + body
io.open("submission/PRD.md", "w", encoding="utf-8", newline="\n").write(prd)
print("ok")
