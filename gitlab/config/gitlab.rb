# GitLab Configuration - BantuDevLab Sovereign African Edition
# Fused with BantuDevLab Core (Zero-Trust ZKP, Gemma 5B, Sovereign SAST)

external_url 'http://git.cybersocle.site'

nginx['enable'] = true
nginx['listen_port'] = 80
nginx['listen_https'] = false

gitlab_rails['gitlab_shell_ssh_port'] = 2222
gitlab_rails['time_zone'] = 'Africa/Abidjan'

# African Sovereign Multi-Tenancy & Datacenter
gitlab_rails['instance_name'] = 'BANTUDEVLAB — GitLab Sovereign Panafrican'
gitlab_rails['extra_sign_in_text'] = 'Zero-Trust ZKP Sovereign African Authentication Enabled'

# Authentication: Integration of Bantu Zero-Knowledge Proof (ZKP) Strategy
# Charge la strategie OmniAuth Bantu ZKP si presente localement ou via initializer
[
  '/opt/gitlab/embedded/service/gitlab-rails/config/initializers/bantu_zkp.rb',
  '/opt/gitlab/embedded/service/gitlab-rails/lib/gitlab/auth/bantu_zkp.rb',
  File.expand_path('../../gitlab/lib/gitlab/auth/bantu_zkp.rb', __dir__ || '.'),
  File.expand_path('../lib/gitlab/auth/bantu_zkp.rb', __dir__ || '.'),
  File.expand_path('./gitlab/lib/gitlab/auth/bantu_zkp.rb', Dir.pwd)
].each do |strategy_file|
  if File.exist?(strategy_file)
    require strategy_file
    break
  end
end

gitlab_rails['omniauth_enabled'] = true
gitlab_rails['omniauth_allow_single_sign_on'] = ['bantu_zkp']
gitlab_rails['omniauth_block_auto_created_users'] = false
gitlab_rails['omniauth_providers'] = [
  {
    name: 'bantu_zkp',
    label: 'Connexion Souveraine Zero-Trust ZKP',
    strategy_class: 'Gitlab::Auth::BantuZkp',
    args: {
      client_id: 'bantu_gitlab_sovereign_client',
      client_secret: ENV['DJANGO_SECRET_KEY'] || '',
      strategy_class: 'Gitlab::Auth::BantuZkp',
      site: 'http://django_app:8000',
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

# Resource and Worker Optimization (Anti-Crash Loop & OOM Protection)
puma['worker_processes'] = 2
puma['min_threads'] = 1
puma['max_threads'] = 1
sidekiq['concurrency'] = 2
prometheus_monitoring['enable'] = false
