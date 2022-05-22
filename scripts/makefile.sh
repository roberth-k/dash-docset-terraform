#!/usr/bin/env bash
set -euo pipefail

readonly srcdir=$1
readonly dstdir=$2
readonly terraform_docs_dir="$srcdir/terraform/website/docs"

echo "TARGETS :="

find $terraform_docs_dir -type f -name '*.mdx' -print0 \
| while read -d $'\0' input_file
do
    provider_dir="$dstdir/Contents/Resources/Documents/terraform"
    barename=$(basename "$input_file" | cut -d. -f1)
    output_file="$provider_dir/$(realpath -m --relative-to $terraform_docs_dir $(dirname $input_file))/$barename.html"

    echo ""
    echo "TARGET := $(pwd)/$output_file"
    echo "TARGETS += \$(TARGET)"
    echo "\$(TARGET): $(pwd)/$input_file"
    echo "	@mkdir -p \$(dir \$@)"
    echo "	render.py --in \$< --out \$@ --docset $(realpath -m $dstdir) --provider $(realpath -m $provider_dir)"
done

echo ""
echo "html: \$(TARGETS)"
echo ""
