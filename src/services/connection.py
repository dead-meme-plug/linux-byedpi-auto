from abc import ABC, abstractmethod
import subprocess
import httpx
from loguru import logger
from typing import List, Protocol
from core.config import settings

class IConnectionTester(Protocol):
    def test_connection(self, host: str) -> bool: ...

class IProcessManager(Protocol):
    def start_byedpi(self, args: List[str]) -> subprocess.Popen: ...
    def stop_byedpi(self, process: subprocess.Popen): ...

class HTTPConnectionTester(IConnectionTester):
    def __init__(self):
        self.timeout = settings.TIMEOUT
        self.proxy = settings.PROXY_URL
        self.limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }

    def test_connection(self, host: str) -> bool:
        try:
            if not host.startswith(('http://', 'https://')):
                host = f'https://{host}'
            
            with httpx.Client(
                proxy=self.proxy,
                timeout=self.timeout,
                limits=self.limits
            ) as client:
                logger.debug(f"Testing connection to {host}")
                response = client.get(host)
                logger.debug(f"Response from {host}: {response.status_code}")
                return True
        except Exception as e:
            logger.error(f"Connection test failed for {host}: {str(e)}")
            return False

class ByeDPIProcessManager(IProcessManager):
    def start_byedpi(self, args: List[str]) -> subprocess.Popen:
        command = [settings.BYEDPI_PATH] + args
        return subprocess.Popen(command)

    def stop_byedpi(self, process: subprocess.Popen):
        process.terminate()
