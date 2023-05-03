import networkx as nx
import matplotlib.pyplot as plt
import copy

class DecentralizedAlg:
    def __init__(self, graph):
        self.graph = graph
        self.vectors = {}
        self.vectors_old = {}
        self.graphPaths = {}

        # Create starting vector tables and path lists
        for i in self.graph.nodes():
            self.vectors[i] = {i:float('inf') for i in self.graph.nodes()}
            self.graphPaths[i] = {i:[] for i in self.graph.nodes()}
            self.getStartingVector(i)
    
    def find_shortest_path(self, start, end):
        # Returns the shortest path
        while self.vectors != self.vectors_old:
            self.vectors_old = copy.deepcopy(self.vectors)
            for nodes in self.graph.nodes():
                self.bellman(nodes)
        
        return self.vectors[start][end], self.get_path(start, end)

    def get_path(self,node,target):
        if node == target: return str(target)
        else: return str(node) + ", " + self.get_path(self.graphPaths[node][target][-1], target)        

    def bellman(self, node):
        cost = nx.get_edge_attributes(self.graph, 'weight')
        computations = {}
        computationIndex = {}
        # Computations hold calculations, while index holds which node it connects to
        for nodes in self.graph.nodes():
            computations[nodes] = []
            computationIndex[nodes] = []
            for currentNode in self.graph.neighbors(node):
                if currentNode in self.vectors_old[currentNode]:
                    if (currentNode, node) in cost:
                        computations[nodes].append(cost[(currentNode, node)] + self.vectors_old[currentNode][nodes])
                    else:
                        computations[nodes].append(cost[(node, currentNode)] + self.vectors_old[currentNode][nodes])
                    computationIndex[nodes].append(currentNode)

        computations[node] = [0] # at the current node, the minimum is 0 

        for routers in self.vectors_old[node]:
                value = min(computations[routers])
                nodeIndex = min(range(len(computations[routers])), key=computations[routers].__getitem__)
                self.vectors[node][routers] = value
                self.graphPaths[node][routers].append(computationIndex[routers][nodeIndex])
                # Update graphVectors instead of old -> new table


    def getStartingVector(self,node):
        # Creates starting vector table for every node
        neighbours = self.graph.neighbors(node)
        cost = nx.get_edge_attributes(self.graph, 'weight')

        for neighbour in neighbours:
            try:
                self.vectors[node][neighbour] = cost[(node, neighbour)]
            except: self.vectors[node][neighbour] = cost[(neighbour, node)]
    
    def printVectorTable(self):
        # Concatenate all tables into a string variable
        toReturn = "Vector Table:\n"
        for key,value in self.vectors.items():
            toReturn += f"Node: {key}, table = {value}\n"
        
        # Return the concatenated string variable
        return toReturn

if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge('A', 'B',weight=8)
    G.add_edge('A', 'D',weight=1)

    G.add_edge('B', 'C',weight=1)
    G.add_edge('B', 'E',weight=1)

    G.add_edge('D', 'G',weight=1)
    G.add_edge('D', 'E',weight=1)

    G.add_edge('E', 'F',weight=1)
    G.add_edge('E', 'H',weight=1)

    G.add_edge('F', 'I',weight=1)

    G.add_edge('H', 'G',weight=1)
    G.add_edge('H', 'I',weight=1)

    #print([i for i in G.neighbors("A")])
    #labels = nx.get_edge_attributes(G,'weight')

    #print(labels)

    app = DecentralizedAlg(G)

    print("shortest path\n")
    print(app.find_shortest_path("A", "C"))

    print("vector table\n")
    app.printVectorTable()

    nx.draw(G, with_labels=True, arrows=True)
    plt.show()
