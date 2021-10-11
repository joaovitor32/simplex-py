from Simplex import Simplex
from Table import Table
from Plot import Plot

if __name__ == "__main__":
    yaml_path = './src/data/simplex.yaml'
    
    plot = Plot(yaml_path)
    table = Table(yaml_path)
    simplex = Simplex(table, plot)

    simplex.plot.render_feasible_region()

    simplex._calculate()
    simplex.table._display_matrix()
