#!/usr/bin/env sh

echo "Branch Name: $1"

if [[ $1 == 'release' ]]; then
  pip-compile
  pip-compile -f https://download.pytorch.org/whl/torch_stable.html model_requirements.in
else
  pip-compile --pre
  pip-compile --pre -f https://download.pytorch.org/whl/torch_stable.html model_requirements.in
fi
