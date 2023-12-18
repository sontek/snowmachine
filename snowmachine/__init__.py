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
    #    "rainbow",
]

bad_colors = ["RESET"]
codes = vars(Fore)
colors = []
for code in codes:
    if not code.endswith("_EX") and code not in bad_colors:
        colors.append(code.lower())


def get_terminal_size():
    return shutil.get_terminal_size((80, 20))


columns, rows = get_terminal_size()


def get_random_color():
    # We don't want to use black and white in our rainbow
    bad_colors = ["black", "white"]
    color_options = [color for color in colors if color not in bad_colors]
    return random.choice(color_options)


@click.group()
def cli():
    pass


@cli.command()
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
    help="Change the particle used.",
)
@click.option(
    "--color",
    default=None,
    help="Change the color of the particle.",
    type=click.Choice(colors + ["rainbow"]),
)
def snow(speed, stack, particle, color):
    clear_screen()
    # This ends up formatted as column being the key and then [0] is row and
    # [1] is the particle. For example:
    # {"1": [0, "*"]}
    snowflakes = {}
    current_rows = {}

    while True:
        col = random.choice(range(1, int(columns)))

        # Don't print snowflakes right next to each other, since
        # unicode flakes take 2 spaces
        if col % 2 == 0:
            continue

        # its already on the screen, move it
        if col in snowflakes.keys():
            move_flake(snowflakes, current_rows, col, stack, particle, color)
        else:
            # otherwise put it on the screen
            flake = particle if particle else get_random_flake()
            snowflakes[col] = [1, flake]
            print_snowflake_col(snowflakes, col, color)

        # key any flakes on the screen moving
        for flake in snowflakes.keys():
            move_flake(snowflakes, current_rows, flake, stack, particle, color)

        final_speed = 1.0 / speed

        try:
            time.sleep(final_speed)
        except KeyboardInterrupt:
            clear_screen()
            sys.exit(0)


@cli.command()
@click.option("--light-delay", default=1, help="Seconds between light changes")
@click.option(
    "--color",
    default="green",
    help="Change the color of the tree",
    type=click.Choice(colors + ["rainbow"]),
)
@click.option(
    "--lights-color",
    default=None,
    help="Change the color of the lights",
    type=click.Choice(colors + ["rainbow"]),
)
@click.option(
    "--snow-color",
    default=None,
    help="Change the color of the snow.",
    type=click.Choice(colors + ["rainbow"]),
)
@click.option(
    "--particle",
    default="*",
    help="Change the partice used for the leaves.",
)
@click.option("--snow", default=True, help="Render snow")
@click.option("--snow-particle", default=None, help="The particle for snow")
@click.option("--snow-speed", default=20, help="Speed that the snow will fall")
def tree(light_delay, color, lights_color, snow_color, particle, snow, snow_particle, snow_speed):
    clear_screen()
    # (row, col, particle)
    treeparts = []
    trunkparts = []

    particle = particle or '*'

    trunk_size = 3
    tree_rows = rows - trunk_size
    # Draw the tree
    j = 1
    for i in range(int(tree_rows / 2), tree_rows):
        for k in range(j):
            center = int((columns / 2) - (j / 2)) + k
            treeparts.append((i, center, particle, color))
        # Keep the particles even so they balance properly
        j += 2

    trunk_width = 9
    for i in range(tree_rows, tree_rows + trunk_size):
        for k in range(trunk_width):
            center = int((columns / 2) - (trunk_width / 2)) + k
            trunkparts.append((i, center, "m"))

    snowflakes = {}
    current_rows = {}

    start = time.time()

    new_tree = treeparts.copy()
    while True:
        if snow:
            ##### SNOW ######
            col = random.choice(range(1, int(columns)))

            # Don't print snowflakes right next to each other, since
            # unicode flakes take 2 spaces
            if col % 2 == 0:
                continue

            # its already on the screen, move it
            if col in snowflakes.keys():
                move_flake(snowflakes, current_rows, col, None, snow_particle, snow_color)
            else:
                # otherwise put it on the screen
                flake = snow_particle if snow_particle else get_random_flake()
                snowflakes[col] = [1, flake]
                print_snowflake_col(snowflakes, col, snow_color)

            # key any flakes on the screen moving
            for flake in snowflakes.keys():
                move_flake(snowflakes, current_rows, flake, None, snow_particle, snow_color)
            ##### SNOW ######

        end = time.time()
        duration = end - start

        if duration > light_delay:
            new_tree = treeparts.copy()
            for part_index, part in enumerate(new_tree):
                final_particle = part[2]
                final_color = color
                # 10% chance we'll be a chrismas light instead of
                # a tree particle.
                if random.random() < 0.10 and part[0]:
                    final_particle = "o"
                    final_color = lights_color if lights_color else get_random_color()

                    new_tree[part_index] = (
                        part[0],
                        part[1],
                        final_particle,
                        final_color,
                    )
            start = time.time()

        for part in new_tree:
            print_character(
                part[0],
                part[1],
                part[2],
                part[3],
            )

        for part in trunkparts:
            print_character(
                part[0],
                part[1],
                part[2],
                "yellow",
            )

        final_speed = 1.0 / snow_speed
        time.sleep(final_speed)


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


def print_character(row, column, character, color):
    output = "\033[%s;%sH%s" % (row, column, character)

    if color:
        if color == "rainbow":
            color_options = [color for color in colors if color not in bad_colors]
            output = getattr(Fore, get_random_color().upper()) + output
        else:
            output = getattr(Fore, color.upper()) + output

    print(output)

    # reset the cursor
    print("\033[1;1H")

    # reset the color
    print("\033[0m")


def print_snowflake_col(snowflakes, col, color):
    print_character(snowflakes[col][0], col, snowflakes[col][1], color)


def move_flake(snowflakes, current_rows, col, stack, particle, color):
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
        print_snowflake_col(snowflakes, col, color)
    else:
        # erase the flake in current location
        print("\033[%s;%sH  " % (snowflakes[col][0], col))
        # move down by one
        snowflakes[col][0] += 1
        print_snowflake_col(snowflakes, col, color)


def signal_handler(sig, frame):
    clear_screen()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    cli()
