import hashlib
import json
from django.utils import timezone
from .models import AuditTrailLog


class AuditTrail:
    """
    Cryptographic manager for immutable audit logging.
    Implements a hash chain (Merkle/blockchain-like linked list) where each entry's
    current_hash is computed over:
        H_curr = SHA-256(H_prev || timestamp || action_type || actor || details_json)
    """

    GENESIS_HASH = '0' * 64

    @staticmethod
    def _compute_hash(prev_hash: str, timestamp_str: str, action_type: str, actor: str, details: dict) -> str:
        canonical_details = json.dumps(details, sort_keys=True, separators=(',', ':'))
        payload = f"{prev_hash}|{timestamp_str}|{action_type}|{actor}|{canonical_details}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    @classmethod
    def record_event(cls, action_type: str, actor: str, details: dict = None) -> AuditTrailLog:
        """
        Records a new immutable audit event linked to the previous log entry.
        """
        if details is None:
            details = {}

        last_entry = AuditTrailLog.objects.order_by('-id').first()
        prev_hash = last_entry.current_hash if last_entry else cls.GENESIS_HASH

        now = timezone.now()
        timestamp_str = now.isoformat()

        current_hash = cls._compute_hash(
            prev_hash=prev_hash,
            timestamp_str=timestamp_str,
            action_type=action_type,
            actor=actor,
            details=details
        )

        log_entry = AuditTrailLog.objects.create(
            timestamp=now,
            action_type=action_type,
            actor=actor,
            details=details,
            prev_hash=prev_hash,
            current_hash=current_hash
        )
        return log_entry

    @classmethod
    def verify_chain_integrity(cls) -> bool:
        """
        Verifies the cryptographic integrity of the entire audit chain.
        Returns True if all hashes are valid and unbroken, False otherwise.
        """
        entries = list(AuditTrailLog.objects.order_by('id'))
        if not entries:
            return True

        expected_prev_hash = cls.GENESIS_HASH
        for entry in entries:
            if entry.prev_hash != expected_prev_hash:
                return False

            timestamp_str = entry.timestamp.isoformat()
            computed_hash = cls._compute_hash(
                prev_hash=entry.prev_hash,
                timestamp_str=timestamp_str,
                action_type=entry.action_type,
                actor=entry.actor,
                details=entry.details
            )

            if entry.current_hash != computed_hash:
                return False

            expected_prev_hash = entry.current_hash

        return True
