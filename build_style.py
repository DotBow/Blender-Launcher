from pathlib import Path
import os


cwd = Path.cwd()
dist = Path(r'source/resources/styles')
styles = (cwd / dist).glob('*.css')

with open(dist / 'global.qss', 'w') as outfile:
    for style in styles:
        outfile.write(style.read_text())
        outfile.write("\n")

os.system('pyrcc5 source/resources/resources.qrc -o source/resources_rc.py')
