from flask import Flask, request, render_template, jsonify
from components import initialise_board, create_battleships, place_battleships
from game_engine import attack
from mp_game_engine import generate_attack

app = Flask(__name__)

class BattleshipGame:
    '''Class for all the variables'''
    def reset(self):
        '''Resets the whole board so that there is no "hijacking"'''
        self.user_board = initialise_board(size=self.board_size)
        self.ai_board = initialise_board(size=self.board_size)
        self.user_ships = create_battleships()
        self.ai_ships = create_battleships()
        self.hit_before = set() #Set list of coordinates where player has hit before
        self.ai_hit_before = set() #Set list of coordinates where AI has hit before

    def __init__(self):
        self.ships = {
            "Aircraft_Carrier": 5,
            "Battleship": 4,
            "Cruiser": 3,
            "Submarine": 3,
            "Destroyer": 2,
        }
        self.board_size = 10
        self.placement = {}
        self.user_board = initialise_board(size=self.board_size)
        self.ai_board = initialise_board(size=self.board_size)
        self.user_ships = create_battleships()
        self.ai_ships = create_battleships()
        self.hit_before = set() #Set list of coordinates where player has hit before
        self.ai_hit_before = set() #Set list of coordinates where AI has hit before

        # Place ships on boards
        '''
        place_battleships(self.user_board, self.user_ships, algorithm='custom')
        place_battleships(self.ai_board, self.ai_ships, algorithm='random')
        '''

    def render_main_template(self, game_finished_message=None):
        '''Renders the main board. When game is finished, message is displayed.'''
        print(self.user_board)
        return render_template('main.html', player_board=self.user_board, game_finished_message=game_finished_message)

    def render_placement_template(self):
        '''Renders the placement board'''
        return render_template('placement.html', ships=self.ships, board_size=self.board_size)

battleship_game = BattleshipGame()

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    '''Renders the board placement first. If placement is done, messages display a success message.'''
    if request.method == 'GET':
        return battleship_game.render_placement_template()
    elif request.method == 'POST':
        battleship_game.placement = request.get_json()
        battleship_game.reset()
        place_battleships(battleship_game.ai_board, battleship_game.ai_ships, algorithm='random')
        place_battleships(battleship_game.user_board, battleship_game.user_ships, algorithm='custom', placement_data=battleship_game.placement)
        print(battleship_game.placement)
        return jsonify({"message": "Received!"})

@app.route('/', methods=['GET', 'POST'])
def root():
    '''Renders the main board'''
    if request.method == 'GET':
        return battleship_game.render_main_template()
    elif request.method == 'POST':
        place_battleships(battleship_game.user_board, battleship_game.user_ships, algorithm='custom', placement_data=battleship_game.placement)
        finished_message = request.form.get('finished_message')
        return battleship_game.render_main_template(game_finished_message=finished_message)

@app.route('/attack', methods=['GET'])
def attack_endpoint():
    '''
    Does all the hits and misses, implementing the game logic.
    '''
    if request.args:
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        coordinates = (x, y)
        
        ## User attacks
        result = attack((x, y), battleship_game.ai_board, battleship_game.ai_ships)

         # Check if the coordinates have been targeted before
        if coordinates in battleship_game.hit_before:
            return "", 409 # Prevent the word "undefined" from showing in the game log by causing parsing error.
        
         # Coordinates are added to a list that are hit before
        battleship_game.hit_before.add(coordinates)

        ## AI attacks
        ai_turn = generate_attack(battleship_game.board_size)

        #AI will keep choosing random coordinates until the coordinates is not in the list of previous hits
        while ai_turn in battleship_game.ai_hit_before:
            ai_turn = generate_attack(battleship_game.board_size)

        ## User attacks
        ai_result = attack(ai_turn, battleship_game.user_board, battleship_game.user_ships)

        # AI coordinates are added to a list that are hit before
        battleship_game.ai_hit_before.add(ai_turn)

        ##print("AI: ", battleship_game.ai_ships)
        ##print("USER: ", battleship_game.user_ships)

        if all(size == 0 for size in battleship_game.ai_ships.values()):
            return jsonify({'hit': result, 'AI_Turn': ai_turn, 'finished': 'Game Over - Player wins'})
        elif all(size == 0 for size in battleship_game.user_ships.values()):
            return jsonify({'hit': ai_result, 'AI_Turn': ai_turn, 'finished': 'Game Over - AI wins'})
        else:
            return jsonify({'hit': result, 'AI_Turn': ai_turn, 'finished': None})
        
if __name__ == "__main__":
    app.template_folder = "templates"
    app.run(debug=True, port=5000)

##Errors
##Placement in placement.html would not show on the players grid in main.html (json file default? Parsing required?)
##Can repeatedly hit the blue spots but not red. Need to restrict blue and red (game_engine?) adding previous hits list turns everything blue. (Fixed)
##AI can hit same spots repeatedly. (Change on mp_game_engine probably)
##Message not displayed when player is defeated. (User ships does not decrease when hit.) (Fixed)
##AI did not play when the user hits the board multiple times. (Improving the AI's ability to accurately hit the battleship).
##When restarting, the ship does not reset. (Fixed)
#########################################################################################################################################
##Fixed
##Placement error due to 2 reasons: 1. Inverted board from components.py (indexing error) 2.Board was not reset, more ships were added to an existing board on player's grid (Causing more confusion).
##Same spot error fixed. Needed to add a set list.
##AI same spot error fixed. Needed to add a while loop to it.
##Needed to add another result for the AI
##Put the hit_before and ai_hit_before in the class.
#########################################################################################################################################
##Note
##There may be a bug where one spot does not change colour when it is targeted. 