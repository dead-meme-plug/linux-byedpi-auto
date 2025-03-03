import signal
from loguru import logger
from services.connection import HTTPConnectionTester, ByeDPIProcessManager
from services.loader import Loader
from services.runner import TestRunner
from services.manager import TestManager
from utils.logger import setup_logger
from utils.reporter import Reporter
from typing import Dict

class Application:
    def __init__(self):
        self.test_runner = TestRunner(
            connection_tester=HTTPConnectionTester(),
            process_manager=ByeDPIProcessManager()
        )
        self.test_manager = TestManager(
            test_runner=self.test_runner,
            loader=Loader()
        )
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

    def _handle_signal(self, signum, frame):
        logger.info(f"Received signal {signum}, terminating...")
        self.test_runner.stop_test()
        exit(0)

    def run(self):
        results = self.test_manager.run_tests()
        self._generate_report(results)

    def _generate_report(self, results: Dict[str, float]):
        logger.info("\nTest Results:")
        for args, success_rate in results.items():
            logger.info(f"Args: {args} - Success Rate: {success_rate:.2f}%")
        
        Reporter.save_results(results)

if __name__ == "__main__":
    setup_logger()
    app = Application()
    app.run()
