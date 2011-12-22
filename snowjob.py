#!/usr/bin/env python
import os
import random
import time

snowflakes = {}
rows, columns = map(int, os.popen('stty size', 'r').read().split())
def move_flake(col):
    if snowflakes[col]+1 == rows:
        snowflakes[col] = 1
    else:
        print "\033[%s;%sH " % (snowflakes[col], col)

        snowflakes[col] += 1

        print "\033[%s;%sH*" % (snowflakes[col], col)
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
            snowflakes[col] = 1
            print "\033[%s;%sH*" % (snowflakes[col], col)

        # keep any flakes on the screen moving
        for flake in snowflakes.keys():
            move_flake(flake)

        time.sleep(0.1)
