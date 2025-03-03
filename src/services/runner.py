from loguru import logger
from typing import List

class TestRunner:
    def __init__(self, connection_tester, process_manager):
        self.connection_tester = connection_tester
        self.process_manager = process_manager
        self.current_process = None

    def test_connection(self, host: str) -> bool:
        return self.connection_tester.test_connection(host)

    def run_single_test(self, args: List[str], hosts: List[str]) -> float:
        success_count = 0
        for host in hosts:
            logger.info(f"Testing connection to {host}")
            if self.test_connection(host):
                success_count += 1
        return success_count / len(hosts) * 100

    def start_test(self, args: List[str]):
        try:
            logger.debug(f"Starting ByeDPI with args: {args}")
            self.current_process = self.process_manager.start_byedpi(args)
            logger.debug("ByeDPI process started successfully")
        except Exception as e:
            logger.error(f"Failed to start ByeDPI with args {args}: {str(e)}")
            raise

    def stop_test(self):
        if self.current_process:
            try:
                logger.debug("Stopping ByeDPI process")
                self.process_manager.stop_byedpi(self.current_process)
                logger.debug("ByeDPI process stopped successfully")
                self.current_process = None
            except Exception as e:
                logger.error(f"Failed to stop ByeDPI process: {str(e)}") 