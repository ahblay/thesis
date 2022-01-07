import numpy as np
import copy
import math, random


class Grid:
    def __init__(self, shape):
        self.grid = self.build_grid(shape)
        self.shape = shape
        self.result = None
        self.steps = []
        self.lower_bound = math.ceil((shape[0]*shape[1] + shape[1]*shape[2] + shape[2]*shape[0]) / 3)

    def build_grid(self, shape):
        grid = np.zeros(shape, dtype=np.int)
        return grid

    def percolate(self, r, start_set):
        self.steps = []
        self.result = self.build_grid(self.shape)
        temp = self.build_grid(self.shape)
        for vertex in start_set:
            self.result[vertex] = 1
            temp[vertex] = 1
        iterations = 0
        active = True
        complete = False
        while active:
            self.steps.append(self.result.copy())
            active = False
            complete = True
            for index in np.ndindex(self.shape):
                if self.result[index] == 0:
                    complete = False
                    if self.get_neighbors(self.result, index) >= r:
                        temp[index] = 1
                        active = True
            iterations += 1
            self.result = copy.deepcopy(temp)
        return complete, self.steps

    def get_neighbors(self, grid, index):
        val = 0
        for i in range(len(index)):
            index_plus = list(index)
            i_plus = index[i] + 1
            index_plus[i] = i_plus
            if i_plus < self.shape[i]:
                val += grid[tuple(index_plus)]

            index_minus = list(index)
            i_minus = index[i] - 1
            index_minus[i] = i_minus
            if i_minus >= 0:
                val += grid[tuple(index_minus)]
        return val

    def improve(self, ss, r, num_dots):
        if num_dots == self.lower_bound:
            message = "Functionality for this test does not exist."
            changes = []
            if self.test_set(r, ss):
                message = "This set cannot be improved. You did it. Congrats."
                return False, changes, message
            # swap dots until some metric (possibily uninfected area?) is improved
            for index in range(len(ss)):
                new_ss = [x for i, x in enumerate(ss) if i != index]

            return False, changes, message
        else:
            # remove dots and test percolation
            message = "Could not improve percolation by removing dots."
            changes = []
            if not self.test_set(r, ss):
                message = "You can only improve a set above the lower bound if it percolates."
                return False, changes, message
            # shuffle list of indices and iterate through them
            indices = list(range(len(ss)))
            random.shuffle(indices)
            for index in indices:
                new_ss = [x for i, x in enumerate(ss) if i != index]
                if self.test_set(r, new_ss):
                    message = f"Successfully removed dot at coordinate {ss[index]}."
                    changes.append((ss[index], None))
                    return True, changes, message
            return False, changes, message

    def test_set(self, r, set):
        self.result = self.build_grid(self.shape)
        for vertex in set:
            self.result[vertex] = 1
        iterations = 0
        active = True
        complete = False
        while active:
            active = False
            complete = True
            for index in np.ndindex(self.shape):
                if self.result[index] == 0:
                    complete = False
                    if self.get_neighbors(self.result, index) >= r:
                        self.result[index] = 1
                        active = True
            iterations += 1
        return complete