from pathlib import Path
import os


cwd = Path.cwd()
dist = Path(r'source/resources/styles')
dark_styles = (cwd / dist / 'dark').glob('*.css')
light_styles = (cwd / dist / 'light').glob('*.css')

with open(dist / 'dark/global.qss', 'w') as outfile:
    for style in dark_styles:
        outfile.write(style.read_text())
        outfile.write("\n")

with open(dist / 'light/global.qss', 'w') as outfile:
    for style in light_styles:
        outfile.write(style.read_text())
        outfile.write("\n")

os.system('pyrcc5 source/resources/resources.qrc -o source/resources_rc.py')
