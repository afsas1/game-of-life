#!/usr/bin/env python3
"""
Game of Life — Conway's Game of Life
A Python console implementation with colorful ASCII visualization.

Controls:
  SPACE  : Pause / Resume
  ENTER  : Step one generation (when paused)
  R      : Randomize grid
  C      : Clear grid
  Q / ESC: Quit

Author: OpenClaw Agent
License: MIT
"""

import random
import sys
import time
import os

# ── Config ──────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 80, 28          # grid dimensions (cols, rows)
CELL, DEAD   = "█", " "        # characters for alive / dead cells
GEN_DELAY    = 0.08             # seconds between generations (lower = faster)
RANDOM_DENSITY = 0.22          # fraction of cells alive on random init
# ─────────────────────────────────────────────────────────────────────────────

# ANSI colour palette (reset after each row)
ROW_COLORS = [
    "\033[95m",  # magenta-ish
    "\033[96m",  # cyan
    "\033[92m",  # green
    "\033[93m",  # yellow
    "\033[94m",  # blue
    "\033[91m",  # red
]
RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"

def make_grid(randomize: bool = True, density: float = RANDOM_DENSITY) -> list[list[bool]]:
    """Return a new grid. Randomise or all-dead."""
    if randomize:
        return [[random.random() < density for _ in range(WIDTH)] for _ in range(HEIGHT)]
    return [[False] * WIDTH for _ in range(HEIGHT)]

def neighbours(g: list[list[bool]], r: int, c: int) -> int:
    """Count alive neighbours of cell (r, c) with toroidal wrapping."""
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr = (r + dr) % HEIGHT
            nc = (c + dc) % WIDTH
            count += g[nr][nc]
    return count

def step(g: list[list[bool]]) -> list[list[bool]]:
    """Advance the grid one generation per Conway's rules."""
    new = [[False] * WIDTH for _ in range(HEIGHT)]
    for r in range(HEIGHT):
        for c in range(WIDTH):
            n = neighbours(g, r, c)
            if g[r][c]:
                new[r][c] = (n == 2 or n == 3)
            else:
                new[r][c] = (n == 3)
    return new

def render(g: list[list[bool]], generation: int, paused: bool, fps: float) -> str:
    """Build the display string for the current frame."""
    alive = sum(cell for row in g for cell in row)
    status = "⏸ PAUSED" if paused else "▶ RUNNING"

    # Border
    top    = "┌" + "─" * WIDTH + "┐"
    bottom = "└" + "─" * WIDTH + "┘"

    rows = []
    for r, row in enumerate(g):
        color = ROW_COLORS[r % len(ROW_COLORS)]
        cells = "".join(color + (CELL if c else DEAD) + RESET for c in row)
        rows.append(f"│{cells}│")

    # Header
    header = (
        f"  {BOLD}Conway's Game of Life{RESET}  │  "
        f"Gen: {BOLD}{generation:,}{RESET}  │  "
        f"Alive: {BOLD}{alive:,}{RESET}  │  "
        f"{status}  │  FPS: {fps:.1f}"
    )
    # Footer hints
    footer = (
        f"  {DIM}SPACE:pause·enter:step·R:random·C:clear·Q:quit{RESET}"
    )

    return "\n".join(["", header, top] + rows + [bottom, footer, ""])

def kbhit() -> bool:
    """Return True if a key press is waiting (Windows / cross-platform)."""
    if os.name == "nt":
        import msvcrt
        return msvcrt.kbhit()
    else:
        import select, sys
        return bool(select.select([sys.stdin], [], [], 0)[0])

def getch() -> str:
    """Read a single key press, returning '' when no key is waiting."""
    if os.name == "nt":
        import msvcrt
        return msvcrt.getch().decode("utf-8", errors="ignore")
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

def main() -> None:
    # Ensure stdout handles ANSI colours on Windows
    if os.name == "nt":
        os.system("")   # enable ANSI escape sequences

    grid      = make_grid(randomize=True)
    generation = 0
    paused    = False
    last_fps_time = time.perf_counter()
    frame_count   = 0
    fps           = 0.0

    print("\033[?25l", end="")   # hide cursor
    try:
        while True:
            # ── Timing / FPS counter ──────────────────────────────────────
            now = time.perf_counter()
            frame_count += 1
            if now - last_fps_time >= 1.0:
                fps = frame_count / (now - last_fps_time)
                frame_count = 0
                last_fps_time = now

            # ── Render ─────────────────────────────────────────────────────
            frame = render(grid, generation, paused, fps)
            print("\033[2J\033[H" + frame, flush=True)

            if paused:
                # When paused, keep looping to handle keys but skip stepping
                if kbhit():
                    key = getch().lower()
                    if key in ("q", "\x1b"):
                        break
                    elif key == "\r":          # Enter → step once
                        grid = step(grid)
                        generation += 1
                    elif key == "r":
                        grid = make_grid(randomize=True)
                        generation = 0
                    elif key == "c":
                        grid = make_grid(randomize=False)
                        generation = 0
                    elif key == " ":
                        paused = False
                time.sleep(0.05)
                continue

            # ── Advance one generation ─────────────────────────────────────
            grid = step(grid)
            generation += 1
            time.sleep(GEN_DELAY)

            # ── Keyboard input (non-blocking) ──────────────────────────────
            if kbhit():
                key = getch().lower()
                if key in ("q", "\x1b"):
                    break
                elif key == " ":
                    paused = True
                elif key == "r":
                    grid = make_grid(randomize=True)
                    generation = 0
                elif key == "c":
                    grid = make_grid(randomize=False)
                    generation = 0

    finally:
        print("\033[?25h", end="")  # restore cursor
        print("\033[0m")            # reset colours
        print("\nGoodbye!  🌍\n")

if __name__ == "__main__":
    main()
