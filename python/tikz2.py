from pylatex import (Document, TikZ, TikZNode,
                     TikZDraw, TikZCoordinate,
                     TikZUserPath, TikZOptions,
                     NewLine, Center, HFill, HorizontalSpace)
from pylatex.base_classes import Environment, CommandBase, Command
from pylatex.package import Package
import numpy as np
from percolate import Grid
import math
import pyperclip


def get_neighbors(grid, index):
    neighbors = []
    l = index[0]
    r = index[1]
    c = index[2]

    candidates = [(l,r-1,c), (l,r+1,c), (l,r,c-1), (l,r,c+1)]

    for candidate in candidates:
        x = candidate[0]
        y = candidate[1]
        z = candidate[2]
        if x >= 0 and y >= 0 and z >= 0:
            try:
                if grid[x][y][z] == 0:
                    neighbors.append(candidate)
            except IndexError:
                pass
    return neighbors


def read_file(filename):
    output = []
    with open(f'input/{filename}.txt', 'r') as f:
        output = f.readlines()
    #print(output)
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
    #print(result)

    #print(l, c, r)

    ss = []
    for i in range(l):
        for j in range(r):
            for k in range(c):
                if result[i][j][k] == 1:
                    ss.append((i, j, k))
    return ss, (l, r, c), result


# takes a numpy ndarray (representing a particular starting infection) as an argument
def build_frames_beamer(grids, scale, filename, chapter, gradient=False, circle_node=True):
    class Frame(Environment):
        packages = [Package('frame')]

    pause = Command('pause')

    # create document
    doc = Document(documentclass="beamer")

    shape = grids[0].shape

    # these may be wrong....
    layers = shape[0]
    rows = shape[1]
    cols = shape[2]

    counter = 0
    added = []

    with doc.create(Frame()):
        with doc.create(Center()):
            scale_args = {"scale": scale}
            with doc.create(TikZ(options=TikZOptions(**scale_args))) as pic:
                for grid in grids:
                    to_draw = []
                    for l in range(layers):
                        for r in range(rows):
                            for c in range(cols):
                                if counter == 0:
                                    node_kwargs = {}
                                    circle = TikZDraw([TikZCoordinate(c, 0 - (r + (l * (rows + 1)))), 'circle'],
                                                      options=TikZOptions(radius='5pt',
                                                                          **node_kwargs))
                                    if not circle_node:
                                        circle = TikZDraw([TikZCoordinate(c, 0 - (r + (l * (rows + 1)))),
                                                           'rectangle',
                                                           TikZCoordinate(c + 1, 1 - (r + (l * (rows + 1))))],
                                                          options=TikZOptions('draw',
                                                                              **node_kwargs))
                                    # add to tikzpicture
                                    pic.append(circle)
                                if grid[l][r][c] == 1:
                                    if gradient:
                                        node_kwargs = {'fill': f'red!{70*counter/len(grids) + 30}',}
                                    else:
                                        node_kwargs = {'fill': f'red',}
                                    circle = TikZDraw([TikZCoordinate(c, 0 - (r + (l * (rows + 1)))), 'circle'],
                                                      options=TikZOptions(radius='5pt',
                                                                          **node_kwargs))
                                    if not circle_node:
                                        circle = TikZDraw([TikZCoordinate(c, 0 - (r + (l * (rows + 1)))),
                                                           'rectangle',
                                                           TikZCoordinate(c + 1, 1 - (r + (l * (rows + 1))))],
                                                          options=TikZOptions('draw',
                                                                              **node_kwargs))
                                    if (c, 0 - (r + (l * (rows + 1)))) not in added:
                                        to_draw.append(circle)
                                        added.append((c, 0 - (r + (l * (rows + 1)))))
                                else:
                                    pass

                    if counter > 0:
                        doc.append(pause)
                    for item in to_draw:
                        pic.append(item)
                    counter += 1

    doc.generate_pdf(f'/Users/abel/Documents/School/Grad School/Research?/Bootstrap Percolation/Thesis/figures/{chapter}/{filename}', clean_tex=False)
    return


