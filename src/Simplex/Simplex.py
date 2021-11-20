import operator
import numpy as np
from Simplex.Plot import Plot
from Simplex.Table import Table
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

# types
min_t = list[int, float]
pivot_data = list[np.array, np.array]


class Simplex:
    @classmethod
    def __init__(self, table: Table, plot: Plot) -> None:
        self.table = table
        self.plot = plot
        self.object_function = self.table._get_tableau()[:, 0]
        self.restriction_table = self.table._get_tableau()[:, 1:]

    @classmethod
    def _get_min_data(self, np_array: np.array) -> min_t:
        value = min(np_array, key=float)
        index = list(np_array).index(value)

        return (index, value)

    @classmethod
    def _sum_arrays(self, np_arr1: np.array, np_arr2: np.array) -> np.array:
        return np_arr1+np_arr2

    @classmethod
    def _update_restriction_table(self, nlp: np.array, pivot_line: np.array, pivot_index: int) -> None:
        for idx, _ in enumerate(self.restriction_table.T):
            if idx is not pivot_index:
                self.restriction_table.T[idx] = self._sum_arrays(
                    -nlp * (pivot_line[idx]), self.restriction_table.T[idx])

    @classmethod
    def _get_b_column(self) -> np.array:
        return self.restriction_table[-1, :]

    @classmethod
    def _get_pivot_column(self, pivot_index: int) -> np.array:
        return self.restriction_table[pivot_index, :]

    @classmethod
    def _get_pivot_data(self, pivot_line: np.array, pivot_index: int) -> pivot_data:
        pivot = pivot_line[pivot_index]
        line_out = self.restriction_table[:, pivot_index]
        return [pivot, line_out]

    @classmethod
    def _calculate(self) -> np.array:

        while len(self.object_function[self.object_function < 0]) > 0:

            (min_z_index, _) = self._get_min_data(self.object_function)

            pivot_line = self._get_pivot_column(min_z_index)

            b = self._get_b_column()

            (pivot_index, pivot) = self._get_min_data(
                (b/pivot_line)[b/pivot_line > 0])

            [pivot, line_out] = self._get_pivot_data(pivot_line, pivot_index)

            nlp = line_out/pivot

            self.object_function = self._sum_arrays(
                self.object_function, (-nlp*self.object_function[min_z_index]))

            self.restriction_table.T[pivot_index] = nlp

            self._update_restriction_table(nlp, pivot_line, pivot_index)

        self.table._set_matrix(
            np.insert(self.restriction_table.T, 0, self.object_function, axis=0))
