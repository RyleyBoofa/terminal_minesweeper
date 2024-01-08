"""
    Minesweeper: practice project
"""

from random import randint

# ============================== GRID ICONS =================================================================
BOMB = "B"
HASH = "#"
CLEAR = "O"

# ============================ PROMPTS/MESSAGES =============================================================
grid_size_prompt = "Please input a difficulty number.\n\nEasy: 2-6\nMedium: 7-14\nHard: 15-20\n\nWhat size grid do you want? "
grid_size_error_msg = "\nInvalid grid size. "
row_check_prompt = "\nWhat row do you want to check? "
row_check_error_msg = "\nInvalid row. "
col_check_prompt = "\nWhat column do you want to check? "
col_check_error_msg = "\nInvalid column. "
press_to_continue = "Press 'enter' to reveal the grid.\n"


# ============================ WELCOME MESSAGE ==============================================================
def welcome():
    """Print welcome message"""

    print("\nWelcome to Minesweeper!\n")
    print(
        "A hash '#' represents an unchecked location.\nYou will input unchecked locations to check if they're clear or not.\n"
    )
    print(
        "A circle 'O' represents a cleared location.\nGood work, now on to the next.\n"
    )
    print("A bomb is represented by a 'B'.\nIf you hit one of these, it's game over.\n")


# ============================ GRID FUNCTIONS ===============================================================
def get_grid_size():
    """Prompt the user for an int between 2-20 to represent the size of the grid"""

    grid_size = get_int_in_range(grid_size_prompt, grid_size_error_msg, 2, 20)
    return grid_size


def generate_grid(grid_size):
    """Generate a grid of #'s of specified size"""

    print(f"\nGenerating grid of size {grid_size}...\n")
    return [[HASH * grid_size] * grid_size]


def print_grid(grid):
    """Draw the grid to the terminal window."""

    for row in grid:
        for col in row:
            print(col)


def replace_grid_location(grid, row, col, new_symbol):
    """Replace the specified grid location's existing symbol with the given symbol"""

    row_content = grid[0][row - 1]
    new_row = ""

    for i, char in enumerate(row_content):
        if i == col - 1:
            new_row += new_symbol
        else:
            new_row += char

    grid[0][row - 1] = new_row


def reveal_grid(grid, bombs):
    """Replace all final unchecked locations with either a B or an O"""

    for i, row in enumerate(grid[0]):
        new_row = ""

        for j, col in enumerate(row):
            if col == BOMB:
                new_row += BOMB

            elif col == CLEAR:
                new_row += CLEAR

            elif col == HASH:
                check = (i, j)
                bomb_here = False

                for bomb in bombs:
                    if bomb == check:
                        new_row += BOMB
                        bomb_here = True

                if bomb_here == False:
                    new_row += CLEAR

        grid[0][i] = new_row

    print_grid(grid)


# ============================ BOMB FUNCTIONS ===============================================================
def plant_bombs(grid_size):
    """Select random grid locations to place bombs"""

    bomb_locations = []
    for i in range(grid_size - 1):
        x = randint(1, grid_size)
        y = randint(1, grid_size)
        for j in range(len(bomb_locations)):
            if bomb_locations[j] == (x, y):
                i -= 1
        bomb_locations.append((x, y))

    print(f"There are {len(bomb_locations)} bombs! Good luck...\n")
    return bomb_locations


def check_for_bomb_at_location(bombs, check_row, check_col):
    """Check the specified location for a bomb and return True if one is there"""

    print(f"\nChecking row {check_row}, column {check_col}...\n")

    # Check list of bombs to see if a bomb is at this location
    for i in range(len(bombs)):
        if check_row == bombs[i][0]:
            if check_col == bombs[i][1]:
                return True
    return False


# ============================ GAME FUNCTIONS ===============================================================
def play_game(grid, grid_size, bombs):
    """Play the game. Repeatedly prompt the player for grid locations until none remain or a bomb is hit."""

    # Begin the game loop
    playing = True
    while playing:
        print_grid(grid)

        if game_won(grid, bombs):
            print("\nYou won!\n\nAll remaining spaces contain bombs!\n")
            input(press_to_continue)
            reveal_grid(grid, bombs)
            print("\nThanks for playing!\n")
            playing = False
            break

        # Prompt the user for a row and column to check
        check_row = get_int_in_range(
            row_check_prompt, row_check_error_msg, 1, grid_size
        )
        check_col = get_int_in_range(
            col_check_prompt, col_check_error_msg, 1, grid_size
        )

        # End the game if a bomb is found at chosen location
        if check_for_bomb_at_location(bombs, check_row, check_col):
            playing = False
            game_over(grid, check_row, check_col, bombs)
        else:
            replace_grid_location(grid, check_row, check_col, CLEAR)


def game_won(grid, bombs):
    """Check if number of remaining hashes equals the number of bombs. If so, return True"""

    hashes_remaining = 0
    for row in grid[0]:
        for i, col in enumerate(row):
            if col == HASH:
                hashes_remaining += 1

    if hashes_remaining <= len(bombs):
        return True
    else:
        return False


def game_over(grid, row, col, bombs):
    """Display where the bomb was and print game-over message"""

    replace_grid_location(grid, row, col, BOMB)
    print_grid(grid)
    print("\nKABOOM!!!\n\nYou found a bomb!\n")

    input(press_to_continue)

    reveal_grid(grid, bombs)

    print("\nGame over!\n")


def main():
    """Run the game"""

    welcome()

    grid_size = get_grid_size()
    grid = generate_grid(grid_size)

    bombs = plant_bombs(grid_size)

    play_game(grid, grid_size, bombs)


# ============================ UTIL FUNCTIONS ===============================================================
def get_int_in_range(prompt: str, error_msg: str, min: int, max: int):
    """
    Get an int from the user between a min and max range (inclusive)
    :param prompt: String to prompt the user with
    :param error_msg: String to display if user doesn't comply
    :param min: Int representing the minimum acceptable value
    :param max: Int representing the maximum acceptable value
    :return:
    """

    # Repeatedly prompt the user until they provide an int
    i = None
    while True:
        try:
            i = int(input(prompt))
            break
        except ValueError:
            print(error_msg, end="")
            print(f"Please input a number between {min} and {max}.\n")

    # Ensure provided int is within valid range
    while not min - 1 < i < max + 1:
        print(error_msg, end="")
        print(f"Please input a number between {min} and {max}.\n")
        try:
            i = int(input(prompt))
        except ValueError:
            pass

    return i


main()
