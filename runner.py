from predator_prey import *
from psuedoMCTSPredator import PsuedoMCTSGreedyPredRandomPrey, PsuedoMCTSGreedyPredSmartPrey1, PsuedoMCTSGreedyPredSmartPrey2, PsuedoMCTSGreedyPredSmartPrey3
from psuedoMCTSPredator import PsuedoMCTSTeammatePredRandomPrey, PsuedoMCTSTeammatePredSmartPrey1, PsuedoMCTSTeammatePredSmartPrey2, PsuedoMCTSTeammatePredSmartPrey3

from smartGreedyPredatorRandomPrey import *
from psuedoMCTSGreedyPredatorRandomPrey import *
'''
from smartGreedyPredatorSmartPrey1 import *
from smartGreedyPredatorSmartPrey2 import *
from smartGreedyPredatorSmartPrey3 import *
from psuedoMCTSGreedyPredatorSmartPrey1 import *
from psuedoMCTSGreedyPredatorSmartPrey2 import *
from psuedoMCTSGreedyPredatorSmartPrey3 import *

from smartTeammatePredatorRandomPrey import *
from smartTeammatePredatorSmartPrey1 import *
from smartTeammatePredatorSmartPrey2 import *
from smartTeammatePredatorSmartPrey3 import *
from psuedoMCTSTeammatePredatorRandomPrey import *
from psuedoMCTSTeammatePredatorSmartPrey1 import *
from psuedoMCTSTeammatePredatorSmartPrey2 import *
from psuedoMCTSTeammatePredatorSmartPrey3 import *
'''
from psuedoMCTSNode import *
import math



#print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator, GreedyPredator, SmartGreedyPredatorRandomPrey],[StationaryPrey], [(1,1)], [(0,0),(0,4),(4,4),(4,0)], 50)))
#print("num iter: " + str(main(10, 10, [PsuedoMCTSTeammatePredatorRandomPrey,PsuedoMCTSTeammatePredatorSmartPrey1, PsuedoMCTSTeammatePredatorSmartPrey2, PsuedoMCTSTeammatePredatorSmartPrey3],[StationaryPrey], preyLocArray=[(1,1)], predLocArray = None, maxIter = 50)))
#print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSGreedyPredatorRandomPrey],[RandomPrey], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(9,0)], maxIter = 50)))
print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSTeammatePredRandomPrey],[RandomPrey], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(9,0)], maxIter = 50)))
print("--------------------------")
print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSTeammatePredSmartPrey1],[SmartPrey1], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
print("--------------------------")
print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSTeammatePredSmartPrey2],[SmartPrey2], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
print("--------------------------")
print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSTeammatePredSmartPrey3],[SmartPrey3], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
print("--------------------------")
# print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator,GreedyPredator,
# GreedyPredator],[StationaryPrey], [(1,1)], [(0,0),(0,4),(4,4),(4,0)], 50)))