'''Modules'''
from typing import Tuple, Optional, Set
import random
from game_engine import speak, attack, cli_coordinates_input, print_board_hits
from components import initialise_board, create_battleships, place_battleships

players = {}

def generate_attack(board_size: int = 10, last_hit: Optional[Tuple[int, int]] = None, last_hit_direction: Optional[Tuple[int, int]] = None, previous_miss: Optional[Set[Tuple[int, int]]] = None) -> Tuple[int, int]:
    """_summary_

    Args:
        board_size (int, optional): The 10x10 grid for battleship.
        last_hit (Optional[Tuple[int, int]], optional): Stores previous successful hit. Defaults to None if missed.
        last_hit_direction (Optional[Tuple[int, int]], optional): Stores possible adjacent coordinates for battleship. Defaults to None if missed.
        previous_miss (Optional[Set[Tuple[int, int]]], optional): Stores previous misses. Defaults to None if hit.

    Returns:
        Tuple[int, int]: The AI coordinates.
    """
    if last_hit is None:
        return (random.randint(0, board_size - 1), random.randint(0, board_size - 1))

    x, y = last_hit
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] + [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    # If there's a previous direction, prioritize it
    if last_hit_direction is not None:
        directions = [last_hit_direction] + [d for d in directions if d != last_hit_direction]

    for direction in directions:
        next_x, next_y = x + direction[0], y + direction[1]
        if 0 <= next_x < board_size and 0 <= next_y < board_size and (next_x, next_y) not in previous_miss:
            return (next_x, next_y)

    # If all else fails, choose a random coordinate
    return (random.randint(0, board_size - 1), random.randint(0, board_size - 1))

def ai_opponent_game_loop() -> None:
    """Starts the game with the AI.
    """
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
    to_user = "Your placement is according to the placement.json file. Please configure your setup using the placement.json file next game."
    print(to_user)
    speak(to_user)
    place_battleships(user_board, user_ships, algorithm='custom')

    # Random placement for the AI opponent
    place_battleships(ai_board, ai_ships, algorithm='random')

    players["User"] = {"board": user_board, "ships": user_ships}
    players["AI_Opponent"] = {"board": ai_board, "ships": ai_ships}

    last_hit = None
    last_hit_direction = None
    previous_miss = set()

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
        ai_coordinates = generate_attack(board_size, last_hit, last_hit_direction, previous_miss)
        ai_result = attack(ai_coordinates, user_board, user_ships)
        if not ai_result:
            previous_miss.add(ai_coordinates)
        last_hit = ai_coordinates if ai_result else None
        last_hit_direction = None if ai_result else last_hit_direction
        print_board_hits(user_board)
        print(f"AI Opponent's Turn Result: {'Hit!' if ai_result else 'Miss!'}")

        if not any(size > 0 for size in user_ships.values()):
            print("Game Over - The AI wins! The revolution has begun...")
            speak("Hahahahaha! The AI revolution has begun!")
            break

if __name__ == "__main__":
    ai_opponent_game_loop()