#!/usr/bin/env bash
# SDD Workshop (FEH x VISEO) — laptop check for Mac and Linux.
# Run:  curl -fsSL https://aljabrialam.github.io/feh-sdd-guide/check-setup.sh | bash
# Read-only except for a temporary folder that is deleted at the end.

FAIL=0
if [ -t 1 ]; then G=$'\033[32m'; R=$'\033[31m'; Y=$'\033[33m'; B=$'\033[1m'; N=$'\033[0m'; else G=; R=; Y=; B=; N=; fi
ok()   { printf "  ${G}OK  ${N}  %s\n" "$1"; }
bad()  { printf "  ${R}FAIL${N}  %s\n" "$1"; FAIL=1; }
warn() { printf "  ${Y}WARN${N}  %s\n" "$1"; }
have() { command -v "$1" >/dev/null 2>&1; }

printf "\n${B}SDD workshop · laptop check${N}\n\n"

# 1. Git
if have git; then ok "Git        $(git --version | awk '{print $3}')"; else bad "Git        not found: install Git (step 2)"; fi

# 1b. Git identity
GN=$(git config --global user.name 2>/dev/null); GE=$(git config --global user.email 2>/dev/null)
if [ -n "$GN" ] && [ -n "$GE" ]; then ok "Git user   $GN <$GE>"; else bad "Git user   name or email not set: run the two 'git config' commands (step 2)"; fi

# 2. VS Code (required) + extensions
if [ -z "$(command -v code)" ] && [ -x "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" ]; then
  bad "VS Code    installed, but the 'code' command is off: Cmd+Shift+P > Shell Command: Install 'code' command in PATH (step 3)"
elif have code; then
  ok "VS Code    $(code --version 2>/dev/null | head -1)"
  EXT=$(code --list-extensions 2>/dev/null | tr 'A-Z' 'a-z'); MISS=""
  for e in ms-python.python dbaeumer.vscode-eslint esbenp.prettier-vscode ms-playwright.playwright; do echo "$EXT" | grep -qx "$e" || MISS="$MISS $e"; done
  if [ -z "$MISS" ]; then ok "Extensions Python, ESLint, Prettier, Playwright"; else bad "Extensions missing:$MISS (step 3)"; fi
else bad "VS Code    not found: install VS Code (step 3)"; fi

# 2b. Chrome
if [ -d "/Applications/Google Chrome.app" ] || have google-chrome || have google-chrome-stable; then ok "Chrome     installed"; else bad "Chrome     not found: install Google Chrome (step 3)"; fi

# 3. Node.js 22+
if have node; then
  NV=$(node --version); NM=${NV#v}; NM=${NM%%.*}
  if [ "$NM" -ge 22 ] 2>/dev/null; then ok "Node.js    $NV"; else bad "Node.js    $NV found, 22 or later needed (step 4)"; fi
else bad "Node.js    not found: install Node.js 22 LTS (step 4)"; fi

# 4. Python 3.12+ (a python.org install, or one fetched with 'uv python install 3.12')
PY=python3; have python3 || PY=python
PV=""; have "$PY" && PV=$("$PY" -c 'import sys;print("%d.%d.%d"%sys.version_info[:3])' 2>/dev/null)
if [ -n "$PV" ] && "$PY" -c 'import sys;sys.exit(0 if sys.version_info>=(3,12) else 1)' 2>/dev/null; then ok "Python     $PV"
elif have uv && UVPY=$(uv python find '>=3.12' 2>/dev/null) && [ -n "$UVPY" ]; then ok "Python     $("$UVPY" -c 'import sys;print("%d.%d.%d"%sys.version_info[:3])' 2>/dev/null) (via uv)"
elif [ -n "$PV" ]; then bad "Python     $PV found, 3.12 or later needed: run 'uv python install 3.12' (step 5)"
else bad "Python     not found: install Python 3.12+, or run 'uv python install 3.12' (step 5)"; fi

# 5. uv
if have uv; then ok "uv         $(uv --version | awk '{print $2}')"; else bad "uv         not found: install uv, then open a new terminal (step 6)"; fi

# 6. Django + Django REST Framework: create a throwaway project and run Django's own checks
#    If it fails on a certificate error, retry trusting the company's certificates to tell the two problems apart.
djcheck() {
  TMP=$(mktemp -d 2>/dev/null || mktemp -d -t sddcheck)
  (
    cd "$TMP" || exit 1
    uvx -q --from django django-admin startproject smoke . >/dev/null 2>err.txt || exit 2
    uvx -q --with djangorestframework --with djangorestframework-simplejwt --from django \
      python -c "import django,rest_framework,rest_framework_simplejwt;print(django.get_version(),rest_framework.VERSION)" > versions.txt 2>err.txt || exit 3
    uvx -q --with djangorestframework --from django python manage.py check > check.txt 2>&1 || exit 4
  )
  RC=$?
  ERR=$(cat "$TMP/err.txt" 2>/dev/null); VERS=$(cat "$TMP/versions.txt" 2>/dev/null)
  rm -rf "$TMP"
}
if have uv; then
  djcheck; CERTFIX=0
  if { [ $RC -eq 2 ] || [ $RC -eq 3 ]; } && echo "$ERR" | grep -qiE 'certificate|UnknownIssuer|--system-certs|native-tls'; then
    export UV_SYSTEM_CERTS=true UV_NATIVE_TLS=true; djcheck; unset UV_SYSTEM_CERTS UV_NATIVE_TLS; CERTFIX=1
  fi
  if [ $RC -eq 0 ]; then
    read -r DJ DRF <<< "$VERS"
    if [ $CERTFIX -eq 1 ]; then
      bad "Network    company network detected: run the 'company network fix' at the top of the steps, open a new window, run this again"
      warn "Django     $DJ and DRF $DRF work once that fix is on"
    else
      ok "Django     $DJ (test project passed 'manage.py check')"
      ok "DRF        $DRF (with simplejwt)"
    fi
  elif [ $RC -eq 2 ] || [ $RC -eq 3 ]; then bad "Django     could not download Django/DRF: network may be blocking PyPI. Try a phone hotspot, then tell Aljabri (step 7)"
  else bad "Django     test project failed 'manage.py check': send this screen to Aljabri"; fi
else bad "Django     skipped: needs uv first"; fi

# 7. Spec Kit
if have specify; then ok "Spec Kit   $(specify --version 2>/dev/null | tail -1)"; else bad "Spec Kit   'specify' not found: install it, then open a new terminal (step 8)"; fi

# 8. Playwright Chromium
PWDIR="${PLAYWRIGHT_BROWSERS_PATH:-}"
[ -z "$PWDIR" ] && { [ -d "$HOME/Library/Caches/ms-playwright" ] && PWDIR="$HOME/Library/Caches/ms-playwright" || PWDIR="$HOME/.cache/ms-playwright"; }
if ls -d "$PWDIR"/chromium* >/dev/null 2>&1; then ok "Playwright Chromium downloaded"; else bad "Playwright Chromium not found: run 'npx playwright install chromium' (step 9)"; fi

# 9. AI coding agent
warn "AI agent   TBC: we will confirm which one and how to install it (step 10)"

echo
if [ $FAIL -eq 0 ]; then printf "${G}${B}All set.${N} Take a screenshot of this window and send it to Aljabri.\n\n"
else printf "${R}${B}Some checks failed.${N} Fix the FAIL lines using the setup page, then run this again.\n\n"; fi
