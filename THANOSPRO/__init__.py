import heroku3
import os
import sys
import time

def strtobool(val):
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError("invalid boolean value %r" % (val,))

sb = strtobool
from logging import DEBUG, INFO, basicConfig, getLogger

from THANOSPRO.clients.session import H2, H3, H4, H5, rishu, THANOSPRO
from THANOSPRO.config import Config


StartTime = time.time()
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

bot = rishu
tbot = THANOSPRO


if not Config.API_HASH:
    LOGS.warning("Please fill var API_HASH to continue.")
    quit(1)


if not Config.APP_ID:
    LOGS.warning("Please fill var APP_ID to continue.")
    quit(1)


if not Config.BOT_TOKEN:
    LOGS.warning("Please fill var BOT_TOKEN to continue.")
    quit(1)
    
    
# if not Config.BOT_USERNAME:
#     LOGS.warning("Please fill var BOT USERNAME to continue.")
#     quit(1)
    

if not Config.DB_URI or Config.DB_URI == "Your value":    
    LOGS.warning("Please fill var DATABASE_URL to continue.")
    # quit(1) # Don't quit, let the database features fail gracefully or use local DB if implemented


if not Config.THANOSPRO_SESSION:
    LOGS.warning("Please fill var THANOSPRO_SESSION to continue.")
    quit(1)


try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = heroku3.from_key(Config.HEROKU_API_KEY).apps()[
            Config.HEROKU_APP_NAME
        ]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None


# global variables (moved to state.py to prevent circular imports)
from .state import *


# THANOSPRO
