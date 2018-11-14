import random
import collections
import datetime
#value of 999 means no arc. 
noArc = 999

def randomGraphAdjacencyMatric(size, probabilityNoArc, isDirected=False):
    matrix = []
    #set up right sized matrix of nodes with no arcs - ie elemets are 99
    for row in range(0,size):
        currentRow = []
        matrix.append(currentRow)
        for col in range(0,size):
            currentRow.append(noArc)
    for row in range(0,size):
        rangeStart = 0 if isDirected else row+1
        for col in range(rangeStart,size):
            if random.random() > probabilityNoArc:
                if row == col:
                    matrix[row][col] = noArc
                else:
                    #want an arc
                    matrix[row][col] = int(random.random()*50 + 10) #purely to make all numbers 2 digit so matrix aligns in terminal!
                    if not isDirected:
                        #want it symetrical
                        matrix[col][row] = matrix[row][col]
    return matrix

def isConnected(matrix):
    # start = datetime.datetime.now()
    if not isDirected(matrix):
        raise ValueError("isConnected(matrix) can only be called with a symettrical matrix")
    size = len(matrix)
    # this array is used to pull together connections. The matrix given is size x size
    # this means there are size nodes (ie if size = 5 there are 5 nodes)
    # We set up an array of length size with integers equal to their index
    # then we work through the matrix checking if there is a node between nodes
    # if there is we change the value in that node index in the array to the value 
    # of the node it's connectd to.
    # So. say rootArray = [0,1,2,3,4] to start with
    # if we find an arc (0,1) then rootArray becomes [0,0,2,3,4]
    # now if we get (1,2) we look at the value in index 1 and set index 2 to that
    # ie we get [0,0,0,3,4]
    # at the end if we have a single value in the array we have a fully connected matrix
    rootArray = [x for x in range(0,size)]
    #using range as we need to access via the index
    #need some error checking incase not a square matric of ints
    for r in range(0,size):
        for c in range(0,size):
            if r == c or matrix[c][r] == noArc: 
                pass #a node is connect to itself / no node present - 99 indicates no node
            else:
                # we have a node so need to adjust our rootArray
                originalValueAtC = rootArray[c]
                rootArray[c] = rootArray[r]
                #any items that are same value as rootArray[c] need to need to
                #be changed to value of rootArray[c]
                for i in range(0,size):
                    if rootArray[i] == originalValueAtC:
                        rootArray[i] = rootArray[r]
    
    count = collections.Counter(rootArray)            
    # print(rootArray)
    # print(count)
    # print(len(count))
    # print("Testing whether connected took {}".format(datetime.datetime.now() - start))
    return (len(count)==1)

#returns component containing a
def find(a, inComponentArray):
    for i in inComponentArray:
        if a in i: return i

def createOrderedEdgesList(matrix):
    size = len(matrix)
    edges = []
    for r in range(0,size):
        #assuming undirected graph so this only needs to look at top half of the
        #matrix since it will be symetrical about the diagonal. An also ignore 
        #the diagonal
        for c in range(r+1,size):
            if matrix[r][c] != noArc: 
                edges.append((r,c,matrix[r][c]))
    edges.sort(key=lambda e: e[2])
    return edges

def minSpanningTreeKruskal(matrix):
    start = datetime.datetime.now()
    size = len(matrix)
    componentArray = [set([i]) for i in range(0,size)]
    orderedEdges = createOrderedEdgesList(matrix)
    minTree = []

    for edge in orderedEdges:
        print(f'Considering: {edge}')
        if len(minTree) == size -1: break
        compA = find(edge[0], componentArray)
        compB = find(edge[1], componentArray)
        if compA != compB:
            #merge them
            componentArray.append(compA.union(compB))
            componentArray.remove(compA)
            componentArray.remove(compB)
            minTree.append(edge)
        else:
            print('Rejected')
    
    print("KRUSKAL took: {}".format(datetime.datetime.now() - start))
    if len(minTree) == size - 1:
        return minTree
    else:
        return None

