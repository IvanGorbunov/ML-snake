import unittest

from snake_env import SnakeEnv


class SnakeEnvTests(unittest.TestCase):
    def test_initial_state(self):
        env = SnakeEnv(width=10, height=8, seed=42)
        self.assertEqual(env.score, 0)
        self.assertEqual(len(env.snake), 3)
        self.assertEqual(len(env.get_state()), 11)
        self.assertNotIn(env.food, env.snake)
        self.assertEqual(sum(env.get_state()[3:7]), 1)

    def test_straight_move_and_reward(self):
        env = SnakeEnv(width=10, height=8, seed=42)
        env.food = (0, 0)
        result = env.step(0)
        self.assertEqual(env.snake[0], (4, 6))
        self.assertEqual(result.reward, 0.0)
        self.assertFalse(result.done)

    def test_eat_grows_and_rewards(self):
        env = SnakeEnv(width=10, height=8, seed=42)
        env.food = (4, 6)
        result = env.step(0)
        self.assertEqual(result.score, 1)
        self.assertEqual(result.reward, 10.0)
        self.assertEqual(len(env.snake), 4)
        self.assertNotIn(env.food, env.snake)

    def test_wall_collision(self):
        env = SnakeEnv(width=6, height=4, seed=42)
        env.food = (0, 0)
        for _ in range(2):
            result = env.step(0)
        self.assertFalse(result.done)
        result = env.step(0)
        self.assertTrue(result.done)
        self.assertEqual(result.reward, -10.0)
        with self.assertRaises(RuntimeError):
            env.step(0)

    def test_turn_right_and_left(self):
        env = SnakeEnv(width=10, height=8, seed=42)
        env.food = (0, 0)
        env.step(1)
        self.assertEqual(env.direction, (1, 0))
        env.step(2)
        self.assertEqual(env.direction, (0, 1))

    def test_tail_cell_is_safe_when_moving(self):
        env = SnakeEnv(width=10, height=8, seed=42)
        env.snake = [(4, 5), (4, 4), (5, 4), (5, 5)]
        env.direction_index = 1  # down
        env.food = (0, 0)
        result = env.step(0)  # move into the old tail cell
        self.assertFalse(result.done)
        self.assertEqual(env.snake[0], (5, 5))

    def test_invalid_action(self):
        env = SnakeEnv()
        with self.assertRaises(ValueError):
            env.step(3)


if __name__ == "__main__":
    unittest.main()
