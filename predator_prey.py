import matplotlib.pyplot as plt
import time
import random
import math

showing = False

# base class for agents
class Agent:
    def __init__(self, speed, x, y, taurusMap, id):
        self.speed = speed
        self.x = x
        self.y = y
        self.map = taurusMap
        self.id = id

    def chooseDestination(self):
        return (self.x+1,self.y)

    def getLocation(self):
        return (self.x,self.y)

    def setLocation(self,x,y):
        self.x = x
        self.y = y

    def getId(self):
        return self.id


# base class for prey
class Prey(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    '''
    def chooseDestination(self):
        pass
    '''

# Stationary prey
# used for testing
class StationaryPrey(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    def chooseDestination(self):
        return (self.x,self.y)

# Random moving prey
class RandomPrey(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)
    
    def chooseDestination(self):
        direction = random.randint(0, 3)
        if direction == 0:
            return (self.x + 1, self.y)
        if direction == 1:
            return (self.x - 1, self.y)
        if direction == 2:
            return (self.x, self.y + 1)
        if direction == 3:
            return (self.x, self.y - 1)

# base class for predators
class Predator(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    '''
    def chooseDestination(self):
        pass
    '''

# Greedy predator, constantly attempts to move towards prey
# not very intelligent will get stuck
class GreedyPredator(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    def totalDistanceToAgent(self, agentLocationTuple):
        xOff = abs(self.xMagnitude(agentLocationTuple[0]))
        yOff = abs(self.yMagnitude(agentLocationTuple[1]))
        return xOff + yOff

    def yMagnitude(self, yPreyLocation):
        return self.y - yPreyLocation

    #yPreyLocation is the y value of where the prey is now % map dimensions.
    def yDirection(self, yPreyLocation):
        offset = self.y - yPreyLocation
        #if negative, predator is lower on map than prey
        #if positive, predator is higher on map
        #if 0, then predator on same y as prey
        if offset == 0:
            return 0
        if offset < 0:
            # equal to only applies in case where taursMap.y_len is even, in those cases when you're literally the furthest point away from 
            # the prey on this axis, it doesn't matter in a greedy sense if you go decide to loop around or go from the other direction, so I arbitrarily
            # chose to make it so it goes down.
            if abs(offset) >= math.ceil(self.map.y_len / 2):
                return -1
            if abs(offset) < math.ceil(self.map.y_len / 2):
                return 1
        if offset > 0:
            #same logic as above for = sign in below conditional
            if abs(offset) >= math.ceil(self.map.y_len / 2): 
                return 1
            if abs(offset) < math.ceil(self.map.y_len / 2):
                return -1

    def xMagnitude(self, xPreyLocation):
        return self.x - xPreyLocation

    def xDirection(self, xPreyLocation):
        offset = self.x - xPreyLocation
        #if negative, predator is lower on map than prey
        #if positive, predator is higher on map
        #if 0, then predator on same x as prey
        if offset == 0:
            return 0
        if offset < 0:
            # equal to only applies in case where taursMap.x_len is even, in those cases when you're literally the furthest point away from 
            # the prey on this axis, it doesn't matter in a greedy sense if you go decide to loop around or go from the other direction, so I arbitrarily
            # chose to make it so it goes left.
            if abs(offset) >= math.ceil(self.map.x_len / 2): 
                return -1
            if abs(offset) < math.ceil(self.map.x_len / 2):
                return 1
        if offset > 0:
            #same logic as above for = sign in below conditional
            if abs(offset) >= math.ceil(self.map.x_len / 2): 
                return 1
            if abs(offset) < math.ceil(self.map.x_len / 2):
                return -1

    def findClosestDestination(self):
        x = self.map.getPreyLocations() #this method can return nothing for a while?
        if x == []: # if there's no prey, don't move anywhere.
            return (self.x, self.y)

        [(x, y)] = self.map.getPreyLocations()
                            #N, S, W, E
        unitDirectionArr = [(x, (y + 1) % 5), (x, (y - 1) % 5), ((x - 1) % 5, y), ((x + 1) % 5, y)]
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

    def chooseDestination(self):
        x = self.map.getPreyLocations() #this method can return nothing for a while?
        if x == []: # if there's no prey, don't move anywhere.
            return (self.x, self.y)

        [(x, y)] = self.map.getPreyLocations()

        print(self.map.returnStateOfCell((x, y))) #itself
        print(self.map.returnStateOfCell(((x + 1) % 5, y))) #right
        print(self.map.returnStateOfCell(((x - 1) % 5, y))) #left 
        print(self.map.returnStateOfCell((x, (y + 1) % 5))) #up
        print(self.map.returnStateOfCell((x, (y - 1) % 5))) # down
        #print(self.findClosestDestination())

        goalDestination = self.findClosestDestination()[2]
        
<<<<<<< HEAD
        xOff = self.xDirection(x)
        yOff = self.yDirection(y)
        # we don't want agent to move diagonally, so we have to decide, do we prioritize x movement or y movement, we'll choose so randomly!
=======
        xOff = self.xDirection(goalDestination[0])
        yOff = self.yDirection(goalDestination[1])
        # we dont' want agent to move diagonally, so we have to decide, do we prioritize x movement or y movement, we'll choose so randomly!
>>>>>>> 4321418ba4013c5f056bfbc01f4f598deedf891a
        if xOff != 0 and yOff != 0:
            if random.randint(0,1) == 0:
                return (self.x + xOff, self.y) #ignore y offset
            else:
                return (self.x, self.y + yOff) #ignore x offset
        else:
            #to get here, at least one of the offsets == 0, so we can just include both, and simplify cases.
            return (self.x + xOff, self.y + yOff)
        

        return (self.x, self.y)

class TeammateAwarePredator(Agent):
    def __init__(self, speed, x, y, taurusMap, id):
        super().__init__(speed, x, y, taurusMap, id)

    def h(self,x,y):
        loc = self.map.getAdjacentPreyLocations()
        minDist = float('inf')
        for i in range(loc[0]):
            dist = (loc[0] - x)**2 + (loc[1] - y)**2 
        return 

    def a_star():
        distances = []
        for i in range(self.map.x_len):
            temp = []
            for j in range(self.map.y_len):
                temp.append(-1)
            distances.append(temp)
        
        queue = [[0, (self.x,self.y), []]]
        done = []
        found_adjacent_space = False
        i = 1
        while not found_adjacent_space:
            val = queue[0][1]
            queue = queue[1:]

            north = val[]
        
    
    def chooseDestination(self):
        loc = self.map.getAdjacentPreyLocations()
        
        if x == []:
            return (self.x, self.y)
        [(x, y)] = self.map.getPreyLocations()
        
        
        xOff = self.xDirection(x)
        yOff = self.yDirection(y)
        # we don't want agent to move diagonally, so we have to decide, do we prioritize x movement or y movement, we'll choose so randomly!
        if xOff != 0 and yOff != 0:
            if random.randint(0,1) == 0:
                return (self.x + xOff, self.y) #ignore y offset
            else:
                return (self.x, self.y + yOff) #ignore x offset
        else:
            #to get here, at least one of the offsets == 0, so we can just include both, and simplify cases.
            return (self.x + xOff, self.y + yOff)
        return (self.x, self.y)

    
# keeps track of agents located in map
class TaurusMap:
    def __init__(self, x_len, y_len):
        self.x_len = x_len
        self.y_len = y_len
        self.prey = [] #list of prey objects
        self.predators = [] #list of predator objects
        self.preyLocations = []  #list of tuples representing prey locations
        self.predatorLocations = [] #list of tuples representign predator locations

    # applies taurus to coordinates       
    def taurusCoord(self,loc):
        return (loc[0] % self.x_len, loc[1] % self.y_len)

    # add agent to prey list
    def addPrey(self, new_prey):
        self.prey.append(new_prey)

    # add agent to predator list
    def addPredator(self, new_predator):
        self.predators.append(new_predator)

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
        for loc in self.preyLocations:
            north = self.taurusCoord((loc[0],loc[1]-1))
            south = self.taurusCoord((loc[0],loc[1]+1))
            east = self.taurusCoord((loc[0]+1,loc[1]))
            west = self.taurusCoord((loc[0]-1,loc[1]))
            locations.append([north,south,east,west])
        return locations

    # returns True/False if prey is captured
    def preyCaptured(self):
        preyLocations = self.getPreyLocations()
        for loc in preyLocations:
            predatorLocations = self.getPredatorLocations()
            north = self.taurusCoord((loc[0],loc[1]-1)) in predatorLocations
            south = self.taurusCoord((loc[0],loc[1]+1)) in predatorLocations
            east = self.taurusCoord((loc[0]+1,loc[1])) in predatorLocations
            west = self.taurusCoord((loc[0]-1,loc[1])) in predatorLocations

            if north and south and east and west:
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
        print(" * - - - - - --> x")
        print("   0 1 2 3 4")
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


def main(x_len, y_len, num_predators = 2, predator_speed = 1, num_prey = 1, prey_speed = 1):
    locations = []
    # initialize map
    taurusMap = TaurusMap(x_len,y_len)

    # initialize prey in random locations not overlapping
    i = 0
    while i < num_prey:
        x_val = random.randint(0,x_len-1)
        y_val = random.randint(0,y_len-1)
        if (x_val, y_val) not in locations:
            locations.append((x_val, y_val))
            #prey = Prey(prey_speed, x_val, y_val, taurusMap, 0)
            prey = StationaryPrey(prey_speed, x_val, y_val, taurusMap, 0)
            #prey = RandomPrey(prey_speed, x_val, y_val, taurusMap)
            taurusMap.addPrey(prey)
            i += 1

    # initialize predators in random locations not overlapping
    i = 0
    while i < num_predators:
        x_val = random.randint(0,x_len-1)
        y_val = random.randint(0,y_len-1)
        if (x_val, y_val) not in locations:
            locations.append((x_val, y_val))
            #predator = Predator(predator_speed, x_val, y_val, taurusMap, i + 1)
            predator = GreedyPredator(predator_speed, x_val, y_val, taurusMap, i + 1)
            taurusMap.addPredator(predator)
            i += 1

    
    #global iterations

    # iterate through timesteps of simulation until prey is captured
    iterations = 0
    while not taurusMap.preyCaptured():
        taurusMap.relocate()
        #taurusMap.displayMap()
        taurusMap.printMap()
        time.sleep(1)
        iterations += 1
    

if __name__ == "__main__":
    main(5,5)
