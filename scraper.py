import re
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, pyqtSignal

from _platform import get_platform
from urllib.parse import urljoin


class Scraper(QThread):
    download_row = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent

    def __del__(self):
        self.wait()

    def run(self):
        links = self.get_download_url()

        for link in links:
            self.download_row.emit(link)

    def get_download_url(self):
        links = []

        # Stable Build
        stable = self.scrap_download_links(
            "https://www.blender.org/download", _limit=1)
        links.append(stable[0].replace(
            "https://www.blender.org/download", "https://ftp.nluug.nl/pub/graphics/blender/release"))

        # Daily Builds
        links.extend(self.scrap_download_links(
            "https://builder.blender.org/download"))

        # Experimental Branches
        links.extend(self.scrap_download_links(
            "https://builder.blender.org/download/branches"))

        return links

    def scrap_download_links(self, url, _limit=None):
        platform = get_platform()
        content = urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        links = []

        if platform == 'Windows':
            for link in soup.find_all(limit=_limit, href=re.compile(r'blender-.+win.+64.+zip')):
                links.append(urljoin(url, link['href']).rstrip('/'))
        elif platform == 'Linux':
            for link in soup.find_all(limit=_limit, href=re.compile(r'blender-.+linux.+64.+tar')):
                links.append(urljoin(url, link['href']).rstrip('/'))

        return links
