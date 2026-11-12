from pathlib import Path

path = Path("tests/test_qa_coverage.py")
content = path.read_text(encoding="utf-8")

if "def test_additional_branch_coverage_cadev26" in content:
    content = content[:content.index("    def test_additional_branch_coverage_cadev26")]

addition = """    def test_additional_branch_coverage_cadev26(self):
        # 1. zkp challenge GET redirect
        res_chal = self.client.get("/api/zkp/challenge/?source=gitlab")
        self.assertEqual(res_chal.status_code, 302)
        self.assertIn("/api/zkp/login-ui/", res_chal.url)

        # 2. zkp challenge non-existent user returns 200 dummy challenge (anti-enumeration)
        res_missing = self.client.post(
            "/api/zkp/challenge/",
            {"username": "non_existent_zkp_user_999"},
            content_type="application/json",
        )
        self.assertEqual(res_missing.status_code, 200)
        self.assertIn("challenge_nonce", res_missing.json())

        # 3. zkp rotate-key error paths
        self.client.force_login(self.user)
        res_rot_bad1 = self.client.post(
            "/api/zkp/rotate-key/",
            {"new_public_key_y": "invalid_non_hex"},
            content_type="application/json",
        )
        self.assertEqual(res_rot_bad1.status_code, 400)

        res_rot_bad2 = self.client.post(
            "/api/zkp/rotate-key/",
            {"new_public_key_y": hex(P + 100)},
            content_type="application/json",
        )
        self.assertEqual(res_rot_bad2.status_code, 400)

        res_rot_bad3 = self.client.post(
            "/api/zkp/rotate-key/",
            {"new_public_key_y": "1"},
            content_type="application/json",
        )
        self.assertEqual(res_rot_bad3.status_code, 400)

        # 4. Copilot export and review views
        res_exp_bad = self.client.post(
            "/api/ai/copilot/export/",
            {"messages": "not_a_list"},
            content_type="application/json",
        )
        self.assertEqual(res_exp_bad.status_code, 400)

        res_exp_json = self.client.post(
            "/api/ai/copilot/export/",
            {"messages": [{"role": "user", "content": "hi"}], "format": "json"},
            content_type="application/json",
        )
        self.assertEqual(res_exp_json.status_code, 200)

        res_exp_md = self.client.post(
            "/api/ai/copilot/export/",
            {"messages": [{"role": "user", "content": "hi"}], "format": "markdown"},
            content_type="application/json",
        )
        self.assertEqual(res_exp_md.status_code, 200)

        res_rev_bad = self.client.post(
            "/api/ai/copilot/review/",
            {},
            content_type="application/json",
        )
        self.assertEqual(res_rev_bad.status_code, 400)

        # 5. security scanner engine edge cases
        from apps.security_scanner.engine import calculate_shannon_entropy

        self.assertEqual(calculate_shannon_entropy(""), 0.0)
"""

path.write_text(content + addition, encoding="utf-8")
print("SUCCESS: Updated tests/test_qa_coverage.py")
