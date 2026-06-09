#!/bin/zsh

set -euo pipefail

# Load user shell environment so API keys from ~/.zshrc are available
# when this script is launched outside an interactive terminal.
if [[ -f "$HOME/.zprofile" ]]; then
  source "$HOME/.zprofile"
fi
if [[ -f "$HOME/.zshrc" ]]; then
  source "$HOME/.zshrc"
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
APP_DIR="$SCRIPT_DIR/codequest-ai-tutor"
ROOT_VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"
APP_VENV_PYTHON="$APP_DIR/.venv/bin/python"
APP_URL="http://127.0.0.1:8501"
HEALTH_URL="$APP_URL/_stcore/health"

if [[ -x "$ROOT_VENV_PYTHON" ]]; then
  PYTHON_CMD="$ROOT_VENV_PYTHON"
elif [[ -x "$APP_VENV_PYTHON" ]]; then
  PYTHON_CMD="$APP_VENV_PYTHON"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="$(command -v python3)"
else
  echo "Python 3 was not found."
  echo "Create the virtual environment first, then try again."
  read -r "?Press Enter to close this window..."
  exit 1
fi

if [[ ! -d "$APP_DIR" ]]; then
  echo "App folder not found: $APP_DIR"
  read -r "?Press Enter to close this window..."
  exit 1
fi

cd "$APP_DIR"

if ! "$PYTHON_CMD" -c "import streamlit" >/dev/null 2>&1; then
  echo "Streamlit is not installed for $PYTHON_CMD"
  echo "Install dependencies first with:"
  echo "  $PYTHON_CMD -m pip install -r requirements.txt"
  read -r "?Press Enter to close this window..."
  exit 1
fi

if curl -fsS "$HEALTH_URL" >/dev/null 2>&1; then
  echo "CodeQuest AI Tutor is already running. Opening dashboard..."
  open "$APP_URL"
  exit 0
fi

echo "Starting CodeQuest AI Tutor..."
"$PYTHON_CMD" -m streamlit run app/main.py --server.headless true > /tmp/codequest-ai-tutor.log 2>&1 &

for _attempt in {1..30}; do
  if curl -fsS "$HEALTH_URL" >/dev/null 2>&1; then
    echo "Dashboard is ready. Opening browser..."
    open "$APP_URL"
    exit 0
  fi
  sleep 1
done

echo "The app server did not become ready in time."
echo "Check the log at /tmp/codequest-ai-tutor.log"
read -r "?Press Enter to close this window..."
exit 1