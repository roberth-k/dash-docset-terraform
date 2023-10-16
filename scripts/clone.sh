#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

readonly terraform_version=$1
readonly dstdir=$2

function clone {
    local repo=$1
    local tag=$2
    local dir=$3

    if [[ -f $dir/README.md ]]; then
        1>&2 echo "already cloned: $dir"
        return
    fi

    1>&2 echo "cloning: $repo@$tag"
    mkdir -p $dir
    ( \
        git clone -q -c advice.detachedHead=false -b $tag $repo $dir \
        || (1>&2 echo "failed: $repo@$tag") \
    ) &
}

mkdir -p $dstdir/terraform

clone https://github.com/hashicorp/terraform.git v$terraform_version $dstdir/terraform

while read line; do
    name=$(echo $line | cut -d' ' -f1)
    repo=$(echo $line | cut -d' ' -f2)
    tag=$(echo $line | cut -d' ' -f3)

    clone $repo $tag $dstdir/providers/$name
done < <(cat $SCRIPT_DIR/../version/providers)

wait
