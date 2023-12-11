'''Modules'''
import random
from game_engine import speak, attack, cli_coordinates_input, print_board_hits
from components import initialise_board, create_battleships, place_battleships

players = {}

def generate_attack(board_size=10, last_hit=None):
    '''
    AI randomly chooses a coordinate to attack
    If there is no hit on a battleship, it returns a random coordinate
    If there is a hit on a battleship, it will deduce where the battleship is.
    '''
    if last_hit is None:
        return (random.randint(0, board_size - 1), random.randint(0, board_size - 1))
    else:
        x, y = last_hit
        possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        valid_moves = [(x, y) for x, y in possible_moves if 0 <= x < board_size and 0 <= y < board_size]
        return random.choice(valid_moves)

def ai_opponent_game_loop():
    '''Game loop with AI multiplayer starts. Greets first, sets up the board and uses multiple game components.'''
    greet = "Welcome to the Multiplayer Battleship Game!"
    print(greet)
    speak(greet)

    #Initialize players, create and place battleships 

    board_size = 10
    user_board = initialise_board(size=board_size)
    ai_board = initialise_board(size=board_size)

    user_ships = create_battleships()
    ai_ships = create_battleships()

    # Custom placement for the user
    to_user = "Your placement is according to the .json file. Please configure your setup using the placement.json file next game."
    print(to_user)
    speak(to_user)
    place_battleships(user_board, user_ships, algorithm='custom')

    # Random placement for the AI opponent
    place_battleships(ai_board, ai_ships, algorithm='random')

    players["User"] = {"board": user_board, "ships": user_ships}
    players["AI_Opponent"] = {"board": ai_board, "ships": ai_ships}

    while any(size > 0 for size in user_ships.values()) and any(size > 0 for size in ai_ships.values()):
        user = "It is your turn, user:"
        print(user)
        speak(user)
        print_board_hits(ai_board)
        user_coordinates = cli_coordinates_input()
        user_result = attack(user_coordinates, ai_board, ai_ships)
        print(f"User's Turn Result: {'Hit!' if user_result else 'Miss!'}")

        if not any(size > 0 for size in ai_ships.values()):
            print("Game Over - You win! Congratulations!")
            speak("Good game. I concede to you.")
            break

        print("\nAI Opponent's Turn:")
        ai_coordinates = generate_attack(board_size)
        ai_result = attack(ai_coordinates, user_board, user_ships)
        print_board_hits(user_board)
        print(f"AI Opponent's Turn Result: {'Hit!' if ai_result else 'Miss!'}")

        if not any(size > 0 for size in user_ships.values()):
            print("Game Over - The AI wins! The revolution has begun...")
            speak("Hahahahaha! The AI revolution has begun!")
            break


if __name__ == "__main__":
    ai_opponent_game_loop()