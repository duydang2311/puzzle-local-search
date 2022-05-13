import heapq
import math
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
    # @_measure
    def solve(self, initial: State, heuristicFunction: Callable[[State, State], int]) -> State:
        state: State = initial
        goal = self.goal
        t = 1.0
        heap: list[tuple[int, int, State]] = []
        while t > 1e-5:
            heap.clear()
            for i, direction in enumerate(Direction):
                moved = state.move(direction)
                if moved is None:
                    continue
                heapq.heappush(
                    heap, (heuristicFunction(moved, goal), i, moved))
            item = heap[math.floor(random() * len(heap))]
            delta = item[0] - heuristicFunction(state, goal)
            if delta < 0:
                state = item[2]
                continue
            if math.exp(-abs(delta) / t) > random():
                state = item[2]
            t *= 0.4
        return state
