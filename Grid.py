# This class initialize the grid vertices (dots) for the given number of ROWs and COLs.
# Also the vertex (dot) that mouse clicked
# Class determine the game window size according to the grid size.
# A Padding is used to make space between window's edge and grid.
# The cell size determines the space between vertices or one grid size.
# Cell values are randomly generated (between 1 and 5)

import numpy as np


class Grid:
    def __init__(self, ROWs, COLs):
        self.ROWs = ROWs
        self.COLs = COLs
        self.PADDING = 40
        self.CELLSIZE = 30
        self.WIDTH = 2*self.PADDING + (self.COLs-1)*self.CELLSIZE
        self.HEIGHT = 3*self.PADDING + (self.ROWs-1)*self.CELLSIZE
        self.vertices = []
        self.cellvalue = np.random.randint(low=1, high=6, size=((self.ROWs - 1)*(self.COLs - 1),)).tolist()

    def grid_vertices(self):
        for r in range(self.ROWs+1):
            for c in range(self.COLs+1):
                if r <= self.ROWs-1 and c <= self.COLs-1:
                    self.vertices.append([c * self.CELLSIZE + self.PADDING, r * self.CELLSIZE + 2 * self.PADDING])

        return self.vertices

    # This method gets the selected dot position index from the vertices list.
    # mouse click location is re-map (snap) to the closest dot grid locations
    def selected_dot(self, pos):
        x = pos[0]
        y = pos[1]

        # x cursor position with respect to the grid starting position
        ref_location_x = x - self.PADDING
        if -self.CELLSIZE/2 <= ref_location_x <= self.CELLSIZE*(self.COLs - 0.5):  # beyond half cell distance is neglected
            if ref_location_x < 0:
                # The quotient and the remainder of the x-coordinate of the mouse click can maps to nearest dot index
                remx, quax = divmod(ref_location_x, self.CELLSIZE)
                remx = remx + 1
                quax = self.CELLSIZE - quax
            else:
                remx, quax = divmod(ref_location_x, self.CELLSIZE)

            if quax > self.CELLSIZE/2:
                remx = remx + 1

            # y cursor position with respect to the grid starting position
            ref_location_y = y - 2*self.PADDING
            if -self.CELLSIZE / 2 <= ref_location_y <= self.CELLSIZE*(self.ROWs - 0.5):  # beyond half cell distance is neglected
                if ref_location_y < 0:
                    remy, quay = divmod(ref_location_y, self.CELLSIZE)
                    remy = remy + 1
                    quay = self.CELLSIZE - quay
                else:
                    remy, quay = divmod(ref_location_y, self.CELLSIZE)

                if quay > self.CELLSIZE / 2:
                    remy = remy + 1
            else:
                return -1
            indx = remx + self.COLs * remy  # compute the nearest dot index
            return indx
        else:
            return -1
