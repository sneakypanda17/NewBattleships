import random
import json
import os

def initialise_board(size=10):
    # Initializes and returns a game board as a list of lists filled with 'None', representing an empty board.
    return [[None for _ in range(size)] for _ in range(size)]

def create_battleships(filename='battleships.txt'):
    # Reads battleship data from a file and returns a dictionary with ship names as keys and their sizes as values.
    battleships = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 2 and parts[1].isdigit():
                    battleships[parts[0]] = int(parts[1])
                else:
                    print(f"Invalid format in line: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return battleships

def place_battleships(board, ships, algorithm='simple'):
    # Places ships on the board using the specified algorithm.
    if algorithm == 'simple':
        return place_battleships_simple(board, ships)
    elif algorithm == 'random':
        return place_battleships_random(board, ships)
    elif algorithm == 'custom':
        return place_battleships_custom(board, ships)
    else:
        print(f"Algorithm '{algorithm}' is not implemented yet.")
        return board

def place_battleships_simple(board, ships):
    # Places ships on the board starting from the top, each ship in a new row.
    row = 0
    for ship, size in ships.items():
        if row + size > len(board):
            print(f"Not enough space to place {ship}")
            break
        for col in range(size):
            board[row][col] = ship
        row += 1
    return board

def place_battleships_random(board, ships):
    # Places ships randomly on the board.
    for ship, size in ships.items():
        placed = False
        while not placed:
            row = random.randint(0, len(board) - 1)
            col = random.randint(0, len(board[0]) - 1)
            horizontal = random.choice([True, False])

            if can_place_ship(board, row, col, size, horizontal):
                place_ship(board, ship, row, col, size, horizontal)
                placed = True
    return board

def place_battleships_custom(board, ships):
    # Places ships on the board based on custom placement data from placement.json file.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "placement.json")
    with open(file_path, "r", encoding="utf-8") as placement:
        ship_data = json.load(placement)
    for ship, key in ship_data.items():
        col = int(key[1])
        row = int(key[0])
        direction = key[2]
        length = ships.get(ship)
        if direction == "v":
            for i in range(length):
                board[col + i][row] = ship
        if direction == "h":
            for i in range(length):
                board[col][row + i] = ship
    return board

def can_place_ship(board, row, col, size, horizontal):
    # Checks if a ship can be placed at the specified position.
    if horizontal:
        return all(0 <= col + i < len(board[0]) and board[row][col + i] is None for i in range(size))
    else:
        return all(0 <= row + i < len(board) and board[row + i][col] is None for i in range(size))

def place_ship(board, ship, row, col, size, horizontal):
    # Places a ship on the board at the specified position.
    if horizontal:
        for i in range(size):
            board[row][col + i] = ship
    else:
        for i in range(size):
            board[row + i][col] = ship

def print_board(board):
    # Prints the board to the console for visualization.
    print("  " + " ".join(str(i) for i in range(len(board[0]))))
    for i, row in enumerate(board):
        print(str(i) + " " + " ".join('.' if cell is None else cell for cell in row))

def check_game_over(player, players):
    # Checks if all ships of a player have been sunk.
    return all(size == 0 for size in players[player]["battleships"].values())
