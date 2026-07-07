# cp-sudoku

Exercises: solving sudoku with [OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver).

## Setup

Requires [uv](https://docs.astral.sh/uv/). Then:

```sh
uv sync
```

This creates `.venv/` with `ortools` installed. Run things with `uv run <script.py>`.

## Puzzle format

Puzzles live in `puzzles/`, one file per puzzle. Each file has `#` comment
lines describing the puzzle, followed by one line with the puzzle itself in the
de-facto standard line format (as used by Peter Norvig's sudoku essay and most
puzzle collections):

- 81 characters, cells in row-major order (row 1 left-to-right, then row 2, ...)
- `1`–`9` for given clues
- `.` for an empty cell (some collections use `0`; treat both as empty)

To read a puzzle from a file: skip comment and blank lines, take the first
remaining line.

Example — the first character is row 1 column 1, character 10 is row 2 column 1:

```
..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
```

## Puzzles

- `easy_*.txt` — 2 easy puzzles (Norvig / Project Euler 96); solvable by plain
  constraint propagation.
- `hard_*.txt` — 5 hard puzzles, including Arto Inkala's "AI Escargot" and his
  2012 "world's hardest sudoku", plus a 17-clue puzzle (17 is the proven
  minimum number of clues for a unique solution).
- `edge_empty.txt` — an empty grid; feasible but with astronomically many
  solutions, useful for testing solution enumeration with a limit.
- `edge_infeasible.txt` — no clue directly conflicts with another, yet the
  puzzle has no solution; the solver should report INFEASIBLE.

Every `easy_*` and `hard_*` puzzle has been verified to have exactly one
solution, so a correct solver needs no reference solutions: check that the
output grid satisfies all sudoku constraints and contains the given clues.
