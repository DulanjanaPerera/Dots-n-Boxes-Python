# This class creates,

# A) cell dictionary which contains
#     1. cell index (key)
#     2. 4 vertex locations
#     3. 4 vertex index in vertices list
#     4. cell value
#     5. which player select a edge ("A" - AI, "P" - Player).
#        The 4th person who completes the finale edge owns the cell value

# This dictionary is used to keep the track of which users select the edge of a particular cell
# and create rectangle for the completed cell


# B) edge cell dictionary which contains cell indexes for the corresponding edge
#    Eg:- 0-->1 (top) edge is corresponds with cell '0'. But the right edge of that cell is corresponds
#    with both '0' and '1'
#    This helps to determine the which cell is currently player is try to obtain


class Cells():
    def __init__(self, ROWs, COLs, vertices, cellvalue):
        self.ROWs = ROWs
        self.COLs = COLs
        self.vertices = vertices
        self.cellvalue = cellvalue
        self.cellDictionary = {}
        for i in range(len(self.cellvalue)):
            quo, rem = divmod(i, self.COLs-1)
            # generate the locations of the cell corners and cell value and empty list for edge selection
            self.cellDictionary.update({i: [[self.vertices[i+quo], self.vertices[i+quo+1],
                                            self.vertices[self.COLs + i + quo], self.vertices[self.COLs + i + quo + 1]],
                                            [i+quo, i+quo+1, self.COLs + i + quo, self.COLs + i + quo + 1],
                                            self.cellvalue[i], []]})

        self.edgecell = {}
        # generate corresponding cells for the edge.
        # if it is a horizontal edge, then top and bottom cells are corresponding edges
        for i in range(len(self.cellDictionary)):
            # top, left, right and bottom edge vertices
            keylist = [str(self.cellDictionary.get(i)[1][0]) + "," + str(self.cellDictionary.get(i)[1][1]),
                       str(self.cellDictionary.get(i)[1][0]) + "," + str(self.cellDictionary.get(i)[1][2]),
                       str(self.cellDictionary.get(i)[1][1]) + "," + str(self.cellDictionary.get(i)[1][3]),
                       str(self.cellDictionary.get(i)[1][2]) + "," + str(self.cellDictionary.get(i)[1][3]),
                       ]

            for key in keylist:
                if not (key in self.edgecell.keys()):
                    self.edgecell.update({key: [i]})
                else:
                    self.edgecell[key].append(i)

        self.childDictionary = {}
        # define the neighbor dots for the each dot to draw the lines (edges)
        # this is similar to finding the associated moves for current tile in 8-puzzle game
        for i in range(len(self.vertices)):
            quo, rem = divmod(i, self.COLs)

            if quo == 0 and rem == 0:
                self.childDictionary.update({i: [[i + 1, i + self.COLs], [str(i)+","+str(i + 1), str(i)+","+str(i + self.COLs)]]})
            elif quo == 0 and rem > 0:
                if rem == self.COLs - 1:
                    self.childDictionary.update({i: [[i + self.COLs, i - 1], [str(i)+","+str(i + self.COLs), str(i - 1)+","+str(i)]]})
                else:
                    self.childDictionary.update({i: [[i + 1, i + self.COLs, i - 1], [str(i)+","+str(i + 1), str(i)+","+str(i + self.COLs), str(i - 1)+","+str(i)]]})
            elif quo == self.ROWs - 1 and rem == 0:
                self.childDictionary.update({i: [[i + 1, i - self.COLs], [str(i)+","+str(i + 1), str(i - self.COLs)+","+str(i)]]})
            elif quo == self.ROWs - 1 and rem > 0:
                if rem == self.COLs - 1:
                    self.childDictionary.update({i: [[i - 1, i - self.COLs], [str(i - 1)+","+str(i), str(i - self.COLs)+","+str(i)]]})
                else:
                    self.childDictionary.update({i: [[i + 1, i - 1, i - self.COLs], [str(i)+","+str(i + 1), str(i - 1)+","+str(i), str(i - self.COLs)+","+str(i)]]})
            elif self.ROWs - 1 > quo > 0 and rem == 0:
                self.childDictionary.update({i: [[i + 1, i + self.COLs, i - self.COLs], [str(i)+","+str(i + 1), str(i)+","+str(i + self.COLs), str(i - self.COLs)+","+str(i)]]})
            elif self.ROWs - 1 > quo > 0 and rem > 0:
                if rem == self.COLs - 1:
                    self.childDictionary.update({i: [[i + self.COLs, i - 1, i - self.COLs], [str(i)+","+ str(i + self.COLs), str(i - 1)+","+str(i), str(i - self.COLs)+","+str(i)]]})
                else:
                    self.childDictionary.update({i: [[i + 1, i + self.COLs, i - 1, i - self.COLs], [str(i)+","+str(i + 1), str(i)+","+str(i + self.COLs),str(i - 1)+","+str(i), str(i - self.COLs)+","+str(i)]]})

    def edge_to_dots(self, edge):
        # convert the string edge ('0,1') to the numeric vertices([0,1]) for other computation
        sList = edge.split(sep=',')
        verList = [int(r) for r in sList]
        return verList
