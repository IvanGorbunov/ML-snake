import curses
import random
from collections import deque
from turtle import screensize, width
from xxlimited import foo

TICK_MS = 140
MIN_HEIGHT = 12
MIN_WIDTH = 35

KEY_DIRECTIONS = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
    ord("w"): (-1, 0),
    ord("s"): (1, 0),
    ord("a"): (0, -1),
    ord("d"): (0, 1),
}


def create_food(snake, height, width):
    occupied = set(snake)
    free_cells = [
        (y, x)
        for y in range(3, height - 1)
        for x in range(1, width - 1)
        if (y, x) not in occupied
    ]
    return random.choice(free_cells) if free_cells else None


def draw(screen: curses.window, snake, food, score):
    height, width = screen.getmaxyx()

    screen.erase()
    screen.border()

    status = f"Score: {score} | WASD/arrows: move R: restart Q: quit"

    screen.addstr(1, 2, status[: width - 4])
    screen.hline(2, 1, curses.ACS_HLINE, width - 2)

    for index, (y, x) in enumerate(snake):
        char = "@" if index == 0 else "o"
        screen.addch(y, x, char)

    if food is not None:
        screen.addch(food[0], food[1], "*")

    screen.refresh()


def ask_restart(screen, message):
    height, width = screen.getmaxyx()

    screen.addstr(1, 2, message[: width - 4])
    screen.refresh()
    screen.timeout(-1)

    while True:
        key = screen.getch()

        if key in (ord("r"), ord("R")):
            return True

        if key in (ord("q"), ord("Q")):
            return False

        if key == curses.KEY_RESIZE:
            return True


def play(screen):
    height, width = screen.getmaxyx()

    if height < MIN_HEIGHT or width < MIN_WIDTH:
        screen.erase()
        screen.addstr(0, 0, "Enlarge terminal to at last 35x12"[: width - 1])
        screen.refresh()
        screen.timeout(-1)
        screen.getch()
        return False

    start_y = height // 2
    start_x = width // 2
    snake = deque(
        [
            (start_y, start_x),
            (start_y, start_x - 1),
            (start_y, start_x - 2),
        ]
    )

    direction = (0, 1)
    score = 0
    food = create_food(snake, height, width)

    while True:
        draw(screen, snake, food, score)

        screen.timeout(TICK_MS)
        key = screen.getch()

        if key in (ord("q"), ord("Q")):
            return False

        if key in (ord("r"), ord("R"), curses.KEY_RESIZE):
            return True

        new_direction = KEY_DIRECTIONS.get(key)

        if new_direction is not None:
            reverse = (-direction[0], -direction[1])

            if new_direction != reverse:
                direction = new_direction

        head_y, head_x = snake[0]
        new_head = (
            head_y + direction[0],
            head_x + direction[1],
        )

        hit_wall = not (3 <= new_head[0] < height - 1 and 1 <= new_head[1] < width - 1)

        if hit_wall:
            return ask_restart(screen, "Game over! R: restart | Q: quit")

        # Столкновение с телом
        eating = new_head == food

        hit_self = new_head in snake and (eating or new_head != snake[-1])

        if hit_self:
            return ask_restart(screen, "Game over! R: restart | Q: quit")

        # Перемещение
        snake.appendleft(new_head)

        if eating:
            score += 1
            food = create_food(snake, height, width)

            if food is None:
                draw(screen, snake, food, score)
                return ask_restart(screen, "You win! R: restart | Q: quit")
        else:
            snake.pop()


def main(screen):
    curses.curs_set(0)
    screen.keypad(True)

    while play(screen=screen):
        pass


if __name__ == "__main__":
    curses.wrapper(main)
