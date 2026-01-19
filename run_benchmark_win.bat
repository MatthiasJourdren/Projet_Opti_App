@echo off
title Benchmark TSP - Automatisation

echo ========================================
echo       Lancement du Benchmark TSP
echo ========================================

:: Lancer le benchmark (utilisation de python, assurez-vous qu'il est dans le PATH)
python benchmark.py

:: Vérifier le code de retour (0 = succès)
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Benchmark termine avec succes.
    echo ----------------------------------------
    echo       Generation des graphiques...
    echo ----------------------------------------
    
    python plot_results.py
    
    echo.
    echo [OK] Termine ! Les resultats sont dans le dossier 'results'.
) else (
    echo.
    echo [ERREUR] Une erreur est survenue lors du benchmark.
)

:: Pause pour laisser la fenêtre ouverte
pause
