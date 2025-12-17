@echo off
REM make.bat v2 - Avec support VENV force

REM 1. Chemin vers le Python de l'environnement virtuel
set VENV_PYTHON=.\venv\Scripts\python.exe
set VENV_PIP=.\venv\Scripts\pip.exe

REM 2. Verification si venv existe
if not exist "%VENV_PYTHON%" (
    echo [ERREUR] L'environnement virtuel n'existe pas.
    echo Veuillez lancer : python -m venv venv
    goto end
)

if "%1" == "" goto help

if "%1" == "install" (
    echo Installation dans le venv...
    "%VENV_PIP%" install -r ../requirements.txt
    "%VENV_PIP%" install -r ../dev_requirements.txt
    goto end
)

if "%1" == "test" (
    echo Lancement de tous les tests...
    "%VENV_PYTHON%" -m pytest tests/
    goto end
)

if "%1" == "unit_test" (
    echo Lancement des tests unitaires...
    "%VENV_PYTHON%" -m pytest -k "not performance" tests/
    goto end
)

if "%1" == "perf_test" (
    echo Lancement des tests de performance...
    "%VENV_PYTHON%" -m pytest -k "performance" tests/
    goto end
)

if "%1" == "coverage" (
    echo Generation du rapport de couverture...
    "%VENV_PYTHON%" -m coverage run -m pytest -k "not performance" tests/
    "%VENV_PYTHON%" -m coverage report -m
    "%VENV_PYTHON%" -m coverage html
    goto end
)

if "%1" == "lint" (
    echo Verification de la qualite du code...
    "%VENV_PYTHON%" -m ruff check src/ tests/
    goto end
)

if "%1" == "doc" (
    echo Generation de la documentation...
    "%VENV_PYTHON%" -m pdoc --html --output-dir docs src/
    goto end
)

:help
echo Usage: .\make [target]
echo Targets disponibles: install, test, unit_test, perf_test, coverage, lint, doc

:end