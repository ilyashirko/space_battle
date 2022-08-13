import asyncio
import curses
import os
import random
from itertools import cycle

from curses_tools import draw_frame, get_frame_size, read_controls

DELAY = 500


async def get_asyncio_sleep(loops_num=DELAY):
    for _ in range(loops_num):
        await asyncio.sleep(0)


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await get_asyncio_sleep(random.randint(1, DELAY))

        canvas.addstr(row, column, symbol)
        await get_asyncio_sleep(random.randint(1, DELAY))

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await get_asyncio_sleep(random.randint(1, DELAY))

        canvas.addstr(row, column, symbol)
        await get_asyncio_sleep(random.randint(1, DELAY))


async def fire(canvas,
               start_row,
               start_column,
               rows_speed=-0.3,
               columns_speed=0):
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await get_asyncio_sleep()

    canvas.addstr(round(row), round(column), 'O')
    await get_asyncio_sleep()

    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 1 < row < max_row and 1 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await get_asyncio_sleep()
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def starship_animation(canvas, max_x, max_y, starships):
    starship_height, starship_width = get_frame_size(starships[1])
    pos_x, pos_y = int(max_x // 2), int(max_y // 2)

    for pos in cycle([1, 2, 1, 2, 2, 1, 2, 1]):
        rows_direction, columns_direction, _ = read_controls(canvas)
        if 0 < pos_x + columns_direction < max_x - starship_width:
            pos_x += columns_direction
        if 0 < pos_y + rows_direction < max_y - starship_height:
            pos_y += rows_direction

        draw_frame(canvas, pos_y, pos_x, starships[pos], False)
        canvas.refresh()
        draw_frame(canvas, pos_y, pos_x, starships[pos], True)
        await get_asyncio_sleep()


def draw(canvas, stars_ratio=0.06):
    canvas.border()
    curses.curs_set(False)

    screen = curses.initscr()
    screen.nodelay(True)

    max_y, max_x = screen.getmaxyx()

    stars_num = int(max_x * max_y * stars_ratio)
    coroutines = list()

    coordinates = [
        (x, y)
        for x in range(1, max_x - 1)
        for y in range(1, max_y - 1)
    ]

    for _ in range(stars_num):
        random_coord = random.choice(coordinates)
        coordinates.remove(random_coord)
        x, y = random_coord
        coroutines.append(
            blink(
                canvas=canvas,
                row=y,
                column=x,
                symbol=random.choice('+*.:')
            )
        )

    coroutines.append(
        fire(
            canvas=canvas,
            start_row=int(max_y // 2),
            start_column=int(max_x // 2),
            rows_speed=-0.2,
        )
    )

    starships = dict()
    frames_files = os.listdir('frames')
    for num, frame_file in enumerate(frames_files):
        with open(f'frames/{frame_file}', 'r') as rocket:
            starships[num + 1] = rocket.read()

    coroutines.append(starship_animation(canvas, max_x, max_y, starships))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
