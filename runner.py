from random import Random
from predator_prey import *
from psuedoMCTSPredator import PsuedoMCTSGreedyPredRandomPrey, PsuedoMCTSGreedyPredSmartPrey1, PsuedoMCTSGreedyPredSmartPrey2, PsuedoMCTSGreedyPredSmartPrey3
from psuedoMCTSPredator import PsuedoMCTSTeammatePredRandomPrey, PsuedoMCTSTeammatePredSmartPrey1, PsuedoMCTSTeammatePredSmartPrey2, PsuedoMCTSTeammatePredSmartPrey3

from smartPredator import SmartGreedyPredRandomPrey, SmartGreedyPredSmartPrey1, SmartGreedyPredSmartPrey2, SmartGreedyPredSmartPrey3
from smartPredator import SmartTeammatePredRandomPrey, SmartTeammatePredSmartPrey1, SmartTeammatePredSmartPrey2, SmartTeammatePredSmartPrey3

from psuedoMCTSNode import *

# Variables:
board_sizes = [5, 10, 20]
types_of_predators = [
    [ GreedyPredator, TeammateAwarePredator ],
    [ 
        [ PsuedoMCTSGreedyPredRandomPrey, PsuedoMCTSGreedyPredSmartPrey1, PsuedoMCTSGreedyPredSmartPrey2, PsuedoMCTSGreedyPredSmartPrey3],
        [ PsuedoMCTSTeammatePredRandomPrey, PsuedoMCTSTeammatePredSmartPrey1, PsuedoMCTSTeammatePredSmartPrey2, PsuedoMCTSTeammatePredSmartPrey3]
    ],
    [
        [ SmartGreedyPredRandomPrey, SmartGreedyPredSmartPrey1, SmartGreedyPredSmartPrey2, SmartGreedyPredSmartPrey3],
        [ SmartTeammatePredRandomPrey, SmartTeammatePredSmartPrey1, SmartTeammatePredSmartPrey2, SmartTeammatePredSmartPrey3]
    ]
]

types_of_prey = [RandomPrey, SmartPrey1, SmartPrey2, SmartPrey3]

# Testing
GP = GreedyPredator
print("num iter: " + str(main(5, 5, [GP,GP, GP, PsuedoMCTSGreedyPredRandomPrey],[RandomPrey], preyLocArray=None, predLocArray = None, maxIter = 50)))
        


#PsuedoMCTS

print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSGreedyPredRandomPrey],[RandomPrey], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 50)))
print("num iter: " + str(main(5, 5, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, PsuedoMCTSTeammatePredRandomPrey],[RandomPrey], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 50)))
print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSGreedyPredSmartPrey1],[SmartPrey1], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
print("num iter: " + str(main(10, 10, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, PsuedoMCTSTeammatePredSmartPrey1],[SmartPrey1], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSGreedyPredSmartPrey2],[SmartPrey2], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
print("num iter: " + str(main(10, 10, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, PsuedoMCTSTeammatePredSmartPrey2],[SmartPrey2], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSGreedyPredSmartPrey3],[SmartPrey3], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
print("num iter: " + str(main(10, 10, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, PsuedoMCTSTeammatePredSmartPrey3],[SmartPrey3], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))

#Smart
print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator, GreedyPredator, SmartGreedyPredRandomPrey],[RandomPrey], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 50)))
print("num iter: " + str(main(5, 5, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, SmartTeammatePredRandomPrey],[RandomPrey], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 50)))
print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, SmartGreedyPredSmartPrey1],[SmartPrey1], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
print("num iter: " + str(main(5, 5, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, SmartTeammatePredSmartPrey1],[SmartPrey1], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 20)))
print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator, GreedyPredator, SmartGreedyPredSmartPrey2],[SmartPrey2], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 20)))
print("num iter: " + str(main(5, 5, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, SmartTeammatePredSmartPrey2],[SmartPrey2], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 20)))
print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator, GreedyPredator, SmartGreedyPredSmartPrey3],[SmartPrey3], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 20)))
print("num iter: " + str(main(5, 5, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, SmartTeammatePredSmartPrey3],[SmartPrey3], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 20)))
