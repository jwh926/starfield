"""starfield.py - classic windows 9x starfield screensaver in your terminal"""

import curses
import random
import time

SCALE = 24
MIN_Z = 32
MAX_Z = 128
Z_NEAR = 24
Z_MEDIUM = 61
SPEED_INCREMENT = 0.2
MIN_SPEED = 0.1
MAX_SPEED = 10.0


class Star:
    def __init__(self, width, height):
        self.reset(width, height)

    def reset(self, width, height):
        # set the star's position(coordinates) randomly
        self.x = random.uniform(-width, width)
        self.y = random.uniform(-height, height)
        self.z = random.uniform(MIN_Z, MAX_Z)

    def update(self, speed):
        # check if the star's z coordinate is out of bounds
        self.z -= speed
        if self.z <= 0:
            return True
        return False

    def get_screen_pos(self, width, height):
        # perspective projection (special thx to claude)
        sx = int(self.x / self.z * SCALE + width / 2)
        sy = int(self.y / self.z * SCALE + height / 2)

        if 0 <= sx < width and 0 <= sy < height:
            return sx, sy
        return None, None


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    height, width = stdscr.getmaxyx()

    num_stars = 100
    stars = []

    speed = 1.0

    try:
        while True:
            key = stdscr.getch()
            # q to quit, + or - to adjust the stars' speed
            if key == ord("q"):
                break
            elif key == curses.KEY_UP or key == ord("+"):
                speed = min(speed + SPEED_INCREMENT, MAX_SPEED)
            elif key == curses.KEY_DOWN or key == ord("-"):
                speed = max(speed - SPEED_INCREMENT, MIN_SPEED)
            elif key == curses.KEY_RESIZE:
                height, width = stdscr.getmaxyx()
                stdscr.clear()

            stdscr.clear()  # do we really need optimization for this? i don't think so.

            # render stars gradually at start
            if len(stars) < num_stars:
                stars.append(Star(width, height))

            for star in stars:
                if star.update(speed):
                    star.reset(width, height)

                sx, sy = star.get_screen_pos(width, height)

                if any((sx, sy)):
                    if star.z < Z_NEAR:
                        char = "#"
                    elif star.z < Z_MEDIUM:
                        char = "+"
                    else:
                        char = "."
                    color = curses.color_pair(1)
                    try:
                        stdscr.addstr(sy, sx, char, color)
                    except curses.error:
                        pass

            stdscr.refresh()
            # since i don't exactly know how to limit fps in curses, so i'll just... `sleep`. :3
            time.sleep(0.067)  # about 15 fps

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    curses.wrapper(main)
