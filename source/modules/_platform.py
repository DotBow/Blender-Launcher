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
