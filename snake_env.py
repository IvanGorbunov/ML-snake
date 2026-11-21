"""Headless Snake environment for human play and reinforcement learning.

Coordinates are (row, column). Actions are relative:
0 = straight, 1 = turn right, 2 = turn left.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

Position = tuple[int, int]
Direction = tuple[int, int]
DIRECTIONS: tuple[Direction, ...] = (
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
    (-1, 0),  # up
)


@dataclass(frozen=True, slots=True)
class StepResult:
    state: tuple[int, ...]
    reward: float
    done: bool
    score: int
    won: bool


class SnakeEnv:
    def __init__(self, width: int = 20, height: int = 15, seed: int | None = None):
        if width < 5 or height < 3:
            raise ValueError("Board must be at least 5 columns and 3 rows")
        self.width = width
        self.height = height
        self.rng = random.Random(seed)
        self.reset()

    def reset(self) -> tuple[int, ...]:
        cy, cx = self.height // 2, self.width // 2
        self.snake: list[Position] = [(cy, cx), (cy, cx - 1), (cy, cx - 2)]
        self.direction_index = 0
        self.score = 0
        self.steps_since_food = 0
        self.done = False
        self.won = False
        self.food = self._place_food()
        return self.get_state()

    @property
    def direction(self) -> Direction:
        return DIRECTIONS[self.direction_index]

    def _place_food(self) -> Position | None:
        occupied = set(self.snake)
        free = [
            (y, x)
            for y in range(self.height)
            for x in range(self.width)
            if (y, x) not in occupied
        ]
        return self.rng.choice(free) if free else None

    def _would_collide(self, position: Position) -> bool:
        y, x = position
        if not (0 <= y < self.height and 0 <= x < self.width):
            return True
        # The tail vacates its cell on any non-eating move.
        eating = position == self.food
        return position in self.snake and (eating or position != self.snake[-1])

    def get_state(self) -> tuple[int, ...]:
        """11 inputs: danger straight/right/left; direction L/R/U/D; food L/R/U/D."""
        y, x = self.snake[0]

        def danger(offset: int) -> int:
            dy, dx = DIRECTIONS[(self.direction_index + offset) % 4]
            return int(self._would_collide((y + dy, x + dx)))

        food_y, food_x = self.food if self.food is not None else (y, x)
        return (
            danger(0),
            danger(1),
            danger(-1),
            int(self.direction_index == 2),  # left
            int(self.direction_index == 0),  # right
            int(self.direction_index == 3),  # up
            int(self.direction_index == 1),  # down
            int(food_x < x),
            int(food_x > x),
            int(food_y < y),
            int(food_y > y),
        )

    def step(self, action: int) -> StepResult:
        if self.done:
            raise RuntimeError("Episode finished; call reset() before step()")
        if action not in (0, 1, 2):
            raise ValueError("Action must be 0 (straight), 1 (right), or 2 (left)")

        self.direction_index = (self.direction_index + {0: 0, 1: 1, 2: -1}[action]) % 4
        y, x = self.snake[0]
        dy, dx = self.direction
        next_head = (y + dy, x + dx)
        if self._would_collide(next_head):
            self.done = True
            return StepResult(self.get_state(), -10.0, True, self.score, False)

        self.snake.insert(0, next_head)
        self.steps_since_food += 1
        reward = 0.0
        if next_head == self.food:
            self.score += 1
            reward = 10.0
            self.steps_since_food = 0
            self.food = self._place_food()
            if self.food is None:
                self.done = True
                self.won = True
        else:
            self.snake.pop()

        if not self.done and self.steps_since_food > 100 * len(self.snake):
            self.done = True
            reward = -10.0

        return StepResult(self.get_state(), reward, self.done, self.score, self.won)
