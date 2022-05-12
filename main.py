from solver import Solver
from state import State
from solver import HillClimbingSolver


goal = State([1, 2, 3, 0, 8, 7, 6, 4, 5])
initial = State([1, 2, 3, 6, 5, 4, 7, 8, 0])
print('initial state is', initial.matrix)
print('goal state is', goal.matrix)

print('Hill Climbing misplaced: ', end='')
HillClimbingSolver(goal).solve(initial, Solver.misplaced)
print('Hill Climbing manhattan: ', end='')
HillClimbingSolver(goal).solve(initial, Solver.manhattan)
