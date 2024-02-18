import argparse
import logging

from functools import lru_cache
from injector import inject


class LogFactory:

    @inject
    def __init__(self, parsed_args: argparse.Namespace):
        self._parsed_args = parsed_args

    @lru_cache
    def logger(self, name: str):
        log_level = logging.DEBUG if self._parsed_args.debug else logging.WARNING

        logger = logging.getLogger(name)
        logger.setLevel(log_level)

        if not logger.hasHandlers():
            ch = logging.StreamHandler()
            ch.setLevel(log_level)

            formatter = logging.Formatter("%(message)s")
            ch.setFormatter(formatter)

            logger.addHandler(ch)

        return logger
