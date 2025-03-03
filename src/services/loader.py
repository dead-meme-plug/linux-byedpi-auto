from typing import List
from pathlib import Path
from loguru import logger
from core.config import settings

class Loader:
    @staticmethod
    def _validate_file(file_path: str) -> bool:
        path = Path(file_path)
        if not path.exists():
            logger.error(f"File {file_path} does not exist")
            return False
        if not path.is_file():
            logger.error(f"{file_path} is not a file")
            return False
        if path.stat().st_size == 0:
            logger.error(f"File {file_path} is empty")
            return False
        return True

    @staticmethod
    def _format_host(host: str) -> str:
        host = host.strip()
        if not host.startswith(('http://', 'https://')):
            return f'https://{host}'
        return host

    @staticmethod
    def load_args() -> List[List[str]]:
        if not Loader._validate_file(settings.ARGS_FILE):
            return []
        
        with open(settings.ARGS_FILE, 'r') as file:
            return [line.strip().split() for line in file if line.strip() and not line.startswith('#')]

    @staticmethod
    def load_hosts() -> List[str]:
        if not Loader._validate_file(settings.HOSTS_FILE):
            return []
        
        with open(settings.HOSTS_FILE, 'r') as file:
            return [Loader._format_host(line) for line in file if line.strip()]
