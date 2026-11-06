# GitLab Configuration - BantuDevLab Sovereign African Edition
# Fused with BantuDevLab Core (Zero-Trust ZKP, Gemma 5B, Sovereign SAST)

external_url 'http://localhost:3001'

gitlab_rails['gitlab_shell_ssh_port'] = 2222
gitlab_rails['time_zone'] = 'Africa/Abidjan'

# African Sovereign Multi-Tenancy & Datacenter
gitlab_rails['instance_name'] = 'BANTUDEVLAB — GitLab Sovereign Panafrican'
gitlab_rails['extra_sign_in_text'] = 'Zero-Trust ZKP Sovereign African Authentication Enabled'

# Authentication: Integration of Bantu Zero-Knowledge Proof (ZKP) Strategy
gitlab_rails['omniauth_enabled'] = true
gitlab_rails['omniauth_allow_single_sign_on'] = ['bantu_zkp']
gitlab_rails['omniauth_block_auto_created_users'] = false
gitlab_rails['omniauth_providers'] = [
  {
    name: 'bantu_zkp',
    label: 'Connexion Souveraine Zero-Trust ZKP',
    args: {
      client_id: 'bantu_gitlab_sovereign_client',
      client_secret: ENV['DJANGO_SECRET_KEY'] || '',
      site: 'http://127.0.0.1:8001',
      authorize_url: '/api/zkp/challenge/',
      token_url: '/api/zkp/verify/',
      user_info_url: '/api/zkp/userinfo/'
    }
  }
]

# GitLab CI/CD: Automated SAST & Gemma 5B AI Review
gitlab_ci['gitlab_ci_all_broken_builds'] = true
gitlab_rails['sast_scanner_endpoint'] = 'http://127.0.0.1:8001/api/security/scan/'
gitlab_rails['ai_assistant_endpoint'] = 'http://127.0.0.1:8001/api/ai/review-pr/'

# Webhook Secret Configuration
gitlab_rails['webhook_secret_token'] = ENV['GITLAB_WEBHOOK_SECRET'] || 'bantu_gitlab_webhook_secret_2026'
