# python_snake_game_model.py
# author: Robin Jiang

# this module contains the logic or "model" part of the snake game

import random

# global constants

# possible states for a block
POSSIBLE_STATES = (" ", "H", "B", "P")


# exceptions
class MoveAfterGameOverError(Exception):
    """For if the game tries to continue after the game is over"""
    pass


class SnakeGameState:
    """class that represents one board for a snake game"""
    def __init__(self, rows: int = 9, cols: int = 9):
        """Minimum 3 rows and 3 cols. preferred odd number"""
        # board that represents a game
        self._board: list[list['Block']] = []
        for row in range(rows):
            self._board.append([])
            for col in range(cols):
                self._board[row].append(Block())

        # pointers to the head and tail of the snake (represented by a singly linked list)
        self._snake_head = self._create_snake()
        self._snake_tail = self._snake_head

        # dictionary for mapping direction and symbol for head of snake (only for shell game)
        self._parsing_key = {"N": "^", "E": ">", "S": "v", "W": "<"}

        # whether the game is still going on
        self._game_over = False

        # if the snake needs to grow twice
        self._still_growing = False
        self._length = 1

        # if the current point has been eaten
        self._point_eaten = True

        # if the snake has already turned (it can only turn once per block)
        self._already_turned = False

        # next move queue for turning
        self._next_move = None

        # point coordinates
        self._point_coordinates = None


    def progress_game(self) -> None:
        self._require_game_not_over()
        next_row, next_col = self._calculate_next_block_location()
        if not self._game_over:
            self._already_turned = False
            # next = towards the head
            next_head = Block(state="H", direction=self._snake_head.get_direction(), row=next_row, col=next_col,
                              next_value=None)
            ate_point = self._board[next_row][next_col].get_state() == "P"
            too_short = self._length < 3
            if ate_point or too_short or self._still_growing:
                if ate_point and too_short:
                    self._still_growing = True
                else:
                    #FIGURE THIS OUT FOR 2 POINTS RIGHT OFF THE BAT
                    self._still_growing = False

                if ate_point:
                    # set game loop up to create new point
                    self._point_eaten = True
                self._length += 1
            else:
                to_del = self._snake_tail
                self._snake_tail = self._snake_tail.get_next()
                self._board[to_del.get_row()][to_del.get_column()] = Block()
            self._board[next_row][next_col] = next_head
            self._snake_head.set_next(next_head)
            self._snake_head.set_state("B")
            self._snake_head = next_head
            if self._next_move is not None:
                self._next_move()
                self._next_move = None
            if self._point_eaten:
                self.create_random_point()

    def turn_north(self) -> None:
        """turns the snake north if possible"""

        if self._snake_head.get_direction() in ("E", "W") and not self._already_turned:
            self._snake_head.set_direction("N")
            self._already_turned = True
        elif self._already_turned and self._next_move is None:
            self._next_move = self.turn_north

    def turn_east(self) -> None:
        """turns the snake east if possible"""
        if self._snake_head.get_direction() in ("N", "S") and not self._already_turned:
            self._snake_head.set_direction("E")
            self._already_turned = True
        elif self._already_turned and self._next_move is None:
            self._next_move = self.turn_east

    def turn_south(self) -> None:
        """turns the snake south if possible"""
        if self._snake_head.get_direction() in ("E", "W") and not self._already_turned:
            self._snake_head.set_direction("S")
            self._already_turned = True
        elif self._already_turned and self._next_move is None:
            self._next_move = self.turn_south

    def turn_west(self) -> None:
        """turns the snake west if possible"""
        if self._snake_head.get_direction() in ("N", "S") and not self._already_turned:
            self._snake_head.set_direction("W")
            self._already_turned = True
        elif self._already_turned and self._next_move is None:
            self._next_move = self.turn_west

    def print_board(self) -> None:
        """prints the board"""
        print(self._prepare_print_board())

    def get_board(self) -> list[list['Block']]:
        """returns a copy of the board"""
        copy_board = []
        for row in range(len(self._board)):
            copy_board.append([])
            for col in range(len(self._board[0])):
                copy_board[row].append(self._board[row][col].make_copy())
        return copy_board

    def create_random_point(self) -> None:
        """Creates a random point and adds it to the board."""
        eligible_blocks = []
        for row in range(len(self._board)):
            for col in range(len(self._board[0])):
                if self._board[row][col].get_state() == " ":
                    # empty board spot
                    eligible_blocks.append((row, col))
        row, col = random.choice(eligible_blocks)
        self._point_coordinates = (row, col)
        self._board[row][col] = Block(row=row, col=col, state="P")
        self._point_eaten = False

    def get_game_over(self) -> bool:
        return self._game_over

    def get_snake_length(self) -> int:
        """returns the length of the snake"""
        return self._length

    def get_snake_tail(self) -> 'Block':
        return self._snake_tail

    def get_point_coordinates(self) -> tuple[int, int]:
        return self._point_coordinates

    # protected class methods
    def _prepare_print_board(self) -> str:
        """returns one str for the shell to print the board"""
        str_to_print = "_" * 3 * len(self._board[0]) + "__" + "\n"
        for row in range(len(self._board)):
            str_to_print += "|"
            for col in range(len(self._board[0])):
                str_to_print += " " + self._parse_state(self._board[row][col]) + " "
            str_to_print += "|\n"
        str_to_print += "_" * 3 * len(self._board[0]) + "__"
        return str_to_print

    def _parse_state(self, block: 'Block') -> str:
        """Parses the state of the board from block state to a str of length one"""
        # B = body, H = head, P = point
        state = block.get_state()
        if state == "B":
            return "B"
        elif state == "H":
            return self._parsing_key[block.get_direction()]
        elif state == "P":
            return "P"
        else:
            return "."

    def _require_game_not_over(self) -> None:
        if self._game_over:
            raise MoveAfterGameOverError

    def _create_snake(self) -> 'Block':
        """Makes a snake for the board. Intended for use only when the board is first initialized."""
        head = Block(state="H", direction="N", row=int(len(self._board)/2), col=int(len(self._board[0])/2) )
        self._board[head.get_row()][head.get_column()] = head
        return head

    def _calculate_next_block_location(self) -> tuple[int, int]:
        """Returns the row and column of the next block if the snake is to move forward.
        Checks to see if the next location is viable"""
        direction = self._snake_head.get_direction()
        row, col = -1, -1
        if direction == "N" or direction == "S":
            if direction == "N":
                row = self._snake_head.get_row() - 1
            else:
                row = self._snake_head.get_row() + 1
            col = self._snake_head.get_column()
        elif direction == "E" or direction == "W":
            if direction == "E":
                col = self._snake_head.get_column() + 1
            else:
                col = self._snake_head.get_column() - 1
            row = self._snake_head.get_row()
        self._require_next_row_and_column_are_valid(row, col)
        return row, col

    def _require_next_row_and_column_are_valid(self, row: int, col: int) -> None:
        """Sets game_over to True if the next position for the head is invalid"""
        if not(0 <= row < len(self._board)) or not(0 <= col < len(self._board[0])):
            self._game_over = True
            return
        if self._board[row][col].get_state() == "B" or self._board[row][col].get_state() == "H":
            self._game_over = True
            return



