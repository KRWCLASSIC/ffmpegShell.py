@echo off
timeout /t 1 /nobreak >nul
pip install -r requirements.txt
timeout /t 3 /nobreak >nul
exit