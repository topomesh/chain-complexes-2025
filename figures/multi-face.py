import numpy as np
from numpy import pi as π
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
from zmsh import polytopal

fig = plt.figure()

rng = np.random.default_rng(seed=42)
num_vertices = 7
θs = np.linspace(0, 2 * π, num_vertices + 1)[:-1]
xs = np.column_stack((np.cos(θs), np.sin(θs)))

# Make a random polygon and plot it
d_0, d_1, d_2 = polytopal.random_polygon(num_vertices, rng)
triangles = polytopal.to_simplicial([d_0, d_1, d_2])

ax = fig.add_subplot(131)
ax.set_aspect("equal")
ax.axis("off")
δ = 0.5
ax.set_xlim((-1 - δ, +1 + δ))
ax.set_ylim((-1 - δ, +1 + δ))
ax.triplot(*xs.T, triangles, c="black")

zs = np.vstack(
    (
        np.column_stack((xs, np.zeros(len(xs)))),
        np.array([[0, 0, 1], [0, 0, -1]]),
    )
)

# Form the suspension of the polygon and plot it
e_0, e_1, e_2, e_3 = polytopal.join_vertices([d_0, d_1, d_2])
#triangle_ids = np.flatnonzero(np.count_nonzero(e_3, axis=1) == 2)
triangle_ids = np.arange(d_2.shape[1])
k_2 = e_2[:, triangle_ids]

triangles = polytopal.to_simplicial([e_0, e_1, k_2])

edge_ids0 = np.arange(d_1.shape[1])
segments0 = zs[[np.flatnonzero(col) for col in e_1[:, edge_ids0].T]]
line_collection0 = Line3DCollection(segments0, color="black", linewidth=2.0)
edge_ids1 = np.setdiff1d(np.arange(e_1.shape[1]), edge_ids0)
segments1 = zs[[np.flatnonzero(col) for col in e_1[:, edge_ids1].T]]
line_collection1 = Line3DCollection(segments1, color="black", linewidth=1.0)

azim = 270

ax = fig.add_subplot(132, projection="3d")
ax.view_init(azim=azim, elev=15)
ax.axis("off")
δ = -0.35
for method in [ax.set_xlim, ax.set_ylim, ax.set_zlim]:
    method((-1 - δ, +1 + δ))
segments = zs[[np.flatnonzero(col) for col in e_1.T]]
poly_collection = Poly3DCollection(zs[triangles], alpha=0.5)
ax.add_collection(line_collection0)
ax.add_collection(line_collection1)
ax.add_collection(poly_collection)

# Form the edge insertion of the suspension and plot it
interior_edge_ids = np.flatnonzero(np.count_nonzero(d_2, axis=1) > 1)
s = polytopal.merge([d_0, d_1, d_2], interior_edge_ids)

boundary_edge_ids = np.setdiff1d(np.arange(d_1.shape[1]), interior_edge_ids)
e_1 = d_1[:, boundary_edge_ids]
e_2 = (d_2 @ s).reshape((-1, 1))[boundary_edge_ids]

cone = polytopal.join_vertex([d_0, e_1, e_2])
f_0, f_1, f_2, f_3, f_4 = polytopal.join_vertex(cone)

null_poly_ids = np.flatnonzero(np.count_nonzero(f_3[:, 2:], axis=1) == 0)
poly_ids = np.setdiff1d(np.arange(f_2.shape[1]), null_poly_ids)

g_2 = f_2[:, poly_ids]
g_3 = f_3[poly_ids, 2:]

triangle_ids = np.flatnonzero(np.count_nonzero(g_3, axis=1) == 2)
k_2 = g_2[:, triangle_ids]
edge_ids = np.flatnonzero(np.count_nonzero(k_2, axis=1))
triangles = polytopal.to_simplicial([f_0, f_1, k_2])

ax = fig.add_subplot(133, projection="3d")
ax.view_init(azim=azim, elev=60)
ax.axis("off")
δ = -0.35
for method in [ax.set_xlim, ax.set_ylim, ax.set_zlim]:
    method((-1 - δ, +1 + δ))
segments = zs[[np.flatnonzero(col) for col in f_1[:, edge_ids].T]]
line_collection = Line3DCollection(segments, color="black")
poly_collection = Poly3DCollection(zs[triangles], alpha=0.5)
ax.add_collection(line_collection)
ax.add_collection(poly_collection)
fig.savefig("multi-face.pdf", bbox_inches="tight")
