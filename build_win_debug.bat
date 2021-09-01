if exist __pycache__ rd /S /Q __pycache__
if exist build rd /S /Q build
if exist dist rd /S /Q dist
if exist "Blender Launcher.spec" del /Q "Blender Launcher.spec"

python -OO -m PyInstaller ^
--hidden-import "pynput.keyboard._win32" ^
--hidden-import "pynput.mouse._win32" ^
--clean ^
--noconsole ^
--noupx ^
--onefile ^
--debug=all ^
--icon="source\resources\icons\desktop.ico" ^
--name="Blender Launcher" ^
--version-file="version.txt" ^
--add-binary="source\resources\icons\winblender.ico;files" ^
source\main.py
