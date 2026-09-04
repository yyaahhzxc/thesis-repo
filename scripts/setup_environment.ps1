# One-Click Environment Setup Script for Windows
# Run in PowerShell: .\scripts\setup_environment.ps1

Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "   Thesis Project Automated Environment Setup  " -ForegroundColor Cyan
Write-Host "===============================================`n" -ForegroundColor Cyan

# 1. Check & Install LaTeX Compiler (MiKTeX via winget)
Write-Host "[1/4] Checking LaTeX compiler..." -ForegroundColor Yellow
if (Get-Command pdflatex -ErrorAction SilentlyContinue) {
    $ver = (pdflatex --version | Select-Object -First 1)
    Write-Host "  -> [OK] pdflatex found: $ver" -ForegroundColor Green
} else {
    Write-Host "  -> [!] pdflatex not found. Attempting automatic installation via winget..." -ForegroundColor Magenta
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "  -> Installing MiKTeX (this may prompt Windows UAC approval)..." -ForegroundColor Yellow
        winget install --id MiKTeX.MiKTeX -e --accept-package-agreements --accept-source-agreements
        Write-Host "  -> [!] Note: You may need to restart VS Code or PowerShell after installation to refresh your system PATH." -ForegroundColor Magenta
    } else {
        Write-Host "  -> [ERROR] winget not detected. Please manually install TeX Live or MiKTeX from https://miktex.org/download" -ForegroundColor Red
    }
}

# 2. Install VS Code LaTeX Workshop Extension
Write-Host "`n[2/4] Checking VS Code LaTeX Workshop extension..." -ForegroundColor Yellow
if (Get-Command code -ErrorAction SilentlyContinue) {
    Write-Host "  -> Installing / Updating James-Yu.latex-workshop..." -ForegroundColor Cyan
    code --install-extension James-Yu.latex-workshop --force
    Write-Host "  -> [OK] Extension configured." -ForegroundColor Green
} else {
    Write-Host "  -> [!] 'code' CLI not found in PATH. Ensure you install 'LaTeX Workshop' manually in VS Code." -ForegroundColor Magenta
}

# 3. Setup Python Virtual Environment
Write-Host "`n[3/4] Setting up Python virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    Write-Host "  -> Creating venv..." -ForegroundColor Cyan
    python -m venv venv
} else {
    Write-Host "  -> Existing venv found." -ForegroundColor Green
}

if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "  -> Activating venv and installing requirements..." -ForegroundColor Cyan
    .\venv\Scripts\activate
    pip install -r requirements.txt
    Write-Host "  -> [OK] Python dependencies installed." -ForegroundColor Green
} else {
    Write-Host "  -> [!] venv activation script not found. Installing via global python..." -ForegroundColor Magenta
    pip install -r requirements.txt
}

# 4. Verify Paper Build
Write-Host "`n[4/4] Verifying paper compilation..." -ForegroundColor Yellow
if (Get-Command pdflatex -ErrorAction SilentlyContinue) {
    python scripts/build_paper.py
    Write-Host "`n===============================================" -ForegroundColor Green
    Write-Host "   Setup complete! All systems operational.    " -ForegroundColor Green
    Write-Host "===============================================`n" -ForegroundColor Green
} else {
    Write-Host "`n===============================================" -ForegroundColor Yellow
    Write-Host "   Setup nearly complete!                      " -ForegroundColor Yellow
    Write-Host "   Restart VS Code now so pdflatex is loaded.  " -ForegroundColor Yellow
    Write-Host "   Then run: python scripts/build_paper.py      " -ForegroundColor Yellow
    Write-Host "===============================================`n" -ForegroundColor Yellow
}
