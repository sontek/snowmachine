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

    particle = particle or get_random_flake()

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
                move_flake(snowflakes, current_rows, col, None, particle, snow_color)
            else:
                # otherwise put it on the screen
                flake = snow_particle if snow_particle else get_random_flake()
                snowflakes[col] = [1, flake]
                print_snowflake_col(snowflakes, col, snow_color)

            # key any flakes on the screen moving
            for flake in snowflakes.keys():
                move_flake(snowflakes, current_rows, flake, None, particle, snow_color)
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

@cli.command()
@click.option("--speed", default=14, help="Increase to make it snow faster.")
@click.option(
    "--plowchar",
    default="truck",
    help="Choose your plow character",
    type=click.Choice(["truck","person"]),
)
@click.option(
    "--min_snowtimer",
    default=120,
    help="Minimum time to snow before starting to plow. Defaults to 120 cylces",
)
@click.option(
    "--max_snowtimer",
    default=200,
    help="maximum time to snow before starting to plow. Defaults to 200 cycles",
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
def snowplow(speed, plowchar, min_snowtimer, max_snowtimer, particle, color):
    clear_screen()
    # This ends up formatted as column being the key and then [0] is row and
    # [1] is the particle. For example:
    # {"1": [0, "*"]}
    snowflakes = {}
    current_rows = {}
    snowTimer = random.randrange(min_snowtimer,max_snowtimer)
    curSnowTimer = 0
    waitForLastFlakeTime = rows
    curWaitForLastFlakeTimer = 0
    isSnowing = True
    isPlowing = False
    hasLastFlakeFallen = False
    curSnowPlowColumn = columns
    maxPlowCharWidth = 0
    isMovingLeft = True
    
    # The spaces are used to blank out characters so make sure to pad the images.
    asciiTruckLeft = {
    7:"             /================ ",
    6:"      ___   //  @||----------| ",
    5:"    _|___|_//_\_|||_____|____| ",
    4:"   |  ____ |     ||    /___  |> ",
    3:"   | |    \|_____||___|    \ |> ",
    2:"]_/|_|  O  \__________|  O  \|| ",  
    1:"]     \___/~~          \___/~~ "  

    }
    
    asciiTruckRight = {
    7:" ================\\             ",
    6:"  |----------||@  \\\   ___     ",
    5:"  |____|_____|||_/_\\\_|___|_   ",
    4:" <|  ___\    ||     | ____  |   ",
    3:" <| /    |___||_____|/    | |   ",
    2:" ||/  O  |__________/  O  |_|\_[",
    1:"    \___/            \___/     ["
    }

    asciiPersonLeft = {
    3:"   @  ",
    2:"  /|\ ",
    1:"]//^\ "
    }

    # Sometimes escape trickery is needed like with the backslash.
    asciiPersonRight = {
    3:"  @   ",
    2:" /|\  ",
    1:" /^\\\["   
    }
    
    # If the plowchar is truck, then we need to flip the left and right
    if (plowchar == "truck" and isMovingLeft):
        plowchar = asciiTruckLeft
    elif (plowchar == "truck"):
        plowchar = asciiTruckRight
    # If the plowchar is person, then we need to flip the left and right
    if (plowchar == "person" and isMovingLeft):
        plowchar = asciiPersonLeft
    elif (plowchar == "person"):
        plowchar = asciiPersonRight
    # Get the longest string in the ascii array, used to calculate screen buffer spice on the sides so they can move offscreen.
    maxPlowCharWidth = max(len(value) for value in plowchar.values())



    while True:
        col = random.choice(range(1, int(columns)))

        # Don't print snowflakes right next to each other, since
        # unicode flakes take 2 spaces
        if col % 2 == 0:
            continue

        # its already on the screen, move it
        if col in snowflakes.keys() and hasLastFlakeFallen == False:
            move_plow_flake(snowflakes, col, particle, color, isSnowing)
        else:
            # we only want to move snowflakes if it's snowing.
            if (isSnowing):
                # otherwise put it on the screen
                flake = particle if particle else get_random_flake()
                snowflakes[col] = [1, flake]
                print_snowflake_col(snowflakes, col, color)

        # key any flakes on the screen moving
        for flake in snowflakes.keys():
            if (hasLastFlakeFallen == False):
                move_plow_flake(snowflakes, flake, particle, color, isSnowing)
        # if it's snowing do the regular speed
        if (isSnowing):
            final_speed = 1.0 / speed
            curSnowTimer += 1
        else:
            # It's plow time!
            if (isPlowing):
                maxPlowCharWidth = max(len(value) for value in plowchar.values())
                # Speed up time for plowing * 2
                final_speed = 0.5 / speed
                
                # If there is a snowflake in our current column, erase the flake delete it from snowflakes.
                if curSnowPlowColumn in snowflakes.keys():
                    print("\033[%s;%sH  " % (snowflakes[curSnowPlowColumn][0], curSnowPlowColumn))
                    snowflakes.pop(curSnowPlowColumn)
                
                if (isMovingLeft):
                    # Lets the plow drive off the screen to the left.
                    if curSnowPlowColumn + maxPlowCharWidth >= 0:
                        # This is magic, let's iterate through each row and print out each character of the ascii truck.
                        for key, value in plowchar.items():
                            for index, character in enumerate(value):
                                print_character(rows-key,curSnowPlowColumn + index,character,color)
                        # decrease the plow column
                        curSnowPlowColumn -= 1
                            
                    else:
                        # If we aren't plowing anymore let's clear the screen and reset variables.
                        clear_screen()
                        isPlowing = False
                        isSnowing = True
                        hasLastFlakeFallen = False
                        isMovingLeft = False
                        if (plowchar == asciiTruckLeft):
                            plowchar = asciiTruckRight
                        if (plowchar == asciiPersonLeft):
                            plowchar = asciiPersonRight     
                  
                elif (not isMovingLeft):
                    # Lets the plow drive off the screen to the right.
                    if curSnowPlowColumn <= columns + maxPlowCharWidth:
                        # This is magic, let's iterate through each row and print out each character of the ascii truck.
                        for key, value in plowchar.items():
                            for index, character in enumerate(reversed(value)):
                                print_character(rows-key,curSnowPlowColumn - index,character,color)
                        # increase the plow column since we're going right
                        curSnowPlowColumn += 1
                    else:
                        # If we aren't plowing anymore let's clear the screen and reset variables.
                        clear_screen()
                        isPlowing = False
                        isSnowing = True
                        hasLastFlakeFallen = False
                        isMovingLeft = True
                        if (plowchar == asciiTruckRight):
                            plowchar = asciiTruckLeft
                        if (plowchar == asciiPersonRight):
                            plowchar = asciiPersonLeft
  
                    
            else:
                # We want to wait until all of the snowflakes have fallen before we start plowing.
                if (hasLastFlakeFallen):
                    # We are ready to plow, last snowflake has fallen
                    isPlowing = True
                    # right before we plow lets set the plow position based on moving direction.
                    if (isMovingLeft):
                        curSnowPlowColumn = columns
                    elif (not isMovingLeft):
                        curSnowPlowColumn = 0
        
                    curWaitForLastFlakeTimer = 0
                else:
                    if (curWaitForLastFlakeTimer >= waitForLastFlakeTime):
                        hasLastFlakeFallen = True
                    else:
                        curWaitForLastFlakeTimer += 1
        #Time for now until the timer reaches the snowTimer.
        if (curSnowTimer >= snowTimer):
            # Time to stop snowing
            isSnowing = False
            curSnowTimer = 0
            snowTimer = random.randrange(min_snowtimer,max_snowtimer)

        try:
            time.sleep(final_speed)
        except KeyboardInterrupt:
            clear_screen()
            sys.exit(0)

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

def move_plow_flake(snowflakes, col, particle, color, isSnowing):
    # Rows is the max amount of rows on the screen,
    # so settings the column to the rows count means
    # putting it at the bottom of the screen

    current_row = rows

    # If next row is the end, lets start a new snow flake, but only if it's snowing.
    if isSnowing:
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
    # If it's not snowing and the snowflake isn't touching the ground let's move it down.
    else:
        if snowflakes[col][0] +1 != current_row:
            # erase the flake in current location
            print("\033[%s;%sH  " % (snowflakes[col][0], col))
            # move down by one
            snowflakes[col][0] += 1
            print_snowflake_col(snowflakes, col, color)

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