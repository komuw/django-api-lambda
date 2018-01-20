import os
import sys
import logging
import structlog

from django.core.management import execute_from_command_line

from log_lib import KeyValueRenderer

if __name__ == "__main__":
    # Set up structured logging
    logging.basicConfig(
        format="%(message)s\n",
        stream=sys.stdout,
        level=logging.DEBUG,
    )
    structlog.configure(
        logger_factory=structlog.stdlib.LoggerFactory(),
        processors=[
            structlog.processors.UnicodeEncoder(),
            KeyValueRenderer(),
        ]
    )

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    execute_from_command_line(sys.argv)
