# tools/shell.py

import os


def run_command(cmd: str):
    return os.popen(cmd).read()
