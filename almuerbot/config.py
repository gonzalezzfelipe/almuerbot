"""Handle configurable values for the whole of the package.

There are 2 different ways of overriding default configurations, and these
are, in order of importance:

* Environment variables:
  * Every configuration will be looked for in the environment as
      ``'ALMUERBOT_{key.upper()}'``.
* TOML configuration file.
  * A TOML config file can be placed on the following path:
    ``'{ALMUERBOT_HOME}/almuerbot.json'``. ``ALMUERBOT_HOME`` is to be defined
    on the environment, defaults to ``~``.

"""
import datetime as dt
import os
from collections import namedtuple

from almuerbot.utils import parse_from_env

ALMUERBOT_HOME = os.getenv('ALMUERBOT_HOME') or os.path.expanduser('~')
INSTALATION_DIR = os.path.dirname(os.path.realpath(__file__))

_constants = {}

# General
_constants.update({
    'ALMUERBOT_HOME': ALMUERBOT_HOME,
    'INSTALATION_DIR': INSTALATION_DIR,
    'DATABASE_URI': f'sqlite:///{ALMUERBOT_HOME}/almuerbot.db',
    'SECRET_KEY': 'dev',
    'WEBAPP_PORT': 5000,
    'WEBAPP_HOST': 'localhost',
    'WEBAPP_DEBUG': True,
    'MAX_DISTANCE': 2,
    'WEIGHTS': {
        'price_weight': 3, 'wait_time_weight': 2, 'innovation_weight': 5}
})

# Personal configurations in stardust config file.
try:
    with open(os.path.join(ALMUERBOT_HOME, 'almuerbot.json')) as _file:
        _user_config = json.load(_file)
except FileNotFoundError:
    _user_config = {}
_constants.update(_user_config)

# Environment variables
_env_config = {}
for key in _constants:
    env_key = key
    if not env_key.startswith('STARDUST_'):
        env_key = 'STARDUST_' + env_key
    if os.getenv(env_key, None) is not None:
        _env_config[key] = parse_from_env(os.getenv(env_key))
_constants.update(_env_config)

constants = (namedtuple('Constants', _constants)(**_constants))
