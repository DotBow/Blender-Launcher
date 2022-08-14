import json
import re
import time
from enum import Enum
from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal

from modules._platform import _check_output, get_platform, set_locale


class BuildInfo:
    file_version = "1.2"
    # https://www.blender.org/download/lts/
    lts_tags = ('2.83', '2.93', '3.3', '3.7')

    def __init__(self, link, subversion,
                 build_hash, commit_time, branch,
                 custom_name="", is_favorite=False):
        self.link = link

        if any(w in subversion.lower()
               for w in ['release', 'rc']):
            subversion = re.sub(
                '[a-zA-Z ]+', " Candidate ", subversion).rstrip()

        self.subversion = subversion
        self.build_hash = build_hash
        self.commit_time = commit_time

        if branch == 'stable' and subversion.startswith(self.lts_tags):
            branch = 'lts'

        self.branch = branch
        self.custom_name = custom_name
        self.is_favorite = is_favorite

        self.platform = get_platform()

    def __eq__(self, other):
        if (self is None) or (other is None):
            return False
        elif (self.build_hash is not None) and (other.build_hash is not None):
            return self.build_hash == other.build_hash
        else:
            return self.subversion == other.subversion


class BuildInfoReader(QThread):
    Mode = Enum('Mode', 'READ WRITE', start=1)
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, path, build_info=None,
                 archive_name=None, mode=Mode.READ):
        QThread.__init__(self)
        self.path = Path(path)
        self.build_info = build_info
        self.mode = mode
        self.archive_name = archive_name
        self.platform = get_platform()

    def run(self):
        if self.mode == self.Mode.READ:
            try:
                build_info = self.read_build_info()
                self.finished.emit(build_info)
            except Exception:
                self.finished.emit(None)
        elif self.mode == self.Mode.WRITE:
            try:
                self.write_build_info(self.build_info)
                self.finished.emit(0)
            except Exception:
                self.finished.emit(None)

        return

    def read_blender_version(self, old_build_info=None):
        set_locale()

        if self.path.parent.name == 'bforartists':
            blender_exe = "bforartists.exe"
        elif self.platform == 'Windows':
            blender_exe = "blender.exe"
        elif self.platform == 'Linux':
            blender_exe = "blender"
        elif self.platform == 'macOS':
            blender_exe = "Blender/Blender.app/Contents/MacOS/Blender"

        exe_path = self.path / blender_exe
        version = _check_output([exe_path.as_posix(), "-v"])
        version = version.decode('UTF-8')

        ctime = re.search("build commit time: " + "(.*)", version)[1].rstrip()
        cdate = re.search("build commit date: " + "(.*)", version)[1].rstrip()
        strptime = time.strptime(cdate + ' ' + ctime, "%Y-%m-%d %H:%M")
        commit_time = time.strftime("%d-%b-%y-%H:%M", strptime)
        build_hash = re.search("build hash: " + "(.*)", version)[1].rstrip()
        subversion = re.search("Blender " + "(.*)", version)[1].rstrip()

        subfolder = self.path.parent.name

        if self.archive_name is None:
            name = self.path.name
        else:
            name = self.archive_name

        if subfolder == 'bforartists':
            branch = "bforartists"
        if subfolder == 'daily':
            branch = "daily"

            # If branch from console is empty, it is probably stable release
            if len(subversion.split(' ')) == 1:
                subversion += " Stable"
        elif subfolder == 'custom':
            branch = name
        elif subfolder == 'experimental':
            # Sensitive data! Requires proper folder naming!
            match = re.search(r'\+(.+?)\.', name)

            # Fix for naming conventions changes after 1.12.0 release
            if match is None:
                if old_build_info is not None:
                    branch = old_build_info.branch
            else:
                branch = match.group(1)
        elif subfolder == 'stable':
            branch = "stable"

        # Recover user defined favorites builds information
        custom_name = ""
        is_favorite = False

        if old_build_info is not None:
            custom_name = old_build_info.custom_name
            is_favorite = old_build_info.is_favorite

        build_info = BuildInfo(
            self.path.as_posix(),
            subversion,
            build_hash,
            commit_time,
            branch,
            custom_name,
            is_favorite
        )

        return build_info

    def write_build_info(self, build_info):
        data = {}

        data['file_version'] = BuildInfo.file_version
        data['blinfo'] = []

        data['blinfo'].append({
            'branch': build_info.branch,
            'subversion': build_info.subversion,
            'build_hash': build_info.build_hash,
            'commit_time': build_info.commit_time,
            'custom_name': build_info.custom_name,
            'is_favorite': build_info.is_favorite,
        })

        path = self.path / '.blinfo'

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file)

        return data

    def read_build_info(self):
        path = self.path / '.blinfo'

        # Check if build information is already present
        if path.is_file():
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            build_info = self.build_info_from_json(data['blinfo'][0])

            # Check if file version changed
            if ('file_version' not in data) or \
                    (data['file_version'] != BuildInfo.file_version):
                new_build_info = self.read_blender_version(build_info)
                self.write_build_info(new_build_info)
                return new_build_info
            else:
                return build_info
        # Generating new build information
        else:
            build_info = self.read_blender_version()
            self.write_build_info(build_info)
            return build_info

    def build_info_from_json(self, blinfo):
        build_info = BuildInfo(
            self.path.as_posix(),
            blinfo['subversion'],
            blinfo['build_hash'],
            blinfo['commit_time'],
            blinfo['branch'],
            blinfo['custom_name'],
            blinfo['is_favorite']
        )

        return build_info
