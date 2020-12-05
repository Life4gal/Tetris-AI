import Src.AI as AI
import Src.Piece as Piece
import pygame
import typing
import random

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1200
BLOCK_SIZE = 50
COLUMNS = 10
ROWS = 20
GAME_FIELD_END_X = (SCREEN_WIDTH - BLOCK_SIZE * COLUMNS) // 2 - BLOCK_SIZE + BLOCK_SIZE * COLUMNS
GAME_FIELD_END_Y = (SCREEN_HEIGHT - BLOCK_SIZE * (ROWS + 1)) // 2 + BLOCK_SIZE * ROWS

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris-AI")
clock = pygame.time.Clock()
clock.tick(60)
font = pygame.font.SysFont("Comic Sans MS", 60)

ai = AI.AI(COLUMNS, ROWS)


def get_random_color() -> typing.Tuple[int, int, int]:
	return random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)


def draw_board():
	screen.fill((0, 0, 0))
	for row in range(ROWS):
		column = 0
		row_value = ai.tetris.board[row]
		# after every action we replace all block, so if this row has no block
		# we think above rows also are
		if row_value == 0:
			return
		while column < COLUMNS:
			if row_value & 1:
				pygame.draw.rect(
					screen,
					get_random_color(),
					(
						GAME_FIELD_END_X - column * BLOCK_SIZE,
						GAME_FIELD_END_Y - row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
					),
					5, 5
				)
			row_value >>= 1
			column += 1


def draw_score():
	score = font.render(f"Score: {ai.total_row_removed}", True, get_random_color())
	rect = score.get_rect()
	rect.topleft = (SCREEN_WIDTH // 2 - rect.w // 2, (SCREEN_HEIGHT - BLOCK_SIZE * ROWS) // 2)
	screen.blit(score, rect)


def draw_current_piece():
	height = (SCREEN_HEIGHT - BLOCK_SIZE * ROWS) // 2 + BLOCK_SIZE
	# we just need the last character of name
	name = font.render(f"Current Piece: {ai.current_piece.name[-1]}", True, get_random_color())
	rect = name.get_rect()
	rect.topleft = (SCREEN_WIDTH // 2 - rect.w // 2, height)
	screen.blit(name, rect)

	# use the first data for show
	data: Piece.DataFormat = ai.current_piece.value[0]
	height += rect.h
	sx = SCREEN_WIDTH // 2 - (BLOCK_SIZE * data.width) // 2
	for row in data.orientation:
		column = 0
		while column < data.width:
			if row & 1:
				pygame.draw.rect(
					screen,
					get_random_color(),
					(sx + BLOCK_SIZE * column, height, BLOCK_SIZE, BLOCK_SIZE),
					5, 5
				)
			row >>= 1
			column += 1
		height += BLOCK_SIZE


if __name__ == '__main__':
	while True:
		ai.play()
		draw_board()
		draw_score()
		draw_current_piece()
		pygame.display.update()
