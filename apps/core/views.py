from django.db.models import Avg
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai_assistant.models import AIInteractionLog
from apps.gitea_client.client import GiteaClient
from apps.security_scanner.models import SecurityAuditReport
from apps.zkp_auth.models import SovereignIdentity

from .models import SovereignOrganization


def home_view(request):
    """Page d'accueil de la forge logicielle souveraine BANTUDEVLAB."""
    repos = GiteaClient().list_repositories()[:3]
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
    client = GiteaClient()
    repos = client.list_repositories()
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


class SovereignOrganizationListCreateView(APIView):
    """
    DEV-02: Support Multi-Tenancy & Organisations Africaines.
    Endpoints pour créer et lister les entités souveraines (banques centrales, ministères, universités, startups).
    """

    def get(self, request):
        entity_type = request.query_params.get("entity_type")
        country = request.query_params.get("country")
        queryset = SovereignOrganization.objects.all()

        if entity_type:
            queryset = queryset.filter(entity_type=entity_type)
        if country:
            queryset = queryset.filter(country_code=country.upper())

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
                "repositories_count": org.repositories.count(),
                "created_at": org.created_at.isoformat(),
            }
            for org in queryset
        ]
        return Response({"count": len(orgs), "organizations": orgs}, status=status.HTTP_200_OK)

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
