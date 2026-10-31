import hmac
import hashlib
import json
from django.test import TestCase, Client, override_settings
from django.conf import settings
from django.contrib.auth.models import User
from apps.zkp_auth.crypto import ZKPCrypto, P, Q, G
from apps.core.models import AuditTrailLog
from apps.core.audit import AuditTrail


class Axe1SecurityTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    # SEC-01: Validation HMAC des Webhooks Gitea
    def test_sec01_webhook_rejected_without_signature(self):
        payload = json.dumps({'repository': {'name': 'test-repo'}})
        response = self.client.post(
            '/api/forge/webhook/',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn('X-Gitea-Signature manquant', response.json().get('error', ''))

    def test_sec01_webhook_rejected_with_invalid_signature(self):
        payload = json.dumps({'repository': {'name': 'test-repo'}})
        response = self.client.post(
            '/api/forge/webhook/',
            data=payload,
            content_type='application/json',
            HTTP_X_GITEA_SIGNATURE='invalid_hmac_hash'
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn('invalide', response.json().get('error', ''))

    def test_sec01_webhook_accepted_with_valid_signature(self):
        payload = json.dumps({'repository': {'name': 'test-repo'}, 'pusher': {'username': 'kwame'}})
        secret = getattr(settings, 'GITEA_WEBHOOK_SECRET', '').encode('utf-8')
        signature = hmac.new(secret, payload.encode('utf-8'), hashlib.sha256).hexdigest()

        response = self.client.post(
            '/api/forge/webhook/',
            data=payload,
            content_type='application/json',
            HTTP_X_GITEA_SIGNATURE=signature
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('received'))

    # SEC-02: Validation du Sous-Groupe Cryptographique ZKP
    def test_sec02_subgroup_validation_valid_key(self):
        x, y = ZKPCrypto.generate_keypair()
        self.assertTrue(ZKPCrypto.validate_public_key(y))

    def test_sec02_subgroup_validation_invalid_keys(self):
        # Boundaries: y <= 1 or y >= P-1
        self.assertFalse(ZKPCrypto.validate_public_key(1))
        self.assertFalse(ZKPCrypto.validate_public_key(0))
        self.assertFalse(ZKPCrypto.validate_public_key(P))
        self.assertFalse(ZKPCrypto.validate_public_key(P - 1))
        self.assertFalse(ZKPCrypto.validate_public_key(-5))
        # Element not in subgroup: for safe prime P = 2*Q + 1, quadratic non-residues satisfy y^Q mod P == P - 1 != 1
        # P - 1 mod P has order 2, not Q: (P-1)^Q mod P == (-1)^Q mod P == -1 mod P != 1 (Q is prime > 2, hence odd)
        self.assertFalse(ZKPCrypto.validate_public_key(P - 1))

    def test_sec02_register_rejected_on_invalid_subgroup_key(self):
        # Attempt to register with a non-subgroup key y = P - 1 or y = 1
        invalid_y = hex(1)
        response = self.client.post(
            '/api/zkp/register/',
            data=json.dumps({
                'username': 'attacker',
                'public_key_y': invalid_y,
                'country_code': 'CIV'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('sous-groupe', response.json().get('error', ''))

    # SEC-03: Protection contre l'Énumération d'Utilisateurs
    def test_sec03_challenge_non_existent_user_returns_200(self):
        response = self.client.post(
            '/api/zkp/challenge/',
            data=json.dumps({'username': 'ghost_user_that_does_not_exist'}),
            content_type='application/json'
        )
        # Status code must be 200 with identical JSON schema
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['username'], 'ghost_user_that_does_not_exist')
        self.assertIn('challenge_nonce', data)
        self.assertIn('expires_at', data)
        self.assertEqual(len(data['challenge_nonce']), 64)

    # SEC-04: Rate Limiting & Throttling
    def test_sec04_throttling_configured(self):
        self.assertIn('zkp', settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'])
        self.assertIn('scanner', settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'])
        self.assertEqual(settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['zkp'], '5/minute')
        self.assertEqual(settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['scanner'], '10/minute')

    # SEC-05: Durcissement des En-têtes HTTP & Cookies
    def test_sec05_security_headers_and_cookie_settings(self):
        self.assertTrue(settings.SECURE_BROWSER_XSS_FILTER)
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertEqual(settings.X_FRAME_OPTIONS, 'DENY')
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, 'Lax')
        self.assertTrue(settings.CSRF_COOKIE_HTTPONLY)
        self.assertEqual(settings.CSRF_COOKIE_SAMESITE, 'Lax')

        # Check response headers from middleware
        response = self.client.get('/')
        self.assertIn('Content-Security-Policy', response.headers)
        self.assertEqual(response.headers['X-Frame-Options'], 'DENY')
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')

    # SEC-06: Journal d'Audit Immuable (Audit Trail)
    def test_sec06_audit_trail_chained_hashing_and_integrity(self):
        AuditTrailLog.objects.all().delete()
        log1 = AuditTrail.record_event('ZKP_AUTH', 'user1', {'status': 'SUCCESS'})
        log2 = AuditTrail.record_event('REPO_CREATE', 'user1', {'repository': 'repo1'})
        log3 = AuditTrail.record_event('VULN_SCAN', 'user1', {'issues': 0})

        self.assertEqual(log1.prev_hash, AuditTrail.GENESIS_HASH)
        self.assertEqual(log2.prev_hash, log1.current_hash)
        self.assertEqual(log3.prev_hash, log2.current_hash)

        # Verify integrity succeeds
        self.assertTrue(AuditTrail.verify_chain_integrity())

        # Tamper with an entry and verify integrity fails
        log2.details = {'repository': 'tampered_repo'}
        log2.save()
        self.assertFalse(AuditTrail.verify_chain_integrity())

    def test_sec06_actions_generate_audit_logs(self):
        initial_count = AuditTrailLog.objects.count()

        # 1. ZKP Auth
        x, y = ZKPCrypto.generate_keypair()
        self.client.post(
            '/api/zkp/register/',
            data=json.dumps({'username': 'audit_test_user', 'public_key_y': hex(y)}),
            content_type='application/json'
        )
        chal = self.client.post(
            '/api/zkp/challenge/',
            data=json.dumps({'username': 'audit_test_user'}),
            content_type='application/json'
        ).json()
        proof = ZKPCrypto.generate_proof(secret_x=x, public_y=y, message=chal['challenge_nonce'])
        self.client.post(
            '/api/zkp/verify/',
            data=json.dumps({
                'username': 'audit_test_user',
                'challenge_nonce': chal['challenge_nonce'],
                'commitment_t': proof['commitment_t'],
                'response_s': proof['response_s']
            }),
            content_type='application/json'
        )

        # 2. Repo Create
        self.client.post(
            '/api/forge/repositories/',
            data=json.dumps({'name': 'audit-forge-repo'}),
            content_type='application/json'
        )

        # 3. Vuln Scan
        self.client.post(
            '/api/security/scan/',
            data=json.dumps({'content': 'x = 1', 'filename': 'test.py'}),
            content_type='application/json'
        )

        new_count = AuditTrailLog.objects.count()
        self.assertGreaterEqual(new_count - initial_count, 3)
        self.assertTrue(AuditTrail.verify_chain_integrity())
