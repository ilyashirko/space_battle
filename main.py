import asyncio
import curses
import time
import random
from types import NoneType

async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(random.randint(1, 20)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(random.randint(1, 20)):
            await asyncio.sleep(0)
        

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(random.randint(1, 20)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(random.randint(1, 20)):
            await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def draw(canvas, row=3, column=3):
    
    screen = curses.initscr()
    max_y, max_x = screen.getmaxyx()
    coroutines = list()
    stars_num = int(max_x * max_y // 5)
    coordinates = list()
    for x in range(1, max_x - 1):
        for y in range(1, max_y - 1):
            coordinates.append((x, y))

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
    canvas.border()
    fireshot = fire(
        canvas=canvas,
        start_row=int(max_y // 2),
        start_column=int(max_x // 2),
        rows_speed=-2,
    )

    while True:
        for coroutine in coroutines.copy():
            coroutine.send(None)
        try:
            fireshot.send(None)
        except (StopIteration, RuntimeError):
            pass

        time.sleep(0.5)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)