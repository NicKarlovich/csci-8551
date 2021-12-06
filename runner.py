from predator_prey import *

print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator,GreedyPredator,GreedyPredator],[StationaryPrey], [(1,1)], [(0,0),(0,4),(4,4),(4,0)], 50)))