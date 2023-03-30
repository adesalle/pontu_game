from agent import AlphaBetaAgent
import minimax

"""
Agent skeleton. Fill in the gaps.
"""

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

    def get_action(self, state, last_action, time_left):
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
        for action in actions:
            newState = state.copy()
            newState.apply_action(action)
            yield action, newState



    """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """

    def cutoff(self, state, depth):
        self.cur_depth = depth
        if self.time < 15:
            return not (depth < 1) or state.game_over()
        if state.turns > 4:
            return not (depth < 3) or state.game_over()
        if state.turns > 9:
            return not (depth < 4) or state.game_over()
        if state.turns > 12:
            return not (depth < 5) or state.game_over()
        return not(depth < 2) or state.game_over()

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
                utility += offset * 5 * (len(state.move_dir(player, pawn)))

        return utility

