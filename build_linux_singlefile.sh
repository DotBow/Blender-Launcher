PYTHONOPTIMIZE=2 pyinstaller \
--clean \
--noconsole \
--noupx \
--onefile \
--windowed \
--icon="source/resources/icons/desktop.ico" \
--name="Blender Launcher" \
--version-file="source/version.txt" \
source/main.py
