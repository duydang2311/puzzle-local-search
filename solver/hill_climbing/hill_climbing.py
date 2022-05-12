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
        # decrement to make heap sort by first come first served
        decrement = 0
        visited: set[tuple[int, ...]] = set()
        heap: list[tuple[int, int, State]] = []
        Solver._push(heap, heuristicFunction(initial, self.goal),
                     (decrement := decrement - 1), initial)
        while len(heap) != 0:
            _, _, state = Solver._pop(heap)
            if state.matrix == self.goal.matrix:
                print("found,", len(visited), 'states expanded,',
                      state.depth, 'depths')
                # state.print_trace()
                break
            for i in Direction:
                moved = state.move(i)
                if moved is None or tuple(moved.matrix) in visited:
                    continue
                Solver._push(heap, heuristicFunction(
                    moved, self.goal), (decrement := decrement - 1), moved)
                Solver._visit(visited, moved.matrix)
