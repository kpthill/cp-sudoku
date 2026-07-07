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
    model.add_all_different( [ model_vars[r][c] for c in range(9) ] )

  for c in range(9):
    model.add_all_different( [ model_vars[r][c] for r in range(9) ] )

  for off_r in range(3):
    for off_c in range(3):
      model.add_all_different( [
          model_vars[3*off_r + numpad % 3][3*off_c + numpad // 3]
            for numpad in range(9) ] )
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
        solution_printer = VarArraySolutionPrinter(model_vars)
        solver.parameters.enumerate_all_solutions = True
        status = solver.solve(model, solution_printer)
        print(f"Solution count: {solution_printer.solution_count}")

def print_sudoku_blank(board):
          for r in range(9):
            print(" ".join([str(board[r][c]) if board[r][c] != -1 else "." for c in range(9)]))
def print_sudoku_solved(solver, model_vars):
          for r in range(9):
            print(" ".join([str(solver.value(model_vars[r][c])) for c in range(9)]))


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self) -> None:
        self.__solution_count += 1
        print_sudoku_solved(self, self.__variables)
        print()

    @property
    def solution_count(self) -> int:
        return self.__solution_count

if __name__ == '__main__':
  main()
