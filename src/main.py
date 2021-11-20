from Simplex.Simplex import Simplex
from Simplex.Table import Table
from Simplex.Plot import Plot
from Tableau.SimplexTableau import SimplexTableau

if __name__ == "__main__":
    # The following linex that user pivoting method
    yaml_path = './src/data/simplex.yaml'

    plot = Plot(yaml_path)
    table = Table(yaml_path)
    simplex = Simplex(table, plot)

    simplex.plot.render_feasible_region()

    simplex._calculate()
    simplex.table._display_matrix()

    # The following linex contains the normal method
    yaml_path_tableau = './src/data/simplex-tableau.yaml'

    simplex_tableau = SimplexTableau(yaml_path_tableau)

    simplex_tableau._calculate_response()
