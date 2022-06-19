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
    while True:
        for coroutine in coroutines.copy():
            coroutine.send(None)
        time.sleep(0.1)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)