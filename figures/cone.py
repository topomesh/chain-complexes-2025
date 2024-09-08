import numpy as np
from numpy import pi as π
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
from mpl_toolkits import mplot3d

n1 = 5
θ1 = np.linspace(0, 2 * π, n1 + 1)[:-1]
x1 = np.column_stack((np.cos(θ1), np.sin(θ1)))

n2 = 3
r = 0.35
θ2 = np.linspace(0, 2 * π, n2 + 1)[:-1] + π / n2
x2 = r * np.column_stack((np.cos(θ2), np.sin(θ2)))

x = np.vstack((x1, x2))
triangulation = Triangulation(*x.T)

z = np.concatenate((np.column_stack((x, np.zeros(len(x)))), np.array([[0, 0, 1]])))
v3 = len(z) - 1

added_triangles = []
for (v1, v2) in triangulation.edges:
    added_triangles.append((v1, v2, v3))

cone_triangles = np.concatenate((triangulation.triangles, np.array(added_triangles)))
segments = [(z[v], z[v3]) for v in range(len(x))]
lines = mplot3d.art3d.Line3DCollection(
    segments, color="black", linestyle="dashed", linewidths=1.0
)

fig = plt.figure()
ax0 = fig.add_subplot(121)
ax0.set_aspect("equal")
ax0.set_axis_off()
scale = 1.5
delta = 0.0625
ax0.set_xlim((-scale, +scale))
ax0.set_ylim((-scale + delta, +scale + delta))
ax0.scatter(*x.T, color="black")
ax0.triplot(*x.T, triangulation.triangles, color="black")

ax1 = fig.add_subplot(122, projection="3d")
ax1.set_axis_off()
ax1.triplot(*x.T, triangulation.triangles, color="black")
ax1.add_artist(lines)
ax1.plot_trisurf(z[:, 0], z[:, 1], cone_triangles, z[:, 2], alpha=0.125, color="black")
ax1.scatter(*z.T, color="black")
ax1.set_box_aspect(None, zoom=1.35)

fig.savefig("cone.pdf", bbox_inches="tight")