# takes a numpy ndarray (representing a particular starting infection) as an argument
def heatmap(grids, scale, filename, chapter):
    class Frame(Environment):
        packages = [Package('frame')]

    pause = Command('pause')

    # create document
    doc = Document(documentclass="beamer")

    shape = grids[0].shape

    # these may be wrong....
    layers = shape[0]
    rows = shape[1]
    cols = shape[2]

    counter = 0
    to_draw = []
    added = []

    with doc.create(Frame()):
        with doc.create(Center()):
            scale_args = {"scale": scale}
            with doc.create(TikZ(options=TikZOptions(**scale_args))) as pic:
                for grid in grids:
                    for l in range(layers):
                        for r in range(rows):
                            for c in range(cols):
                                if grid[l][r][c] == 1:
                                    node_kwargs = {'fill': f'red!{100*math.sqrt(counter/len(grids))}',}
                                    circle = TikZDraw([TikZCoordinate(c, 0 - (r + (l * (rows + 1)))),
                                                       'rectangle',
                                                      TikZCoordinate(c+1, 1 - (r + (l * (rows + 1))))],
                                                      options=TikZOptions('draw',
                                                                          **node_kwargs))
                                    if (c, 0 - (r + (l * (rows + 1)))) not in added:
                                        to_draw.append(circle)
                                        added.append((c, 0 - (r + (l * (rows + 1)))))
                                else:
                                    pass
                    counter += 1
                for item in to_draw:
                    pic.append(item)

    doc.generate_pdf(f'/Users/abel/Documents/School/Grad School/Research?/Bootstrap Percolation/Thesis/figures/{chapter}/{filename}_heatmap', clean_tex=False)
    return


# takes a numpy ndarray (representing a particular starting infection) as an argument
# builds frames with numbered infections
def numbered_heatmap(grids, scale, filename, chapter):
    # create document
    doc = Document(documentclass="standalone")

    shape = grids[0].shape

    # these may be wrong....
    layers = shape[0]
    rows = shape[1]
    cols = shape[2]

    counter = 0
    to_draw = []
    added = []

    scale_args = {"scale": scale}
    with doc.create(TikZ(options=TikZOptions(**scale_args))) as pic:
        for grid in grids:
            for l in range(layers):
                for r in range(rows):
                    for c in range(cols):
                        if grid[l][r][c] == 1:
                            node = None
                            if counter == 0:
                                circle_kwargs = {'fill': 'red',}
                                circle = TikZDraw([TikZCoordinate(c, 0 - (r + (l * (rows + 1)))),
                                                   'rectangle',
                                                  TikZCoordinate(c+1, 1 - (r + (l * (rows + 1))))],
                                                  options=TikZOptions('draw',
                                                                      **circle_kwargs))
                            else:
                                node_kwargs = {'scale': '1.3',}
                                node = TikZNode(text=f'{counter}',
                                                at=TikZCoordinate(c+0.5, 0 - (r + (l * (rows + 1)) - 0.5)),
                                                options=TikZOptions(**node_kwargs))
                                circle = TikZDraw([TikZCoordinate(c, 0 - (r + (l * (rows + 1)))),
                                                   'rectangle',
                                                   TikZCoordinate(c + 1, 1 - (r + (l * (rows + 1))))],
                                                  options=TikZOptions('draw'))
                            if (c, 0 - (r + (l * (rows + 1)))) not in added:
                                to_draw.append(circle)
                                if node is not None:
                                    to_draw.append(node)
                                added.append((c, 0 - (r + (l * (rows + 1)))))
                        else:
                            pass
            counter += 1
        for item in to_draw:
            pic.append(item)

    doc.generate_pdf(f'/Users/abel/Documents/School/Grad School/Research?/Bootstrap Percolation/Thesis/figures/{chapter}/{filename}_numbered_heatmap', clean_tex=False)
    return


