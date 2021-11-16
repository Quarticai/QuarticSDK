#!/usr/bin/env sh

echo $NODE_NAME
echo $PIPELINE_NODE
echo $NODE_LABELS
echo $RESERVE
echo $PWD
set -ex

rand=$(shuf -i 1000000000-9999999999 -n 1)

make test
echo "end....."
