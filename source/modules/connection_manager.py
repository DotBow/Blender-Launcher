import ssl
import sys

from urllib3 import PoolManager, ProxyManager, make_headers
from urllib3.contrib.socks import SOCKSProxyManager

from modules._platform import get_cwd, get_platform_full, is_frozen
from modules.settings import (get_proxy_host, get_proxy_password,
                              get_proxy_port, get_proxy_type, get_proxy_user,
                              get_use_custom_tls_certificates)

proxy_types_chemes = {
    1: "http://",
    2: "https://",
    3: "socks4a://",
    4: "socks5h://"
}


class ConnectionManager():
    def __init__(self, version, proxy_type=get_proxy_type()) -> None:
        self.version = version
        self.proxy_type = get_proxy_type()
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
        if self.proxy_type == 0:  # Use generic requests
            if get_use_custom_tls_certificates():
                # Generic requests with CERT_REQUIRED
                self.manager = PoolManager(
                    num_pools=50, maxsize=10, headers=self._headers,
                    cert_reqs=ssl.CERT_REQUIRED,
                    ca_certs=self.cacert)
            else:
                # Generic requests w/o CERT_REQUIRED
                self.manager = PoolManager(
                    num_pools=50, maxsize=10, headers=self._headers)
        else:  # Use Proxy
            ip = get_proxy_host()
            port = get_proxy_port()
            scheme = proxy_types_chemes[self.proxy_type]

            if self.proxy_type > 2:  # Use SOCKS Proxy
                if get_use_custom_tls_certificates():
                    # SOCKS Proxy with CERT_REQUIRED
                    self.manager = SOCKSProxyManager(
                        proxy_url="{0}{1}:{2}".format(scheme, ip, port),
                        num_pools=50, maxsize=10, headers=self._headers,
                        username=get_proxy_user(),
                        password=get_proxy_password(),
                        cert_reqs=ssl.CERT_REQUIRED, ca_certs=self.cacert)
                else:
                    # SOCKS Proxy w/o CERT_REQUIRED
                    self.manager = SOCKSProxyManager(
                        proxy_url="{0}{1}:{2}".format(scheme, ip, port),
                        num_pools=50, maxsize=10, headers=self._headers,
                        username=get_proxy_user(),
                        password=get_proxy_password())
            else:  # Use HTTP Proxy
                # HTTP Proxy autherification headers
                auth_headers = make_headers(
                    proxy_basic_auth='{0}:{1}'.format(
                        get_proxy_user(), get_proxy_password()))

                if get_use_custom_tls_certificates():
                    # HTTP Proxy with CERT_REQUIRED
                    self.manager = ProxyManager(
                        proxy_url="{0}{1}:{2}".format(scheme, ip, port),
                        num_pools=50, maxsize=10,
                        headers=self._headers, proxy_headers=auth_headers,
                        cert_reqs=ssl.CERT_REQUIRED, ca_certs=self.cacert)
                else:
                    # HTTP Proxy w/o CERT_REQUIRED
                    self.manager = ProxyManager(
                        proxy_url="{0}{1}:{2}".format(scheme, ip, port),
                        num_pools=50, maxsize=10,
                        headers=self._headers, proxy_headers=auth_headers)
