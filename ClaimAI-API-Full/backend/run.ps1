Set-Location $PSScriptRoot
if (!(Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Run setup_windows.bat first."
    exit 1
}
& ".venv\Scripts\python.exe" app.py
