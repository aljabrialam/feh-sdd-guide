# SDD Workshop (FEH x VISEO) — laptop check for Windows PowerShell.
# Run:  irm https://aljabrialam.github.io/feh-sdd-guide/check-setup.ps1 | iex
# Read-only except for a temporary folder that is deleted at the end.

$script:fail = $false
function Ok($m)   { Write-Host "  OK    $m" -ForegroundColor Green }
function Bad($m)  { Write-Host "  FAIL  $m" -ForegroundColor Red; $script:fail = $true }
function Warn($m) { Write-Host "  WARN  $m" -ForegroundColor Yellow }
function Have($c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }

Write-Host ""
Write-Host "SDD workshop - laptop check" -ForegroundColor White
Write-Host ""

# 1. Git
if (Have git) { Ok ("Git        " + ((git --version) -replace 'git version ','')) } else { Bad "Git        not found: install Git for Windows (step 2)" }

# 1b. Git identity
if (Have git) {
  $gn = (git config --global user.name); $ge = (git config --global user.email)
  if ($gn -and $ge) { Ok "Git user   $gn <$ge>" } else { Bad "Git user   name or email not set: run the two 'git config' commands (step 2)" }
}

# 2. VS Code (required) + extensions
if (Have code) {
  Ok ("VS Code    " + ((code --version | Select-Object -First 1)))
  $ext = @(code --list-extensions | ForEach-Object { $_.ToLower() })
  $miss = @('ms-python.python','dbaeumer.vscode-eslint','esbenp.prettier-vscode','ms-playwright.playwright') | Where-Object { $ext -notcontains $_ }
  if ($miss.Count -eq 0) { Ok "Extensions Python, ESLint, Prettier, Playwright" } else { Bad ("Extensions missing: " + ($miss -join ', ') + " (step 3)") }
}
elseif ((Test-Path "$env:LOCALAPPDATA\Programs\Microsoft VS Code\Code.exe") -or (Test-Path "$env:ProgramFiles\Microsoft VS Code\Code.exe")) { Bad "VS Code    installed, but the 'code' command isn't on PATH: reinstall with 'Add to PATH' ticked (step 3)" }
else { Bad "VS Code    not found: install VS Code (step 3)" }

# 2b. Chrome
$chrome = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe", "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe")
if ($chrome | Where-Object { Test-Path $_ }) { Ok "Chrome     installed" } else { Bad "Chrome     not found: install Google Chrome (step 3)" }

# 3. Node.js 22+
if (Have node) {
  $nv = (node --version).Trim()
  $nm = [int]($nv.TrimStart('v').Split('.')[0])
  if ($nm -ge 22) { Ok "Node.js    $nv" } else { Bad "Node.js    $nv found, 22 or later needed (step 4)" }
} else { Bad "Node.js    not found: install Node.js 22 LTS (step 4)" }

# 4. Python 3.12+ (a python.org install, or one fetched with 'uv python install 3.12')
$py = $null
foreach ($c in @('python','py','python3')) { if (Have $c) { $py = $c; break } }
$pv = $null; $pyok = $false
if ($py) {
  $pv = (& $py -c "import sys;print('%d.%d.%d'%sys.version_info[:3])" 2>$null | Out-String).Trim()
  & $py -c "import sys;sys.exit(0 if sys.version_info>=(3,12) else 1)" 2>$null | Out-Null
  $pyok = ($LASTEXITCODE -eq 0 -and $pv)
}
$uvpy = $null
if (-not $pyok -and (Have uv)) { $uvpy = (uv python find '>=3.12' 2>$null | Out-String).Trim() }
if ($pyok) { Ok "Python     $pv" }
elseif ($uvpy -and (Test-Path $uvpy)) { Ok ("Python     " + ((& $uvpy -c "import sys;print('%d.%d.%d'%sys.version_info[:3])" | Out-String).Trim()) + " (via uv)") }
elseif ($pv) { Bad "Python     '$pv' found, 3.12 or later needed: run 'uv python install 3.12' (step 5)" }
else { Bad "Python     not found: install Python 3.12+, or run 'uv python install 3.12' (step 5)" }

# 5. uv
if (Have uv) { Ok ("uv         " + ((uv --version).Split(' ')[1])) } else { Bad "uv         not found: install uv, then reopen PowerShell (step 6)" }

