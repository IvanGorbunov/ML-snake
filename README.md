# Snake AI, curses + PyTorch, NvChad tutorial

An independently written tutorial implementation inspired by the architecture of
Patrick Loeber's snake-ai-pytorch. It retains a terminal-based Snake game,
separates its logic from curses, and implements a small DQN agent.

## 0. Prepare (Ubuntu 22.04, Python 3.12)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

The environment, human game, random baseline and unit tests need no third-party packages:

```bash
python -m unittest discover -s tests -v
python snake.py
python random_agent.py --episodes 100
```

## 1. Install the ML dependency (CPU)

```bash
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -c 'import torch; print(torch.__version__)'
```

## 2. Train and evaluate

```bash
python train.py --episodes 300
python evaluate.py --random --episodes 100
python evaluate.py --episodes 100
python watch_ai.py
```

The policy checkpoint is written to `model/snake_dqn.pt`. Training is stochastic;
300 episodes is an exercise, not a guarantee of high scores. CPU execution is enough.

## API contract

- `env.reset()` returns 11 binary features in the order danger straight/right/left,
  direction left/right/up/down, food left/right/up/down.
- `env.step(action)` accepts 0=straight, 1=turn right, 2=turn left.
- It returns `StepResult(state, reward, done, score, won)`.
- Rewards are +10 for food, -10 for collision/starvation, 0 otherwise.
- This is a learning demonstration, not a Gymnasium-compliant environment.

## Neovim exercises

```bash
NVIM_APPNAME=nvim-python nvim snake_env.py
```

- `/def step` to jump to the update method, `n` for next match.
- `gd` to jump to local definitions with a working LSP.
- `ciw`, `yyp`, `o`, `A`, `u`, `.` to edit efficiently.
- `<Space>ff` for file search (NvChad); `:e train.py` without plugins.
- `:w` to save; `:!python -m unittest discover -s tests -v` to test.
- Use `:checkhealth vim.lsp` for modern Neovim (rather than assuming `:LspInfo`).

## Learning checkpoints

1. Inspect `snake_env.py`, explain why it doesn't import curses.
2. In `snake.py`, map WASD into relative turns 0/1/2.
3. In `random_agent.py`, measure baseline over 100 episodes.
4. In `model.py`, check 11 -> 256 -> 3 outputs and 3843 parameters.
5. In `train.py`, identify state/action/reward/next_state/done, replay, target network.
6. Compare `evaluate.py --random` with the saved Q network using same test seeds.
7. Try epsilon schedules, different board sizes, target sync intervals, report mean scores.
