class agent:
    def __init__(self, speed, x, y, taurusMap):
        pass

    def chooseDestination(self):
        pass

    def getLocation(self):
        return (x,y)

class taurusMap:
    def __init__(self, dim):
        self.dim = dim
        self.agents = []
        
    def validMove(self,x,y):
        return (x % self.dim, y % self.dim)
    

    def addAgent(x,y):
        
        
    def getAgentLocations():
        locations = []
        for agent in self.agents:
            locations.append(agent.getLocation())
        return locations
