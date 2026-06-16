import heroku3
import os
import sys
import time

def strtobool(val):
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid boolean value %r" % (val,))

sb = strtobool
from logging import DEBUG, INFO, basicConfig, getLogger

from THANOSPRO.config import Config
from THANOSPRO.state import *


# StartTime will be initialized in the main startup function
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))


if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=INFO)


LOGS = getLogger(__name__)

# These will be initialized in the main startup function
bot = None
tbot = None

def validate_config():
    if not Config.API_HASH:
        LOGS.warning("Please fill var API_HASH to continue.")
        sys.exit(1)
    if not Config.APP_ID:
        LOGS.warning("Please fill var APP_ID to continue.")
        sys.exit(1)
    if not Config.BOT_TOKEN:
        LOGS.warning("Please fill var BOT_TOKEN to continue.")
        sys.exit(1)
    if not Config.DB_URI:    
        LOGS.warning("Please fill var DATABASE_URL to continue.")
        sys.exit(1)
    if not Config.THANOSPRO_SESSION:
        LOGS.warning("Please fill var THANOSPRO_SESSION to continue.")
        sys.exit(1)

def init_heroku():
    global HEROKU_APP
    try:
        if Config.HEROKU_API_KEY and Config.HEROKU_APP_NAME:
            HEROKU_APP = heroku3.from_key(Config.HEROKU_API_KEY).apps()[
                Config.HEROKU_APP_NAME
            ]
    except Exception:
        HEROKU_APP = None


# THANOSPRO
