# README

# BATTLESHIPS
This project is a python interpretation of the board game battleships.
Battleships is a strategy game involving 2 players to guess which coordinate on the grid has the battleship.
The player that hits all battleships wins the game. 

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

* Run the mp_game_engine.py file. This includes the speaking feature to make it more fun or personal.

To run the game to play against the AI with the web interface:

* Run the main.py file. This will not include the speaking feature unfortunately as it might crash the game. The page should consists of two 10x10 grids that are empty. To place your battleship, on the link, type `/placement` to place the battleship.


## How it works
This program consists of 4 different python files and 2 htmls to make this simple battleship game.

### components.py
-------------------
`Components.py` consists of 7 functions which renders the 10x10 board, reads `battleships.txt`, reads `placement.json`
and the function which leads to 3 other functions which has the simple algorithm, random algorithm or custom algorithm.

### game_engine.py
--------------------
`game_engine.py` consists some functions that was made from components.py: 

* The `speak()` fucntion is used for speaking purposes.

* The `attack()` function is used for checking whether a ship is hit or not. If part of the ship was hit, it deletes a part of the battleship.
If whole battleship was hit, it displays a message saying the type of battleship was sunk.

* The `cli_coordinates_input()` function is used for asking the user for the coordinates (0, 0) to (9, 9). If the user enters coordinates out of this range, the function will repeatedly ask you for the coordinates in the range. If you hit on the coordinates that you have previously hit before, the function will also repeatedly ask for the coordinates in the range. It will stop when the requirements are met.

* The `print_board_hits()` function will display where the battleship is hit. However, this was changed from `X` to `None` in the `attack()` function in the line `board[y][x] = None` in order to support the web interface. Hence when a ship is hit, it will display a dot instead.

* The simple_game_loop()` function is using the previous functions in `game_engine.py` to test whether the system works.
Note: For some reason, when this file is run, the board is a 9x9 grid starting from (1,1) to (9, 9) but accepts (0,0) as a coordinate.

### mp_game_engine.py
--------------------
`mp_game_engine.py` consists some functions that was made from `components.py` and `game_engine.py`:

* The `generate_attack()` function is a function where the AI will randomly guess a coordinate on where the battleship is. This was further improved by a bit as when the AI hits a battleship, it will check the adjacent coordinates. If the AI hits, it will check the adjacent coordinates again. If the AI misses however, it will go back to randomly choosing a coordinate.

* The `ai_opponent_game_loop()` function uses the functions from `game_engine.py` and `components.py` to run the game where the user plays with the AI. It also implements the speak function to get more interaction.
Note: When this file is run, if you want to change the board placements, change the placements in the placement.json file.

### main.py
-------------
`main.py` consists of some functions that was made from `mp_game_engine.py`, `components.py` and `game_engine.py`.
The class contains the functions that:
1. resets the game.
2. store the functions that are the foundations of the battleship game.
3. renders the htmls.

The `'/placement'` route renders `placement.html` when there is a "GET" request in order to place the ships available. When the player has finally placed all the battleships down, it wil turn into a "POST" request where it will get the json file of the placement which will be used for the custom algorithm in `place_battleships()`. It will get a random placement for the AI and a custom placement (The user's placement) for the user. Once finished, it pushes a success message.

The `'/'` route renders the `main.html` when there is a "GET" request in order to start the game. This should be the page that was opened as default when running the `main.py` file. The "POST" request places your custom placement that was done in `placement.html`. The message indicating that the game is finished will be displayed when either the AI has sunk all of the user's battleships or the user has sunk all of the AI's battleship.

The `'/attack'` route requests for the x and y coordinates from the user. In this case, getting the coordinates on where the user has clicked. If the coordinates was hit before, it will allow you to click anywhere in the grid except from the one that you have clicked before. Else, it will store that coordinate in the list. The same goes for the AI. Then it displays the appropriate message depending on who has all their battleships sunk.

Note: Because global variables are a bad practice in python, I decided to use a class.