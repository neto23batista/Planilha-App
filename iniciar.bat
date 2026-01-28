@echo off
title Controle Financeiro Profissional

echo.
echo ========================================
echo  Controle Financeiro Profissional
echo ========================================
echo.
echo Iniciando aplicativo...
echo.

python controle_financeiro_app.py

if errorlevel 1 (
    echo.
    echo ERRO: Nao foi possivel iniciar o aplicativo.
    echo Verifique se o Python esta instalado corretamente.
    echo.
    pause
)
