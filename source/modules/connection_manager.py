import ssl
import sys

from urllib3 import PoolManager, ProxyManager

from modules._platform import get_cwd, get_platform_full, is_frozen
from modules.settings import get_proxy_host, get_proxy_port


class ConnectionManager():
    def __init__(self, version, proxy_type=0) -> None:
        self.version = version
        self.proxy_type = proxy_type
        self.manager = None

        self._headers = {
            'user-agent': 'Blender Launcher/{0} ({1})'.format(
                self.version, get_platform_full())}

        if is_frozen() is True:
            self.cacert = sys._MEIPASS + "/files/custom.pem"
        else:
            self.cacert = (
                get_cwd() / "source/resources/certificates/custom.pem").as_posix()

    def setup(self):
        if self.proxy_type == 0:  # None
            self.manager = PoolManager(
                num_pools=50, maxsize=10, headers=self._headers,
                cert_reqs=ssl.CERT_REQUIRED,
                ca_certs=self.cacert)
        else:  # Use proxy
            if self.proxy_type == 1:  # HTTP
                scheme = "http://"
            elif self.proxy_type == 2:  # HTTPS
                scheme = "https://"
            elif self.proxy_type == 3:  # SOCKS4
                scheme = "socks4a://"
            elif self.proxy_type == 4:  # SOCKS5
                scheme = "socks5h://"

            ip = get_proxy_host()
            port = get_proxy_port()
            self.manager = ProxyManager(
                proxy_url="{0}{1}:{2}".format(scheme, ip, port),
                num_pools=50, maxsize=10, headers=self._headers,
                cert_reqs=ssl.CERT_REQUIRED,
                ca_certs=self.cacert)
