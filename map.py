
class priorityDictionary(dict):  #Initialized as binary heap of dicitionary 
    def __init__(self):		     #Used to optimize graphs 
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        if len(self) == 0:
            return
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2*insertionPoint+1
                if smallChild+1 < len(heap) and \
                        heap[smallChild] > heap[smallChild+1]:
                    smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]
	
    def __iter__(self):
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]
        return iterfn()
	
    def __setitem__(self,key,val):
        dict.__setitem__(self,key,val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v,k) for k,v in self.iteritems()]
            self.__heap.sort()
        else:
            newPair = (val,key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and \
                    newPair < heap[(insertionPoint-1)//2]:
                heap[insertionPoint] = heap[(insertionPoint-1)//2]
                insertionPoint = (insertionPoint-1)//2
            heap[insertionPoint] = newPair
	
    def setdefault(self,key,val):
        if key not in self:
            self[key] = val
        return self[key]                                  # source:http://code.activestate.com/recipes/117228-priority-dictionary/

#---------------------------------------------------------Utilities for graph

def add_vertex(vert_dict, node):
    vert_dict[node] = {}

def get_vertex(vert_dict, n):
    if n in vert_dict:
        return vert_dict[n]
    else:
        return None

def add_edge(vert_dict, frm, to, cost = 0):
    if frm not in vert_dict:
        add_vertex(vert_dict,frm)
    if to not in vert_dict:
        add_vertex(vert_dict,to)

    vert_dict[frm][to] = cost
    vert_dict[to][frm] = cost

def get_vertices(vert_dict):
    return vert_dict.keys()

#------------------------------------------------------------------------------

def shortestPath(G,start,end):  # Dijkstra's algorithm implimentation

	D = {}			   # dictionary of final distances
	P = {}			   # dictionary of path
	Q = priorityDictionary()   
	Q[start] = 0
	
	for v in Q:
		D[v] = Q[v]
		if v == end: break
		
		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w not in D:
				if w not in Q or vwLength < Q[w]:# The vertex w is not present in the list of connections or
					Q[w] = vwLength		         # If we found a shotter path that distance in updated
					P[w] = v		             # That vertex is also added to the path dict

	Path = []
	while 1:
		Path.append(end)	
		if end == start: break
		end = P[end]
	Path.reverse()
	return Path

#------------------------------------------------------------------------------


if __name__ == '__main__':

    g={}									# Nested dict for representation of graphs. For any vertex v,g[v] is itself a dictionary
    
    with open("tn_graph.txt")as f:
        lines = f.read().split("\n")
        
    node_no = int(lines[0])
    
    for i in range(node_no):
        add_vertex(g,i)
    
    edge_no = int(lines[node_no+1])
    
    for i in range(edge_no):
        k = lines[i+node_no+2].split(" ")
        add_edge(g,k[0],k[1], float (k[3]))
    
    points = []
    points.append(input())
    for i in range(points[0]):
	points.append(input())

    path_list = []
    print(points[1])
    for i in range(int(points[0])-1):						# Finding shortest path along every pair
        path_list.append(shortestPath(g,str(points[i+1]),str(points[i+2])))
    path_list.append(shortestPath(g,str(points[-1]),str(points[1])))
    
    for i in path_list:
        for j in range(1,len(i)):
            print "%s"%i[j]
