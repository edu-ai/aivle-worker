import logging

from .entry_point import start

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    start()
    # start_sandbox()
