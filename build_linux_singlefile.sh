PYTHONOPTIMIZE=2 pyinstaller \
--clean \
--noconsole \
--noupx \
--onefile \
--windowed \
--icon="source/resources/icons/desktop.ico" \
--name="Blender Launcher" \
--add-binary="update.sh:files" \
source/main.py
