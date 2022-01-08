from pylatex import (Document, TikZ, TikZNode,
                     TikZDraw, TikZCoordinate,
                     TikZUserPath, TikZOptions,
                     NewLine, Center)
from pylatex.base_classes import Environment, CommandBase, Command
from pylatex.package import Package
import numpy as np
from percolate import Grid
import math


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
def build_frames(grids, scale, filename, chapter, gradient=False, circle_node=True):
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
            heatmap(steps, scale, filename, chapter)
        else:
            build_frames(steps, scale, filename, chapter, circle_node=circles)
    else:
        step_amount = input('first step? [y/n]:')
        if step_amount == 'y':
            if h == 'y':
                heatmap(steps[0:1], scale, filename, chapter)
            else:
                build_frames(steps[0:1], scale, filename, chapter, circle_node=circles)
        else:
            step_amount = input('first two steps? [y/n]:')
            if step_amount == 'y':
                if h == 'y':
                    heatmap(steps[0:2], scale, filename, chapter)
                else:
                    build_frames(steps[0:2], scale, filename, chapter, circle_node=circles)
            else:
                print("ABORTING without diagram")
                return
    print(f"diagram saved to: figures/{chapter}/{filename}.pdf")
    return


if __name__ == '__main__':

    '''
    neighbors = 3
    scale = .5
    filename = '18x33x2'

    ss, shape, result = read_file(filename)
    g = Grid(shape)
    success, steps = g.percolate(neighbors, ss)
    print(steps[0])
    #heatmap(steps, scale, filename)
    build_frames(steps[1:2], scale, filename, circle_node=True)
    '''

    dialog()