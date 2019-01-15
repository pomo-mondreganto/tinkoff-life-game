#!/usr/bin/env python3

import os
import random
import copy
import time
from curses import wrapper


CELL_TYPES = {
	'empty': 0,
	'mountain': 1,
	'fish': 2,
	'shripm': 3,
}

CELL_VALUES = [
	'  ',
	b'\xF0\x9F\x8F\x94'.decode('utf-8'),
	b'\xF0\x9F\x90\xA0'.decode('utf-8'),
	b'\xF0\x9F\xA6\x90'.decode('utf-8'),
]

CELL_PROBABILITIES = [
	0.76,
	0.08,
	0.08,
	0.08,
]


def get_stty_size():
	return map(int, os.popen('stty size', 'r').read().split())


def get_random_cell():
	value = random.random()
	for i, prob in enumerate(CELL_PROBABILITIES):
		if prob >= value:
			return i
		value -= prob
	return 3


def show_field(field, stdscr):
	for line in field:
		formatted_line = ' '.join(map(lambda x: CELL_VALUES[x], line)).rstrip() + '\n'
		stdscr.addstr(formatted_line)
	stdscr.refresh()


def generate_random_field(height, width):
	return [[get_random_cell() for _ in range(width)] for _ in range(height)]

def initialize_game():
	rows, columns = get_stty_size()
	rows //= 2
	columns //= 4
	return generate_random_field(rows, columns)


def count_type(field, row, col, t):
	DR = [0, 0, 1, 1, 1, -1, -1, -1]
	DC = [1, -1, 1, -1, 0, 1, -1, 0]
	cnt = 0

	for dr, dc in zip(DR, DC):
		nrow = row + dr
		ncol = col + dc
		if nrow < 0 or nrow < 0 or nrow >= len(field) or ncol >= len(field[0]):
			continue
		if field[nrow][ncol] == t:
			cnt += 1

	return cnt


def update_field(field):
	new_field = copy.deepcopy(field)
	for row, line in enumerate(field):
		for col, cell in enumerate(line):
			if cell == 0:
				cnt_fish = count_type(field, row, col, 2)
				if cnt_fish >= 3:
					new_field[row][col] = 2
					continue

				cnt_shrimp = count_type(field, row, col, 3)
				if cnt_shrimp >= 3:
					new_field[row][col] = 3
					continue
				
			elif cell == 2 or cell == 3:
				cnt_same = count_type(field, row, col, cell)
				if cnt_same < 2 or cnt_same >= 4:
					new_field[row][col] = 0
	return new_field


def event_loop(field, stdscr):
	while True:
		field = update_field(field)
		stdscr.erase()
		show_field(field, stdscr)
		time.sleep(1 / 14)


def main(stdscr):
	field = initialize_game()

	stdscr.clear()
	show_field(field, stdscr)
	event_loop(field, stdscr)


if __name__ == '__main__':
	wrapper(main)
