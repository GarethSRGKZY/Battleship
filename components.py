'''Modules'''
import random
import json

#Initialise board
def initialise_board(size=10):
    '''Returns a 10 x 10 board with the word None.'''
    return [[None] * size for _ in range(size)]

#create battleships
def create_battleships(filename="battleships.txt"):
    '''Opens battleship.txt file as filename is default.'''
    with open(filename, 'r', encoding="utf-8") as file:
        battleships_data = file.readlines()

    battleships = {}
    for line in battleships_data:
        name, size = line.strip().split(':')
        battleships[name] = int(size)

    return battleships

def placement_from_file(filename="placement.json"):
    '''Parsing the JSON file'''
    with open(filename, 'r',  encoding="utf-8") as file:
        placement_json = file.read()
        placement_data = json.loads(placement_json)
        return placement_data

#Place battleships
def place_battleships(board, ships, algorithm='simple', placement_data=placement_from_file("placement.json")):
    '''Battleship will be placed according to the algorithm'''
    if algorithm == 'simple':
        return simple_placement(board, ships)
    elif algorithm == 'random':
        return random_placement(board, ships)
    elif algorithm == 'custom':
        return custom_placement(board, ships, placement_data)
    else:
        raise ValueError("Invalid algorithm")

#Simple
def simple_placement(board, ships):
    '''Simple algorithm: Placing ships in horizontal rows only. Starting from (0,0)'''
    row = 0
    for ship_name, ship_size in ships.items():
        for i in range(ship_size):
            board[row][i] = ship_name
        row += 1
    return board

#Random
def random_placement(board, ships):
    '''Random algorithm: Placing ships in either horizontal or vertical. Placing ships in random coordinates.'''
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
def custom_placement(board, ships, placement_data):
    '''Custom algorithm: This is according to the placement.json file.'''
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