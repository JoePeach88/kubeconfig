import os
import subprocess
import platform


def set_env_variable(name, value):
    os.environ[name] = value

    system = platform.system()

    if system == 'Windows':
        subprocess.call(
            ['set', f'{name}={value}'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True,
            close_fds=False
        )

    elif system in ('Linux', 'Darwin'):
        subprocess.call(
            ['export', f'{name}="{value}"'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True,
            close_fds=False
        )