# 6. Django + Django REST Framework: create a throwaway project and run Django's own checks
#    If it fails on a certificate error, retry trusting the company's certificates to tell the two problems apart.
function DjCheck {
  $tmp = Join-Path $env:TEMP ("sddcheck-" + [guid]::NewGuid().ToString('N').Substring(0,8))
  New-Item -ItemType Directory -Path $tmp | Out-Null
  Push-Location $tmp
  $r = @{ stage = 'ok'; vers = ''; err = '' }
  $r.err = (uvx -q --from django django-admin startproject smoke . 2>&1 | Out-String)
  if ($LASTEXITCODE -ne 0) { $r.stage = 'download' }
  if ($r.stage -eq 'ok') {
    $out = (uvx -q --with djangorestframework --with djangorestframework-simplejwt --from django python -c "import django,rest_framework,rest_framework_simplejwt;print(django.get_version(),rest_framework.VERSION)" 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0) { $r.stage = 'download'; $r.err = $out } else { $r.vers = ($out.Trim() -split "`r?`n")[-1] }
  }
  if ($r.stage -eq 'ok') {
    uvx -q --with djangorestframework --from django python manage.py check 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { $r.stage = 'check' }
  }
  Pop-Location
  Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
  return $r
}
if (Have uv) {
  $r = DjCheck; $certfix = $false
  if ($r.stage -eq 'download' -and $r.err -match 'certificate|UnknownIssuer|system-certs|native-tls') {
    $env:UV_SYSTEM_CERTS = 'true'; $env:UV_NATIVE_TLS = 'true'
    $r = DjCheck; $certfix = $true
    Remove-Item Env:UV_SYSTEM_CERTS, Env:UV_NATIVE_TLS -ErrorAction SilentlyContinue
  }
  if ($r.stage -eq 'ok') {
    $parts = $r.vers.Split(' ')
    if ($certfix) {
      Bad "Network    company network detected: run the 'company network fix' at the top of the steps, reopen PowerShell, run this again"
      Warn ("Django     " + $parts[0] + " and DRF " + $parts[1] + " work once that fix is on")
    } else {
      Ok ("Django     " + $parts[0] + " (test project passed 'manage.py check')")
      Ok ("DRF        " + $parts[1] + " (with simplejwt)")
    }
  } elseif ($r.stage -eq 'download') { Bad "Django     could not download Django/DRF: network may be blocking PyPI. Try a phone hotspot, then tell Aljabri (step 7)" }
  else { Bad "Django     test project failed 'manage.py check': send this screen to Aljabri" }
} else { Bad "Django     skipped: needs uv first" }

# 7. Spec Kit
if (Have specify) {
  $sv = ([regex]::Match(((specify --version 2>$null) | Out-String), '\d+\.\d+\.\d+')).Value
  if ($sv -and ([version]$sv -ge [version]'1.1.0')) { Ok "Spec Kit   $sv" }
  else { Bad ("Spec Kit   " + $(if ($sv) { $sv } else { 'unknown version' }) + " found, 1.1 or later needed: run 'uv tool install --force specify-cli' (step 8)") }
} else { Bad "Spec Kit   'specify' not found: install it, then reopen PowerShell (step 8)" }

# 8. Playwright Chromium
$pw = if ($env:PLAYWRIGHT_BROWSERS_PATH) { $env:PLAYWRIGHT_BROWSERS_PATH } else { Join-Path $env:LOCALAPPDATA 'ms-playwright' }
if (Test-Path (Join-Path $pw 'chromium*')) { Ok "Playwright Chromium downloaded" } else { Bad "Playwright Chromium not found: run 'npx playwright install chromium' (step 9)" }

# 9. GitHub Copilot (the script can't see the sign-in: step 10 has a chat test for that)
if (Have code) {
  if ($ext -contains 'github.copilot-chat') { Ok "Copilot    Copilot Chat installed (do the practice run in step 10)" }
  else { Bad "Copilot    Copilot Chat missing: run 'code --install-extension GitHub.copilot-chat' (step 10)" }
} else { Bad "Copilot    skipped: needs VS Code and the 'code' command first (step 3)" }

Write-Host ""
if (-not $script:fail) { Write-Host "All set. Take a screenshot of this window and send it to Aljabri." -ForegroundColor Green }
else { Write-Host "Some checks failed. Fix the FAIL lines using the setup page, then run this again." -ForegroundColor Red }
Write-Host ""
