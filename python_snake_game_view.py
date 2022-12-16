# python_snake_game_view.py
# author: Robin Jiang

# this module contains the gui or "view" of the snake game

import pygame
import python_snake_game_model
import random

# global constants
TARGET_FRAMERATE = 30
CYCLE_SPEED = TARGET_FRAMERATE / 6
ROWS = 9
COLUMNS = 16
FONT = "Arial"
BACKGROUND_COLOR = pygame.Color(7, 70, 77)
TEXT_COLOR = pygame.Color(255, 255, 255)
BOARD_COLOR = pygame.Color(6, 42, 46)
BOARD_BORDER_COLOR = pygame.Color(11, 125, 138)
BUTTON_BACKGROUND_COLOR = pygame.Color(13, 105, 115)
BODY_COLOR = pygame.Color(50, 200, 100)
HEAD_COLOR = pygame.Color(50, 100, 200)
POINT_COLOR = pygame.Color(200, 50, 50)


# KEY_DICT = {pygame.K_LEFT: "LEFT", pygame.K_a: "LEFT", pygame.K_UP: "UP", pygame.K_w: "UP", pygame.K_s: "DOWN", pygame.K_DOWN: "DOWN", pygame.K_d: "RIGHT", pygame.K_RIGHT: "RIGHT"}


