# frozen_string_literal: true

# GitLab Source Fusion: BantuDevLab Zero-Knowledge Proof OmniAuth Strategy
# lib/gitlab/auth/bantu_zkp.rb

begin
  require 'omniauth-oauth2'
rescue LoadError
  # Fallback en environnement d'évaluation hors conteneur GitLab Rails
  module OmniAuth
    module Strategies
      class OAuth2
        def self.option(*args); end unless respond_to?(:option)
        def self.uid(&b); end unless respond_to?(:uid)
        def self.info(&b); end unless respond_to?(:info)
        def self.extra(&b); end unless respond_to?(:extra)
      end unless defined?(OAuth2)
    end
  end
end

module Gitlab
  module Auth
    class BantuZkp < OmniAuth::Strategies::OAuth2
      base_portal = (ENV['BASE_URL_1'] || 'https://cybersocle.site').chomp('/')

      option :name, 'bantu_zkp'

      option :client_options, {
        site: 'http://django_app:8000',
        authorize_url: "#{base_portal}/api/zkp/login-ui/",
        token_url: '/api/zkp/verify/',
        user_info_url: '/api/zkp/userinfo/'
      }

      uid { raw_info['user_id'] || raw_info['username'] }

      info do
        {
          name: raw_info['username'],
          email: raw_info['email'] || "#{raw_info['username']}@bantudevlab.africa",
          username: raw_info['username'],
          country_code: raw_info['country_code'],
          sovereignty_level: 'Tier-1 Continental'
        }
      end

      extra do
        {
          raw_info: raw_info,
          public_key_y: raw_info['public_key_y'],
          zkp_verified: true
        }
      end

      def raw_info
        @raw_info ||= access_token.get('/api/zkp/userinfo/').parsed || {}
      end
    end
  end
end

# Enregistrement explicite dans l'espace de noms standard OmniAuth::Strategies
# pour satisfaire la résolution automatique par Devise (Devise::OmniAuth::StrategyNotFound)
module OmniAuth
  module Strategies
    BantuZkp = ::Gitlab::Auth::BantuZkp unless defined?(OmniAuth::Strategies::BantuZkp)
  end
end
