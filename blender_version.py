import json
import os
import re
import subprocess
import time
from pathlib import Path
from subprocess import DEVNULL

from _platform import get_platform
from settings import *

if get_platform() == 'Windows':
    from subprocess import CREATE_NO_WINDOW


def write_blender_version(folder):
    # Read Blender Version
    platform = get_platform()

    if platform == 'Windows':
        blender_exe = "blender.exe"
    elif platform == 'Linux':
        blender_exe = "blender"

    exe_path = Path(get_library_folder()) / folder / blender_exe

    if platform == 'Windows':
        info = subprocess.check_output(
            [exe_path.as_posix(), "-v"],
            creationflags=CREATE_NO_WINDOW,
            shell=True,
            stderr=DEVNULL, stdin=DEVNULL)
    elif platform == 'Linux':
        info = subprocess.check_output(
            [exe_path.as_posix(), "-v"], shell=False,
            stderr=DEVNULL, stdin=DEVNULL)

    info = info.decode('UTF-8')

    ctime = re.search("build commit time: " + "(.*)", info)[1].rstrip()
    cdate = re.search("build commit date: " + "(.*)", info)[1].rstrip()
    strptime = time.strptime(cdate + ' ' + ctime, "%Y-%m-%d %H:%M")
    commit_time = time.strftime("%d-%b-%H:%M", strptime)
    build_hash = re.search("build hash: " + "(.*)", info)[1].rstrip()
    subversion = re.search("Blender " + "(.*)", info)[1].rstrip()

    try:
        folder_parts = folder.replace(
            "blender-", "").replace("-windows64", "").rsplit('-', 2)

        if len(folder_parts) > 2:
            branch = folder_parts[0]
        elif len(folder_parts) > 1:
            branch = "Experimental"
        else:
            branch = "Release"
    except e:
        branch = "None"

    # Write Version Information
    data = {}
    data['blinfo'] = []
    data.append({
        'branch': branch,
        'subversion': subversion,
        'build_hash': build_hash,
        'commit_time': commit_time,
    })

    path = Path(get_library_folder()) / folder / '.blinfo'

    with open(path, 'w') as file:
        json.dump(data, file)


def read_blender_version(folder):
    path = Path(get_library_folder()) / folder / '.blinfo'

    if not path.is_file():
        write_blender_version(folder)

    with open(path) as file:
        data = json.load(file)
        return data['blinfo'][0]
