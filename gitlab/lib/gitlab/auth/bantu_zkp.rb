# frozen_string_literal: true

# GitLab Source Fusion: BantuDevLab Zero-Knowledge Proof OmniAuth Strategy
# lib/gitlab/auth/bantu_zkp.rb

require 'omniauth-oauth2'

module Gitlab
  module Auth
    class BantuZkp < OmniAuth::Strategies::OAuth2
      option :name, 'bantu_zkp'

      option :client_options, {
        site: 'http://127.0.0.1:8001',
        authorize_url: '/api/zkp/challenge/',
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
