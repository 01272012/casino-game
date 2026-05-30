# Casino Game

A single-player casino game suite built with Python and Pygame.

## Features

- **Blackjack** - Fully implemented card game
- **Slots** - Coming soon
- **Roulette** - Coming soon
- **Pool** - Coming soon
- **Horse Racing** - Coming soon

## Installation

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Game Features

- Player progression system (track wins, balance, statistics)
- Clean menu system
- Progressive graphics
- Actual game logic (no placeholder simulations)

## Project Structure

```
casino_game/
├── main.py              # Main game loop
├── player.py            # Player state management
├── ui.py                # UI components (buttons, inputs)
├── games/
│   ├── blackjack.py     # Blackjack game
│   ├── slots.py         # Slots game (stub)
│   ├── roulette.py      # Roulette game (stub)
│   ├── pool.py          # Pool game (stub)
│   └── horse_racing.py  # Horse racing game (stub)
└── requirements.txt
```

## Development Notes

- Start with `pip install -r requirements.txt`
- Blackjack is fully implemented as an example
- Each game module is independent and can be worked on separately
- The UI framework is in place for easy expansion
