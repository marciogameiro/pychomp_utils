### PlotCubicalComplex.py
### MIT LICENSE 2022 Marcio Gameiro

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, FancyArrow
from matplotlib.collections import PatchCollection

import numpy as np

def PlotCubicalComplex2D(cubical_complex, fig_w=7, fig_h=7, plot_faces=True, plot_edges=True, plot_verts=True, blowup=False,
                         plot_axis=False, axis_labels=True, xlabel='$x$', ylabel='$y$', fontsize=15, fig_fname=None, dpi=300):
    """Plot a 2D cubical cell complex"""
    # Cells line width
    line_width = 2
    # Vertex size
    vert_size = 0.1
    if blowup:
        vert_size = 0.08
    # Cells minimum width
    cell_width = 0.5

    def fringe_cell(cell):
        """Check if a cell is a fringe cell"""
        return cubical_complex.rightfringe(cell)

    def boundary_cell(cell):
        """Check if a cell is a boundary cell"""
        # Fringe cells are not boundary cells
        if fringe_cell(cell):
            return False
        # A vertex is boundary if any of its star is a fringe cell
        if cubical_complex.cell_dim(cell) == 0:
            return any(cubical_complex.rightfringe(c) for c in cubical_complex.star({cell}))
        # Other cells are boundary if any of their boundaries is a face of a fringe cell
        for cell_bdry in cubical_complex.boundary({cell}):
            if any(cubical_complex.rightfringe(c) for c in cubical_complex.star({cell_bdry})):
                return True
        return False

    def vertex_color(cell):
        """Return vertex color"""
        if fringe_cell(cell):
            return 'black'
        if boundary_cell(cell):
            return 'red'
        return 'blue'

    def edge_color(cell):
        """Return edge color"""
        if fringe_cell(cell):
            return 'black'
        if boundary_cell(cell):
            return 'darkred'
        return 'blue'

    def face_color(cell):
        """Return face color"""
        if fringe_cell(cell):
            return '#d3d3d3'
        if boundary_cell(cell):
            return '#ffb6c1'
        return '#add8e6'

    def real_coord(k):
        """Return a real value for a cell coordinate"""
        # If blowup complex make the blowup cells smaller
        # real_coord = lambda k: ((3 * k) // 2) * cell_width
        # This will return values such that the cell widths
        # alternate between cell_width and 2 * cell_width
        if blowup:
            return ((3 * k) // 2) * cell_width
        return k

    def cell_vertices(cell):
        """Get real coordinates for the vertices of a cell"""
        # Get the cell complex coordinates of cell
        coords = cubical_complex.coordinates(cell)
        # Get real coordinates for the cell base vertex
        v0 = (real_coord(coords[0]), real_coord(coords[1]))
        if cubical_complex.cell_dim(cell) == 0:
            return [v0]
        # Get real coordinates for remaining edge vertex
        if cubical_complex.cell_dim(cell) == 1:
            # Get the shape of this cell (see pychomp)
            shape = cubical_complex.cell_shape(cell)
            # Add 1 to the appropriate entries to get coords of the other vertex
            coords1 = [coords[d] + (1 if (shape & (1 << d)) else 0) for d in range(D)]
            v1 = (real_coord(coords1[0]), real_coord(coords1[1]))
            return [v0, v1]
        # Get real coordinates for the remaining vertices of face
        v1 = (real_coord(coords[0] + 1), real_coord(coords[1]))
        v2 = (real_coord(coords[0] + 1), real_coord(coords[1] + 1))
        v3 = (real_coord(coords[0]),     real_coord(coords[1] + 1))
        return [v0, v1, v2, v3]

    # Get the cell complex dimension
    D = cubical_complex.dimension()

    # Plot verts as polygon patches
    if plot_verts:
        vertex_patches = []
        # Loop through the vertices
        for cell in cubical_complex(0):
            # Get cell vertices
            cell_verts = cell_vertices(cell)
            # Get the single vertex
            cell_vert = cell_verts[0]
            # Get the vertex color
            vert_clr = vertex_color(cell)
            # Plot vertex as a filled circle
            polygon = Circle(cell_vert, vert_size, fc=vert_clr, ec='black')
            vertex_patches.append(polygon)

    # Plot edges as polygon patches
    if plot_edges:
        edge_patches = []
        # Loop through the edges
        for cell in cubical_complex(1):
            # Get cell vertices
            cell_verts = cell_vertices(cell)
            # Get edge as a tuple of vertices
            cell_edge = tuple(cell_verts)
            # Get the edge color
            edge_clr = edge_color(cell)
            # Plot edge as a polygon and add to polygon patches
            polygon = Polygon(cell_edge, fc=edge_clr, ec=edge_clr, closed=True)
            edge_patches.append(polygon)

    # Plot faces as polygon patches
    if plot_faces:
        face_patches = []
        # Loop through the faces
        for cell in cubical_complex(D):
            # Get cell vertices
            cell_verts = cell_vertices(cell)
            # Get face as a tuple of vertices
            cell_face = tuple(cell_verts)
            # Get the face color
            face_clr = face_color(cell)
            # Plot face as a polygon and add to polygon patches
            polygon = Polygon(cell_face, fc=face_clr, ec='none', closed=True)
            face_patches.append(polygon)

    # Create patchs collections for dims 0, 1, and 2
    if plot_verts:
        p0 = PatchCollection(vertex_patches, match_original=True)
    if plot_edges:
        p1 = PatchCollection(edge_patches, match_original=True)
        p1.set_linewidths(line_width)
    if plot_faces:
        p2 = PatchCollection(face_patches, match_original=True)
        p2.set_linewidths(line_width)
    # Create figure axis
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    # Add collections to the axis
    if plot_faces:
        ax.add_collection(p2)
    if plot_edges:
        ax.add_collection(p1)
    if plot_verts:
        ax.add_collection(p0)
    # Add axis labels
    if axis_labels:
        ax.set_xlabel(xlabel, fontsize=fontsize)
        ax.set_ylabel(ylabel, fontsize=fontsize)
    # Set tick labels size
    ax.tick_params(labelsize=fontsize)
    # Set aspect ratio
    ax.set_aspect('equal')
    # ax.set_aspect('auto')
    # Auto scale axis
    ax.autoscale_view()
    # Axis in on by default
    if not plot_axis:
        plt.axis('off')
    if fig_fname:
        fig.savefig(fig_fname, dpi=dpi, bbox_inches='tight')
    plt.show()
