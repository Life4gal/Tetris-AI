import typing

# alias
StandardBoard = typing.List[int]
StandardOrientation = typing.List[int]


class __StandardDataFormat:
	# Standard data storage format for each piece used by our algorithm
	def __init__(
			self,
			orientation: StandardOrientation,
			width: int,
			height: int):
		self.orientation: StandardOrientation = orientation
		self.width = width
		self.height = height
		self.__validation()

	def __validation(self) -> None:
		assert len(self.orientation) == self.height, \
			f"Error: size must be {self.height}, but got {len(self.orientation)}"
		for i in self.orientation:
			assert i <= (1 << self.width) - 1, \
				f"Error: invalid number in {self.orientation}, " \
				f"the max should less than {(1 << self.width) - 1} (bit length is {self.width}) "


# alias
StandardPiece = typing.List[__StandardDataFormat]


# Current Game State, this info is usually only obtained after game over
class StandardGameStateInfo:
	def __init__(self, is_game_over: bool = True):
		self.is_game_over: bool = is_game_over


# Game continued, how about current state in game board
class StandardMoveStateInfo(StandardGameStateInfo):
	def __init__(
			self,
			current_landing_height: int,
			best_orientation: StandardOrientation,
			eliminated_rows: int):
		StandardGameStateInfo.__init__(self, False)
		self.current_landing_height: int = current_landing_height
		self.best_orientation: StandardOrientation = best_orientation
		self.eliminated_rows: int = eliminated_rows


# How to place to get the best evaluation coefficient
class StandardMoveEvaluatedInfo:
	def __init__(
			self,
			best_orientation: StandardOrientation,
			best_place_column: int):
		self.best_orientation: StandardOrientation = best_orientation
		self.best_place_column: int = best_place_column


class StandardTetris:
	# In the case of the current number of columns, the value indicates that the row is full
	FULL_ROW_VALUE: int = 2 ** 10 - 1

	def __init__(self, columns: int, rows: int):
		self.number_of_columns: int = columns
		self.number_of_rows: int = rows

		self.board: StandardBoard = [0 for _ in range(self.number_of_rows)]

		StandardTetris.FULL_ROW_VALUE = 2 ** self.number_of_columns - 1
