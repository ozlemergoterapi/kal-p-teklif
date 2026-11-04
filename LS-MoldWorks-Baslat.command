#!/bin/bash
set -euo pipefail
export PATH="/opt/homebrew/opt/node@22/bin:/opt/homebrew/bin:/usr/local/opt/node@22/bin:/usr/local/bin:$PATH"
export PYTHONNOUSERSITE=1
on_error(){
  /usr/bin/osascript -e 'display alert "LS MoldWorks açılamadı" message "Kurulum tamamlanamadı. Terminal penceresindeki son hata metnini destek için paylaşın." as critical' || true
}
trap on_error ERR
project_dir="$(cd "$(dirname "$0")" && pwd)"
if [[ ! -f "$project_dir/package.json" || ! -f "$project_dir/requirements-cad.txt" ]]; then
  project_dir="$(/usr/bin/osascript -e 'POSIX path of (choose folder with prompt "LS MoldWorks program klasörünü seçin. İçinde package.json ve requirements-cad.txt dosyaları bulunmalı.")')" || exit 0
fi
if [[ ! -f "$project_dir/package.json" || ! -f "$project_dir/requirements-cad.txt" || ! -f "$project_dir/desktop/main.cjs" ]]; then
  /usr/bin/osascript -e 'display alert "Program klasörü bulunamadı" message "GitHub dosyalarının bulunduğu klasörü seçin. İçinde package.json ve desktop klasörü olmalı."'
  exit 1
fi
cd "$project_dir"
for tool in node npm python3.12 tesseract; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    /usr/bin/osascript -e 'display alert "Gerekli araç bulunamadı" message "Node 22, Python 3.12 ve Tesseract kurulu olmalı. Bu başlatıcı, bu araçları daha önce kurduğunuz bilgisayar içindir."'
    exit 1
  fi
done
printf '\nLS MOLDWORKS\nİlk kurulum otomatik hazırlanıyor. Bu pencereyi kapatmayın.\n\n'
if [[ ! -x .venv-cad/bin/python ]]; then
  python3.12 -m venv .venv-cad
fi
export LS_CAD_PYTHON="$project_dir/.venv-cad/bin/python"
python_fingerprint="$(/usr/bin/shasum -a 256 requirements-cad.txt | /usr/bin/awk '{print $1}')"
if [[ ! -f .venv-cad/.ls-requirements || "$(cat .venv-cad/.ls-requirements)" != "$python_fingerprint" ]]; then
  "$LS_CAD_PYTHON" -m pip install --requirement requirements-cad.txt
  "$LS_CAD_PYTHON" scripts/runtime_check.py
  printf '%s' "$python_fingerprint" > .venv-cad/.ls-requirements
fi
node_fingerprint="$(/usr/bin/shasum -a 256 package-lock.json | /usr/bin/awk '{print $1}')"
if [[ ! -f node_modules/.ls-package-lock || "$(cat node_modules/.ls-package-lock)" != "$node_fingerprint" || ! -f public/vendor/three.module.js ]]; then
  npm ci --no-audit --no-fund
  node node_modules/electron/install.js
  printf '%s' "$node_fingerprint" > node_modules/.ls-package-lock
fi
if [[ ! -f node_modules/electron/path.txt ]]; then
  node node_modules/electron/install.js
fi
printf '\nProgram açılıyor…\n'
"$project_dir/node_modules/.bin/electron" "$project_dir"
