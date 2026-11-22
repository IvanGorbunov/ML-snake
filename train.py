import argparse
import random
import statistics
from collections import deque

from snake_env import SnakeEnv

MEMORY_SIZE = 50_000


def collect_experiencw(episodes: int, seed: int = 42) -> None:
    rng = random.Random(seed)
    env = SnakeEnv(seed=seed)

    replay = deque(maxlen=MEMORY_SIZE)
    scores: list[int] = []
    for episode in range(1, episodes + 1):
        state = env.reset()
        while not env.done:
            action = rng.randrange(3)
            result = env.step(action)
            replay.append(
                (
                    state,
                    action,
                    result.reward,
                    result.state,
                    result.done,
                )
            )

            state = result.state

        scores.append(env.score)

        print(f"Episode {episode:>3}: score={env.score}, replay={len(replay)}")
    print(f"Mean score: {statistics.mean(scores)}:.2f")
    print(f"Best score: {max(scores)}")
    print(f"Transitions collected: {len(replay)}")
    print(f"Example transition: {replay[0]}")
    print(f"Total episodes: {episodes}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Snake DQN traning: step 1")
    parser.add_argument("--episodes", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    if args.episodes < 1:
        parser.error("--episodes must be at least 1")
    collect_experiencw(episodes=args.episodes, seed=args.seed)


if __name__ == "__main__":
    main()
