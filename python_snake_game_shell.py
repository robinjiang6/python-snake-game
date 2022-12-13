# python_snake_game_shell.py
# author: Robin Jiang
#
# this implements a shell version of the python game

import python_snake_game_model

def run() -> None:
    """Runs the shell game"""
    rows, cols = _get_dimensions()
    game = python_snake_game_model.SnakeGameState(rows, cols)
    game.print_board()
    while not game.get_game_over():
        next_move = input().strip().upper()
        if len(next_move) == 0:
            game.progress_game()
        elif next_move == "W":
            game.turn_north()
        elif next_move == "D":
            game.turn_east()
        elif next_move == "S":
            game.turn_south()
        elif next_move == "A":
            game.turn_west()
        game.print_board()
    print()
    print("GAME OVER")

def _get_dimensions() -> tuple[int, int]:
    """Asks the user for the dimensions of the board"""
    rows, cols = 0, 0
    while rows < 1:
        try:
            rows = int(input("number of rows: "))
            if rows < 1:
                print("enter a number greater than or equal to 1")
        except ValueError:
            print("invalid input")
    while cols < 1:
        try:
            cols = int(input("number of columns: "))
            if cols < 1:
                print("enter a number greater than or equal to 1")
        except ValueError:
            print("invalid input")
    return rows, cols


if __name__ == "__main__":
    run()
