import sys

class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}
        self.distance = sys.maxsize #开始顶点到此顶点的长度
        self.color = 'white'    # 标记 未发现“白色” 发现临接顶点设置其为“灰色”  完成当前节点的遍历探索设置当前节点为“黑色”
        self.pred = None    # 前驱节点
        self.finishTime = 0     #发现时所走步数
        self.discovery = 0      #完成遍历时所走的步数

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight
    def __repr__(self):
        return str(self.id)+' connectedTo: ' + str([x.id for x in self.connectedTo])
    def __str__(self):
        return str(self.id)+' connectedTo: ' + str([x.id for x in self.connectedTo])
    
    def setDistance(self,dis):
        self.distance = dis
    def setColor(self,color):
        self.color = color 
    def setPred(self,p):
        self.pred = p
    def setFinishTime(self,finish_time):
        self.finishTime = finish_time
    def setDiscovery(self,discovery):
        self.discovery = discovery
    def getConnections(self):
        return self.connectedTo.keys()
    def getId(self):
        return self.id
    def getWeight(self,nbr):
        return self.connectedTo[nbr]
    def getDistance(self):
        return self.distance
    def getColor(self):
        return self.color
    def getPred(self):
        return self.pred
    def getFinishTime(self):
        return self.finishTime
    def getDiscovery(self):
        return self.discovery
class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex
    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None
    def __contains__(self,n):
        return n in self.vertList
    def addEdge(self,f,t,weight=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t],weight)
    def getVertices(self):
        return self.vertList.keys()
    def __iter__(self):
        return iter(self.vertList.values())

    def dfs(self):
        pass
class myQueue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self,item):         #倒插法
        self.items.insert(0,item)
    def dequeue(self):              #删除列表中的最后一个元素，由于是倒插法，故删除第一个元素
        return self.items.pop()
    def size(self):
        return len(self.items)

class DFSGraph(Graph):
    def __init__(self):
        super().__init__()
        self.time = 0
    def dfs(self):
        for aVertex in self:
            aVertex.setColor('white')
            aVertex.setPred(-1)
        for aVertex in self:
            if aVertex.getColor()=='white':
                self.dfsvisit(aVertex)
                print('\n')     #不同分支的DFS树，生成DFS森林
    def dfsvisit(self,startVertex):
        startVertex.setColor('gray')
        self.time+=1
        startVertex.setDiscovery(self.time)
        for nextVertex in startVertex.getConnections():
            if nextVertex.getColor()=='white':
                nextVertex.setPred(startVertex)
                self.dfsvisit(nextVertex)
        startVertex.setColor('black')
        print(startVertex.getId(),end='')
        self.time+=1
        startVertex.setFinishTime(self.time)

class BFSGraph(Graph):      #同DFS森林
    def __init__(self):
        super().__init__()
    def bfs(self):
        for aVertex in self:
            aVertex.setDistance(0)
            aVertex.setPred(None)
        for aVertex in self:
            if aVertex.getPred()==None:
                self.bfsvisit(aVertex)
                print('\n')
    def bfsvisit(self,start_v):
        dfsQueue = myQueue()
        dfsQueue.enqueue(start_v)
        while dfsQueue.size()>0:
            curr_v = dfsQueue.dequeue()
            for nbr in curr_v.getConnections():
                if nbr.getColor()=='white':
                    nbr.setColor('gray')
                    nbr.setDistance(curr_v.getDistance()+1)
                    nbr.setPred(curr_v)
                    dfsQueue.enqueue(nbr)
            curr_v.setColor('black')
            print(curr_v.getId(),end='')

