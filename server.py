"""Main Module"""

import logging
import argparse

from flask import Flask

from settings import Configurations
from src.api_v1 import v1

HOST = Configurations.HOST
PORT = Configurations.PORT

app = Flask(__name__)

app.register_blueprint(blueprint=v1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SMSWithoutBorders Custom Platform WhatsApp"
    )
    parser.add_argument(
        "-l", "--logs", default="info", help="Set server log level (default = INFO)"
    )
    args = parser.parse_args()

    log_level_value = args.logs.upper()
    log_level_numeric_value = getattr(logging, log_level_value, None)
    if not isinstance(log_level_numeric_value, int):
        raise ValueError(f"Invalid log level: {log_level_value}")

    logging.basicConfig(level=log_level_numeric_value)

    app.run(host=HOST, port=PORT)
