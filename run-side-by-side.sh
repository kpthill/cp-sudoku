#!/bin/sh

set -eu

watch -n1 -x bash -c '
	diff -y <( uv run sudoku.py puzzles/easy_euler2.txt  ) \
		<( uv run sudoku.py puzzles/underspecify_euler2.txt )'
