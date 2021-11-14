# base class for agents
class Agent:
    def __init__(self, speed, x, y, taurusMap):
        self.speed = speed
        self.x = x
        self.y = y
        self.map = taurusMap

    def chooseDestination(self):
        pass

    def getLocation(self):
        return (self.x,self.y)

    def setLocation(self,x,y):
        self.x = x
        self.y = y


# base class for prey
class Prey(Agent):
    def __init__(self, speed, x, y, taurusMap):
        super().__init__(speed, x, y, taurusMap)

    def chooseDestination(self):
        pass


# base class for predators
class Predator(Agent):
    def __init__(self, speed, x, y, taurusMap):
        super().__init__(speed, x, y, taurusMap)

    def chooseDestination(self):
        pass


# keeps track of agents located in map
class TaurusMap:
    def __init__(self, x_len, y_len):
        self.x_len = x_len
        self.y_len = y_len
        self.prey = []
        self.predators = []

    # applies taurus to coordinates       
    def taurusCoord(self,x,y):
        return (x % self.x_len, y % self.y_len)

    # add agent to prey list
    def addPrey(self, new_prey):
        self.prey.append(new_prey)

    # add agent to predator list
    def addPredator(self, new_predator):
        self.predators.append(new_predator)

    # get (x,y) coordinates for each prey
    def getPreyLocations(self):
        locations = []
        for agent in self.prey:
            locations.append(agent.getLocation())
        return locations

    # get (x,y) coordinates for each predator
    def getPredatorLocations(self):
        locations = []
        for agent in self.prey:
            locations.append(agent.getLocation())
        return locations

    # returns True/False if prey is captured
    def preyCaptured(self):
        preyLocations = getPreyLocations()
        for location in preyLocations:
            predatorLocations = getPredatorLocations()
            north = taurusCoord(location[0],location[1]-1) in predatorLocations
            south = taurusCoord(location[0],location[1]+1) in predatorLocations
            east = taurusCoord(location[0]+1,location[1]) in predatorLocations
            west = taurusCoord(location[0]-1,location[1]) in predatorLocations

            if north and south and east and west:
                return True

        return False

    def relocate(self):
        # prey determine their moves
        preyMoves = []
        for prey in self.prey:
            preyMoves.append(prey.chooseDestination())

        # predator determine their moves
        predatorMoves = []
        for predator in self.predators():
            predatorMoves.append(predator.chooseDestination())

        # prey move first, don't move if spot already taken
        for i in range(len(preyMoves)):
            prey = self.prey[i]
            move = preyMoves[i]
            if move not in self.getPreyLocations() and move not in self.getPredatorLocations():
                prey.setLocation(move[0], move[1])

        # predators then move, don't move if spot already taken
        for i in range(len(predatorMoves)):
            prey = self.predators[i]
            move = predatorMoves[i]
            if move not in self.getPreyLocations() and move not in self.getPredatorLocations():
                predator.setLocation(move[0], move[1])
            
            
def main(x_len, y_len, num_predators = 4, predator_speed = 1, num_prey = 1, prey_speed = 1):
    locations = []
    taurusMap = TaurusMap(x_len,y_len)

    i = 0
    while i < num_prey:
        x_val = random.randint(x_len)
        y_val = random.randint(y_len)
        if (x_val, y_val) not in locations:
            locations.append(x_val, y_val)
            prey = Prey(prey_speed, x_val, y_val)
            taurusMap.addPrey(prey)
            i += 1

    i = 0
    while i < num_predator:
        x_val = random.randint(x_len)
        y_val = random.randint(y_len)
        if (x_val, y_val) not in locations:
            locations.append(x_val, y_val)
            predator = Predator(predator_speed, x_val, y_val)
            taurusMap.addPrey(predator)
            i += 1

    iterations = 0
    while not taurusMap.preyCaptured():
        taurusMap.relocate()
        iterations += 1

    print(iterations)
    

if __name__ == "__main__":
    main()

    
