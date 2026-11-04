import curses


def main(screen):
    curses.curs_set(0)

    screen.border()

    height, width = screen.getmaxyx()
    y = height // 2
    x = width // 2

    screen.addch(y, x, "@")

    screen.refresh()
    screen.getch()


if __name__ == "__main__":
    curses.wrapper(main)