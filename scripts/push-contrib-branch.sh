#!/usr/bin/env bash
set -euo pipefail

readonly repo=$(mktemp -d)
readonly artefact=$(mktemp)
readonly tag="${GITHUB_REF##*/}"
readonly version="${tag#v}"

readonly release=$(curl -fs "${GITHUB_API_URL}/repos/${GITHUB_REPOSITORY}/releases/tags/$tag")
readonly artefact_url=$(echo "$release" | jq -r ".assets[0].browser_download_url")

curl -sfL -o "$artefact" "$artefact_url"

git clone \
	--branch master \
	https://github.com/Kapeli/Dash-User-Contributions.git \
	"$repo"

cd "$repo"

readonly branch_name="terraform-$tag"

git checkout -b "$branch_name"
cd docsets/Terraform

readonly tgz_name="Terraform.tgz"

docset_json=$(mktemp)
cat docset.json | \
	jq \
		--arg version "$version" \
		--arg tgz "$tgz_name" \
		--indent 4 \
		'
			.version = $version |
			.specific_versions =
				[{
					version: $version,
					archive: ("versions/"+$version+"/"+$tgz)
				}] +
				.specific_versions
		' \
	> "$docset_json"

mkdir -p "versions/$version"

mv "$docset_json" docset.json
cp "$artefact" "$tgz_name"
cp "$artefact" "versions/$version/$tgz_name"

git add -A
git commit -m "Terraform.docset $tag"

git push \
	"https://${CI_USER_USERNAME}:${CI_USER_ACCESS_TOKEN}@github.com/roberth-k/Dash-User-Contributions.git" \
	"HEAD:$branch_name"
