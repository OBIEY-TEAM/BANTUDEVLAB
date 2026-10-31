from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from .engine import SecurityScannerEngine
from .models import SecurityAuditReport

class ScanCodeView(APIView):
    """
    Scans code snippets or files for vulnerabilities, hardcoded secrets,
    and digital sovereignty violations.
    Throttled to 10 req/min.
    """
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'scanner'

    def post(self, request):
        content = request.data.get('content')
        filename = request.data.get('filename', 'snippet.py')
        repository_name = request.data.get('repository_name', 'sovereign-repo')

        if not content:
            return Response({'error': 'content est requis pour le scan'}, status=status.HTTP_400_BAD_REQUEST)

        result = SecurityScannerEngine.scan_code(filename=filename, content=content)

        # Store persistent audit report
        SecurityAuditReport.objects.create(
            repository_name=repository_name,
            file_scanned=filename,
            total_issues=result['total_issues'],
            critical_count=result['critical'],
            high_count=result['high'],
            medium_count=result['medium'],
            sovereignty_score=result['sovereignty_score'],
            status_rating=result['status_rating'],
            raw_findings=result['issues'],
        )

        # Audit trail recording
        from apps.core.audit import AuditTrail
        AuditTrail.record_event(
            action_type='VULN_SCAN',
            actor=request.user.username if request.user.is_authenticated else 'anonymous-scanner',
            details={
                'repository': repository_name,
                'file_scanned': filename,
                'total_issues': result['total_issues'],
                'critical_count': result['critical'],
                'sovereignty_score': result['sovereignty_score'],
            }
        )

        return Response(result, status=status.HTTP_200_OK)


class SecurityAuditHistoryView(APIView):
    """Lists past security and sovereignty audit reports."""
    def get(self, request):
        audits = SecurityAuditReport.objects.all().order_by('-scanned_at')[:20]
        data = [
            {
                "id": a.id,
                "repository_name": a.repository_name,
                "file_scanned": a.file_scanned,
                "total_issues": a.total_issues,
                "critical_count": a.critical_count,
                "sovereignty_score": a.sovereignty_score,
                "status_rating": a.status_rating,
                "scanned_at": a.scanned_at.isoformat(),
            }
            for a in audits
        ]
        return Response({"count": len(data), "audits": data}, status=status.HTTP_200_OK)
