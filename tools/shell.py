# tools/shell.py

import os


def run_command(cmd):

    result = os.system(cmd)

    return result
