from __future__ import annotations
import math
from typing import Callable
from state.state import State
import heapq
import abc


class Solver():
    __metaclass__ = abc.ABCMeta

    def __init__(self, goal: State):
        self.goal = goal

    @staticmethod
    def misplaced(state1: State, state2: State):
        misplaced = 0
        for i, _ in enumerate(state1.matrix):
            if state1.matrix[i] != state2.matrix[i]:
                misplaced += 1
        return misplaced

    @staticmethod
    def manhattan(state1: State, state2: State):
        cost = 0
        pos: list[int] = [0 for _ in range(9)]
        for i, v in enumerate(state2.matrix):
            pos[v] = i
        for i, _ in enumerate(state1.matrix):
            if i != pos[state1.matrix[i]]:
                cost += abs((i % 3) - (pos[state1.matrix[i]] % 3)) + \
                    abs(math.floor(i / 3) -
                        math.floor(pos[state1.matrix[i]] / 3))
        return cost

    @staticmethod
    def _push(heap: list[tuple[int, int, State]], cost: int, identity: int, state: State):
        heapq.heappush(heap, (cost, identity, state))

    @staticmethod
    def _pop(heap: list[tuple[int, int, State]]):
        return heapq.heappop(heap)

    @staticmethod
    def _visit(visitedSet: set[tuple[int, ...]], matrix: list[int]):
        visitedSet.add(tuple(matrix))

    @abc.abstractmethod
    def solve(self, initial: State, heuristicFunction: Callable[[State, State], int]) -> State:
        pass
