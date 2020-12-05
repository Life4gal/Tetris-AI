"""
This file is about the implementation of the Tetris Game(Actually there is nothing here)
"""

import typing


class Info:
    def __init__(
            self,
            landing_height: int = 0,
            best_place_column: int = 0,
            best_orientation: typing.List[int] = None,
            row_removed: int = 0,
            game_over: bool = False):
        """
        The information about what this action cause
        There is some redundancy, not all functions need these variables, but it simplifies the implementation
        :param landing_height:
            The height where the piece is put
            (= the height of the column + (the height of the piece / 2))
        :param best_place_column: Which column is the best place
        :param best_orientation: The best orientation to place
        :param row_removed: The number of rows eliminated
        :param game_over: Is game over
        """
        self.landing_height: int = landing_height
        self.column: int = best_place_column
        self.orientation: typing.List[int] = best_orientation
        self.row_removed: int = row_removed
        self.game_over: bool = game_over


class Tetris:
    # In the case of the current number of columns, the value indicates that the row is full
    FULL_ROW_VALUE = 2 ** 10 - 1

    def __init__(self, columns: int, rows: int):
        self.number_of_columns = columns
        self.number_of_rows = rows

        self.board = [0 for _ in range(self.number_of_rows)]

        Tetris.FULL_ROW_VALUE = 2 ** self.number_of_columns - 1
