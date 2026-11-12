@echo off
REM =========================================================================
REM  BANTUDEVLAB - Script de Deploiement Automatique Docker
REM =========================================================================

echo [1/3] Verification des prerequis Docker...
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Docker n'est pas installe ou pas dans le PATH.
    echo Veuillez installer Docker Desktop depuis https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo [2/3] Construction et demarrage des conteneurs BANTUDEVLAB...
docker compose up -d --build

if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Le demarrage de la composition Docker a echoue.
    pause
    exit /b %ERRORLEVEL%
)

echo [3/3] Deploiement termine avec succes !
echo.
echo =========================================================================
echo  SERVICES BANTUDEVLAB DISPONIBLES :
echo =========================================================================
echo  - Portail BantuDevLab  : http://localhost:8001/
echo  - Connexion Gitea      : http://localhost:3002/user/login
echo  - Moteur Forge Git     : http://localhost:3001/
echo.
echo  Provisionnement des comptes :
echo  - Administrateur : configure via variables d'environnement (BANTU_ADMIN_USER, BANTU_ADMIN_PASSWORD)
echo  - Demonstration CADEV 2026 : compte 'cadev_evaluator' (authentification ZKP sans mot de passe)
echo =========================================================================
pause
