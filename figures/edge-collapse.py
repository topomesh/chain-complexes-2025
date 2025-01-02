import numpy as np
from numpy import pi as π
import zmsh
import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
for ax in axes.flatten():
    ax.set_aspect("equal")
    ax.axis("off")


ϕ = np.array([0.0, 0.0])
u = np.array([1.0, 0.0])
v = np.array([np.cos(π / 3), np.sin(π / 3)])

# First example: a nice case
xs = np.array([-v, u - v, 2 * u - v, -u, ϕ, u, 2 * u, v - u, v, v + u]) - 0.5 * u

triangles = np.array(
    [
        [0, 1, 4],
        [1, 2, 5],
        [0, 4, 3],
        [1, 5, 4],
        [2, 6, 5],
        [3, 4, 7],
        [4, 5, 8],
        [5, 6, 9],
        [4, 8, 7],
        [5, 9, 8],
    ],
    dtype=int,
)

Xs = np.column_stack((np.ones(len(xs)), xs))
assert (np.linalg.det(Xs[triangles]) > 0).all()

vertex_ids = [4, 5]
D = zmsh.polytopal.from_simplicial(triangles)
E = zmsh.polytopal.edge_collapse(D, vertex_ids)
new_triangles = zmsh.polytopal.to_simplicial(E)

zs = xs.copy()
zs[vertex_ids[0], :] = zs[vertex_ids, :].mean(axis=0)
zs[vertex_ids[1], :] = np.array([np.nan, np.nan])

Zs = np.column_stack((np.ones(len(zs)), zs))
assert (np.linalg.det(Zs[new_triangles]) > 0).all()


# Less nice case
triangle_id = 6
ys = np.row_stack((xs, xs[triangles[triangle_id]].mean(axis=0)))

added_triangles = np.array([[4, 5, 10], [5, 8, 10], [10, 8, 4]], dtype=int)
bad_triangles = np.row_stack(
    (np.delete(triangles, triangle_id, axis=0), added_triangles)
)

D = zmsh.polytopal.from_simplicial(bad_triangles)
E = zmsh.polytopal.edge_collapse(D, vertex_ids)
new_bad_triangles = zmsh.polytopal.to_simplicial(E)

Ys = np.column_stack((np.ones(len(ys)), ys))
print(np.linalg.det(Ys[bad_triangles]))
print(np.linalg.det(Ys[new_bad_triangles]))

ws = ys.copy()
ws[vertex_ids[0], :] = ws[vertex_ids, :].mean(axis=0)
ws[vertex_ids[1], :] = np.array([np.nan, np.nan])

position = -2 * u + v
sizes = [81.0 if k in vertex_ids else 36.0 for k in range(len(xs))]
axes[0, 0].annotate("(a)", position, size="large")
axes[0, 0].triplot(*xs.T, triangles=triangles, color="black")
axes[0, 0].plot(*xs[vertex_ids, :].T, linewidth=4.0, color="black")
axes[0, 0].scatter(*xs.T, s=sizes, c="black");

axes[0, 1].annotate("(b)", position, size="large")
axes[0, 1].scatter(*zs.T, s=sizes, c="black")
axes[0, 1].triplot(*zs.T, triangles=new_triangles, color="black");

axes[1, 0].annotate("(c)", position, size="large")
sizes = [81.0 if k in vertex_ids else 36.0 for k in range(len(ys))]
axes[1, 0].scatter(*ys.T, s=sizes, c="black")
axes[1, 0].triplot(*ys.T, triangles=bad_triangles, color="black")
axes[1, 0].plot(*ys[vertex_ids, :].T, linewidth=4.0, color="black")

axes[1, 1].annotate("(d)", position, size="large")
axes[1, 1].triplot(*ws.T, triangles=new_bad_triangles, color="black")
axes[1, 1].scatter(*ws.T, s=sizes, c="black")

fig.savefig("edge-collapse.pdf", bbox_inches="tight")

