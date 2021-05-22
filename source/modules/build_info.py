import json
import re
import time
from enum import Enum
from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal

from modules._platform import _check_output, get_platform, set_locale


class BuildInfo:
    file_version = "1.1"
    # https://www.blender.org/download/lts/
    lts_tags = ('2.83', '2.93', '3.3', '3.7')

    def __init__(self, link_type, link, subversion,
                 build_hash, commit_time, branch,
                 custom_name="", is_favorite=False):
        self.link_type = link_type
        self.link = link

        if any(w in subversion.lower()
               for w in ['release', 'candidate', 'rc']):
            subversion = re.sub('[a-zA-Z ]+', " RC ", subversion).rstrip()

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
            return self.get_name() == other.get_name()

    def get_name(self):
        if self.link_type == 'link':
            if self.platform == 'Linux':
                return Path(self.link).with_suffix('').stem
            elif self.platform in {'Windows', 'macOS'}:
                return Path(self.link).stem
        elif self.link_type == 'path':
            return Path(self.link).name


class BuildInfoReader(QThread):
    Mode = Enum('Mode', 'READ WRITE', start=1)
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, path, build_info=None, mode=Mode.READ):
        QThread.__init__(self)
        self.path = Path(path)
        self.build_info = build_info
        self.mode = mode
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

    def read_blender_version(self):
        set_locale()

        if self.platform == 'Windows':
            blender_exe = "blender.exe"
        elif self.platform == 'Linux':
            blender_exe = "blender"

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
        name = self.path.name

        if subfolder == 'daily':
            branch = "daily"
        elif subfolder == 'custom':
            branch = name
        else:
            if self.platform == 'Windows':
                folder_parts = name.replace(
                    "blender-", "").replace("-windows64", "").rsplit('-', 2)
            elif self.platform == 'Linux':
                folder_parts = name.replace(
                    "blender-", "").replace("-linux64", "").rsplit('-', 2)

            if subfolder == 'experimental':
                branch = re.findall(r'\+(.+?)\.', name)[0]
            elif subfolder == 'stable':
                branch = "stable"
                subversion = folder_parts[0]

        build_info = BuildInfo(
            'path',
            self.path.as_posix(),
            subversion,
            build_hash,
            commit_time,
            branch
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

        if not path.is_file():
            build_info = self.read_blender_version()
            self.write_build_info(build_info)
            return build_info

        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if ('file_version' not in data) or \
                (data['file_version'] != BuildInfo.file_version):
            build_info = self.read_blender_version()
            self.write_build_info(build_info)
            return build_info
        else:
            blinfo = data['blinfo'][0]

            build_info = BuildInfo(
                'path',
                self.path.as_posix(),
                blinfo['subversion'],
                blinfo['build_hash'],
                blinfo['commit_time'],
                blinfo['branch'],
                blinfo['custom_name'],
                blinfo['is_favorite']
            )

            return build_info
