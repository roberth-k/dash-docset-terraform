#!/usr/bin/env bash
set -euo pipefail

GITHUB_API_URL=${GITHUB_API_URL:-https://api.github.com}

terraform_version=$( \
    curl -s "${GITHUB_API_URL}/repos/hashicorp/terraform/releases?per_page=50" \
    | jq -r '[.[] | select(.draft == false and .prerelease == false) | select(.name) | .name][0]' \
)

# remove v from the start of the tag
terraform_version=${terraform_version#v}

echo "$terraform_version"
