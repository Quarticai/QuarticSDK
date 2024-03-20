#!/usr/bin/env sh

echo $NODE_NAME
echo $PIPELINE_NODE
echo $NODE_LABELS
echo $RESERVE
echo $PWD
set -ex

rand=$(shuf -i 1000000000-9999999999 -n 1)

apt-get install libcurl4-gnutls-dev -y
pip install -U pip==23.1.0
pip install pip-tools==6.13.0

echo "installing requirements"
#bash ./jenkins_scripts/update_dependency.sh $BRANCH_NAME

cat requirements.txt
pip install -r requirements.txt

make test
echo "end....."
