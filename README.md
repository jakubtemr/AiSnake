# Snake Game with LLM

A minimal terminal implementation of the classic Snake game where every move is decided by a Large Language Model instead of a player or a search algorithm.

## Overview

The board is a 6×6 grid rendered as text (`O` = snake, `F` = food). On each turn the current game state — snake body, current direction, food position, and board size — is sent to an LLM served by [Groq](https://groq.com/) (`llama3-70b-8192`), which answers with a direction tuple such as `(1, 0)`. The snake moves one tile per second, grows when it reaches the food, wraps around the edges of the board, and the game ends when it runs into itself.

The point of the project is to watch how well an LLM handles a simple spatial planning loop — not to play Snake well.

## Installation

1. **Install dependencies**

   Requires Python 3.

   ```bash
   pip install groq python-dotenv
   ```

2. **Set up Groq**

   Create an account at [Groq](https://console.groq.com/) and generate an API key in the dashboard.

3. **Configure your environment**

   Rename `.env_example` to `.env` and add your key:

   ```
   API_KEY="your_groq_api_key_here"
   ```

## Usage

```bash
python snake.py
```

The board is printed once per turn together with the direction chosen by the model. Stop the game with `Ctrl+C`, or wait for the snake to collide with itself.

## How it works

- `get_llm_direction()` builds the prompt: a system message with the rules (movement tuples, wrap-around walls, no immediate reversal) and a user message with the serialized game state.
- The call uses `max_tokens=6` and `temperature=0.1` so the model returns just the tuple.
- The answer is parsed with `eval()` and applied to the snake's head.

## Limitations

- The model's reply is passed straight to `eval()`, so a malformed answer crashes the game. This is fine for a local toy, but do not point it at an untrusted endpoint.
- There is no retry or validation layer — an illegal move (such as reversing into the snake's own neck) simply ends the game.
- Board size (`width, height = 6, 6`), the model name, and the one-second turn delay are hardcoded near the top of `snake.py`.

## License

MIT — see [LICENSE](LICENSE).
