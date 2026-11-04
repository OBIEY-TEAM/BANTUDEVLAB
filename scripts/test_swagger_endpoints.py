import urllib.request
import json
import sys

base_url = "http://127.0.0.1:3002"

# 1. Read Swagger JSON
try:
    with urllib.request.urlopen(f"{base_url}/swagger.v1.json", timeout=10) as resp:
        swagger_data = json.loads(resp.read().decode("utf-8"))
        paths = list(swagger_data.get("paths", {}).keys())
        print(f"[OK] Swagger JSON loaded: {len(paths)} endpoints detected.")
        print("Sample endpoints:", paths[:10])
except Exception as e:
    print(f"[ERROR] Failed to read swagger JSON: {e}")
    sys.exit(1)

# 2. Test key endpoints
test_endpoints = [
    ("/api/v1/version", "GET", 200),
    ("/api/v1/repos/search", "GET", 200),
    ("/api/v1/users/search", "GET", 200),
    ("/api/v1/nodeinfo", "GET", 200),
    ("/api/v1/settings/api", "GET", 200),
    ("/api/swagger", "GET", 200),
]

for endpoint, method, expected_code in test_endpoints:
    url = f"{base_url}{endpoint}"
    req = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"[OK] {method} {endpoint} -> Status {resp.status} (Expected {expected_code})")
    except urllib.error.HTTPError as e:
        print(f"[{'OK' if e.code == expected_code else 'FAIL'}] {method} {endpoint} -> Status {e.code}")
    except Exception as e:
        print(f"[ERROR] {method} {endpoint} -> {e}")
