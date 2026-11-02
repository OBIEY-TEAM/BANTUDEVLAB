# frozen_string_literal: true

# GitLab Source Fusion: Sovereign Security Scanner Integration
# lib/gitlab/security/sovereignty_scanner.rb

module Gitlab
  module Security
    class SovereigntyScanner
      API_ENDPOINT = "http://127.0.0.1:8001/api/security/scan/"

      attr_reader :project, :commit

      def initialize(project, commit)
        @project = project
        @commit = commit
      end

      def execute!
        diff_payload = project.repository.diff_stats(commit.id)
        payload = {
          code_content: diff_payload,
          repository_url: project.http_url_to_repo,
          commit_sha: commit.sha,
          branch_name: commit.ref_name
        }

        response = Gitlab::HTTP.post(
          API_ENDPOINT,
          headers: { 'Content-Type' => 'application/json' },
          body: payload.to_json,
          timeout: 10
        )

        return unless response.success?

        record_audit_findings!(response.parsed_response)
      end

      private

      def record_audit_findings!(report)
        score = report['sovereignty_score'] || 100
        findings = report['findings'] || []

        # Enforce sovereign security gate
        if score < 70
          project.add_merge_request_security_block!(commit.sha, "Sovereignty score #{score}/100 is below the threshold.")
        end
      end
    end
  end
end
