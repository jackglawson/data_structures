import numpy as np
import itertools
import matplotlib.pyplot as plt


def points_fall_in_cube(rs: np.ndarray, centre: np.ndarray, width: float):
    """Returns a boolean mask indicating which particles fall within the cube"""
    falls_within_bounds = np.all([centre - width / 2 <= rs, rs < centre + width / 2], axis=0)
    falls_within_all_bounds = np.all(falls_within_bounds, axis=1)
    return falls_within_all_bounds


class OctreeNode:
    """Single node for the Octree data structure"""
    def __init__(self, rs: np.ndarray, radii: np.ndarray, centre: np.ndarray, width: float):
        self.centre = centre
        self.width = width
        self.num_particles = len(rs)

        if self.num_particles <= 1:
            self.children = []

        else:
            self.children = self._make_children(rs, radii)

    def _make_children(self, rs: np.ndarray, radii: np.ndarray):
        new_width = self.width / 2
        new_centres = np.vstack([self.centre + new_width / 2, self.centre - new_width / 2]).T
        new_centres = itertools.product(*new_centres)
        return [self._make_child(rs, radii, np.array(centre), new_width) for centre in new_centres]

    @staticmethod
    def _make_child(rs: np.ndarray, radii: np.ndarray, centre: np.ndarray, width: float):
        mask = points_fall_in_cube(rs, centre, width)
        selected_rs = rs[mask]
        selected_radii = radii[mask]
        return OctreeNode(selected_rs, selected_radii, centre, width)

    def __repr__(self):
        return 'Node at {} with width {} and {} particles'.format(tuple(self.centre), self.width, self.num_particles)


class Octree:
    """
    An efficient data structure for detecting collisions between spheres, or calculating forces between many spheres
    when the force from a distant set of spheres can be approximated as coming from a single point
    """

    def __init__(self, rs: np.ndarray, radii: np.ndarray, centre: np.ndarray = None, width: float = None):
        """
        rs: ndarray (particle, dimension)
        radii: ndarray (particle)
        centre: ndarray (dimension)
        width: float
        """

        if centre is None:
            centre = np.mean(rs, axis=0)

        if width is None:
            width = np.max(rs) * 2 + 1

        self.root = OctreeNode(rs, radii, centre, width)

    def plot(self, rs: np.ndarray):
        ax = plt.axes()
        ax.axis('scaled')
        ax.set_xlim(self.root.centre[0] - self.root.width / 2, self.root.centre[0] + self.root.width / 2)
        ax.set_ylim(self.root.centre[1] - self.root.width / 2, self.root.centre[1] + self.root.width / 2)
        ax.scatter(rs[:, 0], rs[:, 1])

        all_nodes = self.dfs()
        for node in all_nodes:
            ax.hlines(node.centre[1] + node.width / 2, node.centre[0] - node.width / 2, node.centre[0] + node.width / 2)
            ax.hlines(node.centre[1] - node.width / 2, node.centre[0] - node.width / 2, node.centre[0] + node.width / 2)
            ax.vlines(node.centre[0] + node.width / 2, node.centre[1] - node.width / 2, node.centre[1] + node.width / 2)
            ax.vlines(node.centre[0] - node.width / 2, node.centre[1] - node.width / 2, node.centre[1] + node.width / 2)

        plt.show()

    def dfs(self):
        """Depth-first search"""
        discovered_nodes = []
        first_vertex = self.root
        stack = [first_vertex]
        while stack:
            v = stack.pop()
            discovered_nodes.append(v)
            stack += v.children

        return discovered_nodes
