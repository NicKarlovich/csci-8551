import matplotlib.pyplot as plt
import time
import random
import math
import numpy

showing = False

# base class for agents
class Agent:
    def __init__(self, speed, x, y, taurusMap, id):
        self.speed = speed
        self.x = x
        self.y = y
        self.map = taurusMap
        self.id = id

    def tauCoords(self, x, y):
        return (x % self.map.x_len, y % self.map.y_len)

    def chooseDestination(self):
        return (self.x+1,self.y)

    def getLocation(self):
        return (self.x,self.y)

    def setLocation(self,x,y):
        self.x = x
        self.y = y

    def getId(self):
        return self.id    
    
    def randomDirection(self):
        direction = random.randint(0, 3)
        if direction == 0: # right
            out = self.tauCoords(self.x + 1, self.y)
        if direction == 1: # left
            out = self.tauCoords(self.x - 1, self.y)
        if direction == 2: # up
            out = self.tauCoords(self.x, self.y + 1)
        if direction == 3: # down
            out = self.tauCoords(self.x, self.y - 1)
        return out

    def softmax(self, valueA, temp, allDirectionsValues):
        num = math.exp(valueA / temp)
        den = 0
        for i in range(0, len(allDirectionsValues)):
            den += (i / temp)
        return num / den


# Stationary prey
# used for testing
class StationaryPrey(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    def createSimulatedSelf(self):
        temp = SimulatedStationaryPrey(0,0,0,0,0)
        temp.speed = self.speed
        temp.x = self.x
        temp.y = self.y
        temp.map = self.map
        temp.id = self.id
        return temp

    def chooseDestination(self):
        return (self.x,self.y)

class SimulatedStationaryPrey(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    def chooseDestination(self):
        return (self.x,self.y)

# Random moving prey
class RandomPrey(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
    
    def createSimulatedSelf(self):
        temp = SimulatedRandomPrey(0,0,0,0,0)
        temp.speed = self.speed
        temp.x = self.x
        temp.y = self.y
        temp.map = self.map
        temp.id = self.id
        return temp

    def chooseDestination(self):
        return self.randomDirection()

# Random moving prey
class SimulatedRandomPrey(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
    
    def chooseDestination(self):
        return self.randomDirection()

class SmartPrey1(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    def chooseDestination(self):
        predLoc = self.map.getPredatorLocations()
        adjPreyLoc = self.map.getAdjacentPreyLocations()[0]

        x_distances = [0,0,0,0]
        y_distances = [0,0,0,0]
        for i in range(len(adjPreyLoc)):
            for j in range(len(predLoc)):
                x_distances[i] += self.map.getXDistance(adjPreyLoc[i],predLoc[j])
                y_distances[i] += self.map.getYDistance(adjPreyLoc[i],predLoc[j])

        maxIndex = 0
        maxVal = -float("inf")
        for i in range(len(x_distances)):
            choice = min(x_distances[i],y_distances[i])
            if choice > maxVal:
                maxVal = choice
                maxIndex = i

        return adjPreyLoc[maxIndex]

class SmartPrey2(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    def chooseDestination(self):
        predLoc = self.map.getPredatorLocations()
        adjPreyLoc = self.map.getAdjacentPreyLocations()[0]

        x_distances = [0,0,0,0]
        y_distances = [0,0,0,0]
        for i in range(len(adjPreyLoc)):
            for j in range(len(predLoc)):
                x_distances[i] += self.map.getXDistance(adjPreyLoc[i],predLoc[j])
                y_distances[i] += self.map.getYDistance(adjPreyLoc[i],predLoc[j])

        maxIndex = 0
        maxVal = -float("inf")
        for i in range(len(x_distances)):
            choice = max(x_distances[i],y_distances[i])
            if choice > maxVal:
                maxVal = choice
                maxIndex = i

        return adjPreyLoc[maxIndex]

class SmartPrey3(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    def chooseDestination(self):
        predLoc = self.map.getPredatorLocations()
        adjPreyLoc = self.map.getAdjacentPreyLocations()[0]

        distances = [0,0,0,0]
        for i in range(len(adjPreyLoc)):
            for j in range(len(predLoc)):
                distances[i] += self.map.getTotalDistance(adjPreyLoc[i],predLoc[j])
                
        maxIndex = 0
        maxVal = -float("inf")
        for i in range(len(x_distances)):
            if distances[i] > maxVal:
                maxVal = distances[i]
                maxIndex = i

        return adjPreyLoc[maxIndex]


# Greedy predator, constantly attempts to move towards prey, follows logic defined in paper
class GreedyPredator(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    #takes in x and y, returns a tuple with the value modulo'd by mapsize
    def tauCoords(self, x, y):
        return (x % self.map.x_len, y % self.map.y_len)

    def totalDistanceToAgent(self, agentLocationTuple):
        xOff = abs(self.xMagnitude(agentLocationTuple[0]))
        yOff = abs(self.yMagnitude(agentLocationTuple[1]))
        return xOff + yOff

    def yMagnitude(self, yPreyLocation):
        #offset = self.y - yPreyLocation
        offset = yPreyLocation - self.y
        
        # the distance to prey location is less than half the board length, 
        # thus it is faster than wrapping around toroidal nature of board 
        if abs(offset) < math.ceil(self.map.y_len / 2):
            yMag = offset
        else:
            # It is faster to wrap around toroidal nature of board to
            # reach goal location, if abs(offset) == math.ceil(...) then it is equal distance to go either 
            # direction.  Happen to choose to swap direction in this implementation, doesn't matter though
            if offset < 0:
                yMag = offset + self.map.y_len
            elif offset > 0:
                yMag = offset - self.map.y_len
            else: #offset == 0
                yMag = 0
        return yMag
        
    def yDirection(self, yPreyLocation):
        yMag = self.yMagnitude(yPreyLocation)
        if yMag < 0:
            dir = -1
        if yMag > 0:
            dir = 1
        if yMag == 0:
            dir = 0
        return dir

    def xMagnitude(self, xPreyLocation):
        #offset = self.x - xPreyLocation
        offset = xPreyLocation - self.x
        
        # the distance to prey location is less than half the board length, 
        # thus it is faster than wrapping around toroidal nature of board 
        if abs(offset) < math.ceil(self.map.x_len / 2):
            xMag = offset
        else:
            # It is faster to wrap around toroidal nature of board to
            # reach goal location, if abs(offset) == math.ceil(...) then it is equal distance to go either 
            # direction.  Happen to choose to swap direction in this implementation, doesn't matter though
            if offset < 0:
                xMag = offset + self.map.x_len
            elif offset > 0:
                xMag = offset - self.map.x_len
            else: #offset == 0
                xMag = 0
        return xMag

    def xDirection(self, xPreyLocation):
        xMag = self.xMagnitude(xPreyLocation)
        if xMag < 0:
            dir = -1
        if xMag > 0:
            dir = 1
        if xMag == 0:
            dir = 0
        return dir

    # Returns (cardinal direction, distance to that direction, coord of closest destination on taurus)
    def findClosestDestination(self):
        x = self.map.getPreyLocations()
        if x == []: # if there's no prey, don't move anywhere.
            return (self.x, self.y)

        [(x, y)] = self.map.getPreyLocations()
                            #N, S, W, E
        unitDirectionArr = [self.tauCoords(x, y + 1), self.tauCoords(x, y - 1), self.tauCoords(x - 1, y), self.tauCoords(x + 1, y)]
        namedDirectionsArr = ['north', 'south', 'west', 'east']
        lengthArr = map(self.totalDistanceToAgent, unitDirectionArr)
        stateOfLocationsArr = map(self.map.returnStateOfCell, unitDirectionArr)
        tempLengthDict = dict(zip(namedDirectionsArr, lengthArr))
        tempStateDict = dict(zip(namedDirectionsArr, stateOfLocationsArr))
        stateDict = {key:val for key, val in tempStateDict.items() if val == "empty"}
        lengthDict = dict(sorted(tempLengthDict.items(), key = lambda x:x[1]))
        coordDict = dict(zip(namedDirectionsArr, unitDirectionArr))

        for k,v in lengthDict.items():
            if k in stateDict.keys():
                coord = coordDict[k]
                return(k, v, coord)
        
        return ('none', -1)

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

    '''
        Next codeblock represents:
        * let d = dim_max, if m_d is not blocked, take it
        * let d = dim_min, if m_d is not blocked, take it

        Outer if-elif statement checks which direction (x or y) has the larger dim_max.  For either case, we 
        then check if the location we want to move is empty. if it is, then we move there, if it isn't, 
        then we go to the direction that is the dim_min since there are only two directions, the other 
        axis will always be the dim_min, so we can then check that direction to see if it's empty, and 
        if it is move to that location.
    '''    
    def dimDirectionChooser(self):
        goalDestination = self.findClosestDestination()[2]
            
        xOff = self.xDirection(goalDestination[0])
        yOff = self.yDirection(goalDestination[1])
        out = ""
        if abs(self.xMagnitude(goalDestination[0])) > abs(self.yMagnitude(goalDestination[1])):
            if self.map.returnStateOfCell(self.tauCoords(self.x + xOff, self.y)) == "empty":
                out = self.tauCoords(self.x + xOff, self.y)
            elif self.map.returnStateOfCell(self.tauCoords(self.x, self.y + yOff)) == "empty":
                out = self.tauCoords(self.x, self.y + yOff)
        elif abs(self.xMagnitude(goalDestination[0])) <= abs(self.yMagnitude(goalDestination[1])):
            if self.map.returnStateOfCell(self.tauCoords(self.x, self.y + yOff)) == "empty": 
                out = self.tauCoords(self.x, self.y + yOff)
            elif self.map.returnStateOfCell(self.tauCoords(self.x + xOff, self.y)) == "empty":
                out = self.tauCoords(self.x + xOff, self.y)
        if out == "": # Otherwise move randomly
            out = self.randomDirection()
        return out

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
    
    def createSimulatedSelf(self):
        temp = SimulatedGreedyPredator(0, 0, 0, 0, 0)
        temp.speed = self.speed
        temp.x = self.x
        temp.y = self.y
        temp.map = self.map
        temp.id = self.id
        return temp

class SimulatedGreedyPredator(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    #takes in x and y, returns a tuple with the value modulo'd by mapsize
    def tauCoords(self, x, y):
        return (x % self.map.x_len, y % self.map.y_len)

    def totalDistanceToAgent(self, agentLocationTuple):
        xOff = abs(self.xMagnitude(agentLocationTuple[0]))
        yOff = abs(self.yMagnitude(agentLocationTuple[1]))
        return xOff + yOff

    def yMagnitude(self, yPreyLocation):
        #offset = self.y - yPreyLocation
        offset = yPreyLocation - self.y
        
        # the distance to prey location is less than half the board length, 
        # thus it is faster than wrapping around toroidal nature of board 
        if abs(offset) < math.ceil(self.map.y_len / 2):
            yMag = offset
        else:
            # It is faster to wrap around toroidal nature of board to
            # reach goal location, if abs(offset) == math.ceil(...) then it is equal distance to go either 
            # direction.  Happen to choose to swap direction in this implementation, doesn't matter though
            if offset < 0:
                yMag = offset + self.map.y_len
            elif offset > 0:
                yMag = offset - self.map.y_len
            else: #offset == 0
                yMag = 0
        return yMag
        
    def yDirection(self, yPreyLocation):
        yMag = self.yMagnitude(yPreyLocation)
        if yMag < 0:
            dir = -1
        if yMag > 0:
            dir = 1
        if yMag == 0:
            dir = 0
        return dir

    def xMagnitude(self, xPreyLocation):
        #offset = self.x - xPreyLocation
        offset = xPreyLocation - self.x
        
        # the distance to prey location is less than half the board length, 
        # thus it is faster than wrapping around toroidal nature of board 
        if abs(offset) < math.ceil(self.map.x_len / 2):
            xMag = offset
        else:
            # It is faster to wrap around toroidal nature of board to
            # reach goal location, if abs(offset) == math.ceil(...) then it is equal distance to go either 
            # direction.  Happen to choose to swap direction in this implementation, doesn't matter though
            if offset < 0:
                xMag = offset + self.map.x_len
            elif offset > 0:
                xMag = offset - self.map.x_len
            else: #offset == 0
                xMag = 0
        return xMag

    def xDirection(self, xPreyLocation):
        xMag = self.xMagnitude(xPreyLocation)
        if xMag < 0:
            dir = -1
        if xMag > 0:
            dir = 1
        if xMag == 0:
            dir = 0
        return dir

    # Returns (cardinal direction, distance to that direction, coord of closest destination on taurus)
    def findClosestDestination(self):
        x = self.map.getPreyLocations()
        if x == []: # if there's no prey, don't move anywhere.
            return (self.x, self.y)

        [(x, y)] = self.map.getPreyLocations()
                            #N, S, W, E
        unitDirectionArr = [self.tauCoords(x, y + 1), self.tauCoords(x, y - 1), self.tauCoords(x - 1, y), self.tauCoords(x + 1, y)]
        namedDirectionsArr = ['north', 'south', 'west', 'east']
        lengthArr = map(self.totalDistanceToAgent, unitDirectionArr)
        stateOfLocationsArr = map(self.map.returnStateOfCell, unitDirectionArr)
        tempLengthDict = dict(zip(namedDirectionsArr, lengthArr))
        tempStateDict = dict(zip(namedDirectionsArr, stateOfLocationsArr))
        stateDict = {key:val for key, val in tempStateDict.items() if val == "empty"}
        lengthDict = dict(sorted(tempLengthDict.items(), key = lambda x:x[1]))
        coordDict = dict(zip(namedDirectionsArr, unitDirectionArr))

        for k,v in lengthDict.items():
            if k in stateDict.keys():
                coord = coordDict[k]
                return(k, v, coord)
        
        return ('none', -1)

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

    '''
        Next codeblock represents:
        * let d = dim_max, if m_d is not blocked, take it
        * let d = dim_min, if m_d is not blocked, take it

        Outer if-elif statement checks which direction (x or y) has the larger dim_max.  For either case, we 
        then check if the location we want to move is empty. if it is, then we move there, if it isn't, 
        then we go to the direction that is the dim_min since there are only two directions, the other 
        axis will always be the dim_min, so we can then check that direction to see if it's empty, and 
        if it is move to that location.
    '''    
    def dimDirectionChooser(self):
        goalDestination = self.findClosestDestination()[2]
            
        xOff = self.xDirection(goalDestination[0])
        yOff = self.yDirection(goalDestination[1])
        out = ""
        if abs(self.xMagnitude(goalDestination[0])) > abs(self.yMagnitude(goalDestination[1])):
            if self.map.returnStateOfCell(self.tauCoords(self.x + xOff, self.y)) == "empty":
                out = self.tauCoords(self.x + xOff, self.y)
            elif self.map.returnStateOfCell(self.tauCoords(self.x, self.y + yOff)) == "empty":
                out = self.tauCoords(self.x, self.y + yOff)
        elif abs(self.xMagnitude(goalDestination[0])) <= abs(self.yMagnitude(goalDestination[1])):
            if self.map.returnStateOfCell(self.tauCoords(self.x, self.y + yOff)) == "empty": 
                out = self.tauCoords(self.x, self.y + yOff)
            elif self.map.returnStateOfCell(self.tauCoords(self.x + xOff, self.y)) == "empty":
                out = self.tauCoords(self.x + xOff, self.y)
        if out == "": # Otherwise move randomly
            out = self.randomDirection()
        return out

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
        #print("agent: " + str(self.id) + " is going to: " + str(out))
        return out

class GreedyProbabilisticPredator(GreedyPredator):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
    
    def softmax(self):
        
        return out

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

class TeammateAwarePredator(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    # determines L1-norm distance to nearest adjacent square
    def h(self,coord):
        loc = self.map.getAdjacentPreyLocations()
        minDist = float('inf')
        for i in range(len(loc[0])):
            dist = self.map.getTotalDistance(loc[0][i],coord)
            if dist < minDist:
                minDist = dist
        return minDist
    
    def a_star(self, destination):
        # dictionary containing distance and path
        info = {(self.x,self.y): [0,[]]}
        
        # list of points to explore
        queue = [(self.x,self.y)]

        # list of points that have been explored
        done = []

        # locations of predators, considered obstacles
        predLoc = self.map.getPredatorLocations()
        preyLoc = self.map.getPreyLocations()

        found_adjacent_space = False
        while not found_adjacent_space:
            # get data for closest target
            coord = queue[0]
            path = info[coord][1]
            g = len(path)
            new_path = path + [coord]

            # mark target as done
            done.append(coord)
            queue = queue[1:]

            # stop when we are adjacent to prey
            if coord == destination:
                found_adjacent_space = True
            else:
                # get coords of nearby squares
                new_coords = self.map.getAdjacentSquares(coord)
                
                for pt in new_coords:
                    # determine how close point is to goal
                    h = self.h(pt)
                    f = g + h
                    
                    # if new location is predator, treat as obstacle and ignore
                    if pt not in predLoc and pt not in preyLoc or pt == destination:
                        # if new location is undiscovered
                        if pt not in queue and pt not in done:
                            i = 0
                            inserted = False
                            # insert into sorted queue
                            while i < len(queue) and not inserted:
                                el = queue[i]
                                if info[el][0] > f:
                                    queue.insert(i,pt)
                                    info[pt] = [g+h,new_path]
                                    inserted = True
                                i += 1

                            # insert at end if largest distance away
                            if not inserted:
                                queue.append(pt)
                                info[pt] = [g+h,new_path]


                        # if new location is discovered and not finished
                        elif pt in queue:
                            # if better than previous value, update queue
                            if info[pt][0] > g+h:
                                # update in info and remove from queue
                                queue.remove(pt)
                                
                                i = 0
                                inserted = False
                                # insert into sorted queue
                                while i < len(queue) and not inserted:
                                    el = queue[i]
                                    if info[el][0] > f:
                                        queue.insert(i,pt)
                                        info[pt] = [g+h,new_path]
                                        inserted = True
                                    i += 1
                                # insert at end if largest distance away
                                if not inserted:
                                    queue.append(pt)
                                    info[pt] = [g+h,new_path]

        # return first step of shortest path
        if len(new_path) == 1:
            return self.map.getPreyLocations()[0]
        else:
            return new_path[1]
    
    def chooseDestination(self):
        adjPreyLoc = self.map.getAdjacentPreyLocations()[0]
        predLoc = self.map.getPredatorLocations()

        # calculate distances to each adjacent location for each predator
        distances = [[],[],[],[]]
        for i in range(len(predLoc)):
            loc = predLoc[i]
            for target in adjPreyLoc:
                dist = self.map.getTotalDistance(loc,target)
                distances[i].append((dist,loc,target))

        # sort each predator's choices by shortest distance
        for dist in distances:
            dist.sort()
       
        # keeps track of choice
        choices = [0,0,0,0]

        # keeps track of predators who have not picked yet
        unchosen = [0,1,2,3]

        # keeps track of destination each predator chose
        chosen_dest = [None, None, None, None]
        
        done = False
        while len(unchosen) > 0:
            # look at choices predators have made
            current_dest_choice = []
            for i in unchosen:
                current_dest_choice.append(distances[i][choices[i]])

            # choose minimum choice of predator farthest away
            increment = []
            maxIndex = 0
            maxVal = 0
            for i in range(len(unchosen)):
                if current_dest_choice[i][0] > maxVal:
                    maxIndex = i
                    maxVal = current_dest_choice[i][0]

            # remove chosen predator from list so it doesn't change
            predIndex = unchosen[maxIndex]
            chosen_dest[predIndex] = current_dest_choice[maxIndex][2]
            unchosen.remove(predIndex)
            
            # make sure that next choice is not a duplicate
            for i in unchosen:
                curVal = distances[i][choices[i]]
                while curVal[2] in chosen_dest:
                    choices[i] += 1
                    curVal = distances[i][choices[i]]
        print(chosen_dest)
        
        # find this predator
        thisPredator = None
        for i in range(len(predLoc)):
            if self.getLocation() == predLoc[i]:
                thisPredator = i

        # set to destination
        destination = chosen_dest[thisPredator]

        # if predator is at goal location, move on prey, otherwise perform A*
        if self.getLocation() == destination:
            first_move = self.map.getPreyLocations()[0]
        else:
            first_move = self.a_star(destination)

        return first_move
    
# keeps track of agents located in map
class TaurusMap:
    def __init__(self, x_len, y_len):
        self.x_len = x_len
        self.y_len = y_len
        self.prey = [] #list of prey objects
        self.predators = [] #list of predator objects
        self.preyLocations = []  #list of tuples representing prey locations
        self.predatorLocations = [] #list of tuples representign predator locations

    def getPredators(self):
        return self.predators

    def getPrey(self):
        return self.prey

    # applies taurus to coordinates       
    def taurusCoord(self,loc):
        return (loc[0] % self.x_len, loc[1] % self.y_len)

    # gets adjacent squares in taurus
    def getAdjacentSquares(self,loc):
        north = self.taurusCoord((loc[0],loc[1]-1))
        south = self.taurusCoord((loc[0],loc[1]+1))
        east = self.taurusCoord((loc[0]+1,loc[1]))
        west = self.taurusCoord((loc[0]-1,loc[1]))
        return [north,south,east,west]

    def getXDistance(self,loc1,loc2):
        x_dist = min((loc1[0]-loc2[0])%self.x_len,(loc2[0]-loc1[0])%self.x_len)
        return x_dist
    
    def getYDistance(self,loc1,loc2):
        y_dist = min((loc1[1]-loc2[1])%self.y_len,(loc2[1]-loc1[1])%self.y_len)
        return y_dist
    
    def getTotalDistance(self,loc1,loc2):
        total_dist = self.getXDistance(loc1,loc2) + self.getYDistance(loc1,loc2)        
        return total_dist
    
    # add agent to prey list
    def addPrey(self, new_prey):
        self.prey.append(new_prey)
        self.updatePreyLocations()

    # add agent to predator list
    def addPredator(self, new_predator):
        self.predators.append(new_predator)
        self.updatePredatorLocations()

    # update (x,y) coordinates for each prey
    def updatePreyLocations(self):
        locations = []
        for agent in self.prey:
            locations.append(agent.getLocation())
        self.preyLocations = locations
        
    # update (x,y) coordinates for each predator
    def updatePredatorLocations(self):
        locations = []
        for agent in self.predators:
            locations.append(agent.getLocation())
        self.predatorLocations = locations

    # get (x,y) coordinates for each predator
    def getPredatorLocations(self):
        return self.predatorLocations

    # get (x,y) coordinates for each prey
    def getPreyLocations(self):
        return self.preyLocations

    # get (x,y) coordinates for adjacent cells next to prey
    def getAdjacentPreyLocations(self):
        locations = []
        for prey in self.prey:
            preyCoord = (prey.x,prey.y)
            locations.append(self.getAdjacentSquares(preyCoord))
        return locations

    # returns True/False if prey is captured
    def preyCaptured(self):
        preyLocations = self.getPreyLocations()
        for loc in preyLocations:
            predatorLocations = self.getPredatorLocations()

            surrounded = True
            adjCoords = self.getAdjacentSquares(loc)

            for adj in adjCoords:
                if adj not in predatorLocations:
                    surrounded = False

            if surrounded:
                return True
            
        return False

    #returns state of a given cell, is of 3 options:
    # `empty`, `prey:{id}`, `predator:{id}`
    def returnStateOfCell(self, locationTuple):
        for prey in self.prey:
            if prey.getLocation() == locationTuple:
                return "prey:" + str(prey.id)
        for pred in self.predators:
            if pred.getLocation() == locationTuple:
                return "predator:" + str(pred.id)
        return "empty"


    # obtains destinations for each agent and moves them
    def relocate(self):
        # prey determine their moves
        preyMoves = []
        for prey in self.prey:
            preyMoves.append(self.taurusCoord(prey.chooseDestination()))
            
        # predator determine their moves
        predatorMoves = []
        for predator in self.predators:
            predatorMoves.append(self.taurusCoord(predator.chooseDestination()))

        # prey move first, don't move if spot already taken
        for i in range(len(preyMoves)):
            prey = self.prey[i]
            move = preyMoves[i]
            if move not in self.getPreyLocations() and move not in self.getPredatorLocations():
                prey.setLocation(move[0], move[1])
                self.updatePreyLocations()

        # predators then move, don't move if spot already taken
        for i in range(len(predatorMoves)):
            predator = self.predators[i]
            move = predatorMoves[i]
            if move not in self.getPreyLocations() and move not in self.getPredatorLocations():
                predator.setLocation(move[0], move[1])
                self.updatePredatorLocations()

    # Helper function which can print out the map in console, rather than using matplotlib
    # Useful for debugging since MatPlotLib doesn't play nice with debugger.
    def printMap(self):
        print(" y")
        print(" ^")
        print(" |")
        for y in range(self.y_len - 1, -1, -1):
            outString = str(y) + "| "
            for x in range(0, self.x_len):
                if (x, y) in self.predatorLocations:
                    for pred in self.predators:
                        if pred.getLocation() == (x, y):
                            outString = outString + str(pred.id) + " "
                elif (x, y) in self.preyLocations:
                    outString = outString + "$ "
                else:
                    outString = outString + "  "
            print(outString)
        print(" *" + str(" -") * self.x_len + " --> x")
        #print(" * - - - - - --> x")
        xAxis = "   "
        for i in range(0, self.x_len):
            xAxis += str(i) + " "
        print(xAxis)    
        print("prey locations (x, y): " + str(self.preyLocations))
        print("predator locations (x, y): " + str(self.predatorLocations))

    # displays map
    def displayMap(self):
        prey_x = []
        prey_y = []
        for loc in self.getPreyLocations():
            prey_x.append(loc[0])
            prey_y.append(loc[1])
        
        plt.scatter(prey_x, prey_y, label= "prey", color= "red", marker= "*")

        predator_x = []
        predator_y = []
        for loc in self.getPredatorLocations():
            predator_x.append(loc[0])
            predator_y.append(loc[1])

        plt.scatter(predator_x, predator_y, label= "predator", color= "blue", marker= "x")

        plt.xlabel('x axis')
        plt.ylabel('y axis')
        plt.xticks(range(0,self.x_len,1))
        plt.yticks(range(0,self.y_len,1))
        plt.legend()

        # function to show the plot
        plt.draw()
        #global iterations
        #plt.savefig("iteration" + str(iterations) + ".png")
        plt.pause(0.0001)
        plt.clf()


#def main(x_len, y_len, predatorClasses, preyClasses, predator_speed = 1, prey_speed = 1):
def main(x_len, y_len, predatorClasses, preyClasses, preyLocArray = None, predLocArray = None, maxIter = 50, predator_speed = 1, prey_speed = 1, output = True):
    locations = []
    # initialize map
    taurusMap = TaurusMap(x_len,y_len)

    if preyLocArray == None:
        # initialize prey in random locations not overlapping
        i = 0
        while i < len(preyClasses):
            x_val = random.randint(0,x_len-1)
            y_val = random.randint(0,y_len-1)
            if (x_val, y_val) not in locations:
                locations.append((x_val, y_val))
                prey = preyClasses[i](prey_speed, x_val, y_val, taurusMap, 0)
                taurusMap.addPrey(prey)
                i += 1
    else:
        i = 0
        while i < len(preyLocArray):
            if preyLocArray[i] not in locations:
                locations.append(preyLocArray[i])
                prey = preyClasses[i](prey_speed, preyLocArray[i][0], preyLocArray[i][1], taurusMap, 0)
                taurusMap.addPrey(prey)
            else:
                print("prey location invalid: " + str(preyLocArray[i]))
                taurusMap.printMap()
                exit(1)
            i += 1

    # initialize predators in random locations not overlapping
    i = 0
    if predLocArray == None:
        while i < len(predatorClasses):
            x_val = random.randint(0,x_len-1)
            y_val = random.randint(0,y_len-1)
            if (x_val, y_val) not in locations:
                locations.append((x_val, y_val))
                predator = predatorClasses[i](predator_speed, x_val, y_val, taurusMap, i + 1)
                taurusMap.addPredator(predator)
                i += 1
    else:
        while i < len(predLocArray):
            if predLocArray[i] not in locations:
                locations.append(predLocArray[i])
                predator = predatorClasses[i](predator_speed, predLocArray[i][0], predLocArray[i][1], taurusMap, i + 1)
                taurusMap.addPredator(predator)
            else:
                print("pred location invalid: " + str(predLocArray[i]))
                taurusMap.printMap()
                print(locations)
                exit(1)
            i += 1
    
    #global iterations

    # iterate through timesteps of simulation until prey is captured
    iterations = 0
    if output:
        taurusMap.printMap()
    while not taurusMap.preyCaptured() and iterations < maxIter:
        taurusMap.relocate()
        #taurusMap.displayMap()
        if output:
            taurusMap.printMap()
            time.sleep(1)
        iterations += 1
    if iterations >= maxIter:
        return -1 #if it couldn't be solved, return -1 to indiciate failure
    else:
        return iterations
    

#if __name__ == "__main__":
    #main(5,5,[GreedyPredator,GreedyPredator,GreedyPredator,GreedyPredator],[RandomPrey])
    #main(5,5,[GreedyPredator],[StationaryPrey])
    #main(10,10,[GreedyPredator, GreedyPredator],[StationaryPrey])

    #main(5,5,[TeammateAwarePredator,TeammateAwarePredator,TeammateAwarePredator,TeammateAwarePredator],[StationaryPrey])
