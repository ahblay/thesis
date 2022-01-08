import numpy as np
from percolate import Grid


def read_file(filename):
    output = []
    with open(f'input/{filename}.txt', 'r') as f:
        output = f.readlines()
    print(output)
    result = []
    layer = []
    for row in output:
        if row != '\n':
            # iterate over columns
            cols = []
            for col in list(row):
                if col == 'O':
                    cols.append(0)
                elif col == 'X':
                    cols.append(1)
                else:
                    pass
            layer.append(cols)
        else:
            result.append(layer)
            layer = []
    result.append(layer)
    l = len(result)
    r = len(result[0])
    c = len(result[0][0])
    print(result)

    print(l, c, r)

    ss = []
    for i in range(l):
        for j in range(r):
            for k in range(c):
                if result[i][j][k] == 1:
                    ss.append((i, j, k))
    return ss, (l, r, c), result


# takes a numpy ndarray (representing a particular starting infection) as an argument
def build_frames(grids):
    with open("latex/output.tex", "w") as f:
        f.write('')

    shape = grids[0].shape

    # these may be wrong....
    layers = shape[0]
    rows = shape[1]
    cols = shape[2]

    view1 = 70
    view2 = 120

    header = [
        '\documentclass[border={10}]{standalone} \n',
        '\\usepackage{tikz} \n',
        '\\usepackage{tikz-3dplot} \n',
        f'\\tdplotsetmaincoords{{{view1}}}{{{view2}}} \n',
        '\\tdplotsetrotatedcoords{0}{0}{0} \n',
        '\\begin{document} \n'
    ]

    tikz = '\\begin{tikzpicture}[scale=2.5,tdplot_rotated_coords, rotated axis/.style={->,purple,ultra thick}, blackBall/.style={ball color = white}, borderBall/.style={ball color = white,opacity=.25}, very thick] \n'

    with open("latex/output.tex", "a+") as f:
        f.writelines(header)
        f.write(tikz)

    nodes = []
    counter = 0
    for grid in grids:
        red_nodes = []
        for l in range(layers):
            for r in range(rows):
                for c in range(cols):
                    if counter == 0:
                        nodes.append(f'\\shade[rotated axis,blackBall] ({r}, {c}, {l}) circle (0.05cm); \n')
                        edges = []
                        for i in [(0,0,1), (0,1,0), (1,0,0)]:
                            edges.append(f'\\draw ({r}, {c}, {l})[gray!20] -- ({r+i[1]}, {c+i[2]}, {l+i[0]}); \n')
                        if l == layers-1:
                            edges.remove(f'\\draw ({r}, {c}, {l})[gray!20] -- ({r}, {c}, {l+1}); \n')
                        if r == rows-1:
                            edges.remove(f'\\draw ({r}, {c}, {l})[gray!20] -- ({r+1}, {c}, {l}); \n')
                        if c == cols-1:
                            edges.remove(f'\\draw ({r}, {c}, {l})[gray!20] -- ({r}, {c+1}, {l}); \n')
                        with open("latex/output.tex", "a+") as f:
                            f.writelines(edges)
                    if grid[l][r][c] == 1:
                        red_nodes.append(f'\\shade[rotated axis,ball color=red] ({r}, {c}, {l}) circle (0.06cm); \n')

        if counter == 0:
            edges = [
                f'\\draw ({rows-1},{cols-1},{layers-1})[black!70] -- (0,{cols-1},{layers-1}); \n',
                f'\\draw ({rows-1},{cols-1},{layers-1})[black!70] -- ({rows-1},0,{layers-1}); \n',
                f'\\draw ({rows-1},{cols-1},{layers-1})[black!70] -- ({rows-1},{cols-1},0); \n'
            ]

            with open("latex/output.tex", "a+") as f:
                f.writelines(edges)
                f.writelines(nodes)

        with open("latex/output.tex", "a+") as f:
            f.write('\\pause; \n')
            f.writelines(red_nodes)

        counter += 1

    close = [
        '\\end{tikzpicture} \n',
        '\\end{document} \n'
    ]
    with open("latex/output.tex", "a+") as f:
        f.writelines(close)
    return


def seven_cubes():
    with open("latex/seven_cubes.tex", "w") as f:
        f.write('')

    view1 = 70
    view2 = 120

    header = [
        '\documentclass[border={10}]{standalone} \n',
        '\\usepackage{tikz} \n',
        '\\usepackage{tikz-3dplot} \n',
        f'\\tdplotsetmaincoords{{{view1}}}{{{view2}}} \n',
        '\\tdplotsetrotatedcoords{0}{0}{0} \n',
        '\\begin{document} \n'
    ]

    tikz = '\\begin{tikzpicture}[scale=2.5,tdplot_rotated_coords, rotated axis/.style={->,purple,ultra thick}, blackBall/.style={ball color = white}, borderBall/.style={ball color = white,opacity=.25}, very thick] \n'

    with open("latex/seven_cubes.tex", "a+") as f:
        f.writelines(header)
        f.write(tikz)

    nodes = []
    counter = 0
    for l in range(4):
        for r in range(4):
            for c in range(4):
                if counter == 0:
                    nodes.append(f'\\shade[rotated axis,blackBall] ({r}, {c}, {l}) circle (0.05cm); \n')
                    edges = []
                    for i in [(0,0,1), (0,1,0), (1,0,0)]:
                        edges.append(f'\\draw ({r}, {c}, {l})[gray!20] -- ({r+i[1]}, {c+i[2]}, {l+i[0]}); \n')
                    if l == 3:
                        edges.remove(f'\\draw ({r}, {c}, {l})[gray!20] -- ({r}, {c}, {l+1}); \n')
                        if r == 3:
                            edges.remove(f'\\draw ({r}, {c}, {l})[gray!20] -- ({r}, {c}, {l}); \n')
                    if r == 3:
                        edges.remove(f'\\draw ({r}, {c}, {l})[gray!20] -- ({r+1}, {c}, {l}); \n')
                    if c == 3:
                        edges.remove(f'\\draw ({r}, {c}, {l})[gray!20] -- ({r}, {c+1}, {l}); \n')
                    with open("latex/seven_cubes.tex", "a+") as f:
                        f.writelines(edges)

    close = [
        '\\end{tikzpicture} \n',
        '\\end{document} \n'
    ]
    with open("latex/seven_cubes.tex", "a+") as f:
        f.writelines(nodes)
        f.writelines(close)
    return


if __name__ == '__main__':

    neighbors = 3
    scale = 1
    filename = '2x2x2'

    ss, shape, result = read_file(filename)
    g = Grid(shape)
    success, steps = g.percolate(neighbors, ss)
    print(steps[0])
    # heatmap(steps[0:1], scale, filename)
    build_frames(steps)
    #seven_cubes()