import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from topomesh import polygonal, delaunay

points = np.array(
    [
        [ 16.5,  -3.5 ],
        [  8.0,   7.75],
        [  9.5,  -2.0 ],
        [  6.5,  -2.0 ],
        [  8.0,   1.5 ],
        [ -3.5,  -0.0 ],
        [ -4.25, -2.0 ],
        [-12.0,  -0.0 ],
        [-10.0,   2.25],
        [-19.0,  -3.5 ],
    ],
)

edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (7, 8), (8, 9), (9, 0)
]

d_0 = np.ones((1, len(points)), dtype=np.int8)
d_1 = np.zeros((len(points), len(edges)), dtype=np.int8)
for edge_id, (v0, v1) in enumerate(edges):
    d_1[(v0, v1), edge_id] = (-1, +1)

d_2 = np.ones((len(edges), 1), dtype=np.int8)
d_2[5] = 0

queue = [list(range(len(edges)))[::-1]]
machine = delaunay.RetriangulationMachine([d_0, d_1, d_2], points, queue)

edge_sets = [np.array(edges)]
while not machine.is_done():
    machine.step()
    d_1 = machine.topology[1]
    num_edges = d_1.shape[1]
    edges = np.array([np.flatnonzero(d_1[:, index]) for index in range(num_edges)])
    edge_sets.append(edges)

fig, axes = plt.subplots(
    nrows=len(edge_sets) // 2,
    ncols=2,
    sharex=True,
    sharey=True,
    constrained_layout=True,
    figsize=(6.4, 3.2),
)

for ax in axes.flatten():
    ax.set_aspect("equal")
    ax.axis("off")

for index, (ax, edge_set) in enumerate(zip(axes.flatten(), edge_sets)):
    ax.scatter(*points.T, 10.0, color="black")
    collection = LineCollection(points[edge_set], color="black")
    ax.add_collection(collection)
    ax.annotate(f"{index}", (points[:, 0].min(), points[:, 1].max() - 4.0), fontsize=20)

fig.savefig("retria.pdf")
