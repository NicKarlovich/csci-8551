from predator_prey import *
import copy
import math

class SmartPredator(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.otherPredType = None
        self.preyType = None

    def setPredPrey(self, pred, prey):
        self.otherPredType = pred
        self.preyType = prey


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

        simPred = []
        for pred in currentPreds:
            simPred.append(pred.createSimulatedSelf())
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
                numMoves = 1 + main(self.map.x_len, self.map.y_len, [self.otherPredType] * 4, [self.preyType], preyLocArray = preyLoc, predLocArray = predLoc, output = False, maxIter = MAX_RUNTIME)
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
            if False:
                out = (x, y)
            else: 
                out = self.dimDirectionChooser()
        print("agent: " + str(self.id) + " is going to: " + str(out))
        return out

# Greedy Predators
class SmartGreedyPredRandomPrey(SmartPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.setPredPrey(GreedyPredator, RandomPrey)

class SmartGreedyPredSmartPrey1(SmartPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.setPredPrey(GreedyPredator, SmartPrey1)

class SmartGreedyPredSmartPrey2(SmartPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.setPredPrey(GreedyPredator, SmartPrey2)

class SmartGreedyPredSmartPrey3(SmartPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.setPredPrey(GreedyPredator, SmartPrey3)

########################################################################
# Teammate Aware Predators
########################################################################
class SmartTeammatePredRandomPrey(SmartPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.setPredPrey(TeammateAwarePredator, RandomPrey)

class SmartTeammatePredSmartPrey1(SmartPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.setPredPrey(TeammateAwarePredator, SmartPrey1)

class SmartTeammatePredSmartPrey2(SmartPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.setPredPrey(TeammateAwarePredator, SmartPrey2)

class SmartTeammatePredSmartPrey3(SmartPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
        self.setPredPrey(TeammateAwarePredator, SmartPrey3)