from math import floor
from random import random
from typing import Any, Callable, TypeVar, cast
from time import time
from state import State
from direction import Direction
from solver.solver import Solver


F = TypeVar('F', bound=Callable[..., Any])


def _measure(func: F) -> F:
    def wrapped(self: Solver, *args: Any, **kwargs: Any):
        start = time()
        try:
            return func(self, *args, **kwargs)
        finally:
            end_ = time() - start
            print(f"\t> {end_} seconds")
    return cast(F, wrapped)


class HillClimbingSolver(Solver):
    @_measure
    def solve(self, initial: State, heuristicFunction: Callable[[State, State], int]):
        state = initial
        goal = self.goal
        neighbours: list[tuple[int, int, State]] = []
        while True:
            for i, direction in enumerate(Direction):
                moved = state.move(direction)
                if moved is None:
                    continue
                cost = heuristicFunction(moved, goal)
                Solver._push(neighbours, cost, i, moved)
            if neighbours[0][0] >= heuristicFunction(state, goal):
                break
            idx = len(neighbours) - 1
            for i, v in enumerate(neighbours):
                if v[0] != neighbours[0][0]:
                    idx = i
                    break
            rand = floor(random() * idx)
            state = neighbours[rand][2]
            neighbours.clear()
        print("local optima,", state.depth, 'depths,',
              heuristicFunction(state, goal), 'costs')
