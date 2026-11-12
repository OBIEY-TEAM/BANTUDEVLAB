"""
Commande d'initialisation souveraine des comptes BANTUDEVLAB (CADEV 2026).
Conforme aux exigences de securite et de conformite CADEV 2026 :
- Aucun mot de passe administrateur en dur.
- Provisionnement d'un compte administrateur UNIQUEMENT si les variables d'environnement sont fournies.
- Creation d'un compte de demonstration non privilegie (cadev_evaluator) sans droits sensibles.
"""

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.zkp_auth.crypto import ZKPCrypto
from apps.zkp_auth.models import SovereignIdentity

DEFAULT_DEMO_MNEMONIC = "savanna baobab sahara kilimanjaro zambezi congo senegal niger atlas oasis unity freedom"


class Command(BaseCommand):
    help = "Initialise les comptes par variables d'environnement et cree le compte de demo non privilegie CADEV."

    def handle(self, *args, **options):
        # 1. Provisionnement conditionnel de l'administrateur via variables d'environnement
        admin_user = os.environ.get("BANTU_ADMIN_USER")
        admin_email = os.environ.get("BANTU_ADMIN_EMAIL", "admin@bantudevlab.africa")
        admin_password = os.environ.get("BANTU_ADMIN_PASSWORD")

        if admin_user and admin_password:
            user, created = User.objects.get_or_create(
                username=admin_user,
                defaults={
                    "email": admin_email,
                    "is_staff": True,
                    "is_superuser": True,
                    "is_active": True,
                },
            )
            user.email = admin_email
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password(admin_password)
            user.save()

            admin_seed = os.environ.get("BANTU_ADMIN_MNEMONIC", DEFAULT_DEMO_MNEMONIC)
            _, pub_y = ZKPCrypto.generate_keypair(secret_seed=admin_seed)
            SovereignIdentity.objects.update_or_create(
                user=user,
                defaults={
                    "public_key_y": format(pub_y, "x"),
                    "country_code": os.environ.get("BANTU_ADMIN_COUNTRY", "CIV"),
                    "is_verified": True,
                },
            )
            action = "cree" if created else "mis a jour"
            self.stdout.write(self.style.SUCCESS(f"Compte administrateur {admin_user} {action} via variables d'environnement."))
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Aucune variable BANTU_ADMIN_USER / BANTU_ADMIN_PASSWORD detectee : aucun compte superutilisateur provisionne."
                )
            )

        # 2. Compte de demonstration CADEV 2026 : strictement NON privilegie (is_staff=False, is_superuser=False)
        demo_user, _ = User.objects.get_or_create(
            username="cadev_evaluator",
            defaults={
                "email": "evaluator@cadev2026.africa",
                "is_staff": False,
                "is_superuser": False,
                "is_active": True,
            },
        )
        demo_user.email = "evaluator@cadev2026.africa"
        demo_user.is_staff = False
        demo_user.is_superuser = False
        demo_user.is_active = True
        demo_user.set_unusable_password()  # Authentification ZKP sans mot de passe
        demo_user.save()

        # Cle publique ZKP issue du mnémonique standard de demonstration
        _, demo_pub_y = ZKPCrypto.generate_keypair(secret_seed=DEFAULT_DEMO_MNEMONIC)
        SovereignIdentity.objects.update_or_create(
            user=demo_user,
            defaults={
                "public_key_y": format(demo_pub_y, "x"),
                "country_code": "SEN",  # Senegal (Dakar - CADEV 2026)
                "is_verified": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Compte de demonstration CADEV 2026 pret : 'cadev_evaluator' (non privilegie, authentification ZKP sans mot de passe)."
            )
        )
