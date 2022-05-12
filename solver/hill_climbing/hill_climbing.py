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


# Random-restart hill climbing
class HillClimbingSolver(Solver):
    @_measure
    def solve(self, initial: State, heuristicFunction: Callable[[State, State], int]):
        heap: list[tuple[int, int, State]] = [
            (heuristicFunction(initial, self.goal), 0, initial)]
        state = initial
        visited: set[tuple[int, ...]] = set()
        increment = 0
        while True:
            # heap.clear()
            if state.matrix == self.goal.matrix:
                print("found,", state.depth, 'depths')
                return
            for direction in Direction:
                moved = state.move(direction)
                if moved is None or tuple(moved.matrix) in visited:
                    continue
                Solver._push(heap, heuristicFunction(
                    moved, self.goal), (increment := increment + 1), moved)
                visited.add(tuple(moved.matrix))
            if heap[0][0] < heuristicFunction(state, self.goal):
                idx = 0
                for i, v in enumerate(heap):
                    idx = i
                    if v[0] != heap[0][0]:
                        break
                state = heap[floor(random() * (idx + 1))][2]
            else:
                state = heap[floor(random() * len(heap))][2]
