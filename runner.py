from random import Random
from predator_prey import *
from psuedoMCTSPredator import PsuedoMCTSGreedyPredRandomPrey, PsuedoMCTSGreedyPredSmartPrey1, PsuedoMCTSGreedyPredSmartPrey2, PsuedoMCTSGreedyPredSmartPrey3, PsuedoMCTSGreedyPredSmartPrey4
from psuedoMCTSPredator import PsuedoMCTSTeammatePredRandomPrey, PsuedoMCTSTeammatePredSmartPrey1, PsuedoMCTSTeammatePredSmartPrey2, PsuedoMCTSTeammatePredSmartPrey3, PsuedoMCTSTeammatePredSmartPrey4

from psuedoMCTSNode import *

import multiprocessing
import time

# Variables:
board_sizes = [5, 10, 20]
types_of_predators = [
    [ GreedyPredator, TeammateAwarePredator ],
    [ 
        [ PsuedoMCTSGreedyPredRandomPrey, PsuedoMCTSGreedyPredSmartPrey1, PsuedoMCTSGreedyPredSmartPrey2, PsuedoMCTSGreedyPredSmartPrey3, PsuedoMCTSGreedyPredSmartPrey4],
        [ PsuedoMCTSTeammatePredRandomPrey, PsuedoMCTSTeammatePredSmartPrey1, PsuedoMCTSTeammatePredSmartPrey2, PsuedoMCTSTeammatePredSmartPrey3, PsuedoMCTSTeammatePredSmartPrey4]
    ]
]

types_of_prey = [RandomPrey, SmartPrey1, SmartPrey2, SmartPrey3]

# Testing
GP = GreedyPredator
TAP = TeammateAwarePredator
PMGPR = PsuedoMCTSGreedyPredRandomPrey
PMGPS1 = PsuedoMCTSGreedyPredSmartPrey1
PMGPS2 = PsuedoMCTSGreedyPredSmartPrey2
PMGPS3 = PsuedoMCTSGreedyPredSmartPrey3
PMGPS4 = PsuedoMCTSGreedyPredSmartPrey4
PMTAPR = PsuedoMCTSTeammatePredRandomPrey
PMTAPS1 = PsuedoMCTSTeammatePredSmartPrey1
PMTAPS2 = PsuedoMCTSTeammatePredSmartPrey2
PMTAPS3 = PsuedoMCTSTeammatePredSmartPrey3
PMTAPS4 = PsuedoMCTSTeammatePredSmartPrey4
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

def getTestVals(PreyType):
    tests = [""] * 16
    testNames = [""] * 16

    fiveByFiveNumIter = 35
    tenByTenNumIter = 120

    if PreyType == RandomPrey:
        PMGP = PMGPR
        PMTAP = PMTAPR
    if PreyType == SmartPrey1:
        PMGP = PMGPS1
        PMTAP = PMTAPS1
    if PreyType == SmartPrey2:
        PMGP = PMGPS2
        PMTAP = PMTAPS2
    if PreyType == SmartPrey3:
        PMGP = PMGPS3
        PMTAP = PMTAPS3
    if PreyType == SmartPrey4:
        PMGP = PMGPS4
        PMTAP = PMTAPS4
#5x5
    # 100 4 greedy
    tests[0] = (5, 5, [GP,GP, GP, GP],[PreyType], None, None, fiveByFiveNumIter, 1, 1, False)
    testNames[0] = "5x5 100 4 greedy,\n"
    
    # 100 3 greedy, 1 team
    tests[1] = (5, 5, [GP,GP, GP, TAP],[PreyType], None, None, fiveByFiveNumIter, 1, 1, False)
    testNames[1] = "5x5 100 3 greedy 1 team,\n"
    
    # 100 4 team
    tests[2] = (5, 5, [TAP,TAP, TAP, TAP],[PreyType], None, None, fiveByFiveNumIter, 1, 1, False)
    testNames[2] = "5x5 100 4 team,\n"
    
    # 100 3 team, 1 greedy
    tests[3] = (5, 5, [TAP,TAP, TAP, GP],[PreyType], None, None, fiveByFiveNumIter, 1, 1, False)
    testNames[3] = "5x5 100 3 team 1 greedy,\n"
    
    # 100 3 greedy, 1 mcts greedy, 
    tests[4] = (5, 5, [GP,GP, GP, PMGP],[PreyType], None, None, fiveByFiveNumIter, 1, 1, False)
    testNames[4] = "5x5 100 3 greedy 1 mcts greedy,\n"
    
    # 100 3 greedy, 1 mcts team, 
    tests[5] = (5, 5, [GP,GP, GP, PMTAP],[PreyType], None, None, fiveByFiveNumIter, 1, 1, False)
    testNames[5] = "5x5 100 3 greedy 1 mcts team,\n"
    
    # 100 3 team, 1 mcts greedy
    tests[6] = (5, 5, [TAP,TAP, TAP, PMGP],[PreyType], None, None, fiveByFiveNumIter, 1, 1, False)
    testNames[6] = "5x5 100 3 team 1 mcts greedy,\n"
    
    # 100 3 team, 1 mcts team
    tests[7] = (5, 5, [TAP,TAP, TAP, PMTAP],[PreyType], None, None, fiveByFiveNumIter, 1, 1, False)
    testNames[7] = "5x5 100 3 team 1 mcts team,\n"

