@echo off

start "" "C:\Users\yusuf\miniconda3\envs\aurashift\pythonw.exe" "oyun.py"
"AuraShift.exe"
taskkill /F /IM pythonw.exe >nul 2>&1