# takes a numpy ndarray (representing a particular starting infection) as an argument
# builds frames in better format
def build_frames(grids, scale, filename, chapter, gradient=False, circle_node=True):

    # create document
    doc = Document(documentclass="standalone")

    shape = grids[0].shape

    # these may be wrong....
    layers = shape[0]
    rows = shape[1]
    cols = shape[2]

    counter = 0

    scale_args = {"scale": scale}
    for grid in grids:
        if counter > 0:
            doc.append(HorizontalSpace("1in"))
        with doc.create(TikZ(options=TikZOptions(**scale_args))) as pic:
            to_draw = []
            for l in range(layers):
                for r in range(rows):
                    for c in range(cols):
                        node_kwargs = {}
                        circle = TikZDraw([TikZCoordinate(c, 0 - (r + (l * (rows + 1)))), 'circle'],
                                          options=TikZOptions(radius='5pt',
                                                              **node_kwargs))
                        if not circle_node:
                            circle = TikZDraw([TikZCoordinate(c, 0 - (r + (l * (rows + 1)))),
                                               'rectangle',
                                               TikZCoordinate(c + 1, 1 - (r + (l * (rows + 1))))],
                                              options=TikZOptions('draw',
                                                                  **node_kwargs))
                        # add to tikzpicture
                        pic.append(circle)
                        if grid[l][r][c] == 1:
                            if gradient:
                                node_kwargs = {'fill': f'red!{70*counter/len(grids) + 30}',}
                            else:
                                node_kwargs = {'fill': f'red',}
                            circle = TikZDraw([TikZCoordinate(c, 0 - (r + (l * (rows + 1)))), 'circle'],
                                              options=TikZOptions(radius='5pt',
                                                                  **node_kwargs))
                            if not circle_node:
                                circle = TikZDraw([TikZCoordinate(c, 0 - (r + (l * (rows + 1)))),
                                                   'rectangle',
                                                   TikZCoordinate(c + 1, 1 - (r + (l * (rows + 1))))],
                                                  options=TikZOptions('draw',
                                                                      **node_kwargs))
                            to_draw.append(circle)
                        else:
                            pass

            for item in to_draw:
                pic.append(item)
            counter += (2 + cols)
        if counter > 25:
            # add newline
            doc.append(NewLine())
            counter = 1

    doc.generate_pdf(f'/Users/abel/Documents/School/Grad School/Research?/Bootstrap Percolation/Thesis/figures/{chapter}/{filename}', clean_tex=False)
    return


# takes a numpy ndarray (representing a particular starting infection) as an argument
# builds frames in better format
def build_graph(grids, scale, filename, chapter):

    # create document
    doc = Document(documentclass="standalone")

    shape = grids[0].shape

    # these may be wrong....
    layers = shape[0]
    rows = shape[1]
    cols = shape[2]

    counter = 0

    scale_args = {"scale": scale}
    for grid in reversed(grids):
        if counter > 0:
            doc.append(HorizontalSpace("1in"))
        with doc.create(TikZ(options=TikZOptions(**scale_args))) as pic:
            to_draw = []
            for l in range(layers):
                for r in range(rows):
                    for c in range(cols):
                        if grid[l][r][c] == 0:
                            node_kwargs = {}
                            circle = TikZDraw([TikZCoordinate(c, 0 - (r + (1 * (rows + 1)))), 'circle'],
                                              options=TikZOptions(radius='2pt',
                                                                  **node_kwargs))
                            neighbors = get_neighbors(grid, [l,r,c])
                            for n in neighbors:
                                line = TikZDraw([TikZCoordinate(c, 0 - (r + (1 * (rows + 1)))),
                                                "--",
                                                TikZCoordinate(n[2], 0 - (n[1] + (1 * (rows + 1))))])
                                pic.append(line)

                            # add to tikzpicture
                            pic.append(circle)
                        if grid[l][r][c] == 1:
                            node_kwargs = {'fill': 'red',}
                            circle = TikZDraw([TikZCoordinate(c, 0 - (r + (1 * (rows + 1)))), 'circle'],
                                              options=TikZOptions(radius='2pt',
                                                                  **node_kwargs))
                            to_draw.append(circle)
                        else:
                            pass

            for item in to_draw:
                pic.append(item)
            counter += (2 + cols)
        if counter > 25:
            # add newline
            doc.append(NewLine())
            counter = 1

    doc.generate_pdf(f'/Users/abel/Documents/School/Grad School/Research?/Bootstrap Percolation/Thesis/figures/{chapter}/{filename}', clean_tex=False)
    return


