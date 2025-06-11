# ssl_session.py
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl

class UnsafeSSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE  # ⛔ 禁用憑證驗證
        kwargs['ssl_context'] = context
        self.poolmanager = PoolManager(*args, **kwargs)

def get_ssl_skipping_session():
    session = requests.Session()
    session.mount("https://", UnsafeSSLAdapter())
    return session

# ✅ monkey patch 用的 .get
session = get_ssl_skipping_session()
get = session.get
# ssl_session.py 最後加這行測試
print("[DEBUG] SSL-skipping session mounted, verify mode:",
      session.adapters["https://"].poolmanager.connection_pool_kw['ssl_context'].verify_mode)
