# frozen_string_literal: true

# GitLab Source Fusion: Gemma 5B AI Review Service
# lib/gitlab/ci/gemma_review_service.rb

module Gitlab
  module Ci
    class GemmaReviewService
      API_ENDPOINT = "http://127.0.0.1:8001/api/ai/review-pr/"

      def self.review_merge_request(merge_request)
        diff_text = merge_request.raw_diffs.to_a.map(&:diff).join("\n")
        payload = {
          pr_title: merge_request.title,
          pr_description: merge_request.description,
          diff_content: diff_text,
          target_branch: merge_request.target_branch
        }

        response = Gitlab::HTTP.post(
          API_ENDPOINT,
          headers: { 'Content-Type' => 'application/json' },
          body: payload.to_json,
          timeout: 30
        )

        return unless response.success?

        review_data = response.parsed_response
        note_body = "### Revue IA Souveraine (Gemma 5B)\n\n#{review_data['analysis']}\n\n**Recommandations de sécurité :**\n#{review_data['recommendations']}"
        merge_request.notes.create!(
          author: User.find_by_username('gemma_ai_reviewer') || User.first,
          note: note_body
        )
      end
    end
  end
end
