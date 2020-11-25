import re
import time
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, pyqtSignal

from modules._platform import get_platform, set_locale
from modules.build_info import BuildInfo


class Scraper(QThread):
    links = pyqtSignal('PyQt_PyObject')
    new_bl_version = pyqtSignal('PyQt_PyObject')
    error = pyqtSignal()

    def __init__(self, parent, man):
        QThread.__init__(self)
        self.parent = parent
        self.manager = man

    def run(self):
        try:
            self.lts_tags = self.get_lts_tags()
            self.links.emit(self.get_download_links())
            self.new_bl_version.emit(self.get_latest_tag())
        except Exception:
            self.error.emit()

        self.manager.clear()
        return

    def get_latest_tag(self):
        r = self.manager.request(
            'GET', 'https://github.com/DotBow/Blender-Launcher/releases/latest')

        url = r.geturl()
        tag = url.rsplit('/', 1)[-1]

        r.release_conn()
        r.close()

        return tag

    def get_download_links(self):
        links = []

        # Stable Builds
        links.extend(self.scrap_stable_releases())

        # Daily Builds
        daily_builds = self.scrap_download_links(
            "https://builder.blender.org/download", 'daily')
        for link in daily_builds:
            links.append(link)

        # Experimental Branches
        experimental = self.scrap_download_links(
            "https://builder.blender.org/download/branches", 'experimental')
        for link in experimental:
            links.append(link)

        return links

    def scrap_download_links(self, url, branch_type, _limit=None):
        platform = get_platform()
        r = self.manager.request('GET', url)
        content = r.data
        soup = BeautifulSoup(content, 'html.parser')
        links = []

        if platform == 'Windows':
            for tag in soup.find_all(limit=_limit, href=re.compile(r'blender-.+win.+64.+zip')):
                links.append(self.new_blender_build(tag, url, branch_type))
        elif platform == 'Linux':
            for tag in soup.find_all(limit=_limit, href=re.compile(r'blender-.+lin.+64.+tar')):
                links.append(self.new_blender_build(tag, url, branch_type))

        r.release_conn()
        r.close()
        return links

    def new_blender_build(self, tag, url, branch_type):
        link = urljoin(url, tag['href']).rstrip('/')

        r = self.manager.request('HEAD', link)
        info = r.headers
        size = str(int(info['content-length']) // 1048576)

        commit_time = None
        build_hash = None

        stem = Path(link).stem
        match = re.findall(r'-\w{12}-', stem)

        if match:
            build_hash = match[-1].replace('-', '')

        # Old buidls style naming
        match = re.search(r'-\d\.\w+-', stem)

        if match is None:
            # New builds style naming
            match = re.search(r'-\d+\.\d+\.\d+-', stem)

        subversion = match.group(0).replace('-', '')

        if branch_type == 'experimental':
            branch = re.search(r'\A.+-blender', stem).group(0)[:-8]
            commit_time = self.get_commit_time(build_hash)
        elif branch_type == 'daily':
            branch = 'daily'
            commit_time = self.get_commit_time(build_hash)
        else:
            if re.sub(r'\D', '', subversion) in self.lts_tags:
                branch = 'lts'
            else:
                branch = 'stable'

        if commit_time is None:
            set_locale()
            self.strptime = time.strptime(
                info['last-modified'], '%a, %d %b %Y %H:%M:%S %Z')
            commit_time = time.strftime("%d-%b-%y-%H:%M", self.strptime)

        r.release_conn()
        r.close()
        return BuildInfo('link', link, subversion, build_hash, commit_time, branch, size)

    def scrap_stable_releases(self):
        releases = []
        url = "https://ftp.nluug.nl/pub/graphics/blender/release/"
        r = self.manager.request('GET', url)
        content = r.data
        soup = BeautifulSoup(content, 'html.parser')

        for release in soup.find_all(href=re.compile(r'Blender\d+\.\d+')):
            href = release['href']
            match = re.search(r'\d+\.\d+', href)

            if (float(match.group(0)) >= 2.79):
                releases.append(urljoin(url, release['href']))

        stable_links = []

        for release in releases:
            links = self.scrap_download_links(release, 'stable')

            for link in links:
                stable_links.append(link)

        r.release_conn()
        r.close()
        return stable_links

    def get_commit_time(self, commit):
        try:
            commit_url = "https://git.blender.org/gitweb/gitweb.cgi/blender.git/commit/"
            r = self.manager.request('GET', commit_url + commit)
            content = r.data
            soup = BeautifulSoup(content, 'html.parser')
            datetime = soup.find_all(
                "span", {"id": re.compile(r'lts-release-')})[1].text

            set_locale()
            self.strptime = time.strptime(
                datetime, '%a, %d %b %Y %H:%M:%S %z')
            commit_time = time.strftime("%d-%b-%y-%H:%M", self.strptime)
            r.release_conn()
            r.close()
            return commit_time
        except Exception as e:
            return None

    def get_lts_tags(self):
        tags = set()

        try:
            lts_url = "https://www.blender.org/download/lts/"
            r = self.manager.request('GET', lts_url)
            content = r.data
            soup = BeautifulSoup(content, 'html.parser')

            for release in soup.find_all(href=re.compile(r'lts-release-.+')):
                href = release['href']
                match = re.search(r'\d+', href)
                tags.add(match.group(0))

            r.release_conn()
            r.close()
            return tags
        except Exception as e:
            return None
