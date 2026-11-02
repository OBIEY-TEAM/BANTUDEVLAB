# =========================================================================
#  BANTUDEVLAB - Script PowerShell de Deploiement Automatique Docker
# =========================================================================

Write-Host "[1/3] Verification des prerequis Docker..." -ForegroundColor Cyan
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker n'est pas installe ou pas accessible dans le PATH."
    exit 1
}

Write-Host "[2/3] Construction et demarrage des conteneurs BANTUDEVLAB..." -ForegroundColor Cyan
docker compose up -d --build

if ($LASTEXITCODE -ne 0) {
    Write-Error "Le demarrage de la composition Docker a echoue avec le code $LASTEXITCODE."
    exit $LASTEXITCODE
}

Write-Host "[3/3] Deploiement termine avec succes !" -ForegroundColor Green
Write-Host ""
Write-Host "=========================================================================" -ForegroundColor Yellow
Write-Host " SERVICES BANTUDEVLAB DISPONIBLES :" -ForegroundColor Yellow
Write-Host "=========================================================================" -ForegroundColor Yellow
Write-Host " - Portail BantuDevLab : http://localhost:8001/"
Write-Host " - Connexion Gitea     : http://localhost:3002/user/login"
Write-Host " - Moteur Forge Git    : http://localhost:3001/"
Write-Host ""
Write-Host " Identifiants administrateur preconfigures :"
Write-Host " - Utilisateur : bantu_admin"
Write-Host " - Mot de passe : BantuAdmin2026!"
Write-Host "=========================================================================" -ForegroundColor Yellow
