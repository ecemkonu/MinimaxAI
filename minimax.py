import datetime
import sys

class gameState: 
    def __init__(self, boxIndexes, horizontalEdges,verticalEdges, maxpScore, minpScore, currPlay, utilityVal, actions):
        self.horizontalEdges = horizontalEdges
        self.verticalEdges = verticalEdges
        self.maxpScore = maxpScore
        self.minpScore = minpScore
        self.boxIndexes = boxIndexes
        self.currPlay = currPlay
        self.utilityVal = utilityVal #utility is set to a large negative num for max & large positive num for min
        self.actions = actions

    def utility(self):
        self.utilityVal = self.maxpScore-self.minpScore
        return self.utilityVal

    def terminalTest(self):
        for edge in self.horizontalEdges:
            if(edge ==0):
                return False
        for edge in self.verticalEdges:
            if(edge == 0):
                return False
        return True

    def generateChilds(self):
        if(self.currPlay == 'MAX'):
            nextPlay = 'MIN'
            nextUtil = 5267
        else:
            nextPlay = 'MAX'
            nextUtil = -5267
        children = []
        nextVerticalEdges = self.verticalEdges.copy()
        for edgeLoc in range(len(self.horizontalEdges)):
            action = 'H'
            if self.horizontalEdges[edgeLoc] == 0:
                action += str(edgeLoc)
                nextHorizontalEdges = self.horizontalEdges.copy()
                nextHorizontalEdges[edgeLoc] = 1
                boxCreated = False
                createdCount = 0
                for h1,h2,v1,v2 in self.boxIndexes:
                    count = 0
                    if h1 == edgeLoc:
                        count = nextVerticalEdges[v1] + nextVerticalEdges[v2] + nextHorizontalEdges[h2]
                        if count == 3:
                            boxCreated = True
                            createdCount +=1
                    elif(h2 ==edgeLoc):
                        count = nextVerticalEdges[v1] + nextVerticalEdges[v2] + nextHorizontalEdges[h1]
                        if count == 3:
                            boxCreated = True
                            createdCount +=1
                if boxCreated:
                    if self.currPlay== 'MAX':
                        nextChild = gameState(self.boxIndexes, nextHorizontalEdges, nextVerticalEdges, self.maxpScore+createdCount, self.minpScore, self.currPlay, self.utilityVal,self.actions+action)
                    else:
                        nextChild = gameState(self.boxIndexes, nextHorizontalEdges, nextVerticalEdges, self.maxpScore, self.minpScore+createdCount, self.currPlay, self.utilityVal,self.actions+action)
                else:
                    nextChild = gameState(self.boxIndexes, nextHorizontalEdges,nextVerticalEdges,self.maxpScore, self.minpScore, nextPlay, nextUtil, self.actions+action)
                children.append(nextChild)

        nextHorizontalEdges = self.horizontalEdges.copy()
        for edgeLoc in range(len(self.verticalEdges)):
            action = 'V'
            if self.verticalEdges[edgeLoc] == 0:
                action  += str(edgeLoc)
                nextVerticalEdges = self.verticalEdges.copy()
                nextVerticalEdges[edgeLoc] = 1
                boxCreated = False
                createdCount = 0 
                for h1,h2,v1,v2 in self.boxIndexes:
                    count = 0
                    if v1 == edgeLoc:
                        count = nextHorizontalEdges[h1] + nextVerticalEdges[v2] + nextHorizontalEdges[h2]
                        if count == 3:
                            boxCreated = True
                            createdCount +=1
                    elif(v2 ==edgeLoc):
                        count = nextVerticalEdges[v1] + nextHorizontalEdges[h2] + nextHorizontalEdges[h1]
                        if count == 3:
                            boxCreated = True
                            createdCount +=1
                if boxCreated:
                    if self.currPlay== 'MAX':
                        nextChild = gameState(self.boxIndexes, nextHorizontalEdges, nextVerticalEdges, self.maxpScore+createdCount, self.minpScore, self.currPlay, self.utilityVal, self.actions+action)
                    else:
                        nextChild = gameState(self.boxIndexes, nextHorizontalEdges, nextVerticalEdges, self.maxpScore, self.minpScore+createdCount, self.currPlay, self.utilityVal, self.actions+action)
                else:
                    nextChild = gameState(self.boxIndexes, nextHorizontalEdges,nextVerticalEdges,self.maxpScore, self.minpScore, nextPlay, nextUtil, self.actions+action)
                children.append(nextChild)
        return children


