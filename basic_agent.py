from agent import AlphaBetaAgent
import minimax

"""
Agent skeleton. Fill in the gaps.
"""
class MyAgent(AlphaBetaAgent):

  """
  This is the skeleton of an agent to play the Tak game.
  """
  def get_action(self, state, last_action, time_left):
    self.last_action = last_action
    self.time_left = time_left
    return minimax.search(state, self)

  """
  The successors function must return (or yield) a list of
  pairs (a, s) in which a is the action played to reach the
  state s.
  """
  def successors(self, state):
    if state != None:
      actions = state.get_current_player_actions()
      list = []
      for action in actions:

        if state.is_action_valid(action):
          newState = state.copy()
          newState.apply_action()
          list.add((action, newState))
      return list

  """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """
  def cutoff(self, state, depth):
    if state != None:
      return depth < 1 and state.game_over()
    return depth < 1

  """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """
  def evaluate(self, state):
    utility = 0
    thisPlayer = state.cur_player
    advPlayer = 1 - thisPlayer
    for player in (thisPlayer, advPlayer):
      offset = 1
      if player != thisPlayer:
        offset = -1

      if(state.game_over()):
        if state.get_winner() == thisPlayer:
          return 100
        else:
          return -100
      for pawn in range(state.size()-2):
        utility += offset * (len(state.move_dir(player, pawn)))
      return utility
