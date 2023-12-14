'''Modules'''
import random
import json
from typing import List, Dict, Union, Any, Literal

#Initialise board
def initialise_board(size: int = 10) -> List[List[Union[None, Any]]]:
    """Returns a 10 x 10 grid with the word None.

    Args:
        size (int, optional): size of board defaults to 10.

    Returns:
        List[List[Union[None, Any]]]: a list with 10 lists with the word None
    """
    return [[None] * size for _ in range(size)]

#create battleships
def create_battleships(filename: str = "battleships.txt") -> Dict[str, int]:
    """Opens battleship.txt file.

    Args:
        filename (str, optional): filename defaults to "battleships.txt".

    Returns:
        Dict[str, int]: dictionary of the info of the battleship.
    """
    with open(filename, 'r', encoding="utf-8") as file:
        battleships_data = file.readlines()

    battleships = {}
    for line in battleships_data:
        name, size = line.strip().split(':')
        battleships[name] = int(size)

    return battleships

def placement_from_file(filename: str = "placement.json") -> Dict[str, List[int]]:
    """Parses the JSON file

    Args:
        filename (str, optional): filename defaults to "placement.json".

    Returns:
        Dict[str, List[int]]: dictionary of the json file.
    """
    with open(filename, 'r',  encoding="utf-8") as file:
        placement_json = file.read()
        placement_data = json.loads(placement_json)
        return placement_data

#Place battleships
def place_battleships(board: List[List[Union[None, Any]]], ships: Dict[str, int], algorithm: Literal['simple', 'random', 'custom'] = 'simple', placement_data: Dict[str, List[int]] = placement_from_file("placement.json")) -> List[List[Union[None, Any]]]:
    """Battleship placed according to algorithm.

    Args:
        board (List[List[Union[None, Any]]]): The 10x10 grid for battleship.
        ships (Dict[str, int]): The dictionary containing the ship's info.
        algorithm (Literal[&#39;simple&#39;, &#39;random&#39;, &#39;custom&#39;], optional): default algorithm is 'simple'.
        placement_data (Dict[str, List[int]], optional): reads the json file from the function placement_from_file("placement.json").

    Raises:
        ValueError: raises invalid algorithm.

    Returns:
        List[List[Union[None, Any]]]: The 10x10 grid for battleship.
    """
    if algorithm == 'simple':
        return simple_placement(board, ships)
    elif algorithm == 'random':
        return random_placement(board, ships)
    elif algorithm == 'custom':
        return custom_placement(board, ships, placement_data)
    else:
        raise ValueError("Invalid algorithm")

#Simple
def simple_placement(board: List[List[Union[None, Any]]], ships: Dict[str, int]) -> List[List[Union[None, Any]]]:
    """The algorithm for simple placement.

    Args:
        board (List[List[Union[None, Any]]]): The 10x10 grid for the battleship game.
        ships (Dict[str, int]): The dictionary of the ship's info.

    Returns:
        List[List[Union[None, Any]]]: The 10x10 grid for the battleship game.
    """
    row = 0
    for ship_name, ship_size in ships.items():
        for i in range(ship_size):
            board[row][i] = ship_name
        row += 1
    return board

#Random
def random_placement(board: List[List[Union[None, Any]]], ships: Dict[str, int]) -> List[List[Union[None, Any]]]:
    """Randomly places the ship on the board.

    Args:
        board (List[List[Union[None, Any]]]): The 10x10 grid for the battleship game.
        ships (Dict[str, int]): The dictionary of the ship's info.

    Returns:
        List[List[Union[None, Any]]]: The 10x10 grid for the battleship game.
    """
    for ship_name, ship_size in ships.items():
        placed = False
        while not placed:
            orientation = random.choice(['h', 'v']) #Random choice of horizontal or vertical
            if orientation == 'h':
                start_row = random.randint(0, len(board) - 1)
                start_col = random.randint(0, len(board) - ship_size)
                if all(board[start_row][start_col + i] is None for i in range(ship_size)):
                    for i in range(ship_size):
                        board[start_row][start_col + i] = ship_name
                    placed = True
            else:
                start_row = random.randint(0, len(board) - ship_size)
                start_col = random.randint(0, len(board) - 1)
                if all(board[start_row + i][start_col] is None for i in range(ship_size)):
                    for i in range(ship_size):
                        board[start_row + i][start_col] = ship_name
                    placed = True
    return board

#Custom
def custom_placement(board: List[List[Union[None, Any]]], ships: Dict[str, int], placement_data: Dict[str, List[int]] = placement_from_file("placement.json")) -> List[List[Union[None, Any]]]:
    """Battleships placed depending on how the user has placed the battleship. Read according to the json file.
    
    Args:
        board (List[List[Union[None, Any]]]): The 10x10 grid for the battleship game.
        ships (Dict[str, int]): The dictionary of the ship's info.
        placement_data (Dict[str, List[int]], optional): reads the json file from the function placement_from_file("placement.json").

    Returns:
        List[List[Union[None, Any]]]: The 10x10 grid for the battleship game.
    """
    for ship_name, position in placement_data.items():
        col, row, orientation = map(str, position)
        col, row= int(col), int(row)
        
        if orientation == 'h':
            for i in range(ships[ship_name]):
                ##print(row, col + i, ship_name, orientation)
                board[row][col + i] = ship_name
        elif orientation == 'v':
            for i in range(ships[ship_name]):
                ##print(row + i, col, ship_name, orientation)
                board[row + i][col] = ship_name
    ##print(board)

    return board

#initialise_board()