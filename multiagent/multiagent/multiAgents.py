# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        currentFood = currentGameState.getFood()
        if Directions.STOP == action:
            return float("-inf")
        for ghost in newGhostStates:
            if(newPos == ghost.getPosition()):
                return float("-inf")

        minDistance = float("inf")
        if(len(newFood.asList()) < len(currentFood.asList())):
            minDistance = 0
        else:
            for food in newFood.asList():
                minDistance = min(minDistance, manhattanDistance(newPos,food))

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore() - minDistance


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(0)
        succesors = [gameState.generateSuccessor(0, action) for action in legalMoves]
        # Choose one of the best actions
        scores = [self.miniMax(state, self.depth, 1) for state in succesors]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def miniMax(self, gameState, depth, agentIndex):

        if (depth <= 0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(agentIndex)
        succesors = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
        numAgents = gameState.getNumAgents()
        nextAgentIndex = ((agentIndex + 1) % numAgents)

        if ((agentIndex % numAgents) == 0):
            score = max([self.miniMax(state, depth, nextAgentIndex) for state in succesors])
        elif ((agentIndex % numAgents) == numAgents - 1):
            score = min([self.miniMax(state, depth - 1, nextAgentIndex) for state in succesors])
        else:
            score = min([self.miniMax(state, depth, nextAgentIndex) for state in succesors])
        
        return score




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float("-inf")
        beta = float("inf")
        legalMoves = gameState.getLegalActions(0)

        for action in legalMoves:
            state = gameState.generateSuccessor(0, action)
            currScore = self.alphaBeta(state, self.depth, 1, alpha, beta)
            if (currScore > alpha):
                alpha = currScore
                bestAction = action

        return bestAction

    def alphaBeta(self, gameState,  depth, agentIndex, alpha, beta):

        if (depth <= 0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(agentIndex)
        numAgents = gameState.getNumAgents()
        nextAgentIndex = ((agentIndex + 1) % numAgents)

        if ((agentIndex % numAgents) == 0):
            for action in legalMoves:
                state = gameState.generateSuccessor(agentIndex, action)
                alpha = max(alpha, self.alphaBeta(state, depth, nextAgentIndex, alpha, beta))
                if(beta <= alpha):
                    break
            return alpha
        elif ((agentIndex % numAgents) == numAgents - 1):
            for action in legalMoves:
                state = gameState.generateSuccessor(agentIndex, action)
                beta = min(beta, self.alphaBeta(state, depth - 1, nextAgentIndex, alpha, beta))
                if(beta <= alpha):
                    break
            return beta
        else:
            for action in legalMoves:
                state = gameState.generateSuccessor(agentIndex, action)
                beta = min(beta, self.alphaBeta(state, depth, nextAgentIndex, alpha, beta))
                if(beta <= alpha):
                    break
            return beta




class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(0)
        succesors = [gameState.generateSuccessor(0, action) for action in legalMoves]
        # Choose one of the best actions
        scores = [self.expectiMax(state, self.depth, 1) for state in succesors]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def expectiMax(self, gameState, depth, agentIndex):

        if (depth <= 0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(agentIndex)
        succesors = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
        numAgents = gameState.getNumAgents()
        nextAgentIndex = ((agentIndex + 1) % numAgents)
        p = 1./len(succesors)

        if ((agentIndex % numAgents) == 0):
            score = max([self.expectiMax(state, depth, nextAgentIndex) for state in succesors])
        elif ((agentIndex % numAgents) == numAgents - 1):
            score = sum([(p*self.expectiMax(state, depth - 1, nextAgentIndex)) for state in succesors])
        else:
            score = sum([(p*self.expectiMax(state, depth, nextAgentIndex)) for state in succesors])
        
        return score



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    curCapsules = currentGameState.getCapsules()
    curScore = currentGameState.getScore()
    curPos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood()
    curFoodCount = currentGameState.getNumFood()
    curGhostStates = currentGameState.getGhostStates()
    curScaredTimes = [ghostState.scaredTimer for ghostState in curGhostStates]

    ghostDist = float("inf")
    scaredGhosts = 0

    for ghost in curGhostStates:
        if(curPos == ghost.getPosition()):
            return float("-inf")
        ghostDist = min(ghostDist,manhattanDistance(curPos,ghost.getPosition()))
        if ghost.scaredTimer != 0:
            scaredGhosts += 1

    foodDistance = float("inf")
    if(curFoodCount == 0):
        foodDistance = 0
    for food in curFood.asList():
        foodDistance = min(foodDistance, manhattanDistance(curPos,food))

    capsuleDistance = float("inf")
    if(len(curCapsules) == 0):
        capsuleDistance = 0
    for capsule in curCapsules:
      capsuleDistance = min(capsuleDistance,manhattanDistance(curPos,capsule))

    # Different combinations were tested but in the end keeping the pacman close
    # to the ghosts was the most effective as when it eats the capsules it eats
    # the ghost as well and gain more points. On the other hand manhattan distance
    # and capsule distance made the pacman more confused at times, so they were
    # removed. 
    return (curScore - (curFoodCount) - (ghostDist/(len(curGhostStates)))
     - (len(curCapsules)))

# Abbreviation
better = betterEvaluationFunction
