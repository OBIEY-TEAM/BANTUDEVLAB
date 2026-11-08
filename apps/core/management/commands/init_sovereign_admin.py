"""
Commande d'initialisation automatique des comptes administrateurs par defaut BANTUDEVLAB.
Cree et met a jour de maniere idempotente :
1. bantu_admin (Superutilisateur Django + Identite ZKP Souveraine)
2. kouame_dev (Superutilisateur / Developpeur Souverain par defaut de l'assistant ZKP)
"""

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.zkp_auth.crypto import ZKPCrypto
from apps.zkp_auth.models import SovereignIdentity

DEFAULT_ADMIN_MNEMONIC = "savanna baobab sahara kilimanjaro zambezi congo senegal niger atlas oasis unity freedom"


class Command(BaseCommand):
    help = "Initialise les comptes administrateurs par defaut (bantu_admin et kouame_dev) avec mot de passe et cle ZKP."

    def handle(self, *args, **options):
        admin_username = os.environ.get("BANTU_DEFAULT_ADMIN_USER", "bantu_admin")
        admin_email = os.environ.get("BANTU_DEFAULT_ADMIN_EMAIL", "admin@bantudevlab.africa")
        admin_password = os.environ.get("BANTU_DEFAULT_ADMIN_PASSWORD", "BantuAdmin2026!")
        mnemonic_seed = os.environ.get("BANTU_DEFAULT_ADMIN_MNEMONIC", DEFAULT_ADMIN_MNEMONIC)

        _, public_y = ZKPCrypto.generate_keypair(secret_seed=mnemonic_seed)
        public_key_hex = format(public_y, "x")

        accounts = [
            (admin_username, admin_email, admin_password, "CIV"),
            ("kouame_dev", "kouame_dev@bantudevlab.africa", admin_password, "CIV"),
        ]

        for username, email, password, country in accounts:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "is_staff": True,
                    "is_superuser": True,
                    "is_active": True,
                },
            )
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password(password)
            user.save()

            SovereignIdentity.objects.update_or_create(
                user=user,
                defaults={
                    "public_key_y": public_key_hex,
                    "country_code": country,
                    "is_verified": True,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Comptes administrateurs souverains prets : {admin_username} / kouame_dev (ZKP + Django Admin)."
            )
        )
