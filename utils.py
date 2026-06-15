import os
import subprocess
import signal
import time
import psutil
from env import SYSTEM_PLATFORM
from helpers import print_message, ERROR, SUCCESS


current_parent = 0


def restart_parent_tree(process: psutil.Process, deep: int, delay_seconds: float = 1.0):
    global current_parent
    parent = process.parent()
    current_parent += 1
    if current_parent == deep and deep != 0:
        parent = None
    if parent is None:
        cmdline = process.cmdline()
        parent_executable = cmdline
        print_message(f"Parent executable: {parent_executable[0]}")

        time.sleep(delay_seconds)

        process.send_signal(signal.SIGTERM)
        print_message(f"Sent SIGTERM to parent process {process.pid}")

        subprocess.Popen(cmdline)
        return True
    return restart_parent_tree(parent, deep)


def restart_parent_terminal_process(deep: int = 2):
    parent_pid = os.getppid()
    print_message(f"Parent terminal PID: {parent_pid}")

    try:
        parent_proc = restart_parent_tree(psutil.Process(parent_pid), deep)

        return parent_proc

    except psutil.NoSuchProcess:
        print_message(f"Error: Parent process {parent_pid} not found.", ERROR)
    except psutil.AccessDenied as e:
        print_message(f"Error: Access denied when signaling parent process {parent_pid}: {e}", ERROR)
    except Exception as e:
        print_message(f"An error occurred while killing the parent: {e}", ERROR)

    return False


def set_env_variable(name, value):
    os.environ[name] = value


    if SYSTEM_PLATFORM == 'Windows':
        subprocess.call(
            ['setx', name, value],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print_message(f"Variable successfully set.", SUCCESS, force=True)
        process_restarted = restart_parent_terminal_process(deep=0)
        if process_restarted:
            print_message('Parent process successfully restarted.', SUCCESS, force=True)
        

    elif SYSTEM_PLATFORM in ('Linux', 'Darwin'):
        shell_profile = os.path.expanduser('~/.bashrc')
        with open(shell_profile, 'a', encoding='utf-8') as f:
            f.write(f'\nexport {name}="{value}"\n')
        print_message(f"Added to '{shell_profile}'. Run 'source {shell_profile}' to apply.", SUCCESS, force=True)
