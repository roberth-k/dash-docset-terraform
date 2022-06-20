#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
GITHUB_API_URL=${GITHUB_API_URL:-https://api.github.com}

terraform_version=$( \
    curl -s "${GITHUB_API_URL}/repos/hashicorp/terraform/releases?per_page=1" \
    | jq -r '[.[] | select(.name) | .name][0]' \
)

# remove v from the start of the tag
terraform_version=${terraform_version#v}

docset_version="${terraform_version}.$(date +%y%m%d)"

echo "$terraform_version" > $SCRIPT_DIR/../version/terraform
echo "$docset_version" > $SCRIPT_DIR/../version/docset
