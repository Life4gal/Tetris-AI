import typing

# alias
StandardBoard = typing.List[int]
StandardOrientationData = typing.List[int]


class StandardDataFormat:
	# Standard data storage format for each piece used by our algorithm
	def __init__(
			self,
			data: StandardOrientationData,
			width: int,
			height: int):
		"""
		:param data:
			In the current orientation, the VALUE of each row of a piece from top to bottom, stored them in a list

			VALUE:
				we use X BIT BINARY to store the state of current row
				X is the COLUMNS of the game board

				e.g.
					X = 10, state is 1000011110
					This means that there are blocks in the 0,5,6,7,8 columns, and the 1,2,3,4,9 columns are empty
					and we store it as a decimal number 542
		:param width: the width of this piece
		:param height: the height of this piece
		"""
		self.data = data
		self.width = width
		self.height = height
		self.__validation()

	def __validation(self) -> None:
		assert len(self.data) == self.height, \
			f"Error: data size must be {self.height}, but got {len(self.data)}"
		for i in self.data:
			assert i <= (1 << self.width) - 1, \
				f"Error: invalid number in {self.data}, " \
				f"the max should less than {(1 << self.width) - 1} (bit length is {self.width}) "


# alias
StandardPiece = typing.List[StandardDataFormat]


class StandardMoveStateInfo:
	def __init__(
			self,
			is_game_over: bool = True,
			current_landing_height: int = 0,
			best_orientation_data: StandardOrientationData = None,
			eliminated_rows: int = 0
	):
		"""
		What are the consequences of this move
		:param is_game_over: is game over?
		:param current_landing_height: current landing height if game is not over
		:param best_orientation_data: the best orientation's data if game is not over, the same as __StandardDataFormat.data
		:param eliminated_rows: how many rows had been eliminated if game is not over
		"""
		self.is_game_over = is_game_over
		self.current_landing_height = current_landing_height
		self.best_orientation_data = best_orientation_data
		self.eliminated_rows = eliminated_rows


class StandardMoveEvaluatedInfo:
	def __init__(
			self,
			best_orientation_data: StandardOrientationData,
			best_place_column: int,
			rotate_times: int):
		"""
		How to place to get the best evaluation coefficient
		:param best_orientation_data: The best orientation's data, the same as __StandardDataFormat.data
		:param best_place_column: Which column to place it
		:param rotate_times:
			Compared to the original piece, how many times is the current piece rotated

			NOTE:
				In fact, we don’t know how many times it had rotated,
				we just traverse all the orientation, so what we actually get is
				the index of the target orientation in the list (starting from 0)

				You can use it to subtract the index of the original piece to get the real times of rotations
		"""
		self.best_orientation: StandardOrientationData = best_orientation_data
		self.best_place_column: int = best_place_column
		self.rotate_times = rotate_times


class StandardTetris:
	# In the case of the current number of columns, the value indicates that the row is full
	FULL_ROW_VALUE: int = 2 ** 10 - 1

	def __init__(self, columns: int, rows: int):
		self.number_of_columns: int = columns
		self.number_of_rows: int = rows

		self.board: StandardBoard = [0 for _ in range(self.number_of_rows)]

		StandardTetris.FULL_ROW_VALUE = 2 ** self.number_of_columns - 1
