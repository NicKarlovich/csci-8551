from random import Random
from predator_prey import *
from psuedoMCTSPredator import PsuedoMCTSGreedyPredRandomPrey, PsuedoMCTSGreedyPredSmartPrey1, PsuedoMCTSGreedyPredSmartPrey2, PsuedoMCTSGreedyPredSmartPrey3
from psuedoMCTSPredator import PsuedoMCTSTeammatePredRandomPrey, PsuedoMCTSTeammatePredSmartPrey1, PsuedoMCTSTeammatePredSmartPrey2, PsuedoMCTSTeammatePredSmartPrey3

from smartPredator import SmartGreedyPredRandomPrey, SmartGreedyPredSmartPrey1, SmartGreedyPredSmartPrey2, SmartGreedyPredSmartPrey3
from smartPredator import SmartTeammatePredRandomPrey, SmartTeammatePredSmartPrey1, SmartTeammatePredSmartPrey2, SmartTeammatePredSmartPrey3

from psuedoMCTSNode import *

import multiprocessing
import time

# Variables:
board_sizes = [5, 10, 20]
types_of_predators = [
    [ GreedyPredator, TeammateAwarePredator ],
    [ 
        [ PsuedoMCTSGreedyPredRandomPrey, PsuedoMCTSGreedyPredSmartPrey1, PsuedoMCTSGreedyPredSmartPrey2, PsuedoMCTSGreedyPredSmartPrey3],
        [ PsuedoMCTSTeammatePredRandomPrey, PsuedoMCTSTeammatePredSmartPrey1, PsuedoMCTSTeammatePredSmartPrey2, PsuedoMCTSTeammatePredSmartPrey3]
    ]
]

types_of_prey = [RandomPrey, SmartPrey1, SmartPrey2, SmartPrey3]

# Testing
GP = GreedyPredator
#print("num iter: " + str(main(5, 5, [GP,GP, GP, PsuedoMCTSGreedyPredRandomPrey],[RandomPrey], preyLocArray=None, predLocArray = None, maxIter = 50)))

