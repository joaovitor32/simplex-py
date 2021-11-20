

# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Tableau.SimplexTableau import SimplexTableau
from unittest.mock import Mock
import unittest
import numpy as np
import yaml

class TestSimple(unittest.TestCase):

    def _load_tableau(self, yaml_path: str) -> None:
        with open(yaml_path, 'r') as stream:
            try:
                input_data: dict = yaml.safe_load(stream)
                self.matrix = None
                self.number_of_free_variables = input_data["FREE_VARIABLES_QTD"]
                self.title = np.array(input_data["TABLEAU"]).T[:, 0]
                self.tableau = np.array(
                    np.array(input_data["TABLEAU"]).T[:, 1:], dtype=np.float64)
                self.cb_response = np.array(input_data["cb_response"],dtype=np.float64)
                self.cn_response =  np.array(input_data["cn_response"],dtype=np.float64)
                self.xn_response = np.array(input_data["xn_response"],dtype=np.float64)
                self.xb_response = np.array(input_data["xb_response"],dtype=np.float64)
                self.gamma_response = np.array(input_data["gamma_response"],dtype=np.float64)
               
                if len(self.tableau) != len(self.title):
                    raise Exception(
                        "tableau and title have different dimensions")

            except yaml.YAMLError as error:
                print("[ERROR] Error processing YAML file:", error)
                sys.exit(1)

    def test_format(self):
        yaml_path = './src/data/simplex-tableau.test.yaml'
        self._load_tableau(yaml_path)

        simplex = SimplexTableau(yaml_path)

        [[cb, cn], [xb, xn], gamma] = simplex._calculate()

        self.assertTrue((cb == self.cb_response).all())
        self.assertTrue((cn == self.cn_response).all())
        self.assertTrue((xb == self.xb_response).all())
        self.assertTrue((xn == self.xn_response).all())
        self.assertTrue((gamma == self.gamma_response).all())
        pass


if __name__ == '__main__':
    unittest.main()
