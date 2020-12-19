import json
import re
import time
from pathlib import Path
from subprocess import CalledProcessError

from PyQt5.QtCore import QThread, pyqtSignal

from modules._platform import _check_output, get_platform, set_locale


class BuildInfo:
    file_version = "1.0"
    # https://www.blender.org/download/lts/
    lts_tags = ('2.83', '2.93', '3.3', '3.7')

    def __init__(self, link_type, link, subversion,
                 build_hash, commit_time, branch, size=None):
        self.link_type = link_type
        self.link = link
        self.subversion = subversion
        self.build_hash = build_hash
        self.commit_time = commit_time

        if branch == 'stable' and subversion.startswith(self.lts_tags):
            branch = 'lts'

        self.branch = branch
        self.size = size

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
            elif self.platform == 'Windows':
                return Path(self.link).stem
        elif self.link_type == 'path':
            return Path(self.link).name


class BuildInfoReader(QThread):
    finished = pyqtSignal('PyQt_PyObject')

    def __init__(self, path):
        QThread.__init__(self)
        self.path = Path(path)
        self.platform = get_platform()

    def run(self):
        build_info = self.read_build_info()
        self.finished.emit(build_info)
        return

    def read_blender_version(self):
        if self.platform == 'Windows':
            blender_exe = "blender.exe"
        elif self.platform == 'Linux':
            blender_exe = "blender"

        exe_path = self.path / blender_exe

        try:
            version = _check_output([exe_path.as_posix(), "-v"])
        except CalledProcessError:
            return 1

        version = version.decode('UTF-8')

        set_locale()
        ctime = re.search("build commit time: " + "(.*)", version)[1].rstrip()
        cdate = re.search("build commit date: " + "(.*)", version)[1].rstrip()
        strptime = time.strptime(cdate + ' ' + ctime, "%Y-%m-%d %H:%M")
        commit_time = time.strftime("%d-%b-%y-%H:%M", strptime)
        build_hash = re.search("build hash: " + "(.*)", version)[1].rstrip()
        subversion = re.search("Blender " + "(.*)", version)[1].rstrip()

        try:
            subfolder = self.path.parent.name
            name = self.path.name

            if self.platform == 'Windows':
                folder_parts = name.replace(
                    "blender-", "").replace("-windows64", "").rsplit('-', 2)
            elif self.platform == 'Linux':
                folder_parts = name.replace(
                    "blender-", "").replace("-linux64", "").rsplit('-', 2)

            if subfolder == 'experimental':
                branch = folder_parts[0]
            elif subfolder == 'daily':
                branch = "daily"
            elif subfolder == 'stable':
                branch = "stable"
                subversion = folder_parts[0]
            elif subfolder == 'custom':
                branch = self.path.name
        except Exception:
            branch = None

        self.write_build_info(branch, subversion, build_hash, commit_time)

    def write_build_info(self, branch, subversion, build_hash, commit_time):
        data = {}

        data['file_version'] = BuildInfo.file_version
        data['blinfo'] = []

        data['blinfo'].append({
            'branch': branch,
            'subversion': subversion,
            'build_hash': build_hash,
            'commit_time': commit_time,
        })

        path = self.path / '.blinfo'

        with open(path, 'w') as file:
            json.dump(data, file)

        return 0

    def read_build_info(self):
        path = self.path / '.blinfo'

        if not path.is_file():
            if self.read_blender_version() == 1:
                return None

        with open(path) as file:
            data = json.load(file)

        if ('file_version' not in data) or (data['file_version'] != BuildInfo.file_version):
            if self.read_blender_version() == 1:
                return None
            else:
                return self.read_build_info()
        else:
            blinfo = data['blinfo'][0]

            build_info = BuildInfo(
                'path',
                self.path.as_posix(),
                blinfo['subversion'],
                blinfo['build_hash'],
                blinfo['commit_time'],
                blinfo['branch']
            )

            return build_info
