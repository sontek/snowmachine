#!/usr/bin/env python
from colorama import init, Fore, Style
import os
import sys
import random
import time
import platform
import click
import shutil
import signal

# initialize colorama
init()

color_options = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "cyan",
    "white",
    "rainbow",
]

bad_colors = ["RESET"]
codes = vars(Fore)
colors = []
for code in codes:
    if not code.endswith("_EX") and code not in bad_colors:
        colors.append(code.lower())


@click.command()
@click.option("--speed", default=14, help="Increase to make it snow faster.")
@click.option(
    "--stack",
    default=None,
    help="Make the snow stack. Options",
    type=click.Choice(["pile"]),
)
@click.option(
    "--particle",
    default=None,
    help="Change the partice used. Could be used to make it rain.",
)
@click.option(
    "--color",
    default=None,
    help="Change the color of the particle.",
    type=click.Choice(colors + ["rainbow"]),
)
def command(speed, stack, particle, color):
    main(speed, stack, particle, color)


snowflakes = {}


def get_terminal_size():
    return shutil.get_terminal_size((80, 20))


columns, rows = get_terminal_size()


def clear_screen(numlines=100):
    """Clear the console.

    numlines is an optional argument used only as a fall-back.
    """
    print(Style.RESET_ALL)

    if os.name == "posix":
        # Unix/Linux/MacOS/BSD/etc
        os.system("clear")
    elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
        os.system("cls")
    else:
        # Fallback for other operating systems.
        print("\n" * rows)


def get_random_flake():
    start = 10048
    end = 10056
    options = list(range(start, end))

    if platform.system() == "Windows":
        # Windows prints a green background on 10055
        # for some reason. It also makes 52 blue?
        options.remove(10052)
        options.remove(10055)
    try:
        # python3 support
        try:
            cmd = unichr
        except NameError:
            cmd = chr

        flake = cmd(random.choice(options))

        return flake
    except:
        pass

    return " *"


current_rows = {}


def print_col(col, color):
    output = "\033[%s;%sH%s" % (snowflakes[col][0], col, snowflakes[col][1])
    # We don't want to use black and white in our rainbow
    bad_colors = ["black", "white"]
    if color:
        if color == "rainbow":
            color_options = [color for color in colors if color not in bad_colors]
            output = getattr(Fore, random.choice(color_options).upper()) + output
        else:
            output = getattr(Fore, color.upper())

    print(output)

    # reset the cursor
    print("\033[1;1H")


def move_flake(col, stack, particle, color):
    # Rows is the max amount of rows on the screen,
    # so settings the column to the rows count means
    # putting it at the bottom of the screen

    if stack == "pile":
        if col not in current_rows:
            current_rows[col] = rows

        current_row = current_rows[col]

        # The current column has reached the top of
        # the screen, lets reset it so it drops the
        # pile back
        if current_row == 1:
            current_row = rows
            current_rows[col] = current_row

        # If next row is the end, lets just move the rows up by one
        if snowflakes[col][0] + 1 == current_row:
            current_rows[col] -= 1
    else:
        current_row = rows

    # If next row is the end, lets start a new snow flake
    if snowflakes[col][0] + 1 == current_row:
        char = particle
        if not particle:
            char = get_random_flake()
        snowflakes[col] = [1, char]
        print_col(col, color)
    else:
        # erase the flake in current location
        print("\033[%s;%sH  " % (snowflakes[col][0], col))
        # move down by one
        snowflakes[col][0] += 1
        print_col(col, color)


def random_printer(speed, particle, stack, color):
    clear_screen()

    while True:
        col = random.choice(range(1, int(columns)))

        # Don't print snowflakes right next to each other, since
        # unicode flakes take 2 spaces
        if col % 2 == 0:
            continue

        # its already on the screen, move it
        if col in snowflakes.keys():
            move_flake(col, stack, particle, color)
        else:
            # otherwise put it on the screen
            flake = particle if particle else get_random_flake()
            snowflakes[col] = [1, flake]
            print_col(col, color)

        # key any flakes on the screen moving
        for flake in snowflakes.keys():
            move_flake(flake, stack, particle, color)

        final_speed = 1.0 / speed

        try:
            time.sleep(final_speed)
        except KeyboardInterrupt:
            clear_screen()
            sys.exit(0)


def main(speed=14, stack=None, particle=None, color=None):
    # Print all the flakes
    # for flake in range(0x2740, 0x2749):
    #   print(f"{flake}: {chr(flake)}")
    random_printer(speed, particle, stack, color)


def signal_handler(sig, frame):
    clear_screen()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    command()
