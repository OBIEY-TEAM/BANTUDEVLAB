from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai_assistant.models import AIInteractionLog
from apps.gitea_client.client import GiteaClient
from apps.gitlab_client.client import GitLabClient
from apps.security_scanner.models import SecurityAuditReport
from apps.zkp_auth.models import SovereignIdentity

from .models import SovereignOrganization


def _positive_int(value, default):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    return number if number > 0 else default


def healthz_view(request):
    """Liveness : le processus repond (utilise par le healthcheck Docker)."""
    return JsonResponse({"status": "ok"})


def readyz_view(request):
    """Readiness : verifie la base de donnees et le cache (sans exposer de detail interne)."""
    from django.core.cache import cache
    from django.db import connection

    checks = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"
    try:
        cache.set("readyz", "1", 5)
        checks["cache"] = "ok" if cache.get("readyz") == "1" else "error"
    except Exception:
        checks["cache"] = "error"
    healthy = all(v == "ok" for v in checks.values())
    return JsonResponse(
        {"status": "ready" if healthy else "degraded", "checks": checks}, status=200 if healthy else 503
    )


def home_view(request):
    """Page d'accueil de la forge logicielle souveraine BANTUDEVLAB."""
    repos = (GitLabClient().list_repositories() or GiteaClient().list_repositories())[:3]
    recent_audits = SecurityAuditReport.objects.all().order_by("-scanned_at")[:3]
    context = {
        "total_repos": len(repos),
        "sovereignty_level": "100% Panafricain",
        "active_nodes": "Systalink Cloud (Abidjan, Dakar, Nairobi, Kigali)",
        "featured_repos": repos,
        "recent_audits": recent_audits,
    }
    return render(request, "core/home.html", context)


def dashboard_view(request):
    """Tableau de bord unifié souverain."""
    repos = GitLabClient().list_repositories() or GiteaClient().list_repositories()
    identities_count = SovereignIdentity.objects.count()
    audits = SecurityAuditReport.objects.all().order_by("-scanned_at")[:10]
    interactions_count = AIInteractionLog.objects.count()

    # PERF-03: Remplacement de la boucle d'agrégation Python par models.Avg SQL
    avg_aggregate = SecurityAuditReport.objects.aggregate(avg_score=Avg("sovereignty_score"))["avg_score"]
    avg_sovereignty = round(avg_aggregate) if avg_aggregate is not None else 98

    context = {
        "total_repos": len(repos),
        "repos": repos,
        "identities_count": identities_count,
        "audits": audits,
        "interactions_count": interactions_count,
        "avg_sovereignty": avg_sovereignty,
    }
    return render(request, "core/dashboard.html", context)


@cache_page(60)
def metrics_view(request):
    """Métriques de souveraineté numérique continentale (mises en cache 60s - PERF-04)."""
    return render(request, "core/metrics.html")


def faq_view(request):
    """Fiche FAQ complète et guide d'utilisation de la forge souveraine BANTUDEVLAB & GitLab."""
    return render(request, "core/faq.html")


class SovereignOrganizationListCreateView(APIView):
    """
    DEV-02: Support Multi-Tenancy & Organisations Africaines.
    Endpoints pour créer et lister les entités souveraines (banques centrales, ministères, universités, startups).
    """

    def get_permissions(self):
        # SEC-021: lecture pour tout utilisateur connecte, creation reservee aux administrateurs.
        return [IsAdminUser()] if self.request.method == "POST" else [IsAuthenticated()]

    def get(self, request):
        entity_type = request.query_params.get("entity_type")
        country = request.query_params.get("country")
        queryset = SovereignOrganization.objects.annotate(repo_total=Count("repositories")).order_by("id")

        if entity_type:
            queryset = queryset.filter(entity_type=entity_type)
        if country:
            queryset = queryset.filter(country_code=country.upper())

        total = queryset.count()
        page = _positive_int(request.query_params.get("page"), 1)
        page_size = min(_positive_int(request.query_params.get("page_size"), 20), 100)
        offset = (page - 1) * page_size

        orgs = [
            {
                "id": org.id,
                "name": org.name,
                "slug": org.slug,
                "entity_type": org.entity_type,
                "entity_type_display": org.get_entity_type_display(),
                "country_code": org.country_code,
                "description": org.description,
                "website": org.website,
                "sovereignty_level": org.sovereignty_level,
                "repositories_count": org.repo_total,
                "created_at": org.created_at.isoformat(),
            }
            for org in queryset[offset : offset + page_size]
        ]
        return Response(
            {"count": total, "page": page, "page_size": page_size, "organizations": orgs}, status=status.HTTP_200_OK
        )

    def post(self, request):
        name = request.data.get("name")
        slug = request.data.get("slug")
        entity_type = request.data.get("entity_type", "REGIONAL_STARTUP")
        country_code = request.data.get("country_code", "CIV")
        description = request.data.get("description", "")
        website = request.data.get("website", "")
        sovereignty_level = request.data.get("sovereignty_level", "Tier-1 Continental")

        if not name or not slug:
            return Response({"error": "name et slug sont requis"}, status=status.HTTP_400_BAD_REQUEST)

        if SovereignOrganization.objects.filter(slug=slug).exists():
            return Response(
                {"error": f"L'organisation avec le slug '{slug}' existe déjà."}, status=status.HTTP_400_BAD_REQUEST
            )

        org = SovereignOrganization.objects.create(
            name=name,
            slug=slug,
            entity_type=entity_type,
            country_code=country_code,
            description=description,
            website=website,
            sovereignty_level=sovereignty_level,
        )

        return Response(
            {
                "message": f"Organisation souveraine '{org.name}' créée avec succès.",
                "organization": {
                    "id": org.id,
                    "name": org.name,
                    "slug": org.slug,
                    "entity_type": org.entity_type,
                    "country_code": org.country_code,
                    "sovereignty_level": org.sovereignty_level,
                },
            },
            status=status.HTTP_201_CREATED,
        )
