from pathlib import Path

p = Path("apps/gitea_client/views.py")
content = p.read_text(encoding="utf-8")

old_target = """class RepositoryListView(APIView):
    \"\"\"Lists repositories from Gitea forge with sovereign metadata.\"\"\"

    permission_classes = [IsAuthenticated]"""

replacement = """class RepositoryListView(APIView):
    \"\"\"Lists repositories from Gitea forge with sovereign metadata.\"\"\"

    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]"""

if old_target in content:
    content = content.replace(old_target, replacement)
    p.write_text(content, encoding="utf-8")
    print("SUCCESS: Added authentication_classes to RepositoryListView")
else:
    print("WARNING: target not found in views.py")
