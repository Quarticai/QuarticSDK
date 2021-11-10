#!/usr/bin/env sh

echo $NODE_NAME
echo $PIPELINE_NODE
echo $NODE_LABELS
echo $RESERVE
echo $PWD
set -ex
echo "$BRANCH_NAME"

export PUBLISH_PYPI=true
export GITHUB_TOKEN="$GIT_TOKEN"

pip install pip==20.2.3
pip install -r requirements.txt
