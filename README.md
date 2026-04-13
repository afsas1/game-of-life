# Conway's Game of Life — Python Console Edition

> A beautiful, colourful ASCII implementation of Conway's Game of Life for the terminal.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Rules

Each cell lives or dies based on its eight neighbours:

| Condition | Result |
|-----------|--------|
| Alive cell + 2 or 3 neighbours | Survives |
| Alive cell + < 2 or > 3 neighbours | Dies (under/overpopulation) |
| Dead cell + exactly 3 neighbours | Becomes alive (reproduction) |

The grid wraps toroidally — cells on the edge connect to the opposite side.

---

## Features

- 🌈 **Rainbow rows** — each row rendered in a different ANSI colour
- ⚡ **Adjustable speed** — change `GEN_DELAY` in the script to go faster or slower
- 🕹️ **Interactive controls** — pause, step, randomise, clear
- 📊 **Live stats** — generation count, alive cells, FPS
- 🖥️ **Cross-platform** — works on Windows, macOS, Linux
- 🎨 **ASCII box-drawing** — clean grid border using Unicode characters

---

## Controls

| Key | Action |
|-----|--------|
| `Space` | Pause / Resume |
| `Enter` | Step one generation (while paused) |
| `R` | Randomise grid |
| `C` | Clear grid |
| `Q` / `Esc` | Quit |

---

## Installation & Running

```bash
# No dependencies required — pure Python 3!

# Run directly
python game_of_life.py

# Or make it executable on Unix
chmod +x game_of_life.py
./game_of_life.py
```

---

## Configuration

Edit the top of `game_of_life.py` to customise:

```python
WIDTH, HEIGHT   = 80, 28       # grid dimensions
CELL, DEAD      = "█", " "    # cell characters
GEN_DELAY       = 0.08         # seconds per generation (lower = faster)
RANDOM_DENSITY  = 0.22         # fraction alive on random init (0.0 – 1.0)
```

---

## Examples of Interesting Patterns

Try pausing, clearing, then switching to **step mode** (Space to pause, then Enter to step) to seed these:

- **Glider**: 5 cells that move diagonally — the simplest spaceship
- **Blinker**: 3 cells that oscillate (period 2)
- **Toad**: 6 cells with period-2 oscillation
- **Beacon**: 6 cells, period-2, looks like a box eating itself
- **Pulsar**: beautiful period-3 oscillator, 48 cells
- **Gosper Glider Gun**: constantly spawns gliders

---

## License

MIT — free to use, modify, and share.
