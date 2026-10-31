from django.shortcuts import render
from apps.zkp_auth.models import SovereignIdentity
from apps.gitea_client.client import GiteaClient
from apps.gitea_client.models import SovereignRepository
from apps.security_scanner.models import SecurityAuditReport
from apps.ai_assistant.models import AIInteractionLog

def home_view(request):
    """Page d'accueil de la forge logicielle souveraine BANTUDEVLAB."""
    repos = GiteaClient().list_repositories()[:3]
    recent_audits = SecurityAuditReport.objects.all().order_by('-scanned_at')[:3]
    context = {
        'total_repos': len(repos),
        'sovereignty_level': '100% Panafricain',
        'active_nodes': 'Systalink Cloud (Abidjan, Dakar, Nairobi, Kigali)',
        'featured_repos': repos,
        'recent_audits': recent_audits,
    }
    return render(request, 'core/home.html', context)

def dashboard_view(request):
    """Tableau de bord unifié souverain."""
    client = GiteaClient()
    repos = client.list_repositories()
    identities_count = SovereignIdentity.objects.count()
    audits = SecurityAuditReport.objects.all().order_by('-scanned_at')[:10]
    interactions_count = AIInteractionLog.objects.count()

    avg_sovereignty = 98
    if audits.exists():
        avg_sovereignty = round(sum(a.sovereignty_score for a in audits) / len(audits))

    context = {
        'total_repos': len(repos),
        'repos': repos,
        'identities_count': identities_count,
        'audits': audits,
        'interactions_count': interactions_count,
        'avg_sovereignty': avg_sovereignty,
    }
    return render(request, 'core/dashboard.html', context)

def metrics_view(request):
    """Métriques de souveraineté numérique continentale."""
    return render(request, 'core/metrics.html')
