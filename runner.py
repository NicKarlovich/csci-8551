from predator_prey import *
import math
import numpy

#Unused
class MCTSNode:
    def __init__(self):
        self.numWins = 0
        self.numTrials = 0
        self.ucb = math.inf
        self.numMoves = -1
        # references to other MCTS nodes
        self.parent = None
        self.left = None
        self.right = None
        self.up = None
        self.down = None
    
    def addWin(self):
        self.numWins += 1
        self.numTrials += 1
        if self.parent != None:
            self.parent.addWin()
    
    def addLoss(self):
        self.numTrials += 1
        if self.parent != None:
            self.parent.addLoss()

    def getParent(self):
        return self.parent

    def getNumTrials(self):
        return self.numTrials

    def getUCB(self):
        return self.ucb

    def updateUCB(self):
        if self.parent == None:
            print("can't update UCB without parent, is this the root?")
        else: 
            if self.numTrials != 0:
                self.ucb = self.numWins / self.numTrials + math.sqrt((2 * math.log(self.parent.getNumTrials())) / self.numTrials )
    
    def createChildren(self):
        if self.left == None:
            self.left = MCTSNode()
            self.left.parent = self
        if self.right == None:
            self.right = MCTSNode()
            self.right.parent = self
        if self.up == None:
            self.up = MCTSNode()
            self.up.parent = self
        if self.down == None:
            self.down = MCTSNode()
            self.down.parent = self

class PsuedoMCTSNode:
    def __init__(self):
        self.score = 0
        self.numTrials = 0
        self.ucb = math.inf
        # references to other MCTS nodes
        self.parent = None
        self.level = 0 #if level = 0, its root, == 1 pred move, ==2 prey move
        self.west = None
        self.east = None
        self.north = None
        self.south = None
    
    def getNumTrialsOfChildren(self):
        return [self.north.numTrials, self.south.numTrials, self.east.numTrials, self.west.numTrials]

    def printMCTSTree(self):
        print("root: ")
        print("score / trials: " + str(self.score) + " / " + str(self.numTrials))
        print("ucb: " + str(self.ucb))

        print("north: ")
        print("score / trials: " + str(self.north.score) + " / " + str(self.north.numTrials))
        print("ucb: " + str(self.north.ucb))

        print("south: ")
        print("score / trials: " + str(self.south.score) + " / " + str(self.south.numTrials))
        print("ucb: " + str(self.south.ucb))

        print("east: ")
        print("score / trials: " + str(self.east.score) + " / " + str(self.east.numTrials))
        print("ucb: " + str(self.east.ucb))

        print("west: ")
        print("score / trials: " + str(self.west.score) + " / " + str(self.west.numTrials))
        print("ucb: " + str(self.west.ucb))

    def addScore(self, score):
        self.score += score
        self.numTrials += 1
        if self.parent != None:
            self.parent.addScore(score)

    def setLevel(self, level):
        self.level = level

    def getParent(self):
        return self.parent

    def getNumTrials(self):
        return self.numTrials

    def getUCB(self):
        return self.ucb

    def getChildrenUCB(self):
        return [self.north.getUCB(), self.south.getUCB(), self.east.getUCB(), self.west.getUCB()]

    def updateUCB(self):
        if self.parent == None:
            print("can't update UCB without parent, is this the root?")
        else: 
            if self.numTrials != 0:
                self.ucb = self.score / self.numTrials + math.sqrt((2 * math.log(self.parent.getNumTrials())) / self.numTrials )
    
    def setChildLevel(self, level):
        self.north.level = level
        self.south.level = level
        self.east.level = level
        self.west.level = level

    def addScoresToChildren(self, scores):
        self.north.addScore(scores[0])
        self.south.addScore(scores[1])
        self.east.addScore(scores[2])
        self.west.addScore(scores[3])

    def createChildren(self):
        if self.north == None:
            self.north = PsuedoMCTSNode()
            self.north.parent = self
        if self.south == None:
            self.south = PsuedoMCTSNode()
            self.south.parent = self
        if self.east == None:
            self.east = PsuedoMCTSNode()
            self.east.parent = self
        if self.west == None:
            self.west = PsuedoMCTSNode()
            self.west.parent = self


