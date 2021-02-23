#!/usr/bin/env sh

echo $NODE_NAME
echo $PIPELINE_NODE
echo $NODE_LABELS
echo $RESERVE
echo $PWD
set -ex
echo "$BRANCH_NAME"

export GITHUB_TOKEN="$GIT_TOKEN"


pip install pip==20.2.3
pip install -r requirements.txt
make build

NAME=quartic_sdk
VERSION=$(awk '$1 == "__version__" {print $NF}' ./quartic_sdk/_version.py | sed "s/'//g")
OS=none
CPU_ARCH=any

WHEEL_FILENAME="$NAME-$VERSION-py3-$OS-$CPU_ARCH.whl"
CODE=$(curl -sS -w '%{http_code}' -F package="@dist/$WHEEL_FILENAME" -o output.txt "https://$GEMFURY_AUTH_TOKEN@push.fury.io/quartic-ai/")
cat output.txt && rm -rf output.txt
if [[ "$CODE" =~ ^2 ]]; then
    echo "$WHEEL_FILENAME Package published successfully"
else
    echo "ERROR: server returned HTTP code $CODE"
    exit 1
fi

if [[ "$BRANCH_NAME" =~ ^[v0-9]*\.[x0-9]*\.[x0-9]*$ ]]; then
  curl -SfL https://github.com/github/hub/releases/download/v2.13.0/hub-linux-amd64-2.13.0.tgz | tar xzv --wildcards 'hub-*/bin/hub' --strip=2
  ./hub release create --draft --prerelease="$VERSION" -t "$BRANCH_NAME" branch -F CHANGELOG.md
  pip install twine==3.3.0 wheel==0.36.2
  twine upload dist/*
fi
