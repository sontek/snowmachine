#!/usr/bin/env python
import os
import sys
import random
import time
import platform

snowflakes = {}

try:
    # Windows Support
    from colorama import init
    init()
except ImportError:
    pass


def get_terminal_size():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            cr = struct.unpack('hh', fcntl.ioctl(
                fd, termios.TIOCGWINSZ,
                '1234'))
        except:
            return None
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])

columns, rows = get_terminal_size()


def clear_screen(numlines=100):
    """Clear the console.

    numlines is an optional argument used only as a fall-back.
    """
    if os.name == "posix":
        # Unix/Linux/MacOS/BSD/etc
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
        os.system('cls')
    else:
        # Fallback for other operating systems.
        print('\n' * rows)


def get_random_flake():
    if not platform.system() == 'Windows':
        try:
            # python3 support
            try:
                cmd = unichr
            except NameError:
                cmd = chr

            flake = cmd(random.choice(range(0x2740, 0x2749)))

            return flake
        except:
            pass

    return " *"


current_rows = {}


def move_flake(col, stack):
    if stack:
        if col not in current_rows:
            current_rows[col] = rows

        current_row = current_rows[col]

        if current_row == 1:
            current_row = rows
            current_rows[col] = current_row
    else:
        current_row = rows

    # If next row is the end, lets start a new snow flake
    if snowflakes[col][0]+1 == current_row:
        snowflakes[col] = [1, get_random_flake()]

        if stack:
            current_rows[col] -= 1
    else:
        print("\033[%s;%sH  " % (snowflakes[col][0], col))

        snowflakes[col][0] += 1

        print("\033[%s;%sH%s" % (snowflakes[col][0], col, snowflakes[col][1]))

        print("\033[1;1H")


def main():
    if len(sys.argv) > 1:
        stack = sys.argv[1] == '--stack'
    else:
        stack = False

    clear_screen()

    while True:
        col = random.choice(range(1, int(columns)))
        # Don't print snowflakes right next to each other, since
        # unicode flakes take 2 spaces
        if col % 2 == 0:
            continue

        # its already on the screen, move it
        if col in snowflakes.keys():
            move_flake(col, stack)
        else:
        # otherwise put it on the screen
            flake = get_random_flake()
            snowflakes[col] = [1, flake]

            print("\033[%s;%sH%s" % (snowflakes[col][0], col,
                                     snowflakes[col][1]))

        # key any flakes on the screen moving
        for flake in snowflakes.keys():
            move_flake(flake, stack)

        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == "__main__":
    main()