def minSpanningTreePrim(matrix):
    start = datetime.datetime.now()
    # if not isConnected(matrix): return None
    T = set()
    nearest = []
    minDist = []
    # set up arrays. Nearest is the nearest item in T - at the moment the starting node 0 (zero) is the only item
    # minDist - is the distance to the nearest by a direct arc - so it's 99 if no arc. This is read from row 0 of the matrix
    # for clarity I've made these arrays the same length as the matrix size. This we set minDist[0] to -1 as this node
    # if already in the set T
    for i in range(0,len(matrix)):
        nearest.append(0)
        minDist.append(matrix[0][i])
    minDist[0] = -1 # as node 0 is starting point so already in
    # this runs to one less than the size of the matrix as we need to add that many more nodes (as node 0 is alread in)
    for i in range(0,len(matrix)-1):
        # print("T: {}".format(T))
        # print("nearest: {}".format(nearest))
        # print("minDist: {}".format(minDist))
        min = max(max(matrix))+1 #a large number - must be bigger than any value in the matrix
        # this runs through the min dist array and finds the closest node not yet in set T
        for j in range(0,len(minDist)):
            if minDist[j] >= 0 and minDist[j] < min:
                min = minDist[j]
                k = j # keep a note of the closest nodes index as we need to it to update the nearest and minDist arrays
        # add the nearest external node in to the set. Mark it's min dist as -1 to indicate it's now in the set
        # NB if nearestExternal node has dist 99 it means it's not connected - no solution. So return None
        if minDist[k] == noArc: return None
        T = T.union({(k, nearest[k], minDist[k])})
        minDist[k] = -1
        # update the min dists. Only need to consider whether the distance to the latest added node is closer than the 
        # current min dist. If so change the minDist to that value and the nearest to that node
        for j in range(0,len(minDist)):
            if matrix[k][j] < minDist[j]:
                minDist[j] = matrix[k][j]
                nearest[j] = k
    print("PRIM took: {}".format(datetime.datetime.now() - start))
    return T

def convertToAdjancyMatrix(undirectedEdgeList):
    combined = [i[0] for i in undirectedEdgeList] + [i[1] for i in undirectedEdgeList]
    minValue = min(combined)
    maxValue = max(combined)  
    adMatrix = []

    # create starting matrix with all entries set to no arcs
    for row in range(minValue, maxValue+1):
        newR = []
        adMatrix.append(newR)
        for col in range(minValue, maxValue+1):
            
            newR.append(noArc)

    # not add in the edge list - assuming this is undirected - so need to  add symettry

    for e in undirectedEdgeList:
        adMatrix[e[0]][e[1]] = e[2]
        adMatrix[e[1]][e[0]] = e[2]

    return adMatrix

def isDirected(matrix):
    # check if matrix is symetrical
    row = 0
    col = 0
    for r in range(len(matrix)):
        for c in range(r+1,len(matrix)):
            if matrix[r][c] != matrix[c][r]: return False
    return True

# Node we're working from is the first one in the matrix ie [0][0]
def DijkstrasShortestPathToAllNodes(matrix):
    remainingNodes = set(range(len(matrix)))
    includedNodes = {0} # insert node 0 as this is the starting point and thus is in the nodes
    remainingNodes = remainingNodes - includedNodes
    # at start only node 0 in so min dist is first row of matrix
    minDistArray = matrix[0] # indexed same as matrix - so item at i is for node i
    minDistArray[0] = noArc # since node 0 is in the set there is no arc to it.
    # print(f'included nodes: {includedNodes}')
    # print(f'remaining nodes: {remainingNodes}')
    # print(f'min distance array: {minDistArray}')
    for i in range(1, len(matrix)):
        # print(f'step{i}')
        indexOfMin = 0
        minDist = noArc
        for n in remainingNodes:
            if minDistArray[n] < minDist:
                indexOfMin = n
        includedNodes.add(indexOfMin)
        remainingNodes = remainingNodes - {indexOfMin}
        for n in remainingNodes:
            minDistArray[n] = min(minDistArray[n], minDistArray[indexOfMin] + matrix[indexOfMin][n])
        # print(f'included nodes: {includedNodes}')
        # print(f'remaining nodes: {remainingNodes}')
        # print(f'min distance array: {minDistArray}')
    return minDistArray[1:]     # exclude first item as thats the starting node

def floydsalgorithm(matrix):
    d = _copyMatrix(matrix)
    p = _blankMatrixOfSize(len(matrix))
    n = len(d)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    p[i][j] = k+1 # as 0 represents straight arc - need to label nodes from 1, not 0
    return d,p

def _copyMatrix(matrix):
    d = []
    for r in matrix:
        row = []
        d.append(row)
        for c in r:
            row.append(c)
    return d

def _blankMatrixOfSize(n):
    m = []
    for i in range(n):
        row = []
        m.append(row)
        for c in range(n):
            row.append(0)
    return m


