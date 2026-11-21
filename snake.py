"""Manual curses UI. The environment itself does not depend on curses."""

import curses

from snake_env import DIRECTIONS, SnakeEnv

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


def draw(screen: curses.window, env: SnakeEnv) -> None:
    height, width = screen.getmaxyx()
    screen.erase()
    screen.border()
    message = f"Score: {env.score} | WASD/arrows: move  R: restart  Q: quit"
    screen.addstr(1, 2, message[: width - 4])
    screen.hline(2, 1, curses.ACS_HLINE, width - 2)
    for index, (y, x) in enumerate(env.snake):
        screen.addch(y + 3, x + 1, "@" if index == 0 else "o")
    if env.food is not None:
        screen.addch(env.food[0] + 3, env.food[1] + 1, "*")
    screen.refresh()


def ask_restart(screen: curses.window, message: str) -> bool:
    _height, width = screen.getmaxyx()
    screen.addstr(1, 2, message[: width - 4])
    screen.refresh()
    screen.timeout(-1)
    while True:
        key = screen.getch()
        if key in (ord("r"), ord("R"), curses.KEY_RESIZE):
            return True
        if key in (ord("q"), ord("Q")):
            return False


def play(screen: curses.window) -> bool:
    height, width = screen.getmaxyx()
    if height < MIN_HEIGHT or width < MIN_WIDTH:
        screen.erase()
        screen.addstr(0, 0, "Enlarge terminal to at least 35x12"[: max(0, width - 1)])
        screen.refresh()
        screen.timeout(-1)
        screen.getch()
        return False

    env = SnakeEnv(width=width - 2, height=height - 4)
    while True:
        draw(screen, env)
        screen.timeout(TICK_MS)
        key = screen.getch()
        if key in (ord("q"), ord("Q")):
            return False
        if key in (ord("r"), ord("R"), curses.KEY_RESIZE):
            return True

        requested_direction = KEY_DIRECTIONS.get(key)
        action = 0  # go straight when no new direction is requested
        if requested_direction is not None:
            new_index = DIRECTIONS.index(requested_direction)
            rotation = (new_index - env.direction_index) % 4
            action = {0: 0, 1: 1, 2: 0, 3: 2}[rotation]

        result = env.step(action)
        if result.done:
            draw(screen, env)
            return ask_restart(
                screen,
                "You win! R: restart | Q: quit"
                if result.won
                else "Game over! R: restart | Q: quit",
            )


def main(screen: curses.window) -> None:
    curses.curs_set(0)
    screen.keypad(True)
    while play(screen):
        pass


if __name__ == "__main__":
    curses.wrapper(main)
