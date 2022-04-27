PYTHONOPTIMIZE=2 pyinstaller \
--hidden-import "pynput.keyboard._xorg" \
--hidden-import "pynput.mouse._xorg" \
--hidden-import "python-xlib" \
--clean \
--noconsole \
--noupx \
--onefile \
--name="Blender Launcher" \
--add-binary="source/resources/certificates/custom.pem:files" \
source/main.py
