import pathlib

root = pathlib.Path(r"c:/Users/User/Desktop/AGENT/BANTUDEVLAB")
p = root / "develop-design.md"
text = p.read_bytes().decode("utf-8").replace("\r\n", "\n")

# Replace unchecked tasks with checked ones
for code in ["DES-01", "DES-02", "DES-03", "NAV-01", "NAV-02", "NAV-03", "NAV-04", "NAV-05", "I18N-01", "I18N-02", "I18N-03", "UI-01", "UI-02", "UI-03"]:
    text = text.replace(f"- [ ] **{code}", f"- [x] **{code}")

p.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
print("develop-design.md tasks marked as completed")