'''

Figure 3(a)
5x5
maxIt = 25 to solve
-- rand prey
100 4 greedy
100 3 greedy, 1 mcts greedy, 5 iter sim (if time)
100 3 greedy, 1 mcts greedy, 10 iter sim
100 3 greedy, 1 mcts greedy, 50 iter sim (if time)
100 3 greedy, 1 mcts greedy, 100 iter sim
100 3 greedy, 1 mcts greedy, 500 iter sim (if time)
100 3 greedy, 1 team
100 3 greedy, 1 mcts team, 5 iter sim (if time)
100 3 greedy, 1 mcts team, 10 iter sim
100 3 greedy, 1 mcts team, 50 iter sim (if time)
100 3 greedy, 1 mcts team, 100 iter sim
100 3 greedy, 1 mcts team, 500 iter sim (if time)

100 4 team
100 3 team, 1 mcts greedy, 5 iter sim (if time)
100 3 team, 1 mcts greedy, 10 iter sim
100 3 team, 1 mcts greedy, 50 iter sim (if time)
100 3 team, 1 mcts greedy, 100 iter sim
100 3 team, 1 mcts greedy, 500 iter sim (if time)
100 3 team, 1 greedy
100 3 team, 1 mcts team, 5 iter sim (if time)
100 3 team, 1 mcts team, 10 iter sim
100 3 team, 1 mcts team, 50 iter sim (if time)
100 3 team, 1 mcts team, 100 iter sim
100 3 team, 1 mcts team, 500 iter sim (if time)

Figure 3(b)
10x10
maxIt = 100
-- rand prey
50 4 greedy
50 3 greedy, 1 mcts greedy, 5 iter sim (if time)
50 3 greedy, 1 mcts greedy, 10 iter sim
50 3 greedy, 1 mcts greedy, 50 iter sim (if time)
50 3 greedy, 1 mcts greedy, 100 iter sim
50 3 greedy, 1 mcts greedy, 500 iter sim (if time)
50 3 greedy, 1 team
50 3 greedy, 1 mcts team, 5 iter sim (if time)
50 3 greedy, 1 mcts team, 10 iter sim
50 3 greedy, 1 mcts team, 50 iter sim (if time)
50 3 greedy, 1 mcts team, 100 iter sim
50 3 greedy, 1 mcts team, 500 iter sim (if time)

50 4 team
50 3 team, 1 mcts greedy, 5 iter sim (if time)
50 3 team, 1 mcts greedy, 10 iter sim
50 3 team, 1 mcts greedy, 50 iter sim (if time)
50 3 team, 1 mcts greedy, 100 iter sim
50 3 team, 1 mcts greedy, 500 iter sim (if time)
50 3 team, 1 greedy
50 3 team, 1 mcts team, 5 iter sim (if time)
50 3 team, 1 mcts team, 10 iter sim
50 3 team, 1 mcts team, 50 iter sim (if time)
50 3 team, 1 mcts team, 100 iter sim
50 3 team, 1 mcts team, 500 iter sim (if time)

Figure fuck you
5x5
maxIt = 25
-- smartprey1 (if time found)
100 4 greedy
100 3 greedy, 1 mcts greedy, (best number iter))
100 3 greedy, 1 team
100 3 greedy, 1 mcts team, (best number iter)

100 4 team
100 3 team, 1 mcts greedy, (best number iter)
100 3 team, 1 greedy
100 3 team, 1 mcts team, (best number iter)

-- smartprey2 (if time found)
100 4 greedy
100 3 greedy, 1 mcts greedy, (best number iter))
100 3 greedy, 1 team
100 3 greedy, 1 mcts team, (best number iter)

100 4 team
100 3 team, 1 mcts greedy, (best number iter)
100 3 team, 1 greedy
100 3 team, 1 mcts team, (best number iter)

-- smartprey3
100 4 greedy
100 3 greedy, 1 mcts greedy, (best number iter))
100 3 greedy, 1 team
100 3 greedy, 1 mcts team, (best number iter)

100 4 team
100 3 team, 1 mcts greedy, (best number iter)
100 3 team, 1 greedy
100 3 team, 1 mcts team, (best number iter)

'''
if __name__ == '__main__':
    #      x, y,  predators                                       ourPred,                       prey,         prey/pred Loc, maxIter, speed, speed, output
    GP = GreedyPredator
    TAP = TeammateAwarePredator
    PMGP = PsuedoMCTSGreedyPredRandomPrey
    PMTAP = PsuedoMCTSTeammatePredRandomPrey
    Prey = SmartPrey1
    tests = [""] * 8
    testNames = [""] * 8
    
    # 100 4 greedy
    '''
    tests[0] = (5, 5, [GP,GP, GP, GP],[RandomPrey], None, None, 25, 1, 1, False)
    # 100 3 greedy, 1 team
    tests[1] = (5, 5, [GP,GP, GP, TAP],[RandomPrey], None, None, 25, 1, 1, False)
    # 100 4 team
    tests[2] = (5, 5, [TAP,TAP, TAP, TAP],[RandomPrey], None, None, 25, 1, 1, False)
    # 100 3 team, 1 greedy
    tests[3] = (5, 5, [TAP,TAP, TAP, GP],[RandomPrey], None, None, 25, 1, 1, False)
    #10x10
    # 50 4 greedy
    tests[4] = (10, 10, [GP,GP, GP, GP],[RandomPrey], None, None, 100, 1, 1, False)
    # 50 3 greedy, 1 team
    tests[5] = (10, 10, [GP,GP, GP, TAP],[RandomPrey], None, None, 100, 1, 1, False)
    # 50 4 team
    tests[6] = (10, 10, [TAP,TAP, TAP, TAP],[RandomPrey], None, None, 100, 1, 1, False)
    # 50 3 team, 1 greedy
    tests[7] = (10, 10, [TAP,TAP, TAP, GP],[RandomPrey], None, None, 100, 1, 1, False)
    '''
    
