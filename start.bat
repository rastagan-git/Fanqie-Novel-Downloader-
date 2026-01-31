@echo off
cd /d %~dp0
call venv\Scripts\activate
python super.py
pause