import numpy as np
from scipy.spatial import Voronoi
from scipy.stats.qmc import PoissonDisk
import matplotlib.pyplot as plt
import pygmsh

rng = np.random.default_rng(seed=1729)
engine = PoissonDisk(2, radius=0.1, seed=rng)
vpoints = engine.random(20)
voronoi = Voronoi(vpoints)

finite_regions = [r for r in voronoi.regions if len(r) > 0 and not (-1 in r)]

vvertices = voronoi.vertices
def max_dist(arr1, arr2):
    return max([np.sqrt(np.sum((x - y)**2)) for x, y in zip(arr1, arr2)])

dist = 0.5
regions = [r for r in finite_regions if max_dist(vpoints, vvertices[r]) < dist]
polygons = [vvertices[r] for r in regions]

fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.axis("off")

for p in polygons:
    p = (np.array([[0, -1], [1, 0]]) @ p.T).T
    with pygmsh.geo.Geometry() as geometry:
        geometry.add_polygon(p, mesh_size=0.05)
        mesh = geometry.generate_mesh()
    points = mesh.points[:, :2]
    triangles = mesh.cells_dict["triangle"]
    ax.triplot(*points.T, triangles, linewidth=0.5, color="black")
    ax.plot(*np.vstack((p, p[0])).T, linewidth=4.0, color="black")

fig.savefig("parallel-mesh.pdf", bbox_inches="tight")
