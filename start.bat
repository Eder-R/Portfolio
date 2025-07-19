@echo off
echo ==== Iniciando LibManager ====

REM Caminho do Python embutido
set PYTHON=_python\pythonw.exe

REM Executa diretamente (sem start) para manter o terminal aberto
"%PYTHON%" LibManagerLauncher.py

REM Espera para mostrar o erro (caso ocorra)
echo.
echo [Pressione qualquer tecla para sair]
pause >nul
exit
