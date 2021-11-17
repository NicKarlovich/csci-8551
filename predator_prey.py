import matplotlib.pyplot as plt
import time
import random

showing = False

# base class for agents
class Agent:
    def __init__(self, speed, x, y, taurusMap):
        self.speed = speed
        self.x = x
        self.y = y
        self.map = taurusMap

    def chooseDestination(self):
        return (self.x+1,self.y)

    def getLocation(self):
        return (self.x,self.y)

    def setLocation(self,x,y):
        self.x = x
        self.y = y


# base class for prey
class Prey(Agent):
    def __init__(self, speed, x, y, taurusMap):
        super().__init__(speed, x, y, taurusMap)

    '''
    def chooseDestination(self):
        pass
    '''

# Random moving prey
class RandomPrey(Agent):
    def __init__(self, speed, x, y, taurusMap):
        super().__init__(speed, x, y, taurusMap)
    
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
    def __init__(self, speed, x, y, taurusMap):
        super().__init__(speed, x, y, taurusMap)

    '''
    def chooseDestination(self):
        pass
    '''

# keeps track of agents located in map
class TaurusMap:
    def __init__(self, x_len, y_len):
        self.x_len = x_len
        self.y_len = y_len
        self.prey = []
        self.predators = []
        self.preyLocations = []
        self.predatorLocations = []

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


def main(x_len, y_len, num_predators = 4, predator_speed = 1, num_prey = 1, prey_speed = 1):
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
            #prey = Prey(prey_speed, x_val, y_val, taurusMap)
            prey = RandomPrey(prey_speed, x_val, y_val, taurusMap)
            taurusMap.addPrey(prey)
            i += 1

    # initialize predators in random locations not overlapping
    i = 0
    while i < num_predators:
        x_val = random.randint(0,x_len-1)
        y_val = random.randint(0,y_len-1)
        if (x_val, y_val) not in locations:
            locations.append((x_val, y_val))
            predator = Predator(predator_speed, x_val, y_val, taurusMap)
            taurusMap.addPredator(predator)
            i += 1

    
    #global iterations

    # iterate through timesteps of simulation until prey is captured
    iterations = 0
    while not taurusMap.preyCaptured():
        taurusMap.relocate()
        taurusMap.displayMap()
        time.sleep(1)
        iterations += 1
    

if __name__ == "__main__":
    main(5,5)