class PriorityQueue:
    def __init__(self):
        self.heapArray = [(0,0)]
        self.currentSize = 0

    def buildHeap(self,alist):
        self.currentSize = len(alist)
        self.heapArray = [(0,0)]
        for i in alist:
            self.heapArray.append(i)
        i = len(alist) // 2            
        while (i > 0):
            self.percDown(i)
            i = i - 1
                        
    def percDown(self,i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapArray[i][0] > self.heapArray[mc][0]:
                tmp = self.heapArray[i]
                self.heapArray[i] = self.heapArray[mc]
                self.heapArray[mc] = tmp
            i = mc
                
    def minChild(self,i):
        if i*2 > self.currentSize:
            return -1
        else:
            if i*2 + 1 > self.currentSize:
                return i*2
            else:
                if self.heapArray[i*2][0] < self.heapArray[i*2+1][0]:
                    return i*2
                else:
                    return i*2+1

    def percUp(self,i):
        while i // 2 > 0:
            if self.heapArray[i][0] < self.heapArray[i//2][0]:
               tmp = self.heapArray[i//2]
               self.heapArray[i//2] = self.heapArray[i]
               self.heapArray[i] = tmp
            i = i//2
 
    def add(self,k):
        self.heapArray.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def delMin(self):
        retval = self.heapArray[1][1]
        self.heapArray[1] = self.heapArray[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapArray.pop()
        self.percDown(1)
        return retval
        
    def isEmpty(self):
        if self.currentSize == 0:
            return True
        else:
            return False

    def decreaseKey(self,val,amt):
        # this is a little wierd, but we need to find the heap thing to decrease by
        # looking at its value
        done = False
        i = 1
        myKey = 0
        while not done and i <= self.currentSize:
            if self.heapArray[i][1] == val:
                done = True
                myKey = i
            else:
                i = i + 1
        if myKey > 0:
            self.heapArray[myKey] = (amt,self.heapArray[myKey][1])
            self.percUp(myKey)
            
    def __contains__(self,vtx):
        for pair in self.heapArray:
            if pair[1] == vtx:
                return True
        return False

if __name__ == "__main__":
    
    def traverse(y):    #由某一结点找根节点
        ls = []
        x = y
        while x.getPred()!=None:
            ls.append(x.getId())
            # print(x.getId())
            x = x.getPred()
        # print(x.getId())  
        ls.append(x.getId())
        for _ in ls:
            print(_, end='')

    def init_graph(Graph):


        for i in range(1,7):
            Graph.addVertex(i)
        
        Graph.addEdge(1,2,6)
        Graph.addEdge(1,3,5)
        Graph.addEdge(1,4,5)
        Graph.addEdge(2,3,5)
        Graph.addEdge(3,4,5)
        Graph.addEdge(2,5,3)
        Graph.addEdge(3,5,6)
        Graph.addEdge(3,6,4)
        Graph.addEdge(4,6,2)
        Graph.addEdge(5,6,6)
        # for i in range(6):
        #     Graph.addVertex(i)
           
        # Graph.addVertex('1W0')
        # Graph.addVertex('120')
        # Graph.addEdge(0,1)
        # Graph.addEdge(0,2)
        # Graph.addEdge(1,3)
        # Graph.addEdge(1,4)
        # Graph.addEdge(2,5)
        # Graph.addEdge(2,6)
        # Graph.addEdge(3,7)
        # Graph.addEdge(4,8)
        # Graph.addEdge(7,9)
        # Graph.addEdge('1W0','120')

        for v in Graph:
            for w in v.getConnections():
                print("({0},{1})".format(v.getId(),w.getId()))

    def init_graph_file(Graph):
        with open('graph_vertx.txt','r') as f:
            for line in f.readlines():
                vertx = line.strip()
                Graph.addVertex(vertx)

        with open('graph_edge.txt','r') as f:
            for line in f.readlines():
                edge = line.strip()
                head,tail,weight = edge.split(',')
                weight = int(weight)
                Graph.addEdge(head,tail,weight)
            for v in Graph:
                for w in v.getConnections():
                  print("({0},{1})".format(v.getId(),w.getId()))
    def prim(G,start):
        pq = PriorityQueue()
        for v in G:
            v.setDistance(sys.maxsize)
            v.setPred(None)
        start.setDistance(0)
        pq.buildHeap([(v.getDistance(),v) for v in G])
        while not pq.isEmpty():
            currentVert = pq.delMin()
            print(currentVert.getId(),end='') 
            for nextVert in currentVert.getConnections():
                newCost = currentVert.getWeight(nextVert)
                if nextVert in pq and newCost<nextVert.getDistance():
                    nextVert.setPred(currentVert)
                    nextVert.setDistance(newCost)
                    pq.decreaseKey(nextVert,newCost)
    # g = Graph()
    # for i in range(6):
    #     g.addVertex(i)

    # print(g.vertList)
    # # g.addEdge(0,1,5)
    # # g.addEdge(0,5,2)
    # # g.addEdge(1,2,4)
    # # g.addEdge(2,3,9)
    # # g.addEdge(3,4,7)
    # # g.addEdge(3,5,3)
    # # g.addEdge(4,0,1)
    # # g.addEdge(5,4,8)
    # # g.addEdge(5,2,1)

    # print('\n 寻根:')
    # traverse(g.getVertex(9))
    # print('\n')

    print('####################BFS_Begin##########################')
    bg = BFSGraph()
    init_graph(bg)
    print(bg.vertList)
    bg.bfs()
    print('\n 逆序寻根')
    traverse(bg.getVertex(5))
    print('\n')
    print('prim算法---按照添加至最小生成树的节点的先后顺序')
    prim(bg,bg.getVertex(1))
    print('\n')
    print('#####################BFS_End############################')
    print('\n')
    print('#####################DFS_Begin##########################')
    dg = DFSGraph()
    init_graph(dg)
    print(dg.vertList)
    dg.dfs()
    print('\n 逆序寻根')
    traverse(bg.getVertex(5))
    print('\n')
    print('prim算法---按照添加至最小生成树的节点的先后顺序')
    prim(dg,dg.getVertex(1))
    print('\n')
    print('#####################DFS_End############################')
    print('\n')
    print("###########----Test_file----########")
    dg = DFSGraph()
    init_graph_file(dg)
    print(dg.vertList)
    dg.dfs()
    print('\n 逆序寻根')
    traverse(bg.getVertex(5))
    print('\n')
    print('prim算法---按照添加至最小生成树的节点的先后顺序')
    prim(dg,dg.getVertex('v1'))
    print('\n')