#5x5
    # 100 3 greedy, 1 mcts greedy, 
    tests[0] = (5, 5, [GP,GP, GP, PMGP],[Prey], None, None, 25, 1, 1, False)
    testNames[0] = "5x5 100 3 greedy 1 mcts greedy,\n"
    
    # 100 3 greedy, 1 mcts team, 
    tests[1] = (5, 5, [GP,GP, GP, PMTAP],[Prey], None, None, 25, 1, 1, False)
    testNames[1] = "5x5 100 3 greedy 1 mcts team,\n"
    
    # 100 3 team, 1 mcts greedy
    tests[2] = (5, 5, [TAP,TAP, TAP, PMGP],[Prey], None, None, 25, 1, 1, False)
    testNames[2] = "5x5 100 3 team 1 mcts greedy,\n"
    
    # 100 3 team, 1 mcts team
    tests[3] = (5, 5, [TAP,TAP, TAP, PMTAP],[Prey], None, None, 25, 1, 1, False)
    testNames[3] = "5x5 100 3 team 1 mcts team,\n"

#10x10
    # 50 3 greedy, 1 mcts greedy, 
    tests[4] = (10, 10, [GP,GP, GP, PMGP],[Prey], None, None, 100, 1, 1, False)
    testNames[4] = "10x10 100 3 greedy 1 mcts greedy,\n"
    
    # 50 3 greedy, 1 mcts team, 
    tests[5] = (10, 10, [GP,GP, GP, PMTAP],[Prey], None, None, 100, 1, 1, False)
    testNames[5] = "10x10 100 3 greedy 1 mcts team,\n"
    
    # 5 3 team, 1 mcts greedy
    tests[6] = (10, 10, [TAP,TAP, TAP, PMGP],[Prey], None, None, 100, 1, 1, False)
    testNames[6] = "10x10 100 3 team 1 mcts greedy,\n"
    
    # 50 3 team, 1 mcts team
    tests[7] = (10, 10, [TAP,TAP, TAP, PMTAP],[Prey], None, None, 100, 1, 1, False)
    testNames[7] = "10x10 100 3 team 1 mcts team,\n"
    
# end
    
    
    numberRuns = 100

    testList = [[0] * numberRuns] * 8
    pool = multiprocessing.Pool(processes=6)
    for i in range(len(tests)):
        #code for only running 50 iters for 10x10
        if i > 3:
            numberRuns = 50
        temp = [tests[i]] * numberRuns
        testList[i] = pool.map(main2, temp)
        
        # removes list brackets
        strOutput = testNames[i] + str(testList)[i][1:-1]

        f = open('output.txt', "a")
        f.write(strOutput + "\n")
        f.close()
        print("Run [" + str(i) + "] done")
    '''
    for i in range(3):
        a = [1,2,3,5,6,78,89]
        f = open('output.txt', "a")
        f.write(str(a) + "\n")
        f.close()
    '''


# 100 3 greedy, 1 mcts greedy, 5 iter sim (if time)
# 100 3 greedy, 1 mcts greedy, 10 iter sim
# 100 3 greedy, 1 mcts greedy, 50 iter sim (if time)
# 100 3 greedy, 1 mcts greedy, 100 iter sim
# 100 3 greedy, 1 mcts greedy, 500 iter sim (if time)

# 100 3 greedy, 1 mcts team, 5 iter sim (if time)
# 100 3 greedy, 1 mcts team, 10 iter sim
# 100 3 greedy, 1 mcts team, 50 iter sim (if time)
# 100 3 greedy, 1 mcts team, 100 iter sim
# 100 3 greedy, 1 mcts team, 500 iter sim (if time)
# 

# 100 3 team, 1 mcts greedy, 5 iter sim (if time)
# 100 3 team, 1 mcts greedy, 10 iter sim
# 100 3 team, 1 mcts greedy, 50 iter sim (if time)
# 100 3 team, 1 mcts greedy, 100 iter sim
# 100 3 team, 1 mcts greedy, 500 iter sim (if time)

