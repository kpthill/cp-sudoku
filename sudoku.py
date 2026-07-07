#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from ortools.sat.python import cp_model

def setup_problem(board):
  model = cp_model.CpModel()
  model_vars = [ [ None for _ in range(9) ] for _ in range(9) ]
  for i in range(9):
    for j in range(9):
      board_var_name = f"s[{i},{j}]"
      if board[i][j] == -1:
        model_vars[i][j] = model.new_int_var(1, 9, board_var_name)
      else:
        model_vars[i][j] = model.new_int_var(board[i][j], board[i][j], board_var_name)

  for r in range(9):
    for c1 in range(9):
      for c2 in range(c1+1,9):
        #print( f"m[{r}, {c1}] != m[{r},{c2}] ")#DEBUG
        model.add( model_vars[r][c1] != model_vars[r][c2] )

  for c in range(9):
    for r1 in range(9):
      for r2 in range(r1+1,9):
        #print( f"m[{r1}, {c}] != m[{r2},{c}] ")#DEBUG
        model.add( model_vars[r1][c] != model_vars[r2][c] )

  for off_r in range(3):
    for off_c in range(3):
      for numpad1 in range(9):
        board1_r = 3*off_r + numpad1 % 3
        board1_c = 3*off_c + numpad1 // 3
        for numpad2 in range(numpad1 + 1, 9):
          board2_r = 3*off_r + numpad2 % 3
          board2_c = 3*off_c + numpad2 // 3
          #print( f"({board1_r}, {board1_c}) -> ({board2_r}, {board2_c})" )#DEBUG
          model.add( model_vars[board1_r][board1_c] != model_vars[board2_r][board2_c] )
  return model, model_vars
  #print(model_vars)#DEBUG
  #print(model)#DEBUG

def parse_sudoku(line):
  assert len(line) == 81
  board = [ [ -1 for _ in range(9) ] for _ in range(9) ]
  for i, c in enumerate(line):
    #print( (c,i) )#DEBUG
    if c != '.':
      board[i // 9][i % 9] = int(c)
  return board

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('filename')

  args = parser.parse_args()

  with open(args.filename, 'r') as f:
    for line in f:
      line = line.rstrip()
      if(line[0] == '#'):
        pass
      else:
        board = parse_sudoku(line)
        model, model_vars = setup_problem(board)
        solver = cp_model.CpSolver()
        status = solver.solve(model)
        for r in range(9):
          print(" ".join([str(board[r][c]) if board[r][c] != -1 else "." for c in range(9)]))
        print("---")
        for r in range(9):
          print(" ".join([str(solver.value(model_vars[r][c])) for c in range(9)]))

if __name__ == '__main__':
  main()
