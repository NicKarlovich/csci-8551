import math

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