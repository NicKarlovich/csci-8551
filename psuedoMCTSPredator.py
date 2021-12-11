from predator_prey import *
from psuedoMCTSNode import *

class PsuedoMCTSPredator(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.resetNode()
        self.otherPredType = None
        self.preyType = None

    def setPredPrey(self, pred, prey):
        self.otherPredType = pred
        self.preyType = prey

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

    def nextToPrey(self, preyX, preyY):
        if self.x == preyX:
            if self.tauCoords(0,self.y - 1)[1] == preyY:
                return True
            elif self.tauCoords(0,self.y + 1)[1] == preyY:
                return True
        elif self.y == preyY:
            if self.tauCoords(self.x - 1, 0)[0] == preyX:
                return True
            elif self.tauCoords(self.x + 1, 0)[0] == preyX:
                return True
        return False

    def createSimulatedSelf(self):
            temp = self.otherPredType(0,0,0,0,self.id)
            temp.speed = self.speed
            temp.x = self.x
            temp.y = self.y
            temp.map = self.map
            temp.id = self.id
            return temp
    
    def dimDirectionChooser(self):
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
        numIter = 100
        MAX_RUNTIME = 10
        avgMoves = [0] * 4
        avgMoveDest = []
        currentPrey = self.map.getPrey()
        currentPreds = self.map.getPredators()
        currentPredLocations = self.map.getPredatorLocations().copy()
        simPrey = []
        for prey in currentPrey:
            simPrey.append(prey.createSimulatedSelf())

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
                outArr[j] = 1 + main(self.map.x_len, self.map.y_len, [self.otherPredType] * 4, [self.preyType], preyLocArray = preyLoc, predLocArray= predLoc, output = False, maxIter = MAX_RUNTIME)
                #outArr[j] = 1 + main(self.map.x_len, self.map.y_len, [GreedyPredator] * 4, [RandomPrey], preyLocArray = preyLoc, predLocArray= predLoc, output = False, maxIter = MAX_RUNTIME)
                
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

# Greedy Predators
class PsuedoMCTSGreedyPredRandomPrey(PsuedoMCTSPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.resetNode()
        self.setPredPrey(GreedyPredator, RandomPrey)

class PsuedoMCTSGreedyPredSmartPrey1(PsuedoMCTSPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.resetNode()
        self.setPredPrey(GreedyPredator, SmartPrey1)

class PsuedoMCTSGreedyPredSmartPrey2(PsuedoMCTSPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.resetNode()
        self.setPredPrey(GreedyPredator, SmartPrey2)

class PsuedoMCTSGreedyPredSmartPrey3(PsuedoMCTSPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.resetNode()
        self.setPredPrey(GreedyPredator, SmartPrey3)

########################################################################
# Teammate Aware Predators
########################################################################
class PsuedoMCTSTeammatePredRandomPrey(PsuedoMCTSPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.resetNode()
        self.setPredPrey(TeammateAwarePredator, RandomPrey)

class PsuedoMCTSTeammatePredSmartPrey1(PsuedoMCTSPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.resetNode()
        self.setPredPrey(TeammateAwarePredator, SmartPrey1)

class PsuedoMCTSTeammatePredSmartPrey2(PsuedoMCTSPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.resetNode()
        self.setPredPrey(TeammateAwarePredator, SmartPrey2)

class PsuedoMCTSTeammatePredSmartPrey3(PsuedoMCTSPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.resetNode()
        self.setPredPrey(TeammateAwarePredator, SmartPrey3)