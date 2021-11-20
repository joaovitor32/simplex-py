from config.colors import bcolors
import numpy as np
import shutil
import yaml
import sys

import copy

from utils.inversa import inversa

np.seterr(divide='ignore', invalid='ignore')

theta_response = list[float, int]
swap_response = list[np.array, np.array]
start_variable_response = list[np.array,
                               np.array, np.array, np.array, np.array, np.array]
calculate_response = list[list, list, np.array]


class SimplexTableau:
    @classmethod
    def __init__(self, yaml_path) -> None:
        self._load_tableau(yaml_path)
        self.c = self.tableau[:, 0]
        self.A = self.tableau[:-1, 1:].T
        self.b = self.tableau[-1, 1:]

    @classmethod
    def _load_tableau(self, yaml_path: str) -> None:
        with open(yaml_path, 'r') as stream:
            try:
                input_data: dict = yaml.safe_load(stream)
                self.matrix = None
                self.number_of_free_variables = input_data["FREE_VARIABLES_QTD"]
                self.title = np.array(input_data["TABLEAU"]).T[:, 0]
                self.tableau = np.array(
                    np.array(input_data["TABLEAU"]).T[:, 1:], dtype=np.float64)

                if len(self.tableau) != len(self.title):
                    raise Exception(
                        "tableau and title have different dimensions")

            except yaml.YAMLError as error:
                print("[ERROR] Error processing YAML file:", error)
                sys.exit(1)

    @classmethod
    def _get_theta_data(self, btil: np.array, re: np.array) -> theta_response:
        theta = np.divide(btil, re)

        value = min(theta, key=float)
        index = list(theta).index(value)

        return [value, index]

    @classmethod
    def _swap(self, a: np.array, b: np.array, index: int, gamma_index: int) -> swap_response:
        a_value = copy.deepcopy(a[index])
        a[index] = b[gamma_index]
        b[gamma_index] = a_value

        return [a, b]

    @classmethod
    def _start_variables(self):
        # Getting  Dimensions of  A
        row_A, column_A = self.A.shape
        # Mounting B matrix
        B = self.A[:, (column_A-self.number_of_free_variables):]

        '''
            Creating Xb and Xn matrix:
                xn -> array de variáveis não básicas
        '''

        # Criar função para pegar essas variáveis básicas
        xn = np.zeros(column_A-self.number_of_free_variables)
        xb = np.zeros(self.number_of_free_variables)

        # Creating N
        N = self.A[:, :(column_A-self.number_of_free_variables)]

        # Creating cb e cn
        cb = self.c[len(self.c)-self.number_of_free_variables:]

        # The -1 is to desconsider the element of b column
        cn = self.c[:len(self.c)-self.number_of_free_variables-1]

        return [cn, cb, N, xn, xb, B]

    @classmethod
    def _calculate_response(self) -> None:
        columns = shutil.get_terminal_size().columns
        [[cb, cn], [xb, xn], gamma] = self._calculate()
        print(f'{bcolors.TITLE} /*-------- Simplex operation result - Non Tableau method ---------*/\n {bcolors.ENDC}'.center(columns))

        print(f'{bcolors.TABLE} cb: {cb} {bcolors.TABLE}'.center(columns))
        print(f'{bcolors.TABLE} cn: {cn} {bcolors.TABLE}'.center(columns))
        print(f'{bcolors.TABLE} xn: {xn} {bcolors.TABLE}'.center(columns))
        print(f'{bcolors.TABLE} xb: {xb} {bcolors.TABLE}'.center(columns))
        print(f'{bcolors.TABLE} gamma: {gamma} {bcolors.TABLE}'.center(columns))

    @classmethod
    def _calculate(self) -> calculate_response:

        [cn, cb, N, xn, xb, B] = self._start_variables()

        '''
            this number is to track wich non basic variable is being choosed
            to be transformed
        '''

        '''
            cn e cb -> variáveis básicas
            xn e xb -> variáveis não básicas
        '''

        # Here the code will run while gammas has at least one positive element
        while True:

            xb = np.dot(inversa(B), self.b)
            R = np.dot(inversa(B), N)

            # calculating new value of gamma
            gamma = copy.deepcopy(cn - np.dot(np.dot(N.T, (inversa(B).T)), cb))

            if(len(gamma[gamma > 0]) == 0):
                return [[cb, cn], [xb, xn], gamma]

            # Getting index of first positive number of gamma
            gamma_index = [i for i, x in enumerate(gamma) if x > 0][0]

            xne = xn[gamma_index]

            re = R.T[gamma_index]
            btil = copy.deepcopy(xb)

            # Getting theta data
            [value, index] = self._get_theta_data(btil, re)

            # Rewriting xn and xb -> Permutation between A elements
            xn[gamma_index] = xb[index]
            xb[index] = xne

            '''
                cb e cn permutam entre si
            '''

            # Rewriting cn and cb
            [cb, cn] = self._swap(cb, cn, index, gamma_index)

            # Change B and N
            [B, N] = self._swap(B, N.T, index, gamma_index)
            N = N.T
