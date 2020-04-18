import locale
import re
import time
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, pyqtSignal

from modules.build_info import BuildInfo
from modules._platform import get_platform


class Scraper(QThread):
    links = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent

    def run(self):
        self.links.emit(self.get_download_links())
        return

    def get_download_links(self):
        links = []

        # Stable Builds
        links.extend(self.scrap_stable_releases())

        # Daily Builds
        daily_builds = self.scrap_download_links(
            "https://builder.blender.org/download")
        for link in daily_builds:
            links.append(link)

        # Experimental Branches
        experimental = self.scrap_download_links(
            "https://builder.blender.org/download/branches")
        for link in experimental:
            links.append(link)

        return links

    def scrap_download_links(self, url, _limit=None):
        platform = get_platform()
        content = urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        links = []

        if platform == 'Windows':
            for tag in soup.find_all(limit=_limit, href=re.compile(r'blender-.+win.+64.+zip')):
                links.append(self.new_blender_build(tag, url))
        elif platform == 'Linux':
            for tag in soup.find_all(limit=_limit, href=re.compile(r'blender-.+linux.+64.+tar')):
                links.append(self.new_blender_build(tag, url))

        return links

    def new_blender_build(self, tag, url):
        link = urljoin(url, tag['href']).rstrip('/')

        info = urlopen(link).info()
        size = str(int(info['content-length']) // 1048576)

        commit_time = None
        build_hash = None

        label = Path(link).stem
        label = label.replace("blender-", "")
        label = label.replace("-windows64", "")
        label_parts = label.rsplit('-', 2)

        if len(label_parts) > 2:
            subversion = label_parts[1]
            branch = label_parts[0]
            build_hash = label_parts[2]
            commit_time = self.get_commit_time(build_hash)
        elif len(label_parts) > 1:
            subversion = label_parts[0]
            branch = 'daily'
            build_hash = label_parts[1]
            commit_time = self.get_commit_time(build_hash)
        else:
            subversion = label_parts[0]
            branch = 'stable'

        if commit_time is None:
            platform = get_platform()

            if platform == 'Windows':
                locale.setlocale(locale.LC_ALL, 'eng_usa')
            elif platform == 'Linux':
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

            self.strptime = time.strptime(
                info['last-modified'], '%a, %d %b %Y %H:%M:%S %Z')
            commit_time = time.strftime("%d-%b-%y-%H:%M", self.strptime)

        return BuildInfo('link', link, subversion, build_hash, commit_time, branch, size)

    def scrap_stable_releases(self):
        releases = []
        url = "https://ftp.nluug.nl/pub/graphics/blender/release/"
        content = urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')

        for release in soup.find_all(href=re.compile(r'Blender\d+.+')):
            releases.append(urljoin(url, release['href']))

        releases = releases[-4:]
        stable_links = []

        for release in releases:
            links = self.scrap_download_links(release)

            for link in links:
                stable_links.append(link)

        return stable_links

    def get_commit_time(self, commit):
        try:
            commit_url = "https://git.blender.org/gitweb/gitweb.cgi/blender.git/commit/"
            content = urlopen(commit_url + commit).read()
            soup = BeautifulSoup(content, 'html.parser')
            datetime = soup.find_all("span", {"class": "datetime"})[1].text
            platform = get_platform()

            if platform == 'Windows':
                locale.setlocale(locale.LC_ALL, 'eng_usa')
            elif platform == 'Linux':
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

            self.strptime = time.strptime(
                datetime, '%a, %d %b %Y %H:%M:%S %z')
            commit_time = time.strftime("%d-%b-%y-%H:%M", self.strptime)
            return commit_time
        except Exception as e:
            return None
