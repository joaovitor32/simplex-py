import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection, ConvexHull
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from config.colors import bcolors

original_restriction = list[np.array, np.array]

font = {'family': 'serif', 'color': bcolors.TITLEPLOT, 'size': 16}


class Plot:

    def __init__(self, yaml_path: str) -> None:
        self._load_tableau(yaml_path)

    @classmethod
    def _load_tableau(self, yaml_path: str) -> None:
        with open(yaml_path, 'r') as stream:
            try:
                input_data: dict = yaml.safe_load(stream)
                self.xlim = np.array(input_data['XLIM'])
                self.ylim = np.array(input_data['YLIM'])
                self.free_variable_qtd = input_data['FREE_VARIABLES_QTD']
                self.halfspaces = np.array(
                    np.array(input_data["TABLEAU"]).T[1:, 1:], dtype=np.float64)

            except yaml.YAMLError as error:
                print("[ERROR] Error processing YAML file:", error)
                sys.exit(1)

    @classmethod
    def _get_original_restriction(self) -> original_restriction:
        _, num_cols = self.halfspaces.shape
        A = self.halfspaces[0:(num_cols-self.free_variable_qtd+1), :]
        b = self.halfspaces[(self.free_variable_qtd+2):, :][0]
        return A.T, b

    @classmethod
    def _eye(self, rows_qtd: int, index: int) -> np.array:
        eye_array = []
        for number in range(index):
            eye_array.append(-np.eye(1, rows_qtd, number)[0])
            eye_array.append(np.eye(1, rows_qtd, number)[0])

        return np.array(eye_array)

    # finds the center of the largest sphere fitting in the convex hull
    @classmethod
    def _get_feasible_point(self, A: np.array, b: np.array) -> np.array:
        norm_vector = np.linalg.norm(A, axis=1)
        A_ = np.hstack((A, norm_vector[:, None]))
        b_ = b[:, None]
        c = np.zeros((A.shape[1] + 1,))
        c[-1] = -1
        res = linprog(c, A_ub=A_, b_ub=b_[:, None], bounds=(None, None))
        return res.x[:-1]

    '''
        Inside this function is going to be desconsidered
        the added free variables
    '''

    @classmethod
    def render_feasible_region(self) -> None:
        A, b = self._get_original_restriction()

        qtd_decision_variables = (
            self.halfspaces.shape[0] - self.free_variable_qtd-1)

        decision_variables_array = self._eye(
            A.T.shape[0], qtd_decision_variables)

        b = np.hstack(
            (b, [-self.xlim[0], self.xlim[1], -self.ylim[0], self.ylim[1]]))

        A = np.vstack((A, decision_variables_array))

        '''
            feasible_point can be considered as an interior
            point.
        '''
        feasible_point = self._get_feasible_point(A, b)

        '''
            Stacked Inequalities of the form Ax + b <= 0 in format [A; b]
            halfspace = [A,-b]
        '''

        halfspaces = np.hstack((A, -b[:, None]))

        hs = HalfspaceIntersection(
            halfspaces, feasible_point)

        ax = plt.subplot(111)

        ax.set_xlim(self.xlim[0], self.xlim[1])
        ax.set_ylim(self.ylim[0], self.ylim[1])

        x = np.linspace(*self.xlim, 100)
        for h in halfspaces:
            if h[1] == 0:
                ax.axvline(-h[2]/h[0], color=bcolors.LINE)
            else:
                ax.plot(x, (-h[2]-h[0]*x)/h[1], color=bcolors.LINE)

        x, y = zip(*hs.intersections)
        points = list(zip(x, y))
        convex_hull = ConvexHull(points)
        polygon = Polygon([points[v]
                          for v in convex_hull.vertices], color=bcolors.REGION)

        ax.add_patch(polygon)
        ax.plot(x, y, 'o', color=bcolors.DOT)
        plt.title("Aplicação do Simplex", fontdict=font)
        plt.ylabel("X2", fontdict=font)
        plt.xlabel("X1", fontdict=font)
        plt.show()
