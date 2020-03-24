if exist __pycache__ rd /S /Q __pycache__
if exist build rd /S /Q build
if exist dist rd /S /Q dist
if exist "Blender Launcher.spec" del /Q "Blender Launcher.spec"

python -OO -m PyInstaller ^
--clean ^
--noconsole ^
--noupx ^
--onefile ^
--windowed ^
--icon="resources\icons\bl_desktop.ico" ^
--name="Blender Launcher" ^
--version-file="version.txt" ^
main.py

pause
