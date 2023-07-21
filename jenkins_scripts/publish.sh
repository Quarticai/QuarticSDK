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

apt-get update && apt-get install libcurl4-gnutls-dev -y

pip install -U pip==22.0.4
pip install pip-tools==7.0.0

echo "creating requirements"
bash ./jenkins_scripts/update_dependency.sh $BRANCH_NAME

cat requirements.txt

pip install importlib-metadata==3.7.0

