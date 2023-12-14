'''Modules'''
from typing import Tuple, List, Dict, Union
import pyttsx3
from components import initialise_board, create_battleships, place_battleships


previous_hits = set()
engine = pyttsx3.init()  

def speak(audio: str) -> None:
    """Making the game more interactive.

    Args:
        audio (str): To read and speak the lines.
    """
    engine.say(audio)
    engine.runAndWait()

def attack(coordinates: Tuple[int, int], board: List[List[Union[None, str]]], battleships: Dict[str, int]) -> bool:
    """Checks whether the target misses or hits or a battleship is sunk.

    Args:
        coordinates (Tuple[int, int]): The coordinates it receives.
        board (List[List[Union[None, str]]]): The 10x10 board.
        battleships (Dict[str, int]): The ship's info.

    Returns:
        bool: True or False to indicate hit or miss.
    """
    x, y = coordinates
    target = board[y][x] #Was originally board[x][y] but modified after logic error...

    if target is not None:
        print("Hit!")
        battleships[target] -= 1

        if battleships[target] == 0:
            print(f"You sunk the {target}!")
            #del battleships[target]

        board[y][x] = None  # Change the symbol when a ship is hit
        return True

    print("Miss!")
    return False

def cli_coordinates_input() -> Tuple[int, int]:
    """Asks user for x and y coordinates.

    Returns:
        Tuple[int, int]: The coordinates of where it wants to hit.
    """
    while True:
        try:
            x = int(input("Enter the X coordinate: "))
            y = int(input("Enter the Y coordinate: "))

            # Check if the coordinates have been targeted before
            if (x, y) in previous_hits:
                print("You have already targeted this spot. Choose different coordinates.")
                speak("You have hit this target before. You are better than this.")
                continue

            if (x > 9 or x < 0) or (y > 9 or y < 0):
                print("Sorry, we only use numbers from 0 to 9")
                x = int(input("Enter the X coordinate: "))
                y = int(input("Enter the Y coordinate: "))
                continue

            previous_hits.add((x, y))
            return x, y
        except ValueError:
            print("Invalid input. Please enter numeric values for coordinates.")

def print_board_hits(board: List[List[Union[None, str]]]) -> None:
    """Prints the board. If a coordinate of a board is hit, an X is returned to the board.
    Returns None from attack for main.py to work instead of 'X'.

    Args:
        board (List[List[Union[None, str]]]): The 10x10 grid.
    """
    for row in board:
        print(" ".join('X' if cell == 'X' else '.' if cell is None else cell for cell in row))

def simple_game_loop() -> None:
    """Starts the game.
    """
    print("Welcome to the Battleship Game!")

    #Initialize the board, create and place battleships
    board_size = 10
    game_board = initialise_board(size=board_size)
    ships = create_battleships()
    place_battleships(game_board, ships, algorithm='custom')

    #Game loop
    while any(size > 0 for size in ships.values()):
        print_board_hits(game_board)
        coordinates = cli_coordinates_input()
        previous_hits.add(coordinates)
        result = attack(coordinates, game_board, ships)
        print(result)

    print("Game Over - All battleships have been sunk!")

if __name__ == "__main__":
    simple_game_loop()