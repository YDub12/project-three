import random

BOARD_SIZE = 5
SHIP_SIZES = [3, 2, 1, 1]  # List of ship sizes

# Symbols
EMPTY_SYMBOL = 'O'
SHIP_SYMBOL = 'S'
HIT_SYMBOL = 'H'
MISS_SYMBOL = 'M'

# Create an empty board
def create_board():
    return [[EMPTY_SYMBOL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Welcome message
def welcome_message(username):
    print(f"Welcome, {username}, to Battleships!\n")
    print(f"You will be playing on a {BOARD_SIZE}x{BOARD_SIZE} grid.\n")
    print("Your goal is to sink all of your opponent's ships.\n")
    print("You will do this by making guesses below.\n")

# Check if a ship can be placed at the specified location
def is_valid_placement(board, row, col, size, orientation):
    if orientation == 'H':
        if col + size > BOARD_SIZE:
            return False
        for i in range(size):
            if board[row][col + i] != EMPTY_SYMBOL:
                return False
    else:  # orientation == 'V'
        if row + size > BOARD_SIZE:
            return False
        for i in range(size):
            if board[row + i][col] != EMPTY_SYMBOL:
                return False
    return True

# Place a single ship on the board
def place_ship(board, row, col, size, orientation):
    for i in range(size):
        if orientation == 'H':
            board[row][col + i] = SHIP_SYMBOL
        else:
            board[row + i][col] = SHIP_SYMBOL

# Let the player manually place ships
def player_place_ships(board):
    print("\nPlace your ships on the board.")
    for size in SHIP_SIZES:
        while True:
            try:
                print_board(board, show_ships=True)
                print(f"\nPlace your ship of size {size}.")
                row = int(input(f"Enter the starting row (0-{BOARD_SIZE-1}): "))
                col = int(input(f"Enter the starting column (0-{BOARD_SIZE-1}): "))
                orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()

                if orientation not in ['H', 'V']:
                    print("Invalid orientation. Please choose H or V.")
                    continue

                if is_valid_placement(board, row, col, size, orientation):
                    place_ship(board, row, col, size, orientation)
                    break
                else:
                    print("Invalid placement. The ship cannot go off the board or overlap with other ships.")
            except ValueError:
                print("Invalid input. Please enter valid numbers for row and column.")

# Randomly place ships on the board (for computer)
def add_computer_ships(board):
    for size in SHIP_SIZES:
        while True:
            orientation = random.choice(['H', 'V'])
            if orientation == 'H':
                row = random.randint(0, BOARD_SIZE - 1)
                col = random.randint(0, BOARD_SIZE - size)
            else:  # 'V'
                row = random.randint(0, BOARD_SIZE - size)
                col = random.randint(0, BOARD_SIZE - 1)

            if is_valid_placement(board, row, col, size, orientation):
                place_ship(board, row, col, size, orientation)
                break

# Display the board (hide ships unless show_ships is True)
def print_board(board, show_ships=False):
    print("  " + " ".join([str(i) for i in range(BOARD_SIZE)]))  # Column numbers
    for idx, row in enumerate(board):
        display_row = []
        for cell in row:
            if cell == SHIP_SYMBOL and not show_ships:
                display_row.append(EMPTY_SYMBOL)
            else:
                display_row.append(cell)
        print(f"{idx} " + " ".join(display_row))  # Row number

# Get player's guess
def get_player_guess(guesses):
    while True:
        try:
            guess = input("Enter your guess (row and column separated by space): ")
            row, col = map(int, guess.strip().split())
            if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
                print(f"Please enter numbers between 0 and {BOARD_SIZE - 1}.")
                continue
            if (row, col) in guesses:
                print("You have already guessed that location. Try again.")
                continue
            return row, col
        except ValueError:
            print("Invalid input format. Please enter two numbers separated by space.")

# Check if a guess is a hit or miss
def check_guess(board, row, col):
    if board[row][col] == SHIP_SYMBOL:
        board[row][col] = HIT_SYMBOL
        print("Hit!")
        return True
    else:
        board[row][col] = MISS_SYMBOL
        print("Miss!")
        return False

# Check if all ships are sunk
def all_ships_sunk(board):
    return all(SHIP_SYMBOL not in row for row in board)

# Computer guess
def computer_guess(player_board, guesses):
    while True:
        row, col = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
        if (row, col) not in guesses:
            guesses.add((row, col))
            print(f"Computer's guess: {row} {col}")
            return row, col

# Main game loop for playing against the computer
def play_against_computer(player_board, computer_board):
    player_guesses = set()
    computer_guesses = set()
    attempts = 0

    while not all_ships_sunk(computer_board):
        # Player's turn
        print("\nCurrent Board:")
        print_board(computer_board)
        row, col = get_player_guess(player_guesses)
        player_guesses.add((row, col))
        check_guess(computer_board, row, col)
        attempts += 1

        if all_ships_sunk(computer_board):
            break

        # Computer's turn
        print("\nComputer is guessing...")
        computer_row, computer_col = computer_guess(player_board, computer_guesses)
        check_guess(player_board, computer_row, computer_col)
        
        # Show the player's board after the computer's guess
        print("\nYour Board (after computer's guess):")
        print_board(player_board, show_ships=True)

    print("\nCongratulations! You sunk all the ships!")
    print(f"It took you {attempts} attempts.")
    print("\nFinal Board:")
    print_board(computer_board, show_ships=True)

# Main function
def main():
    # Get username
    username = input("Enter your username: ")

    # Show welcome message
    welcome_message(username)

    # Create boards for player and computer
    player_board = create_board()
    computer_board = create_board()

    # Player places ships
    print(f"\n{username}, it's time to place your ships.")
    player_place_ships(player_board)

    # Computer places ships
    print("Computer is placing its ships...")
    add_computer_ships(computer_board)

    # Ask if player wants to play against the computer
    play_against_ai = input("Do you want to play against the computer? (yes/no): ").lower() == "yes"

    if play_against_ai:
        play_against_computer(player_board, computer_board)
    else:
        print("\nFinal Board with Ships (debug mode):")
        print_board(computer_board, show_ships=True)

if __name__ == "__main__":
    main()