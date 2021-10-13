
# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import yaml
import numpy as np
import unittest
from unittest.mock import Mock
from Simplex import Simplex
from Table import Table

class TestSimple(unittest.TestCase):

    def _load_tableau(self, yaml_path: str) -> None:
        with open(yaml_path, 'r') as stream:
            try:
                input_data: dict = yaml.safe_load(stream)
                self.matrix = None
                self.title = np.array(input_data["TABLEAU"]).T[:, 0]
                self.tableau = np.array(
                    np.array(input_data["TABLEAU"]).T[:, 1:], dtype=np.float64)
                self.response = np.array(
                    np.array(input_data["TABLEAU_RESULT"]), dtype=np.float64)
                if len(self.tableau) != len(self.title):
                    raise Exception(
                        "tableau and title have different dimensions")

            except yaml.YAMLError as error:
                print("[ERROR] Error processing YAML file:", error)
                sys.exit(1)

    def test_format(self):
        yaml_path = './src/data/simplex.test.yaml'

        self._load_tableau(yaml_path)

        plot = Mock()
        table = Table(yaml_path)
        simplex = Simplex(table, plot)

        simplex._calculate()
        result = simplex.table._get_matrix()

        round_result = np.round(result, 3)
        round_response = np.round(self.response, 3)

        self.assertTrue((round_result == round_response).all())
        pass


if __name__ == '__main__':
    unittest.main()