def readGrid(filename):
    with open(filename) as myFile:
        rowNum = int(myFile.readline())
        colNum = int(myFile.readline())
        horizontalEdges = []
        verticalEdges = []
        for i in range(colNum*(rowNum+1)):
            horizontalEdges.append(int(myFile.readline()))
        for i in range(rowNum*(colNum+1)):
            verticalEdges.append(int(myFile.readline()))
        maxpScore = int(myFile.readline())
        minpScore = int(myFile.readline())
    boxIndexes = [] #  will hold entries for row row col col (horiz e1 horiz e2 vert e1 vert e2)
    for row in range(rowNum):
        for col in range(colNum):
            curr_box = []
            curr_box.append(row*colNum + col)
            curr_box.append(row*colNum + col + colNum)
            curr_box.append(row * (colNum +1) + col)
            curr_box.append(row * (colNum+1) + col+1)
            
            boxIndexes.append(curr_box)
    print("Boxes will be searched in following row, row, col col positions", boxIndexes)
    initState = gameState(boxIndexes, horizontalEdges, verticalEdges, maxpScore, minpScore, 'MAX', -5267, "") #set current player to max, as max will go first
    return initState


def minimax(state):
    num_nodes = 0
    state.utilityVal, action, maxPScore, minPScore, num_nodes = max_value(state, num_nodes)
    print("Maximum Player Score: ",maxPScore)
    print("Minimum Player Score: ",minPScore)
    print("# of Nodes Generated: ", num_nodes)
    return action

def max_value(state, num_nodes):
    if state.terminalTest():
        return (state.utility(), state.actions, state.maxpScore, state.minpScore, num_nodes)
    else:
        children = state.generateChilds()
        maxPScore = state.maxpScore
        minPScore = state.minpScore
        temp = state.utilityVal
        for node in children:
            num_nodes+=1
            if node.currPlay =='MAX':
                util, act, maxv, minv, num_nodes = max_value(node, num_nodes)
            elif node.currPlay == 'MIN':
                util, act, maxv, minv, num_nodes= min_value(node , num_nodes)
            state.utilityVal = max(state.utilityVal, util)   
            if state.utilityVal != temp:
                state.actions = act
                maxPScore = maxv
                minPScore = minv
                temp = state.utilityVal
    return state.utilityVal, state.actions, maxPScore, minPScore, num_nodes

 
def min_value(state, num_nodes):
    if state.terminalTest():
        return(state.utility(), state.actions, state.maxpScore, state.minpScore, num_nodes)
    else:
        children = state.generateChilds()
        maxPScore = state.maxpScore
        minPScore = state.minpScore
        temp = state.utilityVal
        for node in children:
            num_nodes+=1
            if node.currPlay =='MIN':
                util, act, maxv, minv, num_nodes = min_value(node, num_nodes)
            elif node.currPlay == 'MAX':
                util, act, maxv, minv, num_nodes= max_value(node, num_nodes)
            state.utilityVal = min(state.utilityVal, util)

            if state.utilityVal != temp:
                state.actions = act
                maxPScore = maxv
                minPScore = minv
                temp = state.utilityVal
    
    return state.utilityVal, state.actions, maxPScore, minPScore, num_nodes


initState = readGrid(sys.argv[1])
time1 = datetime.datetime.now().microsecond/1000
action = minimax(initState)
time2 = datetime.datetime.now().microsecond/1000
#print(action) #action sequence, for debug purposes
print("Time passed: ",time2-time1, "ms")
