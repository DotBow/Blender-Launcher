import os
import sys
from locale import LC_ALL, setlocale


def get_platform():
    platforms = {
        'linux': 'Linux',
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OSX',
        'win32': 'Windows'
    }

    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


def set_locale():
    platform = get_platform()

    if platform == 'Windows':
        setlocale(LC_ALL, 'eng_usa')
    elif platform == 'Linux':
        setlocale(LC_ALL, 'en_US.UTF-8')


def get_environment():
    # Make a copy of the environment
    env = dict(os.environ)
    # For GNU/Linux and *BSD
    lp_key = 'LD_LIBRARY_PATH'
    lp_orig = env.get(lp_key + '_ORIG')

    if lp_orig is not None:
        # Restore the original, unmodified value
        env[lp_key] = lp_orig
    else:
        # This happens when LD_LIBRARY_PATH was not set
        # Remove the env var as a last resort
        env.pop(lp_key, None)

    return env
