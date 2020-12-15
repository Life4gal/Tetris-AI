import AI.StandardType as StandardType


class AI:
	def __init__(self):
		self.tetris: StandardType.StandardTetris = ...
		self.scores: int = 0

		self.__inited: bool = False

	def set_tetris(self, tetris: StandardType.StandardTetris) -> None:
		"""
		Before playing the game, the user needs to initialize the AI,
		which basically converts the user’s Tetris into a form that can be recognized by the AI,
		and then hand it over to the AI
		:param tetris:
		:return:
		"""
		self.tetris = tetris
		self.__inited = True

	def play(self, current_piece: StandardType.StandardPiece) -> StandardType.StandardMoveStateInfo:
		"""
		Get a random piece, find how and where to place it
		:param current_piece: The Piece
		:return: See StandardType.StandardMoveStateInfo
		"""
		assert self.__inited, f"Error: You should init the AI first!"

		pick: StandardType.StandardMoveEvaluatedInfo = self.__pick_move(current_piece)
		do_it: StandardType.StandardMoveStateInfo = \
			AI.__do_move(self.tetris.board, pick.best_orientation, pick.best_place_column)

		if not do_it.is_game_over:
			self.scores += do_it.eliminated_rows

		return do_it

	def __pick_move(self, current_piece: StandardType.StandardPiece) -> StandardType.StandardMoveEvaluatedInfo:
		"""
		Pick the best move possible (orientation and location) as determined by the evaluation function.
		Given a tetris piece, tries all possible orientations
		and locations and to calculate (what it thinks) is the best move.
		:param current_piece: A tetris piece
		:return: A Sign contained all information we need
		"""
		best_evaluation = -100000
		best_orientation_data: StandardType.StandardOrientationData = []
		best_place_column = 0
		rotate_times = -1

		# Evaluate all possible orientations
		for index, this_shape in enumerate(current_piece):
			orientation_data = this_shape.data

			# Evaluate all possible columns
			for column in range(self.tetris.number_of_columns - this_shape.width + 1):
				# Copy current board
				board = self.tetris.board.copy()
				move_info: StandardType.StandardMoveStateInfo = AI.__do_move(board, orientation_data, column)

				if not move_info.is_game_over:
					evaluation = AI.__evaluate_board_coefficient(move_info, board, self.tetris.number_of_columns)

					if evaluation > best_evaluation:
						best_evaluation = evaluation
						best_orientation_data = orientation_data
						best_place_column = column

						rotate_times = index

		return StandardType.StandardMoveEvaluatedInfo(
			current_piece[0] if len(best_orientation_data) == 0 else best_orientation_data,
			best_place_column,
			rotate_times
		)

	@staticmethod
	def __do_move(
			board: StandardType.StandardBoard,
			best_orientation_data: StandardType.StandardOrientationData,
			which_column: int) -> StandardType.StandardMoveStateInfo:
		"""
		Do a move
		:param board: The game board
		:param best_orientation_data: The data of this piece in current orientation
		:param which_column: Which column this action place
		:return: what happened after this movement done
		"""
		best_orientation_data = AI.__move_piece_horizontally(best_orientation_data, which_column)
		current_landing_height = AI.__get_placeable_row(board, best_orientation_data)

		if current_landing_height + len(best_orientation_data) > len(board):
			return StandardType.StandardMoveStateInfo()

		for i in range(len(best_orientation_data)):
			board[current_landing_height + i] |= best_orientation_data[i]

		# Remove all full rows
		i = 0
		eliminated_rows = 0
		while i < len(best_orientation_data):
			if board[current_landing_height + i] == StandardType.StandardTetris.FULL_ROW_VALUE:
				board.pop(current_landing_height + i)
				# Add an empty row on top
				board.append(0)
				# Since we have decreased the number of rows by one, we need to adjust the index accordingly
				i -= 1
				eliminated_rows += 1
			i += 1

		return \
			StandardType.StandardMoveStateInfo(False, current_landing_height, best_orientation_data, eliminated_rows)

	@staticmethod
	def __move_piece_horizontally(
			orientation_data: StandardType.StandardOrientationData,
			which_column: int) -> StandardType.StandardOrientationData:
		"""
		Move piece to the specified column
		Just need left shift it
		:param orientation_data: The data of this piece in current orientation
		:param which_column: Which column to place
		:return: New orientation_data after move
		"""
		return [(i << which_column) for i in orientation_data]

	@staticmethod
	def __get_placeable_row(
			board: StandardType.StandardBoard,
			orientation_data: StandardType.StandardOrientationData
	) -> int:
		"""
		Find which row current piece could place
		:param board: The game board
		:param orientation_data: The data of this piece in current orientation
		:return: Which row we could place
		"""
		# Descend from top to find the highest row that will collide with the our piece.
		for row in range(len(board) - len(orientation_data), -1, -1):
			# Check if piece collides with the cells of the current row.
			for i in range(len(orientation_data)):
				if (board[row + i] & orientation_data[i]) != 0:
					# Found collision - place piece on row above.
					return row + 1

		return 0  # No collision found, piece should be placed on first row.

	@staticmethod
	def __evaluate_board_coefficient(
			move_info: StandardType.StandardMoveStateInfo,
			board: StandardType.StandardBoard,
			total_columns: int) -> float:
		"""
		Evaluate the board, giving a higher score to boards that "look" better.
		:param move_info: What are the consequences of this move
		:param board: The game board
		:param total_columns: Number of columns in the board
		:return: A number indicating how "good" a board is, the higher the number, the better the board.
		"""
		return \
			move_info.eliminated_rows * 3.4181268101392694 + \
			AI.__get_landing_height(move_info) * -4.500158825082766 + \
			AI.__get_row_transitions(board, total_columns) * -3.2178882868487753 + \
			AI.__get_column_transitions(board, total_columns) * -9.348695305445199 + \
			AI.__get_number_of_holes(board, total_columns) * -7.899265427351652 + \
			AI.__get_well_sums(board, total_columns) * -3.3855972247263626

	@staticmethod
	def __get_landing_height(move_info: StandardType.StandardMoveStateInfo) -> int:
		return move_info.current_landing_height + (len(move_info.best_orientation_data) - 1) // 2

	@staticmethod
	def __get_row_transitions(board: StandardType.StandardBoard, total_columns: int) -> int:
		"""
		A row transition occurs when an empty cell is adjacent to a filled cell on the same row and vice versa.
		:param board: The game board
		:param total_columns: Number of columns in the board
		:return: The total number of row transitions
		"""
		transition = 0
		last_bit = 1

		for row in board:
			bit = 0
			for i in range(total_columns):
				bit = (row >> i) & 1

				if bit != last_bit:
					transition += 1

				last_bit = bit

			if bit == 0:
				transition += 1

			last_bit = 1

		return transition

	@staticmethod
	def __get_column_transitions(board: StandardType.StandardBoard, total_columns: int) -> int:
		"""
		A column transition occurs when an empty cell is adjacent to a filled cell on the same row and vice versa.
		:param board: The game board
		:param total_columns: Number of columns in the board
		:return: The total number of column transitions
		"""
		transition = 0
		last_bit = 1

		for i in range(total_columns):
			for row in board:
				bit = (row >> i) & 1

				if bit != last_bit:
					transition += 1

				last_bit = bit

			last_bit = 1

		return transition

	@staticmethod
	def __get_number_of_holes(board: StandardType.StandardBoard, total_columns: int) -> int:
		"""
		:param board: The game board
		:param total_columns: Number of columns in the board
		:return: The total number of holes
		"""
		holes = 0
		row_holes = 0
		previous_row = board[-1]

		# traverse from top to bottom
		for row in board[-2::-1]:
			row_holes = ~row & (previous_row | row_holes)

			for i in range(total_columns):
				holes += (row_holes >> i) & 1

			previous_row = row

		return holes

	@staticmethod
	def __get_well_sums(board: StandardType.StandardBoard, total_columns: int) -> int:
		"""
		A well is a sequence of empty cells above the top piece in a column such
		that the top cell in the sequence is surrounded (left and right) by occupied
		cells or a boundary of the board.
		:param board: The game board
		:param total_columns: Number of columns in the board
		:return:
			The well sums. For a well of length n, we define the well sums as
			1 + 2 + 3 + ... + n. This gives more significance to deeper holes.
		"""
		well_sums = 0
		# reverse the board, because we travel it from top to bottom
		# use a copy, do not change the origin board
		board_copy = board[::-1]

		# Check for well cells in the "inner columns" of the board.
		# "inner columns" are the columns that aren't touching the edge of the board.
		for i in range(1, total_columns):
			for index, row in enumerate(board_copy):
				if ((row >> i) & 1) == 0 and ((row >> (i - 1)) & 1) == 1 and ((row >> (i + 1)) & 1) == 1:
					# Found well cell, count it + the number of empty cells below it.
					well_sums += 1

					for r in board_copy[index + 1:]:
						if ((r >> i) & 1) == 0:
							well_sums += 1
						else:
							break

		# Check for well cells in the leftmost column of the board.
		for index, row in enumerate(board_copy):
			if ((row >> 0) & 1) == 0 and ((row >> (0 + 1)) & 1) == 1:
				# Found well cell, count it + the number of empty cells below it.
				well_sums += 1

				for r in board_copy[index + 1:]:
					if ((r >> 0) & 1) == 0:
						well_sums += 1
					else:
						break

		# Check for well cells in the rightmost column of the board.
		for index, row in enumerate(board_copy):
			if ((row >> (total_columns - 1)) & 1) == 0 and ((row >> (total_columns - 2)) & 1) == 1:
				# Found well cell, count it + the number of empty cells below it.
				well_sums += 1

				for r in board_copy[index + 1:]:
					if ((r >> (total_columns - 1)) & 1) == 0:
						well_sums += 1
					else:
						break

		return well_sums
