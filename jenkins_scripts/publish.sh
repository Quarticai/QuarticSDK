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

pip install -U pip
pip install pip-tools

echo "creating requirements"
bash ./jenkins_scripts/update_dependency.sh $BRANCH_NAME

cat requirements.txt
pip install -r requirements.txt

