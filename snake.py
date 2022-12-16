# snake.py
# author: Robin Jiang
#
# This is the code for the main executable file that can be played

import python_snake_game_view
import sys
import os


def run() -> None:
    """Creates the paths for the image files and runs the game"""
    img_dir = resource_path("img")
    sound_dir = resource_path("sound")
    python_snake_game_view.SnakeGame(avogadro=os.path.join(img_dir, 'avogadro.png'),
                                     bananabit=os.path.join(img_dir, 'bananabit.png'),
                                     materwelon=os.path.join(img_dir, 'materwelon.png'),
                                     strawberry=os.path.join(img_dir, 'strawberry.png'),
                                     icon=os.path.join(img_dir, 'materwelon.ico')).run()

def resource_path(relative_path):
    """Get absolute path to resource"""
    # got this off the internet for making an executable standalone file
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    run()
