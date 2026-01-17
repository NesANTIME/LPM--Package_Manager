import sys
import time
import itertools


def message(msg, msg_completed, duration = 0.8, num = 1):
    spinner = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
    end_time = time.time() + duration
    indent = " " * num

    while time.time() < end_time:
        sys.stdout.write(f"\r\033[K{indent}{msg} {next(spinner)}")
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write(f"\r\033[K{indent}{msg_completed}\n")
    sys.stdout.flush()