@echo off
rem Double-click to start the Northstar tabletop agents (needs Python and the Ollama app running).
cd /d "%~dp0"
python server.py
pause
