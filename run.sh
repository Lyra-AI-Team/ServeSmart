#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv …"
  curl -Ls https://astral.sh/uv/install.sh | sh
  # add $HOME/.local/bin or the directory uv’s installer prints to your PATH
  export PATH="$HOME/.local/bin:$PATH"
fi

# 2. Create / reuse a virtual-env with Python 3.11
if [ ! -d ".venv" ]; then
  uv venv --python=3.11 .venv
fi
source .venv/bin/activate

# 3. Lightning-fast dependency install
uv pip install -r backend/requirements.txt

pushd backend/app >/dev/null
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
popd >/dev/null

pushd frontend >/dev/null
if [ ! -d "node_modules" ]; then
  npm install --legacy-peer-deps
fi
npm run dev
popd >/dev/null

echo "Stopping backend..."
kill "$BACKEND_PID"