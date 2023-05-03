import networkx as nx

class CentralizedAlg:
    def __init__(self, graph):
        self.graph = graph

    def find_shortest_path(self, start, end):
        distances = {}
        parents = {}
        visited = []
        unvisited = list(self.graph.nodes())

        for node in unvisited:
            distances[node] = float('inf')

        distances[start] = 0

        while unvisited:
            current_node = min(unvisited, key=distances.get)
            for neighbor in self.graph.neighbors(current_node):
                if neighbor in visited:
                    continue

                new_distance = distances[current_node] + self.graph[current_node][neighbor]['weight']
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parents[neighbor] = current_node

            visited.append(current_node)
            unvisited.remove(current_node)

            if current_node == end:
                path = []
                node = end
                while node != start:
                    path.append(node)
                    node = parents[node]
                path.append(start)
                path.reverse()
                return (path, distances)

    def generate_path(self, start, end):
        path = []
        distances = self.find_shortest_path(start, end)[1]
        node = end
        while node != start:
            path.append(node)
            node = self.find_shortest_path(start, end)[0][self.find_shortest_path(start, end)[0].index(node) - 1]
        path.append(start)
        path.reverse()
        return path
