import os
import platform
import sys
from locale import LC_ALL, setlocale
from subprocess import (DEVNULL, PIPE, STDOUT, Popen, call, check_call,
                        check_output)


def get_platform():
    platforms = {
        'linux': 'Linux',
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'macOS',
        'win32': 'Windows'
    }

    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


def get_platform_full():
    return ("{0} {1} {2}").format(get_platform(), os.name, platform.release())


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


def _popen(args):
    platform = get_platform()

    if platform == 'Windows':
        DETACHED_PROCESS = 0x00000008
        proc = Popen(args, shell=True, stdin=None, stdout=None, stderr=None,
                     close_fds=True, creationflags=DETACHED_PROCESS)
    elif platform == 'Linux':
        proc = Popen(args, shell=True, stdout=None, stderr=None,
                     close_fds=True,  preexec_fn=os.setpgrp,
                     env=get_environment())

    return proc


def _check_call(args):
    platform = get_platform()

    if platform == 'Windows':
        from subprocess import CREATE_NO_WINDOW

        returncode = check_call(args, creationflags=CREATE_NO_WINDOW,
                                shell=True, stderr=DEVNULL, stdin=DEVNULL)
    elif platform == 'Linux':
        returncode = check_call(
            args, shell=False, stderr=DEVNULL, stdin=DEVNULL)

    return returncode


def _call(args):
    platform = get_platform()

    if platform == 'Windows':
        from subprocess import CREATE_NO_WINDOW

        call(args, creationflags=CREATE_NO_WINDOW,
             shell=True, stdout=PIPE, stderr=STDOUT, stdin=DEVNULL)
    elif platform == 'Linux':
        pass


def _check_output(args):
    platform = get_platform()

    if platform == 'Windows':
        from subprocess import CREATE_NO_WINDOW

        output = check_output(args, creationflags=CREATE_NO_WINDOW,
                              shell=True, stderr=DEVNULL, stdin=DEVNULL)
    elif platform == 'Linux':
        output = check_output(args, shell=False, stderr=DEVNULL, stdin=DEVNULL)

    return output