#10x10
    # 50 4 greedy
    tests[8] = (10, 10, [GP,GP, GP, GP],[PreyType], None, None, tenByTenNumIter, 1, 1, False)
    testNames[8] = "10x10 50 4 greedy,\n"
    
    # 50 3 greedy, 1 team
    tests[9] = (10, 10, [GP,GP, GP, TAP],[PreyType], None, None, tenByTenNumIter, 1, 1, False)
    testNames[9] = "10x10 50 3 greedy 1 team,\n"

    # 50 4 team
    tests[10] = (10, 10, [TAP,TAP, TAP, TAP],[PreyType], None, None, tenByTenNumIter, 1, 1, False)
    testNames[10] = "10x10 50 4 team,\n"
    
    # 50 3 team, 1 greedy
    tests[11] = (10, 10, [TAP,TAP, TAP, GP],[PreyType], None, None, tenByTenNumIter, 1, 1, False)
    testNames[11] = "10x10 50 3 team 1 greedy,\n"
    
    # 50 3 greedy, 1 mcts greedy, 
    tests[12] = (10, 10, [GP,GP, GP, PMGP],[PreyType], None, None, tenByTenNumIter, 1, 1, False)
    testNames[12] = "10x10 100 3 greedy 1 mcts greedy,\n"
    
    # 50 3 greedy, 1 mcts team, 
    tests[13] = (10, 10, [GP,GP, GP, PMTAP],[PreyType], None, None, tenByTenNumIter, 1, 1, False)
    testNames[13] = "10x10 100 3 greedy 1 mcts team,\n"
    
    # 5 3 team, 1 mcts greedy
    tests[14] = (10, 10, [TAP,TAP, TAP, PMGP],[PreyType], None, None, tenByTenNumIter, 1, 1, False)
    testNames[14] = "10x10 100 3 team 1 mcts greedy,\n"
    
    # 50 3 team, 1 mcts team
    tests[15] = (10, 10, [TAP,TAP, TAP, PMTAP],[PreyType], None, None, tenByTenNumIter, 1, 1, False)
    testNames[15] = "10x10 100 3 team 1 mcts team,\n"

    return tests,testNames


def runTests(tests,testNames):
    numberRuns = 100

    testList = [[0] * numberRuns] * 16
    pool = multiprocessing.Pool(processes=80)
    for i in range(len(tests)):
        #code for only running 50 iters for 10x10
        if i > 3:
            numberRuns = 50
        temp = [tests[i]] * numberRuns
        testList[i] = pool.map(main2, temp)
        
        # removes list brackets
        strOutput = testNames[i] + str(testList[i][1:-1])

        f = open('output.txt', "a")
        f.write(strOutput + "\n")
        f.close()
        print("Run [" + str(i) + "] done")


if __name__ == '__main__':
    #      x, y,  predators                                       ourPred,                       prey,         prey/pred Loc, maxIter, speed, speed, output
		# already ran, in output already
    #tests,testNames = getTestVals(RandomPrey)
    #runTests(tests,testNames)

    tests,testNames = getTestVals(SmartPrey1)
    runTests(tests,testNames)

    tests,testNames = getTestVals(SmartPrey2)
    runTests(tests,testNames)

    tests,testNames = getTestVals(SmartPrey3)
    runTests(tests,testNames)

    tests,testNames = getTestVals(SmartPrey4)
    runTests(tests,testNames)


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

