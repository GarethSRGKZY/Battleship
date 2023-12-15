# README

# BATTLESHIPS
This project is a python interpretation of the board game battleships.
Battleships is a strategy game involving 2 players to guess which coordinate on the grid has the battleship.
The player that hits all battleships wins the game. 

Note: This project was the coursework task for ECM1400 Comp Sci BSC University of Exeter.

-----------------------


# Pytest
This test was run with the test files provided and with the command `python -m pytest` on the terminal / command prompt

(24 passed, 6 warnings)

-----------------------

Installation requirements via

`pip install -r requirements.txt`

in terminal / command prompt

------------------------

## How to use this program
To run the game to play against the AI without web interface:

* At `game_engine.py`, at this line `board[y][x] = None` in the attack function, change `None` into `"X"`.
* Run the `mp_game_engine.py` file. This includes the speaking feature to make it more fun or personal.

To run the game to play against the AI with the web interface:

* If you had changed `None` to `"X"` in the attack function in this line `board[y][x] = None`, change it back to `None`.
* Run the main.py file. This will not include the speaking feature unfortunately as it might crash the game. Click on the link provided in the terminal. The page should consist of two 10x10 grids that are empty. To place your battleship, on the link, type `/placement` to place the battleships and click "Send Game". The game should start.

----------

## Self evaluation:
This project has reached the minimum requirements specified by the specifications:

### Components.py
----------
* `initialise_board` renders the 10x10 board. Coordinates of (0,0) to (9,9)

* `create_battleship` contains the info from battleships.txt

*`place_battleships` will place the battleship depending on the algorithm given.

----------

### game_engine.py
----------
* `attack` determines whether the battleship is hit or missed or the whole of the battleship is sunk.

* `cli_coordinates_input` asks the user for the x and y coordinates between the range of 0-9.

* `simple_game_loop` runs the game using the functions from components.py and the previous functions in the `game_engine` file.

----------

### mp_game_engine.py
----------
* `generate_attack` is the attack function for the AI.

* `ai_opponent_game_loop` runs the game using the functions in `mp_game_engine` file, `components.py` file and the `game_engine.py` file.

----------

### main.py
----------
This file uses classes.

* `/placement` route renders the placement board in placement.html and stores the placement data in a json file when the user is done placing.

* `/` route renders the main board in main.html and uses the placement data from placement.html into the player's grid.

* `/attack` route contains the function for AI and the user to attack. Displays finished message depending on which who has sunk all the opponent's battlehsips.

----------

### Extras
----------
The AI attacks in the generate_attack function has improved from picking random coordinates into attacking an adjacent coordinate when the AI has hit a ship. The AI would also not do a repeated hit when ships are adjacent to each other.

----------
Overall, I felt like I could have done more but debugging the main.py file and improving the AI took some time.

----------
## License and Copyright
© Gareth, student

Licensed under the [MIT License](LICENSE)