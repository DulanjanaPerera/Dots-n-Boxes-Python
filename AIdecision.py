import copy, random


class AIdecision:
    def __init__(self, visitedEdges, childDictionary, cellDictionary, edgeInfo, edge, ply):
        self._ply = ply
        self._visitedEdges = visitedEdges
        self._childDictionary = childDictionary
        self._cellDictionary = cellDictionary
        self._edgeInfo = edgeInfo
        self._edge = edge

        self.nextMove = []
        self.bestMove = None
        self.nextmoveCost = []

        self.ai_score = 0
        self.player_score = 0

        # Randomize the dot space for search better
        self.verList = random.sample(range(len(self._childDictionary)), len(self._childDictionary))
        self.minimaxSearch(self._edge, 0, True, 0, [], {}, float('-inf'), float('inf'))

    # ***Initial method:****
    # The search start from right side dot and rotate counter clockwise direction
    # consider 4x3 dot grid and search start '7,8' edge. The first edge minimax considere is '7,8' But it is already
    # in the visited list. Then it takes '7,10' edge. Then it seach deeper in that edge same as the '7,8'. This actually
    # causes to miss some opportunities of win. For example, if the next actual best move is '4,7' but search start with
    # '7,10' edge, it sees the '4,7' edge as min turn (or the human player turn) which give score to the human player.
    # Then algorithm try to avoid that and select '6,7' edge. This is not ideal.
    #     4
    #     |
    # 6 - 7 - 8
    #     |
    #     10

    # ***New Improved method:
    # randomized the search space and search the best move. this method takes time but take intelligent moves.
    # Even with the depth-3 Bot takes good moves. The Alpha beta pruning speedup the process significantly.

    def minimaxSearch(self, edge, depth, turn, score, path, visited_temp, alpha, beta):

        if depth == self._ply:
            path.append(edge)
            score = self.utility(path)  # calculate the utility
            return score

        if turn:  # Max turn (AI turn)
            score = float('-inf')
            if len(path) != 0:  # neglect the initial edge.
                path.append(edge)  # append the other depth edges to the current path
                visited_temp = copy.deepcopy(self._visitedEdges)  # reset the visited list each time search along new
                {visited_temp.add(p) for p in path}  # add the current path to the visited set
            else:
                visited_temp = copy.deepcopy(self._visitedEdges)  # initialize the visited list for the first time

            for childvertex in self.verList:
                for edge in self._childDictionary[childvertex][1]:
                    if edge not in visited_temp:  # check the previous visit
                        visited_temp.add(edge)
                        score = max(score,
                                    self.minimaxSearch(edge, depth+1, not turn, score, path, visited_temp, alpha, beta))
                        alpha = max(alpha, score)  # assign the score to the alpha
                        if beta <= alpha:  # check the alpha beta pruning logic
                            if len(self._edgeInfo) == len(visited_temp):  # check the finishing edge
                                self.nextmoveCost.append(score)
                                self.nextMove.append(edge)  # add the last edge to the list
                            path.pop()  # remove the
                            break
                        path.pop()  # remove current depth edge from the path to make room for next searching path
                        if depth == 0:
                            # print(edge)
                            self.nextmoveCost.append(score)
                            self.nextMove.append(edge)

            if depth == 0:
                if len(self.nextmoveCost) != 0:
                    del visited_temp
                    maxcost = max(self.nextmoveCost)
                    self.bestMove = self.nextMove[self.nextmoveCost.index(maxcost)]
            return score

        else:  # Min turn (Player turn)
            score = float('inf')
            path.append(edge)  # add the current searching edge to the current path list
            visited_temp = copy.deepcopy(self._visitedEdges)  # reset the visited list
            {visited_temp.add(p) for p in path}  # add the current path to visited list
            for childvertex in self.verList:
                for edge in self._childDictionary[childvertex][1]:
                    if edge not in visited_temp:
                        visited_temp.add(edge)
                        score = min(score,
                                    self.minimaxSearch(edge, depth + 1, not turn, score, path, visited_temp, alpha, beta))
                        beta = min(beta, score)
                        if beta <= alpha:
                            path.pop()
                            break
                        path.pop()  # remove current depth edge from the path to make room for next searching path
            return score

    # Here only consider the utility of total board with current selected edge. Since I use previous selected edges
    # when calculating the utility it function consider the new edges and already selected edges.
    # How?? the non-reference _cellDictionary contains all the previous selections at the _cellDictionary[cell][3] list
    # This deepcopy might increases the time and the space for the program. But it allows to search better.
    def utility(self, path):
        player_score = 0
        ai_score = 0
        Ai = True
        cell_dictionary = copy.deepcopy(self._cellDictionary)  # copy non-reference of the dictionary for each eval
        for edge in path:
            cells = self._edgeInfo[edge]  # retrieve the corresponding cell indices for the selected edge
            for cellIndex in cells:
                if Ai:
                    cell_dictionary.get(cellIndex)[3].append("A")  # update the cell as edge has been drawn
                    if len(cell_dictionary.get(cellIndex)[3]) == 4:  # if all 4 edges are drawn
                        ai_score += cell_dictionary.get(cellIndex)[2]  # get the cell value to player's account
                else:
                    cell_dictionary.get(cellIndex)[3].append("P")
                    if len(cell_dictionary.get(cellIndex)[3]) == 4:
                        player_score += cell_dictionary.get(cellIndex)[2]
            Ai = not Ai
        del cell_dictionary
        return ai_score-player_score
