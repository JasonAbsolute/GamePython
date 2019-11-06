class node:
    def __init__ (self, a, b):
        self.i = a
        self.j = b
        self.parent = None
        self.bestf = 100000
        self.unusable = False
        self.g = 100000
        self.seen = False
        self.mark = False;

    def Mark (self):
        self.mark = True
    def unMark(self):
        self.mark = False

    def updateF (self, f, p):
        if f < self.bestf:
            self.bestf = f
            self.parent = p

    def setUnusable (self):
        self.unusable = True

def initialize ():
    global z

    for i in range (0,10):
        for j in range (0,10):
            z[i][j] = node(i,j);
    """  First maze
    z[2][1].setUnusable()  # Set up the grid
    z[3][1].setUnusable()
    z[4][1].setUnusable()
    z[5][1].setUnusable()
    z[5][2].setUnusable()
    z[6][2].setUnusable()
    z[6][3].setUnusable()
    z[7][3].setUnusable()
    z[7][4].setUnusable()
    z[8][4].setUnusable()
    z[8][5].setUnusable()
    z[8][6].setUnusable()

    z[1][6].setUnusable()
    z[2][6].setUnusable()
    z[3][6].setUnusable()
    z[3][7].setUnusable()
    z[3][8].setUnusable()
   """
    for i in range (0,9):
        z[2][i].setUnusable()
    for i in range (1,10):
        z[5][i].setUnusable();
    printGrid()

def printGrid():                 # Print the scene
    for i in range(10):
        for j in range(10):
            if i==1 and j==5:
                print("S", end="")
            elif i==7 and j==5:
                print ("E", end="")
            elif z[i][j].mark:
              print ("^", end="")
            elif z[i][j].parent != None:
              print (".", end="")
            elif z[i][j].unusable:
              print ("#", end="")
            else:
              print (".", end="")
        print ()

def h (p):
    return (abs(p.i-goalx) + abs(p.j-goaly)) * 10

def g(p):
    return p.g

def f (p):
    return h(p) + g(p)

def inList(p, l):
    for ll in l:
        if ll.i==p.i and ll.j==p.j:
            return ll
    return None

def smallestOpenList ():
    q = openList[0]
    for p in openList:
        if p.bestf < q.bestf:
            q = p
    return q

def neighbors (p):
    nlist = []  # Create a list of neighbors of p
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            ii = p.i + i
            if (ii < 0 or ii >= 10):  # Range check
                continue
            jj = p.j + j
            if (jj < 0 or jj >= 10):
                continue
            nlist = nlist + [z[ii][jj]]
    return nlist

def unMarkAll ():
    for i in range(0,10):
        for j in range(0,10):
            z[i][j].unMark()

def printCost ():
    for i in range(0,10):
        for j in range(0,10):
          if z[i][j].g>300:
            print ("xxx ", end="")
          else:
            print (z[i][j].g," ", end="")
        print()

z = [[None for j in range(10)] for i in range(10)]
initialize()
startNode = z[1][5]   # Where to begin the path
goalNode = z[7][5]    # The place we are trying to reach
openList = []         # Open list; a list of points
closedList = []       # Closed list; a list of points
goalx = 7
goaly = 5

startNode.g = 0
print ("Starting f is ", startNode.bestf)
openList.append(startNode)
print (openList[0].bestf)

while (len(openList) > 0):     # While open list not empty
  p = smallestOpenList()       # Select a node from the open list
  if (p == goalNode):          # We have reached the goal.
    print ("Done.")
    printGrid()
    break

  closedList.append(p)         # Add to closed list
  openList.remove(p)           # remove from open
  nlist = neighbors(p)         # Find all neighbors

  for c in nlist:              # Examine each neighbor, named 'c'
    if c.unusable:             # If unusable or
        continue
    if inList(c,closedList) != None: # if it is in the closed list,
        continue                     # ignore it

    if p.i == c.i or p.j == c.j:  # Distance c to p
        d = 10
    else:
        d = 14
    cost = p.g + d                # New cost of c is old cost + d

    if inList (c,openList) == None:         # c not in the open list
        openList.append(c)
        if cost >= f(c):
            continue
        c.g = cost
        c.parent = p  # Set the parent
        c.bestf = f(c)


  printCost()
  print ("-----------------------------------------------------------")
unMarkAll()

p = z[goalx][goaly]
while (p != startNode):
    print ("<       ", p.i,",",p.j)
    p.Mark()
    p = p.parent


printGrid()
printCost()
