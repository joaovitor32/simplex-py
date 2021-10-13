import sys
import yaml

import numpy as np
from tabulate import tabulate
from config.colors import bcolors
import shutil


class Table:
    def __init__(self, yaml_path) -> None:
        self._load_tableau(yaml_path)

    @classmethod
    def _load_tableau(self, yaml_path: str) -> None:
        with open(yaml_path, 'r') as stream:
            try:
                input_data: dict = yaml.safe_load(stream)
                self.matrix = None
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
    def _get_tableau(self) -> np.array:
        return self.tableau

    @classmethod
    def _get_matrix(self) -> np.array:
        return self.matrix

    @classmethod
    def _set_matrix(self, matrix: np.array) -> None:
        self.matrix = matrix

    @classmethod
    def _display_matrix(self) -> None:
        columns = shutil.get_terminal_size().columns
        print(f'{bcolors.TITLE} /*-------- Simplex operation result ---------*/\n {bcolors.ENDC}'.center(columns))

        tabulated_matrix = tabulate(
            self.matrix, headers=self.title, tablefmt="pretty", stralign='center', numalign="center")

        print(f'{bcolors.TABLE} {tabulated_matrix} {bcolors.ENDC}')
