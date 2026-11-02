# frozen_string_literal: true

# GitLab Source Fusion: Sovereign Identity Model
# app/models/sovereign_identity.rb

class SovereignIdentity < ApplicationRecord
  belongs_to :user, inverse_of: :sovereign_identity

  validates :public_key_y, presence: true, uniqueness: true
  validates :country_code, presence: true, length: { is: 3 }

  scope :verified, -> { where(is_verified: true) }
  scope :by_country, ->(code) { where(country_code: code.to_s.upcase) }

  # Verify Zero-Knowledge Proof commitment on Git actions
  def verify_git_action_proof!(commitment_t, response_s, challenge_nonce)
    # Direct integration with BantuDevLab ZKP Schnorr verification engine
    uri = URI("http://127.0.0.1:8001/api/zkp/verify/")
    req = Net::HTTP::Post.new(uri, 'Content-Type' => 'application/json')
    req.body = {
      username: user.username,
      commitment_t: commitment_t,
      response_s: response_s,
      challenge_nonce: challenge_nonce
    }.to_json

    res = Net::HTTP.start(uri.hostname, uri.port) { |http| http.request(req) }
    res.is_a?(Net::HTTPSuccess)
  end
end
