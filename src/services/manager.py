from loguru import logger
from typing import List

class TestManager:
    def __init__(self, test_runner, loader):
        self.test_runner = test_runner
        self.loader = loader
        self.results = {}

    def run_tests(self):
        args_list = self.loader.load_args()
        hosts = self.loader.load_hosts()

        if not args_list or not hosts:
            logger.error("No valid args or hosts to test")
            return

        self._run_test_batch(args_list, hosts)
        return self.results

    def _run_test_batch(self, args_list: List[List[str]], hosts: List[str]):
        for args in args_list:
            try:
                logger.info(f"Testing with args: {' '.join(args)}")
                self.test_runner.start_test(args)
                
                success_count = 0
                consecutive_errors = 0
                max_consecutive_errors = 5
                
                for host in hosts:
                    try:
                        if self.test_runner.test_connection(host):
                            success_count += 1
                            consecutive_errors = 0
                        else:
                            consecutive_errors += 1
                            logger.error(f"Connection test failed for {host}")
                    except Exception as e:
                        consecutive_errors += 1
                        logger.error(f"Connection test failed for {host}: {str(e)}")
                    
                    if consecutive_errors >= max_consecutive_errors:
                        logger.warning(f"Too many consecutive errors ({consecutive_errors}), skipping this strategy")
                        break
                
                if consecutive_errors < max_consecutive_errors:
                    success_rate = success_count / len(hosts) * 100
                    logger.info(f"Test completed. Success rate: {success_rate:.2f}%")
                    self.results[' '.join(args)] = success_rate
                else:
                    logger.warning(f"Skipping strategy {' '.join(args)} due to consecutive errors")
                    self.results[' '.join(args)] = 0
                
                self.test_runner.stop_test()
            except Exception as e:
                logger.error(f"Test with args {' '.join(args)} failed: {str(e)}")
                self.results[' '.join(args)] = 0 