# makes a diagram for divisibility cases of a given thickness
def grid_diagram(x, y, thickness, filename, chapter, x_forbidden_mod=(), y_forbidden_mod=()):
    doc = Document(documentclass="standalone")

    tikz_kwargs = {'rotate': '270'}

    with doc.create(TikZ(options=TikZOptions(**tikz_kwargs))) as pic:

        for i in range(x):
            node_kwargs = {'scale': '1.3', }
            node_left = TikZNode(text=f'{i+thickness}',
                            at=TikZCoordinate(i+0.5, -0.5),
                            options=TikZOptions(**node_kwargs))
            '''
            node_right = TikZNode(text=f'{i+thickness}',
                                  at=TikZCoordinate(i + 0.5, (y+2)-0.5),
                                  options=TikZOptions(**node_kwargs))
            '''
            pic.append(node_left)
            #pic.append(node_right)
            for j in range(y):
                if i == 0:
                    node_left = TikZNode(text=f'{j+thickness}',
                                    at=TikZCoordinate(-0.5, j+0.5),
                                    options=TikZOptions(**node_kwargs))

                    '''node_right = TikZNode(text=f'{j+thickness}',
                                    at=TikZCoordinate(-0.5, j + (y+2)+0.5),
                                    options=TikZOptions(**node_kwargs))'''
                    pic.append(node_left)
                    #pic.append(node_right)
                if i < j:
                    #color = 'gray'
                    left_color = 'gray'
                elif ((i+thickness)*(j+thickness) + (j+thickness)*thickness + thickness*(i+thickness)) % 3 == 0:
                    #color = 'black'
                    left_color = 'black'
                    if (i+thickness) % 6 in x_forbidden_mod:
                        left_color = 'white'
                    if (j+thickness) % 6 in y_forbidden_mod:
                        left_color = 'white'
                else:
                    #color = 'white'
                    left_color = 'white'
                #cell_right_kwargs = {'fill': color,}
                cell_left_kwargs = {'fill': left_color,}
                cell_left = TikZDraw([TikZCoordinate(i, j),
                                   'rectangle',
                                   TikZCoordinate(i+1, j+1)],
                                  options=TikZOptions('draw', **cell_left_kwargs))
                '''cell_right = TikZDraw([TikZCoordinate(i, (y+2)+j),
                                 'rectangle',
                                 TikZCoordinate(i + 1, (y+2)+j + 1)],
                                options=TikZOptions('draw', **cell_right_kwargs))'''
                pic.append(cell_left)
                #pic.append(cell_right)

    doc.generate_pdf(f'/Users/abel/Documents/School/Grad School/Research?/Bootstrap Percolation/Thesis/figures/{chapter}/{filename}', clean_tex=False)
    return


def dialog():
    neighbors = int(input('neighbors:'))
    scale = float(input('scale:'))
    filename = input('filename:')
    chapter = input('chapter:')
    nodes = input('circle nodes? [y/n]:')
    h = input('heatmap? [y/n]:')
    if nodes == 'y':
        circles = True
    else:
        circles = False

    ss, shape, result = read_file(filename)
    g = Grid(shape)
    success, steps = g.percolate(neighbors, ss)

    step_amount = input("all steps? [y/n]:")

    if step_amount == 'y':
        if h == 'y':
            numbered_heatmap(steps, scale, filename, chapter)
            filename = filename + "_numbered_heatmap"
        else:
            build_frames(steps, scale, filename, chapter, circle_node=circles)
    else:
        step_amount = input('first step? [y/n]:')
        if step_amount == 'y':
            if h == 'y':
                numbered_heatmap(steps[0:1], scale, filename, chapter)
                filename = filename + "_numbered_heatmap"
            else:
                build_frames(steps[0:1], scale, filename, chapter, circle_node=circles)
        else:
            step_amount = input('first two steps? [y/n]:')
            if step_amount == 'y':
                if h == 'y':
                    numbered_heatmap(steps[0:2], scale, filename, chapter)
                    filename = filename + "_numbered_heatmap"
                else:
                    build_frames(steps[0:2], scale, filename, chapter, circle_node=circles)
            else:
                step_amount = input('first n steps? [enter a number, or n to abort]:')
                if step_amount != 'n':
                    step_amount = min(int(step_amount), len(steps))
                    if h == 'y':
                        numbered_heatmap(steps[0:step_amount], scale, filename, chapter)
                        filename = filename + "_numbered_heatmap"
                    else:
                        build_frames(steps[0:step_amount], scale, filename, chapter, circle_node=circles)
                else:
                    print("ABORTING without diagram")
                    return
    print(f"diagram saved to: figures/{chapter}/{filename}.pdf")
    pyperclip.copy(f"figures/{chapter}/{filename}.pdf")
    return


if __name__ == '__main__':

    #neighbors = 3
    #scale = 1
    #filename = 'test'
    #chapter = '3'

    #ss, shape, result = read_file(filename)
    #g = Grid(shape)
    #success, steps = g.percolate(neighbors, ss)
    #heatmap(steps, scale, filename)
    #build_graph(steps, scale, filename, chapter)

    dialog()

    #grid_diagram(19, 19, 6, filename, chapter, x_forbidden_mod=(1,3,5), y_forbidden_mod=(0,2,4))