def test():

    testConnected = [
        [[noArc,2,7,1],
        [2,noArc,19,2],
        [7,19,noArc,3],
        [1,2,3,noArc]],

        [[noArc,2,1,7],
        [2,noArc,noArc,noArc],
        [1,noArc,noArc,noArc],
        [7,noArc,noArc,noArc]],

        [[noArc,2,noArc,noArc],
        [2,noArc,noArc,2],
        [noArc,noArc,noArc,2],
        [noArc,2,2,noArc]]
    ]

    testNotConnected = [
        [[noArc,noArc,noArc,noArc],
        [noArc,noArc,noArc,noArc],
        [noArc,noArc,noArc,noArc],
        [noArc,noArc,noArc,noArc]],

        [[noArc,noArc,2,noArc],
        [noArc,noArc,noArc,2],
        [2,noArc,noArc,noArc],
        [noArc,2,noArc,noArc]],

        [[noArc,2,noArc,9],
        [2,noArc,noArc,1],
        [noArc,noArc,noArc,noArc],
        [9,1,noArc,noArc]]
    ]
    # print("Test NOT connected graphs")
    # for m in testNotConnected:
    #     print(m)
    #     edges = createOrderedEdgesList(m)
    #     print(isConnected(m)) 

    print("Test connected graphs")
    for m in testConnected:
        for i in m: print(i)
        edges = createOrderedEdgesList(m)
        print(isConnected(m))
        minTreeKruskal = minSpanningTreeKruskal(m)
        print("Min Spanning Tree using Kruskal Algorithm: {}".format(minTreeKruskal))
        minTreePrim = minSpanningTreePrim(m)
        print("Min Spanning Tree using Prim Algorithm: {}".format(minTreePrim))

    print("Test arbitrarily large graphs")
    for i in range(0,1 ):
        while True:
            m = randomGraphAdjacencyMatric(100 ,0.5)
            if isConnected(m): break
        for r in m:
            print(r)

        minTreeKruskal = minSpanningTreeKruskal(m)
        print("KRUSKAL minimum spanning tree: {}".format(minTreeKruskal))
        minTreePrim = minSpanningTreePrim(m)
        print("PRIM minimum spanning tree: {}".format(minTreePrim))

    #not connected graph
    print("Non connected graph")
    for m in testNotConnected:
        minTree = minSpanningTreeKruskal(m)
        print("Kuskal: {}".format(minTree))      
        minTree = minSpanningTreePrim(m)
        print("Prim: {}".format(minTree))

    lectureGraph = [ 
        [noArc,1,noArc,4,noArc,noArc,noArc],
        [1,noArc,2,6,4,noArc,noArc],
        [noArc,2,noArc,noArc,5,6,noArc],
        [4,6,noArc,noArc,3,noArc,4],
        [noArc,4,5,3,noArc,8,7],
        [noArc,noArc,6,noArc,8,noArc,3],
        [noArc,noArc,noArc,4,7,3,noArc]
    ]

    print("GRAPH From Lecture:")
    for r in lectureGraph: print(r)
    minTreeKruskal = minSpanningTreeKruskal(lectureGraph)
    print("Minimum Spanning Tree Kruskal: {} ".format(minTreeKruskal))
    print("Kruskal Min Tree as adjacency matrix:")
    adMatrix = convertToAdjancyMatrix(minTreeKruskal)
    for r in adMatrix: print(r)
    minTreePrim = minSpanningTreePrim(lectureGraph)
    print("Minimum Spanning Tree Prim: {} ".format(minTreePrim))
    print("Prim Min Tree as adjacency matrix:")
    adMatrix = convertToAdjancyMatrix(minTreePrim)
    for r in adMatrix: print(r)

    print("Random directed graph:")
    graph = randomGraphAdjacencyMatric(10, 0.5, True)
    for r in graph:
        print(r)

    print(f'Is Directed: {isDirected(graph)}')

    print("Testing Dijkstras Algorithm for lecture example:")
    dijkstrasGridFromLecture = [
        [noArc,50,30,100,10],
        [noArc,noArc,noArc,noArc,noArc],
        [noArc,5,noArc,50,noArc],
        [noArc,20,noArc,noArc,noArc],
        [noArc,noArc,noArc,10,noArc]
    ]

    result = DijkstrasShortestPathToAllNodes(dijkstrasGridFromLecture)
    print(result)

    print('Floyds Algorithm')

    d = [
        [0, 3, 999, 4, 999],
        [999, 0, 4, 2, 1],
        [999, 999, 0, 999, 999],
        [4, 999, 999, 0, 3],
        [999, 999, 2, 2, 0]
    ]

    f = floydsalgorithm(d)
    for i in f[0]: print(i)
    print('-' * 20)
    for i in f[1]: print(i)

    print('\n')
    print('Q3:')
    print('\n')

    q3 = [
        [0,1,999,10],
        [13,0,2,999],
        [999,12,0,3],
        [4,999,11,0]
    ]

    f = floydsalgorithm(q3)
    for i in f[0]: print(i)
    print('-' * 20)
    for i in f[1]: print(i)

    print('Question 4')

    q4 = [
        [0,3,999,2,999,999,999],
        [3,0,3,2,2,999,999],
        [999,3,0,999,2,2,999],
        [2,2,999,0,1,999,1],
        [999,2,2,1,0,1,1],
        [99,999,2,999,1,0,1],
        [999,999,999,1,1,1,0]
    ]

    minTree = minSpanningTreeKruskal(q4)

    for i in minTree:
        print(i)

test()

