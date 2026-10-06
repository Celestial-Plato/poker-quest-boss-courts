@echo off
echo Boss Courts 1.4.0 - Close the game first. Existing BossCourts only.
py -3.11 "%~dp0install_update.py"
if errorlevel 1 goto done
echo Update completed. Restart Poker Quest and start a NEW RUN.
:done
pause