class Block:
    """Class that represents a block of the snake as part of a singly linked list from tail to head.
    Can also be used to represent a Point for the snake to eat, or a blank space."""
    def __init__(self, state: str = " ", next_value: 'Block | None' = None, direction: str | None = None,
                 row: int | None = None, col: int | None = None) -> None:
        """Initializes the attributes of a block. Only state is needed for a point or blank space.
        next_value, direction, row, and col are useful for parts of a snake."""
        if state not in POSSIBLE_STATES:
            raise ValueError
        self._state = state
        self._next = next_value
        self._direction = direction
        self._row = row
        self._col = col
        self._previous_direction = direction

    def __eq__(self, other) -> bool:
        return (self._state == other.get_state() and self._next == other.get_next()
                and self._direction == other.get_direction() and
                self._row == other.get_row() and self._col == other.get_column())

    def __str__(self) -> str:
        return f"Block(state = {self._state}, direction = {self._direction}, " \
               f"previous direction = {self._previous_direction}, row = {self._row}, column = {self._col})"

    def __repr__(self) -> str:
        return self.__str__()

    def get_state(self) -> str:
        return self._state

    def get_next(self) -> 'Block':
        """Returns a pointer to the next value, or None if there is none."""
        return self._next

    def get_direction(self) -> str:
        return self._direction

    def get_previous_direction(self) -> str:
        return self._previous_direction

    def get_row(self) -> int:
        return self._row

    def get_column(self) -> int:
        return self._col

    def set_next(self, next_block: 'Block | None') -> None:
        self._next = next_block

    def set_state(self, state: str) -> None:
        if state not in POSSIBLE_STATES:
            raise ValueError
        self._state = state

    def set_direction(self, direction: str) -> None:
        if direction not in "NESW":
            raise ValueError
        self._direction = direction

    def set_previous_direction(self, direction: str) -> None:
        if direction not in "NESW":
            raise ValueError
        self._previous_direction = direction

    def make_copy(self) -> 'Block':
        return Block(state=self.get_state(), direction=self._direction, col=self._col, row=self._row, next_value=self._next)
