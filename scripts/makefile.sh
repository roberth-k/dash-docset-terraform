#!/usr/bin/env bash
set -euo pipefail

readonly srcdir=$1
readonly dstdir=$2

function emit_terraform_rules {
    local terraform_docs_dir="$srcdir/terraform/website/docs"

    find $terraform_docs_dir -type f -name '*.mdx' -print0 \
    | while read -d $'\0' input_file
    do
        provider_dir="$dstdir/Contents/Resources/Documents/terraform"
        emit_rule "terraform" $terraform_docs_dir $input_file $provider_dir
    done
}

function emit_provider_rules {
    local provider_src=$1

    provider_name=$(realpath --relative-to "$srcdir/providers" $provider_src)
    provider_dir="$dstdir/Contents/Resources/Documents/providers/$provider_name/latest/docs"

    if [[ -d "$provider_src/website/docs" ]]; then
        find "$provider_src/website/docs" -type f \( -name '*.md' -or -name '*.markdown' \) -print0 \
        | while read -d $'\0' input_file
        do
            if [[ "$input_file" == $provider_src/website/docs/cdktf/* ]]; then
                # Ignore CDKTF documentation.
                continue
            fi

            emit_rule "provider" "$provider_src/website/docs" $input_file $provider_dir
        done
    elif [[ -d "$provider_src/docs" ]]; then
        # tfproviderdocs style
        #
        # Some providers (e.g. AWS) have both docs/ and website/docs/, but if the
        # former exists, then the latter is just internal docs.
        find "$provider_src/docs" -type f \( -name '*.md' -or -name '*.markdown' \) -print0 \
        | while read -d $'\0' input_file
        do
            emit_rule "provider" "$provider_src/docs" $input_file $provider_dir
        done
    else
        1>&2 echo "provider $provider_src has an unknown structure"
        exit 1
    fi
}

function emit_rule {
    local flavor=$1
    local input_dir=$2
    local input_file=$3
    local provider_dir=$4

    local reldir=$(realpath -m --relative-to $input_dir $(dirname $input_file))
    local barename=$(basename "$input_file" | cut -d. -f1)

    local output_file
    case $(realpath --relative-to $input_dir $(dirname $input_file)) in
        r|resource|resources)
            output_file="$provider_dir/resources/$barename.html"
            ;;
        d|data-source|data-sources)
            output_file="$provider_dir/data-sources/$barename.html"
            ;;
        *)
            output_file="$provider_dir/$reldir/$barename.html"
            ;;
    esac

    # The following must be a heredoc to prevent output mangling
    # from the parallel searches.

    cat <<EOF

TARGETS += $(pwd)/$output_file
$(pwd)/$output_file: $(pwd)/$input_file
	@mkdir -p \$(dir \$@)
	render.py --in \$< --out \$@ --docset $(realpath -m $dstdir) --provider $(realpath -m $provider_dir) --flavor $flavor
EOF
}

echo "TARGETS :="

emit_terraform_rules

find "$srcdir/providers" -type d -mindepth 2 -maxdepth 2 -print0 \
| while read -d $'\0' provider_src
do
    emit_provider_rules $provider_src
done

# TODO
# The emit_ functions used to run in the background, and there used to be
# a wait here. But this resulted in a Makefile that didn't have the final
# html: rule, for example. Parallelism of the finds is preferred, so have
# to figure out what was going on here.

echo ""
echo "html: \$(TARGETS)"
echo ""
