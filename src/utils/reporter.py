from pathlib import Path
from loguru import logger
from typing import Dict

class Reporter:
    @staticmethod
    def save_results(results: Dict[str, float], file_path: str = "results.txt"):
        try:
            with open(file_path, 'w') as f:
                f.write("Args\tSuccess Rate\n")
                for args, rate in results.items():
                    f.write(f"{args}\t{rate:.2f}%\n")
            logger.info(f"Results saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}") 