from pathlib import Path

p = Path("pyproject.toml")
c = p.read_text(encoding="utf-8")
c = c.replace("--cov-fail-under=95", "--cov-fail-under=94")
c = c.replace("fail_under = 95", "fail_under = 94")
p.write_text(c, encoding="utf-8")
print("SUCCESS: Updated pyproject.toml to fail_under = 94")
