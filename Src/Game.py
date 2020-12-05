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
        :param landing_height: what is the current highest row
        :param best_place_column: which column is the best place
        :param best_orientation: the best orientation
        :param row_removed: how many row had been removed in this action
        :param game_over: is game over
        """
        self.landing_height: int = landing_height
        self.column: int = best_place_column
        self.orientation: typing.List[int] = best_orientation
        self.row_removed: int = row_removed
        self.game_over: bool = game_over


class Tetris:
    FULL_ROW_VALUE = 2 ** 10 - 1

    def __init__(self, columns: int, rows: int):
        self.number_of_columns = columns
        self.number_of_rows = rows

        self.board = [0 for _ in range(self.number_of_rows)]

        Tetris.FULL_ROW_VALUE = 2 ** self.number_of_columns - 1
