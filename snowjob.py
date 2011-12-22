#!/usr/bin/env python
import os
import random
import time

snowflakes = {}

def get_terminal_size():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
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

def get_random_flake():
    flake=unichr(random.choice(range(0x2740, 0x2749)))
    return flake


def move_flake(col):
    if snowflakes[col][0]+1 == rows:
        snowflakes[col] = [1, get_random_flake()]
    else:
        print "\033[%s;%sH " % (snowflakes[col][0], col)

        snowflakes[col][0] += 1
        print u"\033[%s;%sH%s" % (snowflakes[col][0], col,
                snowflakes[col][1])
        print "\033[1;1H"

if __name__ == "__main__":
    os.system('clear')

    while True:
        col = random.choice(range(1, int(columns)))

        # its already on the screen, move it
        if col in snowflakes.keys():
            move_flake(col)
        else:
        # otherwise put it on the screen
            flake = get_random_flake()
            snowflakes[col] = [1, flake]

            print "\033[%s;%sH%s" % (snowflakes[col][0], col,
                    snowflakes[col][1])

        # key any flakes on the screen moving
        for flake in snowflakes.keys():
            move_flake(flake)

        time.sleep(0.1)