# 100 3 team, 1 mcts team, 5 iter sim (if time)
# 100 3 team, 1 mcts team, 10 iter sim
# 100 3 team, 1 mcts team, 50 iter sim (if time)
# 100 3 team, 1 mcts team, 100 iter sim
# 100 3 team, 1 mcts team, 500 iter sim (if time)
# 
# Figure 3(b)
# 10x10
# maxIt = 100
# -- rand prey

# 50 3 greedy, 1 mcts greedy, 5 iter sim (if time)
# 50 3 greedy, 1 mcts greedy, 10 iter sim
# 50 3 greedy, 1 mcts greedy, 50 iter sim (if time)
# 50 3 greedy, 1 mcts greedy, 100 iter sim
# 50 3 greedy, 1 mcts greedy, 500 iter sim (if time)

# 50 3 greedy, 1 mcts team, 5 iter sim (if time)
# 50 3 greedy, 1 mcts team, 10 iter sim
# 50 3 greedy, 1 mcts team, 50 iter sim (if time)
# 50 3 greedy, 1 mcts team, 100 iter sim
# 50 3 greedy, 1 mcts team, 500 iter sim (if time)
# 

# 50 3 team, 1 mcts greedy, 5 iter sim (if time)
# 50 3 team, 1 mcts greedy, 10 iter sim
# 50 3 team, 1 mcts greedy, 50 iter sim (if time)
# 50 3 team, 1 mcts greedy, 100 iter sim
# 50 3 team, 1 mcts greedy, 500 iter sim (if time)

# 50 3 team, 1 mcts team, 5 iter sim (if time)
# 50 3 team, 1 mcts team, 10 iter sim
# 50 3 team, 1 mcts team, 50 iter sim (if time)
# 50 3 team, 1 mcts team, 100 iter sim
# 50 3 team, 1 mcts team, 500 iter sim (if time)






























































    #PsuedoMCTS
    if 1 == 2:
        print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSGreedyPredRandomPrey],[RandomPrey], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 50)))
        print("num iter: " + str(main(5, 5, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, PsuedoMCTSTeammatePredRandomPrey],[RandomPrey], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 50)))
        print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSGreedyPredSmartPrey1],[SmartPrey1], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
        print("num iter: " + str(main(10, 10, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, PsuedoMCTSTeammatePredSmartPrey1],[SmartPrey1], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
        print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSGreedyPredSmartPrey2],[SmartPrey2], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
        print("num iter: " + str(main(10, 10, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, PsuedoMCTSTeammatePredSmartPrey2],[SmartPrey2], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
        print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSGreedyPredSmartPrey3],[SmartPrey3], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
        print("num iter: " + str(main(10, 10, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, PsuedoMCTSTeammatePredSmartPrey3],[SmartPrey3], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))

    #Smart
    '''
        print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator, GreedyPredator, SmartGreedyPredRandomPrey],[RandomPrey], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 50)))
        print("num iter: " + str(main(5, 5, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, SmartTeammatePredRandomPrey],[RandomPrey], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 50)))
        print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, SmartGreedyPredSmartPrey1],[SmartPrey1], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
        print("num iter: " + str(main(5, 5, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, SmartTeammatePredSmartPrey1],[SmartPrey1], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 20)))
        print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator, GreedyPredator, SmartGreedyPredSmartPrey2],[SmartPrey2], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 20)))
        print("num iter: " + str(main(5, 5, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, SmartTeammatePredSmartPrey2],[SmartPrey2], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 20)))
        print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator, GreedyPredator, SmartGreedyPredSmartPrey3],[SmartPrey3], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 20)))
        print("num iter: " + str(main(5, 5, [TeammateAwarePredator,TeammateAwarePredator, TeammateAwarePredator, SmartTeammatePredSmartPrey3],[SmartPrey3], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(3,0)], maxIter = 20)))
    '''
