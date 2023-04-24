from agent import AlphaBetaAgent
import minimax

"""
Agent skeleton. Fill in the gaps.
"""

AcceptRange = 1.1
DIRECTIONS = ['WEST','NORTH','EAST','SOUTH']
class MyAgent(AlphaBetaAgent):
    """
  This is the skeleton of an agent to play the Tak game.
  """

    def __init__(self):
        self.time_left = None
        self.allTime = None
        self.last_action = None
        self.time = 100
        self.cur_depth = 0
        self.curr_bridge = {}

    def get_action(self, state, last_action, time_left):

        self.curr_bridge = {}
        self.last_action = last_action
        self.time_left = time_left
        if(self.allTime == None):
            self.allTime = time_left
            self.pawns = state.size - 2
        self.time = self.time_left * 100 / self.allTime
        return minimax.search(state, self)


    """
  The successors function must return (or yield) a list of
  pairs (a, s) in which a is the action played to reach the
  state s.
  """

    def successors(self, state):
        actions = state.get_current_player_actions()
        actions.sort(key= lambda x : self.move_dir_pos(state, (x[3], x[4])))
        currPlayerAction = []
        for action in actions:
            newState = state.copy()
            newState.apply_action(action)
            if state.cur_player == 1 - self.id:
                yield action, newState
            else:
                if len(state.history) <20:
                    currPlayerAction.append((action, newState))
                else:
                    yield action, newState
        if len(currPlayerAction) != 0:
            newList = self.giveBestUtility(currPlayerAction)
            for nl in newList:
                yield nl

    def move_dir_pos(self, state, pos):
        dirs = []
        adj_bridges = state.adj_bridges_pos(pos)
        adj_pawns = state.adj_pawns_pos(pos)
        for dir in DIRECTIONS:
            if adj_bridges[dir] and not adj_pawns[dir]:
                dirs.append(dir)
        return len(dirs)

    def giveBestUtility(self, actions):
        best = None
        listPreTrier = []
        for action in actions:
            actionUtility = self.evaluate(action[1])
            actionUtility1 = actionUtility
            if actionUtility1 < 0:
                actionUtility1 /= AcceptRange
            else:
                actionUtility1 *= AcceptRange
            if best is None:
                best = actionUtility
            if actionUtility >= best:
                best = actionUtility
                listPreTrier.append((best, action))
                listPreTrier.sort(key=lambda x: x[0], reverse=True)
            elif actionUtility1 >= best:
                listPreTrier.append((actionUtility, action))

        listPreTrier.sort(key=lambda x: x[0], reverse=True)
        index = 0
        lastUtility = listPreTrier[index][0]
        if lastUtility < 0:
            lastUtility /= AcceptRange
        else:
            lastUtility *= AcceptRange
        while lastUtility >= best:
            yield listPreTrier[index][1][0], listPreTrier[index][1][1]
            index +=1
            if index == len(listPreTrier):
                break
            lastUtility = listPreTrier[index][0]
            if lastUtility < 0:
                lastUtility /= AcceptRange
            else:
                lastUtility *= AcceptRange


    """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """

    def cutoff(self, state, depth):
        global AcceptRange
        if self.time < 18:
            return not (depth < 1) or state.game_over()
        #Normaly never done
        if state.turns > 33:
            AcceptRange = 2.3
            return not (depth < 5) or state.game_over()

        if state.turns > 27:
            AcceptRange = 1.6
            return not (depth < 5) or state.game_over()
        if state.turns > 17:
            AcceptRange = 1.5
            return not (depth < 4) or state.game_over()
        if state.turns > 7:
            AcceptRange = 1.3
            return not (depth < 3) or state.game_over()

        return not(depth < 3) or state.game_over()

    """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """
    def evaluate(self, state):
        utility = 0
        thisPlayer = self.id
        advPlayer = 1 - thisPlayer
        for player in (thisPlayer, advPlayer):
            offset = 1
            if player != thisPlayer:
                offset = -1
            if (state.game_over()):
                if state.get_winner() == thisPlayer:
                    return 500
                else:
                    return -500

            for pawn in range(len(state.cur_pos[0])):
                if not state.is_pawn_blocked(player, pawn):
                    direction = state.move_dir(player, pawn)
                    utility += offset * 5 * (len(direction)) / 2
                    x, y = state.get_pawn_position(player, pawn)
                    pos1 = [(x+1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                    for i in direction:
                        if i == 'WEST':
                            pos1.append((x-1, y))
                        elif i =='NORTH':
                            pos1.append((x, y - 1))
                        elif i == 'EAST':
                            pos1.append((x + 1, y))
                        elif i == 'SOUTH':
                            pos1.append((x, y + 1))
                    for pos in pos1:

                        if pos[0]< state.size and pos[0]>= 0 and pos[1]< state.size and pos[1]>= 0:
                            if pos in self.curr_bridge:
                                dir = self.curr_bridge[pos]
                            else:
                                dir = self.move_dir_pos(state, pos) - 1
                            utility += offset * 2 * dir
                    adj = state.adj_pawns(player, pawn)
                    for key, value in adj.items():
                        if key == 'WEST' and (x - 1, y) in state.cur_pos[1-player]:
                            utility += 2 * offset
                        elif key == 'NORTH' and (x, y - 1) in state.cur_pos[1-player]:
                            utility += 2 * offset
                        elif key == 'EAST' and (x + 1, y) in state.cur_pos[1-player]:
                            utility += 2 * offset
                        elif key == 'SOUTH' and (x, y + 1) in state.cur_pos[1-player]:
                            utility += 2 * offset
                    if state.history[len(state.history) - 2][0] == pawn and player == 1 - self.id:
                        utility *= 1.125
                else:
                    utility -= offset * 4



        return utility

    def move_dir_pos(self, state, pos):
        dirs = 0
        adj_bridges = state.adj_bridges_pos(pos)
        for dir in DIRECTIONS:
            if adj_bridges[dir]:
                dirs+=1
        return dirs