class SnakeGame:
    """class that implements the pygame view of a snake game"""

    def __init__(self) -> None:
        self._running = True
        self._cycles = 0
        self._point_cycles = 0
        self._game = python_snake_game_model.SnakeGameState(ROWS, COLUMNS)
        # possible phases: "START", "GAME", "GAME_OVER_ANIMATION", "GAME_OVER"
        self._phase = "START"
        self._starting_button = None
        self._restart_button = None
        self._game_rect = None

        # keeping score
        self._high_score = 0
        self._current_score = 1

        # tuple of possible links to images for body
        self._img_link_tuple = random.choice((('avogadro.png', 'bananabit.png'), ('bananabit.png', 'avogadro.png')))

    def run(self) -> None:
        pygame.init()
        box_width = 50
        self._resize_surface((16 * box_width, 9 * box_width))
        clock = pygame.time.Clock()

        while self._running:
            clock.tick(TARGET_FRAMERATE)
            self._cycles += 1
            self._point_cycles += 1
            if self._cycles == CYCLE_SPEED:
                self._cycles = 0
                if self._phase == "GAME":
                    self._game.progress_game()
                    self._update_score()
                if self._phase == "GAME_OVER_ANIMATION":
                    self._phase = "GAME_OVER"
            if self._point_cycles == 8 * CYCLE_SPEED:
                self._point_cycles = 0
            self._handle_events()
            self._redraw()
        pygame.quit()

    # protected class methods

    def _update_score(self) -> None:
        """updates the score and last snake part version"""
        if self._current_score < self._game.get_snake_length():
            self._current_score = self._game.get_snake_length()
        if self._current_score > self._high_score:
            self._high_score = self._current_score

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                self._turn_snake(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click(event.pos)
        if self._game.get_game_over() and self._phase == "GAME":
            self._phase = "GAME_OVER_ANIMATION"

    def _resize_surface(self, size: tuple[int, int]) -> None:
        """Resizes the pygame window to the size."""
        pygame.display.set_mode(size, pygame.RESIZABLE)

    def _turn_snake(self, key: int) -> None:
        """handles keystrokes to turn the snake when the key is first pressed down"""
        if self._phase == "GAME":
            if self._turn_east(key):
                self._game.turn_east()
            elif self._turn_south(key):
                self._game.turn_south()
            elif self._turn_west(key):
                self._game.turn_west()
            elif self._turn_north(key):
                self._game.turn_north()
        elif self._phase == "START" and key == pygame.K_SPACE:
            self._phase = "GAME"
        elif self._phase == "GAME_OVER" and key == pygame.K_SPACE:
            self._restart_game()

    def _turn_east(self, key: int) -> bool:
        return key in (pygame.K_RIGHT, pygame.K_d)

    def _turn_south(self, key: int) -> bool:
        return key in (pygame.K_DOWN, pygame.K_s)

    def _turn_west(self, key: int) -> bool:
        return key in (pygame.K_LEFT, pygame.K_a)

    def _turn_north(self, key: int) -> bool:
        return key in (pygame.K_UP, pygame.K_w)

    def _redraw(self) -> None:
        """Draws the board"""
        surface = pygame.display.get_surface()
        surface.fill(BACKGROUND_COLOR)
        if self._phase == "START":
            self._draw_start_screen(surface)
        elif self._phase in ("GAME", "GAME_OVER_ANIMATION"):
            self._draw_game(surface)
            self._draw_snake(surface)
            self._blit_score(surface)
        elif self._phase == "GAME_OVER":
            self._draw_game_over(surface)
        pygame.display.flip()

    def _draw_start_screen(self, surface: pygame.Surface) -> None:
        """Draws the start screen"""
        # drawing the button
        self._draw_start_button(surface)
        # drawing the instructions for the game
        self._blit_start_instructions(surface)

    def _draw_start_button(self, surface: pygame.Surface) -> None:
        """draws the starting button the user can press to start the game."""
        width_pix = surface.get_width()
        height_pix = surface.get_height()
        # drawing the button
        self._starting_button = self._calculate_button_dimensions(surface)
        button_height = self._starting_button.height
        border_radius = _round(button_height / 10)
        pygame.draw.rect(surface, BUTTON_BACKGROUND_COLOR, self._starting_button, border_radius=border_radius)
        pygame.draw.rect(surface, TEXT_COLOR, self._starting_button, width=2, border_radius=border_radius)

        # blitting the "START" text over the button
        font = pygame.font.SysFont(FONT, _round(button_height * 0.8))
        text = font.render("START", True, TEXT_COLOR)
        text_box = text.get_rect()
        text_box.center = (width_pix / 2, height_pix / 2)
        surface.blit(text, text_box)

    def _blit_start_instructions(self, surface: pygame.Surface) -> None:
        """blits the starting instructions at the top of the screen for the starting screen."""
        color = TEXT_COLOR
        width_pix = surface.get_width()
        height_pix = surface.get_height()
        font_height = _round(min(width_pix * 0.07, height_pix / 20))
        font = pygame.font.SysFont(FONT, font_height)
        text1 = font.render("Left Arrow = Turn West", True, color)
        text2 = font.render("Right Arrow = Turn East", True, color)
        text3 = font.render("Down Arrow = Turn South", True, color)
        text4 = font.render("Up Arrow = Turn North", True, color)
        text1_box, text2_box, text3_box, text4_box = text1.get_rect(), text2.get_rect(), \
            text3.get_rect(), text4.get_rect()
        text1_box.center = (width_pix / 2, font_height * 1)
        text2_box.center = (width_pix / 2, font_height * 2)
        text3_box.center = (width_pix / 2, font_height * 3)
        text4_box.center = (width_pix / 2, font_height * 4)
        surface.blit(text1, text1_box)
        surface.blit(text2, text2_box)
        surface.blit(text3, text3_box)
        surface.blit(text4, text4_box)

    def _calculate_button_dimensions(self, surface: pygame.Surface) -> pygame.Rect:
        """Calculates the dimensions of the button, and returns the rectangle associated with the button"""
        # The button will only change sizes if the screen is smaller than it.
        # It will not change size proportionally otherwise
        button_width = 300
        button_height = 100

        # calculations for the start button (rect)
        width_pix = surface.get_width()
        height_pix = surface.get_height()
        top_left_x = (width_pix - button_width) / 2
        top_left_y = (height_pix - button_height) / 2
        if width_pix <= button_width + 30:
            top_left_x = (1 - 0.9) / 2 * width_pix
            button_width = 0.9 * width_pix
            button_height = button_width / 3
            top_left_y = (height_pix - button_height) / 2
        if height_pix <= button_height + 10:
            top_left_y = (1 - 0.9) / 2 * height_pix
            button_height = 0.9 * height_pix
            button_width = 3 * button_height
            top_left_x = (width_pix - button_width) / 2

        return pygame.Rect(top_left_x, top_left_y, button_width, button_height)

    def _handle_click(self, pos: tuple[int, int]) -> None:
        """Checks to see if the user clicked on the start button"""
        if self._phase == "START":
            rect = self._starting_button
            if (rect.centerx - rect.width / 2 < pos[0] < rect.centerx + rect.width / 2 and
                    rect.centery - rect.height / 2 < pos[1] < rect.centery + rect.height / 2):
                self._phase = "GAME"
        elif self._phase == "GAME_OVER":
            rect = self._restart_button
            if (rect.centerx - rect.width / 2 < pos[0] < rect.centerx + rect.width / 2 and
                    rect.centery - rect.height / 2 < pos[1] < rect.centery + rect.height / 2):
                self._restart_game()

    def _draw_game(self, surface: pygame.Surface) -> None:
        """draws the game board."""
        width_pix = surface.get_width()
        height_pix = surface.get_height()

        box_width = min(0.9 * width_pix / COLUMNS, 0.8 * height_pix / ROWS)
        game_width = (box_width + 1) * COLUMNS
        game_height = (box_width + 1) * ROWS
        top_left_x = (width_pix - game_width) / 2
        top_left_y = 0.1 * height_pix

        # draw a rectangle to be the background color of the game
        self._game_rect = pygame.Rect(top_left_x, top_left_y, game_width, game_height)
        pygame.draw.rect(surface, BOARD_COLOR, self._game_rect)

        # draws a border around the game, in a rectangle 2px wider and taller and 3px thick
        delta = 3
        board_outline = pygame.Rect(top_left_x - delta, top_left_y - delta,
                                    game_width + 2 * delta - 1, game_height + 2 * delta - 1)
        pygame.draw.rect(surface, BOARD_BORDER_COLOR, board_outline, width=delta)

        # draw the lines inside the board that make a grid pattern
        for delta_rows in range(1, ROWS):
            y_level = _round(top_left_y + delta_rows * (game_height / ROWS) - 1)
            pygame.draw.line(surface, BOARD_BORDER_COLOR, (top_left_x, y_level), (top_left_x + game_width - 2, y_level))
        for delta_cols in range(1, COLUMNS):
            x_level = _round(top_left_x + delta_cols * (game_width / COLUMNS) - 1)
            pygame.draw.line(surface, BOARD_BORDER_COLOR, (x_level, top_left_y),
                             (x_level, top_left_y + game_height - 2))

        self._blit_score(surface)

    def _draw_snake(self, surface: pygame.Surface) -> None:
        """draws the snake on the surface"""

        game = self._game.get_board()
        snake_part = self._game.get_snake_tail()
        # snake_pos used to alternate colors in snake body
        snake_pos = 1
        if self._current_score % 2 == 0:
            snake_pos = 0

        # draw body
        while snake_part.get_next() is not None:
            self._calculate_snake_part_and_draw(surface, snake_part, snake_pos)
            snake_pos += 1
            snake_part = snake_part.get_next()

        # draw head
        self._calculate_snake_part_and_draw(surface, snake_part)

        # draw point
        if self._game.get_point_coordinates() is not None:
            self._calculate_snake_part_and_draw(surface, game[self._game.get_point_coordinates()[0]][self._game.get_point_coordinates()[1]])

    def _calculate_snake_part_and_draw(self, surface: pygame.Surface, snake_part: python_snake_game_model.Block, pos: int = 0) -> None:
        part_x = _round(self._game_rect.topleft[0] + (snake_part.get_column()) * self._game_rect.width / COLUMNS)
        part_y = _round(self._game_rect.topleft[1] + (snake_part.get_row()) * self._game_rect.height / ROWS)
        self._draw_snake_part(part_x, part_y, snake_part, surface, pos)

    def _draw_snake_part(self, x: int, y: int, snake_part: python_snake_game_model.Block,
                         surface: pygame.Surface, pos: int = 0) -> None:
        """Draws one snake part with the top left coordinate of the bounding box being the given x and y."""
        # subtract 1 from width to fit inside the box from trial and error
        width = self._game_rect.width / COLUMNS - 1
        height = self._game_rect.height / ROWS - 1
        bounding_rect = pygame.Rect(x, y, width, height)
        if snake_part.get_state() == "H":
            head_img = pygame.image.load('materwelon.png')
            head_img = pygame.transform.scale(head_img, (width, height))
            head_img = self._rotate_snake_head(head_img, snake_part)
            img_x, img_y = self._calculate_snake_part_coordinates(x, y, width, height, snake_part)
            surface.blit(head_img, (img_x, img_y))
        elif snake_part.get_state() == "P":
            point_img = pygame.image.load('strawberry.png')
            if self._point_cycles <= 20:
                img_width = width * 0.7 + width * 0.3 * (self._point_cycles/(4 * CYCLE_SPEED))
                img_height =  height * 0.7 + height * 0.3 * (self._point_cycles/(4 * CYCLE_SPEED))
                point_img = pygame.transform.scale(point_img, (img_width, img_height))
            else:
                img_width = width - width * 0.3 * ((self._point_cycles - 20)/(4 * CYCLE_SPEED))
                img_height = height - height * 0.3 * ((self._point_cycles - 20)/(4 * CYCLE_SPEED))
                point_img = pygame.transform.scale(point_img, (img_width, img_height))
            point_img = self._rotate_snake_head(point_img, snake_part)
            img_x, img_y = (x + (width - img_width)/2, y + (height - img_height)/2)
            surface.blit(point_img, (img_x, img_y))
        elif snake_part.get_state() == "B":
            pic_link = self._img_link_tuple[pos % 2]
            body_img = pygame.image.load(pic_link)
            body_img = pygame.transform.scale(body_img, (width, height))
            body_img = self._rotate_snake_head(body_img, snake_part)
            img_x, img_y = self._calculate_snake_part_coordinates(x, y, width, height, snake_part)
            surface.blit(body_img, (img_x, img_y))

    def _rotate_snake_head(self, head_img: pygame.image, snake_part: python_snake_game_model.Block) -> pygame.image:
        """rotates the snake block in accordance to the direction it is facing"""
        return_img = head_img
        # no intermediate images turning:
        match snake_part.get_direction():
            case "N":
                return_img = pygame.transform.rotate(head_img, 0)
            case "E":
                return_img = pygame.transform.rotate(head_img, 270)
            case "S":
                return_img = pygame.transform.rotate(head_img, 180)
            case "W":
                return_img = pygame.transform.rotate(head_img, 90)
        return return_img

    def _calculate_snake_part_coordinates(self, x: int, y: int, width: int, height: int,
                                          snake_part: python_snake_game_model.Block) -> tuple[int, int]:
        """calculates the coordinates of the snake part so that it looks animated"""
        multiplier = 1
        max_cycle = int(CYCLE_SPEED)
        if self._phase == "GAME_OVER_ANIMATION":
            if snake_part.get_state() == "H":
                multiplier = -1
            else:
                multiplier = 0
        if (snake_part.get_direction() == "N" and snake_part.get_row() == 0 or
                snake_part.get_direction() == "E" and snake_part.get_column() == COLUMNS - 1 or
                snake_part.get_direction() == "S" and snake_part.get_row() == ROWS - 1 or
                snake_part.get_direction() == "W" and snake_part.get_column() == 0):
            max_cycle = int(max_cycle / 2)
        match snake_part.get_direction():
            case "N":
                y = y - (height / CYCLE_SPEED * min(self._cycles, max_cycle) * multiplier)
            case "E":
                x = x + (width / CYCLE_SPEED * min(self._cycles, max_cycle) * multiplier)
            case "S":
                y = y + (height / CYCLE_SPEED * min(self._cycles, max_cycle) * multiplier)
            case "W":
                x = x - (width / CYCLE_SPEED * min(self._cycles, max_cycle) * multiplier)
        return x, y

    def _blit_score(self, surface: pygame.Surface) -> None:
        """blits the score at the top of the game screen"""
        color = TEXT_COLOR
        width_pix = surface.get_width()
        height_pix = surface.get_height()
        text_width = min(100, _round(width_pix * 0.3))
        text_height = min(_round(text_width / (1.4 * 4)), _round(height_pix / 2 * 0.1))
        font = pygame.font.SysFont(FONT, text_height)
        text_current_score = font.render(f"Score = {self._current_score}", True, color)
        text_high_score = font.render(f"High Score = {self._high_score}", True, color)
        text_box_current_score = text_current_score.get_rect()
        text_box_high_score = text_high_score.get_rect()
        text_box_current_score.center = (width_pix * 0.15, 1.1 * text_height)
        text_box_high_score.center = (width_pix * 0.4, 1.1 * text_height)
        surface.blit(text_current_score, text_box_current_score)
        surface.blit(text_high_score, text_box_high_score)

    def _draw_game_over(self, surface: pygame.Surface) -> None:
        """Draws the game over screen."""
        color = TEXT_COLOR
        width_pix = surface.get_width()
        height_pix = surface.get_height()
        text_width = min(300, _round(width_pix * 0.7))
        text_height = min(_round(text_width / (1.3 * 4)), _round(height_pix / 2 * 0.5))
        font = pygame.font.SysFont(FONT, text_height)
        font_small = pygame.font.SysFont(FONT, _round(text_height * 0.8))
        text_game_over = font.render("GAME OVER", True, color)
        text_current_score = font_small.render(f"Score = {self._current_score}", True, color)
        text_high_score = font_small.render(f"High Score = {self._high_score}", True, color)
        text_box_game_over = text_game_over.get_rect()
        text_box_current_score = text_current_score.get_rect()
        text_box_high_score = text_high_score.get_rect()
        text_box_game_over.center = (width_pix / 2, height_pix / 2 - 2.5 * text_height)
        text_box_current_score.center = (width_pix / 2, height_pix / 2 - 1.3 * text_height)
        text_box_high_score.center = (width_pix / 2, height_pix / 2 - 0.3 * text_height)
        surface.blit(text_game_over, text_box_game_over)
        surface.blit(text_current_score, text_box_current_score)
        surface.blit(text_high_score, text_box_high_score)
        self._draw_restart_button(surface)

    def _draw_restart_button(self, surface: pygame.Surface) -> None:
        """draws the restart button the user can press to restart the game after losing."""
        width_pix = surface.get_width()
        height_pix = surface.get_height()
        # drawing the button
        self._restart_button = self._calculate_button_dimensions(surface)
        self._restart_button.centery = height_pix * 0.7
        button_height = self._restart_button.height
        border_radius = _round(button_height / 10)
        pygame.draw.rect(surface, BUTTON_BACKGROUND_COLOR, self._restart_button, border_radius=border_radius)
        pygame.draw.rect(surface, TEXT_COLOR, self._restart_button, width=2, border_radius=border_radius)

        # blitting the "START" text over the button
        font = pygame.font.SysFont(FONT, _round(button_height * 0.6))
        text = font.render("RESTART", True, TEXT_COLOR)
        text_box = text.get_rect()
        text_box.center = (width_pix / 2, height_pix * 0.7)
        surface.blit(text, text_box)

    def _restart_game(self) -> None:
        """restarts the game"""
        self._game = python_snake_game_model.SnakeGameState(ROWS, COLUMNS)
        self._phase = "GAME"
        self._cycles = 0
        self._current_score = 1


def _round(num: float) -> int:
    """Rounds num to the closest integer, the traditional human way."""
    negative = False
    if num < 0:
        negative = True
        num *= -1
    decimal = num % 1
    if decimal >= 0.5:
        num = int(num) + 1
    else:
        num = int(num)
    if negative:
        return -1 * num
    return num


def _test_rounding() -> None:
    """Tests _round()"""
    for num in range(0, 100):
        assert _round(num + 0.49) == num
        assert _round(num + 0.5) == num + 1
        assert _round(num + 0.51) == num + 1
    for num in range(-100, 0):
        assert _round(num - 0.49) == num
        assert _round(num - 0.5) == num - 1
        assert _round(num - 0.51) == num - 1


_test_rounding()

if __name__ == "__main__":
    SnakeGame().run()