class PsuedoMCTSGreedyPredator(GreedyPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.root = PsuedoMCTSNode()
        self.root.createChildren()
        self.root.setChildLevel(1)

        self.root.north.createChildren()
        self.root.south.createChildren()
        self.root.east.createChildren()
        self.root.west.createChildren()
        self.root.north.setChildLevel(2)
        self.root.south.setChildLevel(2)
        self.root.east.setChildLevel(2)
        self.root.west.setChildLevel(2)

    def resetNode(self):
        self.root = PsuedoMCTSNode()
        self.root.createChildren()
        self.root.setChildLevel(1)

        self.root.north.createChildren()
        self.root.south.createChildren()
        self.root.east.createChildren()
        self.root.west.createChildren()
        self.root.north.setChildLevel(2)
        self.root.south.setChildLevel(2)
        self.root.east.setChildLevel(2)
        self.root.west.setChildLevel(2)

    def createSimulatedSelf(self):
        #temp = SimulatedGreedyPredator(0,0,0,0,0)
        temp = GreedyPredator(0,0,0,0,0)
        temp.speed = self.speed
        temp.x = self.x
        temp.y = self.y
        temp.map = self.map
        temp.id = self.id
        return temp

    def dimDirectionChooser(self):
        #goalDestination = self.findClosestDestination()[2]
        x = self.SimulatePredator()
        return x

    def determineMoveOfUs(self, baseEntry, methodology="ucb"):
        maxV = -math.inf
        if methodology == "ucb":
            values = self.root.getChildrenUCB()
        else:
            values = self.root.getNumTrialsOfChildren()
        i = 0
        index = i
        for x in values:
            if x > maxV:
                maxV = x
                index = i
            i += 1
        #index now stores the index of the maximum value
        #determining what move to make on X
        attemptMove = (-1, -1)
        if index == 0:
            attemptMove = self.tauCoords(baseEntry[0], baseEntry[1] + 1)
        if index == 1:
            attemptMove = self.tauCoords(baseEntry[0], baseEntry[1] - 1)
        if index == 2:
            attemptMove = self.tauCoords(baseEntry[0] + 1, baseEntry[1])
        if index == 3:
            attemptMove = self.tauCoords(baseEntry[0] - 1, baseEntry[1])
        return (attemptMove, index)

    def SimulatePredator(self):
        self.resetNode()
        numIter = 5000
        MAX_RUNTIME = 20
        avgMoves = [0] * 4
        avgMoveDest = []
        currentPrey = self.map.getPrey()
        currentPreds = self.map.getPredators()
        currentPredLocations = self.map.getPredatorLocations().copy()
        simPrey = []
        for prey in currentPrey:
            simPrey.append(prey.createSimulatedSelf())
        '''
        simPred = [None] * len(currentPreds)
        simPred[0] = currentPreds[0].createSimulatedSelf()
        simPred[1] = currentPreds[1].createSimulatedSelf()
        simPred[2] = currentPreds[2].createSimulatedSelf()
        simPred[3] = currentPreds[3].createSimulatedSelf()
        '''
        #for i in range(len(currentPreds)):
        #    simPred[i] = currentPreds[i].createSimulatedSelf()
        simPred = []
        for pred in currentPreds:
            simPred.append(pred.createSimulatedSelf())

        for i in range(0, numIter):
            index = -1
            p = 0
            for pred in currentPreds:
                if pred.getId() == self.getId():
                    index = p
                p += 1
            baseEntry = currentPredLocations[index] #index should always be the last predator
            (attemptMove, dir) = self.determineMoveOfUs(baseEntry, "ucb")
            # prey's random move
            baseCoord = simPrey[0].getLocation()
            outArr = [0, 0, 0, 0]
            for j in range(4):
                if j == 0:
                    move = self.tauCoords(baseCoord[0], baseCoord[1] + 1)
                if j == 1:
                    move = self.tauCoords(baseCoord[0], baseCoord[1] - 1)
                if j == 2:
                    move = self.tauCoords(baseCoord[0] + 1, baseCoord[1])
                if j == 3:
                    move = self.tauCoords(baseCoord[0] - 1, baseCoord[1])

                #Get result of moving prey
                preyLoc = self.map.getPreyLocations().copy()
                predLoc = self.map.getPredatorLocations().copy()
                if move not in preyLoc and move not in predLoc:
                    preyLoc = [move]

                #Pred making moves, ignoring last entry
                predatorMoves = []
                for predator in simPred:
                    predatorMoves.append(self.map.taurusCoord(predator.chooseDestination()))
                
                #get ending locations of moving predator
                # predators then move, don't move if spot already taken
                for k in range(len(predatorMoves) - 1): #-1 because we don't want to deal with the last predator, because that's out simulated boy who's direction is determined by another function
                    predator = self.map.predators[k]
                    move = predatorMoves[k]
                    if move not in preyLoc and move not in predLoc:
                        predLoc[k] = move
                # filling in the last entry in the predLoc array
                #determining index of our mcts, should be last
                if attemptMove not in preyLoc and attemptMove not in predLoc:
                    predLoc[index] = attemptMove
                
                outArr[j] = 1 + main(self.map.x_len, self.map.y_len, [GreedyPredator] * 4, [RandomPrey], preyLocArray = preyLoc, predLocArray= predLoc, output = False, maxIter = MAX_RUNTIME)
                
            # "MCTS Win function"
            for a in range(len(outArr)):
                if outArr[a] == 0: #means the program didnt' finish
                    outArr[a] = 0 #redundant ik
                else:
                    outArr[a] = 1 - (outArr[a] / MAX_RUNTIME)

            if dir == 0:
                self.root.north.addScoresToChildren(outArr)
            if dir == 1:
                self.root.south.addScoresToChildren(outArr)
            if dir == 2:
                self.root.east.addScoresToChildren(outArr)
            if dir == 3:
                self.root.west.addScoresToChildren(outArr)

            self.root.north.updateUCB()
            self.root.south.updateUCB()
            self.root.east.updateUCB()
            self.root.west.updateUCB()

            #self.root.printMCTSTree()
        '''
            for j in range(numIter):
                # add 1 because we basically simulated the above step
                #numMoves = 1 + main(self.map.x_len, self.map.y_len, [GreedyPredator] * 4, [RandomPrey], preyLocArray = preyLoc, predLocArray = predLoc, output = False, maxIter = MAX_RUNTIME)
                numMoves = 1 + main(self.map.x_len, self.map.y_len, [GreedyPredator] * 4, [RandomPrey], preyLocArray = preyLoc, predLocArray = predLoc, output = False, maxIter = MAX_RUNTIME)
                if numMoves == 0: #0 = 1 + -1(-1 from main failing)
                    numMoves = 2 * MAX_RUNTIME #if it wasn't solved, penalize even more for this solution may never have even solved
                avgMoves[i] += numMoves
        '''
        (attempt, aa) = self.determineMoveOfUs(baseEntry, "anything else")
        
        print('best move found (via MCTS):' + str(attempt))
        self.root.printMCTSTree()
        return attempt  

    def chooseDestination(self):
        x = self.map.getPreyLocations()
        if x == []: # if there's no prey, don't move anywhere.
            out = (self.x, self.y)
        else:
            #get prey location
            [(x, y)] = self.map.getPreyLocations()

            #If already neighboring the prey, try to move onto the prey so that if it moves, the predator will follow.
            #if self.nextToPrey(x, y):
            if False:
                out = (x, y)
            else: 
                out = self.dimDirectionChooser()
        print("agent: " + str(self.id) + " is going to: " + str(out))
        return out

class SmartGreedyPredator(GreedyPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    def createSimulatedSelf(self):
        #temp = SimulatedGreedyPredator(0,0,0,0,0)
        temp = GreedyPredator(0,0,0,0,0)
        temp.speed = self.speed
        temp.x = self.x
        temp.y = self.y
        temp.map = self.map
        temp.id = self.id
        return temp

    def dimDirectionChooser(self):
        #goalDestination = self.findClosestDestination()[2]
        x = self.SimulatePredator()
        return x

    def SimulatePredator(self):
        numIter = 100
        avgMoves = [0] * 4
        avgMoveDest = []
        currentPrey = self.map.getPrey()
        currentPreds = self.map.getPredators()
        currentPredLocations = self.map.getPredatorLocations().copy()
        simPrey = []
        for prey in currentPrey:
            simPrey.append(prey.createSimulatedSelf())

        simPred = [None] * len(currentPreds)
        simPred[0] = currentPreds[0].createSimulatedSelf()
        simPred[1] = currentPreds[1].createSimulatedSelf()
        simPred[2] = currentPreds[2].createSimulatedSelf()
        simPred[3] = currentPreds[3].createSimulatedSelf()
        #for i in range(len(currentPreds)):
        #    simPred[i] = currentPreds[i].createSimulatedSelf()
        #for pred in currentPreds:
            #simPred.append(pred.createSimulatedSelf())

        index = -1
        i = 0
        MAX_RUNTIME = 20
        for pred in currentPreds:
            if pred.getId() == self.getId():
                index = i
            i += 1
        baseEntry = currentPredLocations[index] #index should always be the last predator

        #Get where prey wants to go
        preyMoves = []
        for prey in simPrey:
            preyMoves.append(self.map.taurusCoord(prey.chooseDestination()))

        #Determine where preds want to go, eventually going to ignore last entry since
        # that'll be our agent and we want to choose where it goes.
        predatorMoves = []
        for predator in simPred:
            predatorMoves.append(self.map.taurusCoord(predator.chooseDestination()))

        #Get result of moving prey
        preyLoc = self.map.getPreyLocations().copy()
        predLoc = self.map.getPredatorLocations().copy()
        for i in range(len(preyMoves)):
            prey = self.map.prey[i]
            move = preyMoves[i]
            if move not in preyLoc and move not in predLoc:
                preyLoc = [move]
                #move = prey.getLocation() #set "after move" location to not change, because current move failed
                #preyLoc.append(move)

        #get ending locations of moving predator
        # predators then move, don't move if spot already taken
        for i in range(len(predatorMoves) - 1): #-1 because we don't want to deal with the last predator, because that's out simulated boy who's direction is determined by another function
            predator = self.map.predators[i]
            move = predatorMoves[i]
            if move not in preyLoc and move not in predLoc:
                predLoc[i] = move
            '''
            if move in preyLoc or move in predLoc:
                predLoc[i] = predator.getLocation()
            else:
                predLoc[i] = move
                '''

        for i in range(4):
            #modify our direction
            attemptMove = (-1, -1)
            '''
            if i == 0:
                attemptMove = self.tauCoords(baseEntry[0] + 1, baseEntry[1])
            if i == 1:
                attemptMove = self.tauCoords(baseEntry[0] - 1, baseEntry[1])
            if i == 2:
                attemptMove = self.tauCoords(baseEntry[0], baseEntry[1] + 1)
            if i == 3:
                attemptMove = self.tauCoords(baseEntry[0], baseEntry[1] - 1)
            '''
            if i == 2:
                attemptMove = self.tauCoords(baseEntry[0] + 1, baseEntry[1])
            if i == 3:
                attemptMove = self.tauCoords(baseEntry[0] - 1, baseEntry[1])
            if i == 0:
                attemptMove = self.tauCoords(baseEntry[0], baseEntry[1] + 1)
            if i == 1:
                attemptMove = self.tauCoords(baseEntry[0], baseEntry[1] - 1)
            avgMoveDest.append(attemptMove)
            print('attempt move: ' + str(i) + " " + str(attemptMove))
            if attemptMove not in preyLoc and attemptMove not in predLoc:
                predLoc[index] = attemptMove
            # if attempted move not in trouble, make it the move
            # else:, predLoc[index] is already filled with it's current location so no need to update it.

            for j in range(numIter):
                # add 1 because we basically simulated the above step
                #numMoves = 1 + main(self.map.x_len, self.map.y_len, [GreedyPredator] * 4, [RandomPrey], preyLocArray = preyLoc, predLocArray = predLoc, output = False, maxIter = MAX_RUNTIME)
                numMoves = 1 + main(self.map.x_len, self.map.y_len, [GreedyPredator] * 4, [RandomPrey], preyLocArray = preyLoc, predLocArray = predLoc, output = False, maxIter = MAX_RUNTIME)
                if numMoves == 0: #0 = 1 + -1(-1 from main failing)
                    numMoves = 2 * MAX_RUNTIME #if it wasn't solved, penalize even more for this solution may never have even solved
                avgMoves[i] += numMoves
            '''
                if attemptMove in currentPredLocations: #if the attempted move already exists, then 
                    avgMoves[i] = math.inf #don't choose a direction you can't move towards
                else: 
                    currentPredLocations[index] = attemptMove
                    print('test')
                    for j in range(numIter):
                        numMoves = main(self.map.x_len, self.map.y_len, [SimulatedGreedyPredator] * 4, [StationaryPrey], (self.map.getPreyLocations()), currentPredLocations, output = False, maxIter = MAX_RUNTIME)
                        if numMoves == MAX_RUNTIME:
                            numMoves *= 2 #if it wasn't solved, penalize even more for this solution may never have even solved
                        avgMoves[i] += numMoves
            '''
        out = math.inf
        idx = -1
        #finding which move resulted in shortest average solve time (least number of iterations)
        for i in range(len(avgMoves)):
            if avgMoves[i] < out:
                out = avgMoves[i]
                idx = i
        temp = avgMoveDest[idx]
        print('best move found (via simulation):' + str(temp))
        print(avgMoves)
        #print(currentPredLocations)
        return temp

                

    def chooseDestination(self):
        x = self.map.getPreyLocations()
        if x == []: # if there's no prey, don't move anywhere.
            out = (self.x, self.y)
        else:
            #get prey location
            [(x, y)] = self.map.getPreyLocations()

            #If already neighboring the prey, try to move onto the prey so that if it moves, the predator will follow.
            if self.nextToPrey(x, y):
                out = (x, y)
            else: 
                out = self.dimDirectionChooser()
        print("agent: " + str(self.id) + " is going to: " + str(out))
        return out

#Unused
class GreedyMCTSPredator(GreedyPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    def dimDirectionChooser(self):
        goalDestination = self.findClosestDestination()[2]

    def chooseDestination(self):
        x = self.map.getPreyLocations()
        if x == []: # if there's no prey, don't move anywhere.
            out = (self.x, self.y)
        else:
            #get prey location
            [(x, y)] = self.map.getPreyLocations()

            #If already neighboring the prey, try to move onto the prey so that if it moves, the predator will follow.
            if self.nextToPrey(x, y):
                out = (x, y)
            else: 
                out = self.dimDirectionChooser()
        return out
'''
    root = MCTSNode()
    left = MCTSNode()
    right = MCTSNode()
    up = MCTSNode()
    down = MCTSNode()
    root.right = right
    root.left = left
    root.up = up
    root.down = down
    right.parent = root
    left.parent = root
    up.parent = root
    down.parent = root

    nodes = [root, left, right, up, down]

    def printUCB():
        for x in nodes:
            print(x.getUCB())

    def updateUCB():
        for x in nodes:
            x.updateUCB()
    printUCB()

    left.addLoss()
    updateUCB()
    printUCB()

    right.addWin()
    updateUCB()
    printUCB()

    up.addWin()
    updateUCB()
    printUCB()

    right.addWin()
    updateUCB()
    printUCB()
'''

#print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator, GreedyPredator, SmartGreedyPredator],[StationaryPrey], [(1,1)], [(0,0),(0,4),(4,4),(4,0)], 50)))
#print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, SmartGreedyPredator],[StationaryPrey], preyLocArray=[(1,1)], predLocArray = None, maxIter = 50)))
print("num iter: " + str(main(10, 10, [GreedyPredator,GreedyPredator, GreedyPredator, PsuedoMCTSGreedyPredator],[RandomPrey], preyLocArray=[(1,1)], predLocArray = [(2,1),(1,2),(0,1),(7,0)], maxIter = 50)))
# print("num iter: " + str(main(5, 5, [GreedyPredator,GreedyPredator,GreedyPredator,
# GreedyPredator],[StationaryPrey], [(1,1)], [(0,0),(0,4),(4,4),(4,0)], 50)))