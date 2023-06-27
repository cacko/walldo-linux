import os
import corelog
import logging

__name__ = "walldo"

corelog.register(os.environ.get("WALLDO_LOG_LEVEL", "INFO"))
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
