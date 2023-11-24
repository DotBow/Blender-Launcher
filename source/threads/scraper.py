import logging
import re
import time
import traceback
from pathlib import Path
from urllib.parse import urljoin

import cchardet
import lxml
from bs4 import BeautifulSoup, SoupStrainer
from modules._platform import get_platform, set_locale
from modules.build_info import BuildInfo
from PyQt5.QtCore import QThread, pyqtSignal


class Scraper(QThread):
    links = pyqtSignal('PyQt_PyObject')
    new_bl_version = pyqtSignal('PyQt_PyObject')
    error = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, parent, man):
        QThread.__init__(self)
        self.parent = parent
        self.manager = man
        self.platform = get_platform()

        if self.platform == 'Windows':
            filter = r'blender-.+win.+64.+zip$'
            filter_experimental = r'blender-[^\s\/]+-windows\.amd64-release\.zip'
        elif self.platform == 'Linux':
            filter = r'blender-.+lin.+64.+tar+(?!.*sha256).*'
        elif self.platform == 'macOS':
            filter = r'blender-.+(macOS|darwin).+dmg$'

        self.b3d_link = re.compile(filter)
        self.b3d_experimental_link = re.compile(filter_experimental)
        self.hash = re.compile(r'\w{12}')
        self.subversion = re.compile(r'-\d\.[a-zA-Z0-9.]+-')

    def run(self):
        self.get_download_links()
        self.new_bl_version.emit(self.get_latest_tag())
        self.manager.manager.clear()
        self.finished.emit()
        return

    def get_latest_tag(self):
        r = self.manager._request(
            'GET', 'https://github.com/DotBow/Blender-Launcher/releases/latest')

        if r is None:
            return

        url = r.geturl()
        tag = url.rsplit('/', 1)[-1]

        r.release_conn()
        r.close()

        return tag

    def get_download_links(self):
        # Stable Builds
        self.scrap_stable_releases()

        # Daily Builds
        self.scrap_download_links(
            "https://builder.blender.org/download/daily/", 'daily')

        # Experimental Branches
        self.scrap_download_links(
            "https://builder.blender.org/download/experimental", 'experimental')

    def scrap_download_links(self, url, branch_type, _limit=None, stable=False):
        r = self.manager._request('GET', url)

        if r is None:
            return

        content = r.data

        soup_stainer = SoupStrainer('a', href=True)
        soup = BeautifulSoup(content, 'lxml', parse_only=soup_stainer)

        if stable is False:
            for tag in soup.find_all(limit=_limit, href=re.compile(self.b3d_experimental_link)):
                build_info = self.new_blender_build(tag, url, branch_type)

                if build_info is not None:
                    self.links.emit(build_info)

        if stable is True:
            for tag in soup.find_all(limit=_limit, href=re.compile(self.b3d_link)):
                build_info = self.new_blender_build(tag, url, branch_type)

                if build_info is not None:
                    self.links.emit(build_info)

        r.release_conn()
        r.close()

    def new_blender_build(self, tag, url, branch_type):
        link = urljoin(url, tag['href']).rstrip('/')
        r = self.manager._request('HEAD', link)

        if r is None:
            return

        if r.status != 200:
            return None

        info = r.headers

        commit_time = None
        build_hash = None

        stem = Path(link).stem
        match = re.findall(self.hash, stem)

        if match:
            build_hash = match[-1].replace('-', '')

        match = re.search(self.subversion, stem)
        subversion = match.group(0).replace('-', '')

        if branch_type == 'stable':
            branch = 'stable'
        else:
            build_var = ""
            tag = tag.find_next("span", class_="build-var")

            # For some reason tag can be None on macOS
            if tag is not None:
                build_var = tag.get_text()

            if self.platform == 'macOS':
                if 'arm64' in link:
                    build_var = "{0} │ {1}".format(build_var, 'Arm')
                elif 'x86_64' in link:
                    build_var = "{0} │ {1}".format(build_var, 'Intel')

            if branch_type == 'experimental':
                branch = build_var
            elif branch_type == 'daily':
                branch = 'daily'
                subversion = "{0} {1}".format(subversion, build_var)

        if commit_time is None:
            set_locale()
            self.strptime = time.strptime(
                info['last-modified'], '%a, %d %b %Y %H:%M:%S %Z')
            commit_time = time.strftime("%d-%b-%y-%H:%M", self.strptime)

        r.release_conn()
        r.close()
        return BuildInfo(link, subversion,
                         build_hash, commit_time, branch)

    def scrap_stable_releases(self):
        url = "https://download.blender.org/release/"
        r = self.manager._request('GET', url)

        if r is None:
            return

        content = r.data
        soup = BeautifulSoup(content, 'lxml')

        b3d_link = re.compile(r'Blender\d+\.\d+')
        subversion = re.compile(r'\d+\.\d+')

        for release in soup.find_all(href=b3d_link):
            print (release)
            href = release['href']
            match = re.search(subversion, href)

            if (float(match.group(0)) >= 2.79):
                self.scrap_download_links(
                    urljoin(url, href), 'stable', stable=True)

        r.release_conn()
        r.close()
