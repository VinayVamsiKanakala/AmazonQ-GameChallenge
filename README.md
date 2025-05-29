# Python Games Suite

A desktop-based offline games suite built with Python. This application includes multiple classic games with a clean, modern interface.

## Games Included

1. **Snake Game** - Classic snake game where you control a snake to eat food and grow without hitting walls or yourself.
2. **Chess** - Traditional chess game for two players with all standard rules.
3. **Carrom Board** - Simplified version of the popular tabletop game Carrom.
4. **Sliding Puzzle** - A 4x4 sliding tile puzzle where you rearrange tiles to solve the puzzle.
5. **Memory Match** - Card matching game where you flip cards to find matching pairs.

## Features

- Central launcher menu to access all games
- Smooth animations and transitions
- Modern and clean user interface
- Completely offline and lightweight
- Self-contained in a single app folder

## Requirements

- Python 3.6 or higher
- Tkinter (included with most Python installations)
- Optional: Pygame for sound effects

## Installation

1. Clone or download this repository
2. Install the optional dependencies:
   ```
   pip install pygame
   ```
3. Run the main application:
   ```
   python games_suite.py
   ```

## Project Structure

```
games_suite/
│
├── games_suite.py         # Main launcher application
├── games/                 # Individual game modules
│   ├── snake.py           # Snake game implementation
│   ├── chess.py           # Chess game implementation
│   ├── carrom.py          # Carrom board game implementation
│   ├── puzzle.py          # Sliding puzzle game implementation
│   └── cards.py           # Memory match card game implementation
│
└── assets/                # Game assets
    ├── icons/             # Game icons
    ├── images/            # Game images
    │   └── chess/         # Chess piece images
    └── sounds/            # Sound effects
```

## Adding Sound Effects

For the full experience, add sound effect files to the `assets/sounds` directory:
- `eat.wav` - Snake eating food
- `game_over.wav` - Game over sound
- `card_flip.wav` - Card flipping sound
- `match.wav` - Card match sound
- `win.wav` - Victory sound
- `tile_move.wav` - Puzzle tile movement
- `hit.wav` - Carrom piece collision

## Adding Icons

Place game icons in the `assets/icons` directory:
- `app_icon.png` - Main application icon
- `snake_icon.png` - Snake game icon
- `chess_icon.png` - Chess game icon
- `carrom_icon.png` - Carrom game icon
- `puzzle_icon.png` - Puzzle game icon
- `cards_icon.png` - Card game icon

## License

This project is open source and available for personal and educational use.

## Credits

Created as a Python programming exercise to demonstrate GUI development, game logic implementation, and modular code organization.
