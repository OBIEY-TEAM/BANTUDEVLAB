import os
import tarfile
import hashlib
import base64
import urllib.request
import urllib.parse
from pathlib import Path

def package_and_upload():
    archive_path = Path("C:/tmp/figma-import-0cfe5b2163b24b64dfa1a13a26120c54568e4f8dfce3b788b1eefd0462232c3e.archive")
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    source_dir = Path("figma_export")
    
    # Create tar.gz archive with index.html at root
    with tarfile.open(archive_path, "w:gz") as tar:
        for file in source_dir.iterdir():
            tar.add(file, arcname=file.name)
    
    print(f"Created archive at {archive_path} ({archive_path.stat().st_size} bytes)")

    # Read archive bytes
    with open(archive_path, "rb") as f:
        data = f.read()

    checksum = base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")
    print("Checksum:", checksum)

    # Now upload using curl or python requests
    import subprocess
    cmd = [
        "curl", "--fail-with-body", "-X", "POST",
        "https://www.figma.com/blobs/us/upload/figma-agentplat-ugit-us-production",
        "--form-string", "key=uploads/make_folder_imports/2417966991670167800/a8d48c18-4d77-4c1e-895b-24772d4e8258.archive",
        "--form-string", "acl=private",
        "--form-string", "x-amz-checksum-algorithm=SHA256",
        "--form-string", "policy=eyJleHBpcmF0aW9uIjoiMjAyNi0xMS0wNFQxMTo1NzoyM1oiLCJjb25kaXRpb25zIjpbeyJidWNrZXQiOiJmaWdtYS1hZ2VudHBsYXQtdWdpdC11cy1wcm9kdWN0aW9uIn0seyJrZXkiOiJ1cGxvYWRzL21ha2VfZm9sZGVyX2ltcG9ydHMvMjQxNzk2Njk5MTY3MDE2NzgwMC9hOGQ0OGMxOC00ZDc3LTRjMWUtODk1Yi0yNDc3MmQ0ZTgyNTguYXJjaGl2ZSJ9LHsiYWNsIjoicHJpdmF0ZSJ9LFsiY29udGVudC1sZW5ndGgtcmFuZ2UiLDEsMTA3Mzc0MTgyNF0sWyJzdGFydHMtd2l0aCIsIiR4LWFtei1jaGVja3N1bS1zaGEyNTYiLCIiXSxbInN0YXJ0cy13aXRoIiwiJENvbnRlbnQtVHlwZSIsIiJdLHsieC1hbXotY2hlY2tzdW0tYWxnb3JpdGhtIjoiU0hBMjU2In0seyJ4LWFtei1jcmVkZW50aWFsIjoiQVNJQVE0R09TRldDWDRNSFFaMlcvMjAyNjExMDQvdXMtd2VzdC0yL3MzL2F3czRfcmVxdWVzdCJ9LHsieC1hbXotYWxnb3JpdGhtIjoiQVdTNC1ITUFDLVNIQTI1NiJ9LHsieC1hbXotZGF0ZSI6IjIwMjYxMTA0VDEwNTcyM1oifSx7IngtYW16LXNlY3VyaXR5LXRva2VuIjoiSVFvSmIzSnBaMmx1WDJWakVPUC8vLy8vLy8vLy93RWFDWFZ6TFhkbGMzUXRNaUpHTUVRQ0lDU1Q4Vi9JWTIwWVl0MVhnenVOY1M0QlordkFiZzYvb3hadjFWQ2VTM0NrQWlBQ0toMnI3MzdqYytDMlROeFM4MWVyenRjSkZzNjFjdnZ6NzluSGVaTXQvU3JMQlFpcy8vLy8vLy8vLy84QkVBQWFEREEyTURVMk1qYzBOamMxTnlJTW1maFk3aGFod1NVTjQ4bUhLcDhGcHZUN3ZUY2lTK1E5RDFHRExJQTVEN1JaMWQ4WU1PTTdoVTBGaXloSXlGYU1ZdHdvRmplR2FDNjhGWU5UN2o4M2pGNnJQN2l3QitmUkJ4RUJ3QXllYmdERFJudmxXTjlHVlhIUWpOYTRzRzRlVHdGTVZDdEdrY3NNWGVycmYraWlqVDVJckpCWXBFa3k0NHFnMUtobHA1ZjFYN2dsVmpWdkttYitXa0pwUDNDSHFDd29DbkRMalNYeUJTUXAzSkZwN3Y2S05nVWtkaUtCQ0pRVjFhZE9oeWNzZFpVMnkvYW84Sk5aM1NEK0lDR0FJbG91dHVTY1ZyQlA4TGxaUStIVEZDTTFGNU1rQkd5RGRlSjlQc2lJcnp6WkVsMUpyUnBsQ1JBc1NjYTJIM3JRSm1vSXVhNFYrZEpuMTFtdmI0MFgrQVZBN3Ewczl1alVzeGl6S3dVNUZsTzV3OFZvMGRPVGJJNmczVSs0NExaTm10bk1nVUp6SjNoRUpUczU2UzZrelVaVVJRa3R6dWl0dk5DK1ZBRTI4N056SHlXK0MrUmpNWVV5bEdDNmZ5Q2FWeTM0NHlOU3ltc01FcGgxb1dycGYzWlQ1N0tNRFNmVUQ3d1RYcVFjRXFCc01tU3pxVGJCT2ZFL3dhTGM5OTJIL2tZUkRDWGk2TVV3VzYyNXhkRFhzdmVJeXdtZlFKaVF3dldPUUcyczhpa2RzZEhHRWxEWnFGWExCT3dpOWtRbHA4WG9Ob2Z4SUl0ejZLN2xjSzNWM053eElEYzZ6SHJ4N29DSlU1NGlKT3J1R3MyMU9haitBOHduYlNxMVUxdGxRNlRMRmFjeXliUmRhYXdrbFhuNzQxWkFLMUhMcGU4MWtyejJKTUMvbms1M1pVZHk5cWhibzJVWDQ0VkpRRjU1NFpiMEZYajlEUDJEekl5YmNLeC96enBPUTh4Zjdqcm01SlcvVFJEK1RxM2JLQUR6blpIRi9RVERsRTFtMXh0d005OHpnNFFMR21Zb1k4UDhlRlV6ZEdtZStLNG5Vdy84Tnl3OUhmZ2kxSHZFQjhkU0dnU043RVRSTVR4bklPTHVnTGh4ZXdpNnpNRnlEaVVFczVXRTlXbHZrbVVYdXBYZ0VIVkhqVEhhM3VxcElLSjM5MUthS0g4aFhMczg5em9BZFVPS2ZGVHFJSHNldkNiN0RRY3dzSktzMXdZNm1nRytrbVpCb3lmRmNZUlk2MnB5S0dqOVJQTkFmWEVPQWR1L0NSdzFNcTVLRzhvY09oL2t1RlJVM3ZmTHc3WWRPVGRqUmtjKzEwMUtXN0ptdWdpMkMvRWl1amx1SmRxWktLV09NTzJCL2hDNW9kUHRVNG4yV2VCRklQV3ZYWGVvclZEcXc5c1hoUTZIdEJ4K0NKOVJtNUNjQWR6TUNsd0RlRUdzMk9mZElYenRCbDVDb1lMWmJlL2d1dmtMenVTREd4QWJERVh3eHdWTlpJTXMifV19",
        "--form-string", "x-amz-credential=ASIAQ4GOSFWCX4MHQZ2W/20261104/us-west-2/s3/aws4_request",
        "--form-string", "x-amz-algorithm=AWS4-HMAC-SHA256",
        "--form-string", "x-amz-date=20261104T105723Z",
        "--form-string", "x-amz-security-token=IQoJb3JpZ2luX2VjEOP//////////wEaCXVzLXdlc3QtMiJGMEQCICST8V/IY20YYt1XgzuNcS4BZ+vAbg6/oxZv1VCeS3CkAiACKh2r737jc+C2TNxS81erztcJFs61cvvz79nHeZMt/SrLBQis//////////8BEAAaDDA2MDU2Mjc0Njc1NyIMmfhY7hahwSUN48mHKp8FpvT7vTciS+Q9D1GDLIA5D7RZ1d8YMOM7hU0FiyhIyFaMYtwoFjeGaC68FYNT7j83jF6rP7iwB+fRBxEBwAyebgDDRnvlWN9GVXHQjNa4sG4eTwFMVCtGkcsMXerrf+iijT5IrJBYpEky44qg1Khlp5f1X7glVjVvKmb+WkJpP3CHqCwoCnDLjSXyBSQp3JFp7v6KNgUkdiKBCJQV1adOhycsdZU2y/ao8JNZ3SD+ICGAIloutuScVrBP8LlZQ+HTFCM1F5MkBGyDdeJ9PsiIrzzZEl1JrRplCRAsSca2H3rQJmoIua4V+dJn11mvb40X+AVA7q0s9ujUsxizKwU5FlO5w8Vo0dOTbI6g3U+44LZNmtnMgUJzJ3hEJTs56S6kzUZURQktzuitvNC+VAE287NzHyW+C+RjMYUylGC6fyCaVy344yNSymsMEph1oWrpf3ZT57KMDSfUD7wTXqQcEqBsMmSzqTbBOfE/waLc992H/kYRDCXi6MUwW625xdDXsveIywmfQJiQwvWOQG2s8ikdsdHGElDZqFXLBOwi9kQlp8XoNofxIItz6K7lcK3V3NwxIDc6zHrx7oCJU54iJOruGs21Oaj+A8wnbSq1U1tlQ6TLFacyybRdaawklXn741ZAK1HLpe81krz2JMC/nk53ZUdy9qhbo2UX44VJQF554Zb0FXj9DP2DzIybcKx/zzpOQ8xf7jrm5JW/TRD+Tq3bKADznZHF/QTDlE1m1xtwM98zg4QLGmYoY8P8eFUzdGme+K4nUw/8Nyw9Hfgi1HvEB8dSGgSN7ETRMTxnIOLugLhxewi6zMFyDiUEs5WE9WlvkmUXupXgEHVHjTHa3uqpIKJ391KaKH8hXLs89zoAdUOKfFTqIHsevCb7DQcwsJKs1wY6mgG+kmZBoyfFcYRY62pyKGj9RPNAfXEOAdu/CRw1Mq5KG8ocOh/kuFRU3vfLw7YdOTdjRkc+101KW7Jmugi2C/EiujluJdqZKKWOMO2B/hC5odPtU4n2WeBFIPWvXXeorVDqw9sXhQ6HtBx+CJ9Rm5CcAdzMClwDeEGs2OfdIXztBl5CoYLZbe/guvkLzuSDGxAbDEXwxwVNZIMs",
        "--form-string", "x-amz-signature=abeffc6550594b56f3c17e02826b32814c8e558b87184862ac7ed550b08df333",
        "-F", "Content-Type=application/octet-stream",
        "-F", f"x-amz-checksum-sha256={checksum}",
        "-F", f"file=@{archive_path};type=application/octet-stream"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Curl returncode:", res.returncode)
    print("Curl stdout:", res.stdout)
    print("Curl stderr:", res.stderr)

if __name__ == "__main__":
    package_and_upload()
