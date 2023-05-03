import tkinter as tk
from tkinter import *
import networkx as nx
import random
import itertools

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nx_centralizedAlg import CentralizedAlg
from decentralized_networkX import DecentralizedAlg
from tkinter import simpledialog


def create_custom_graph(num_nodes):

    G = nx.Graph()
    for n in range(1, num_nodes + 1):
        number_connectd = simpledialog.askstring(title="number connectd",
                                                 prompt="How many nodes connect with nodes: " + str(
                                                     n),
                                                 parent=root)
        if not number_connectd.isdigit():
            print("Error Please enter valid numbers .")
            return
        for i in range(int(number_connectd)):
            connect_point = simpledialog.askstring(title="connect_point",
                                                   prompt="which nodes is connected with " + str(n) + " node",
                                                   parent=root)
            cost = simpledialog.askstring(title="cost",
                                          prompt="what's the cost between those two nodes",
                                          parent=root)
            if not (connect_point.isdigit() and cost.isdigit()):
                print("Error Please enter valid numbers .")
                return
            G.add_edge(n, int(connect_point), weight=int(cost))
    return G



def create_random_graph(num_nodes, num_edges, cost_range=(1, 10)):
    max_edges = num_nodes * (num_nodes - 1) / 2
    if num_edges > max_edges:
        raise ValueError("num_edges should be at most {}".format(int(max_edges)))

    G = nx.Graph()

    # Add nodes
    G.add_nodes_from(range(1, num_nodes + 1))

    # Add edges and assign costs
    for node in G.nodes():
        if G.degree(node) == 0:
            # Ensure that each node has at least one edge
            node2 = random.choice([n for n in G.nodes() if n != node])
            cost = random.randint(cost_range[0], cost_range[1])
            G.add_edge(node, node2, weight=cost)

    # Add more edges until the desired number is reached
    while G.number_of_edges() < num_edges:
        node1 = random.randint(1, num_nodes)
        node2 = random.randint(1, num_nodes)

        if node1 != node2 and G.edges.get((node1, node2)) is None:
            cost = random.randint(cost_range[0], cost_range[1])
            G.add_edge(node1, node2, weight=cost)

    return G


class GUI:
    def __init__(self, root):
        self.root = root
        self.setup()
        self.graph = None
        self.path = None
        self.length = None


    def setup(self):
        self.root.title("Network Routing Algorithm Visualizer")
        #self.root.maxsize(900, 900)
        self.root.config(bg="dark slate gray")

        self.create_frames()
        self.create_tool_bar()

    def create_frames(self):
        self.left_frame = Frame(self.root, width=200, height=400, bg='peach puff')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        self.right_frame = Frame(self.root, width=850, height=400, bg='DarkGoldenrod1')
        self.right_frame.grid(row=0, column=1, padx=10, pady=5)

    def create_tool_bar(self):
        self.tool_bar = Frame(self.left_frame, width=180, height=185)
        self.tool_bar.grid(row=2, column=0, padx=5, pady=5)

        Label(self.tool_bar, text="Number of Nodes in Graph").grid(
            row=0, column=0, padx=5, pady=5, sticky=W)
        self.nodes_entry = Entry(self.tool_bar)
        self.nodes_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(self.tool_bar, text="Number of Edges in Graph").grid(
            row=1, column=0, padx=5, pady=5, sticky=W)
        self.edges_entry = Entry(self.tool_bar)
        self.edges_entry.grid(row=1, column=1, padx=5, pady=5)

        Button(self.tool_bar, text="Generate Network Graph", command=self.generate_network_graph).grid(
            row=2, column=0, columnspan=1, padx=5, pady=5)
        Button(self.tool_bar, text="Generate Custom Graph", command=self.generate_custom_graph).grid(
             row=2, column=1, columnspan=2, padx=5, pady=5)

        Label(self.tool_bar, text="Origin Node").grid(
            row=3, column=0, padx=5, pady=5, sticky=W)
        self.origin_node_entry = Entry(self.tool_bar)
        self.origin_node_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(self.tool_bar, text="Destination Node").grid(
            row=4, column=0, padx=5, pady=5, sticky=W)
        self.destination_node_entry = Entry(self.tool_bar)
        self.destination_node_entry.grid(row=4, column=1, padx=5, pady=5)

        Button(self.tool_bar, text="Decentralized Algorithm", 
                command=self.show_decentralized_path).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        Button(self.tool_bar, text="Centralized Algorithm",
               command=self.show_centralized_path).grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def generate_network_graph(self):
        num_nodes = self.nodes_entry.get()
        num_edges = self.edges_entry.get()
        if not num_nodes.isdigit() or not num_edges.isdigit():
            print("Error Please enter valid numbers for the number of nodes and edges.")
            return

        num_nodes = int(num_nodes)
        num_edges = int(num_edges)
        G = create_random_graph(num_nodes, num_edges)

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        figure = plt.figure(figsize=(6, 6))
        ax = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, master=self.right_frame)
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        pos = nx.spring_layout(G)
        self.pos = pos  # Store the pos attribute
        nx.draw(G, pos, with_labels=True, node_size=300, ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

        self.graph = G
        self.canvas = canvas  # Store the canvas attribute
        self.ax = ax  # Store the ax attribute

        canvas.draw()
        root.update()

    def generate_custom_graph(self):

        num_nodes = self.nodes_entry.get()

        if not num_nodes.isdigit():
            print("Error Please enter valid numbers for the number of nodes .")
            return

        num_nodes = int(num_nodes)
        G = create_custom_graph(num_nodes)

        # Clear the right_frame before drawing a new graph
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        figure = plt.figure(figsize=(6, 6))
        ax = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, master=self.right_frame)
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        pos = nx.spring_layout(G)
        self.pos = pos  # Store the pos attribute
        nx.draw(G, pos, with_labels=True, node_size=300, ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

        self.graph = G
        self.canvas = canvas  # Store the canvas attribute
        self.ax = ax  # Store the ax attribute

        canvas.draw()
        root.update()

    def show_path_info(self):
            # Remove any existing path and length labels
            if hasattr(self, "path_label"):
                self.path_label.destroy()
            if hasattr(self, "length_label"):
                self.length_label.destroy()

            # Create and display the path label
            self.path_label = Label(
                self.left_frame,
                text=f"Path: {' -> '.join(map(str, self.path))}",
                wraplength=180,
            )
            self.path_label.grid(row=3, column=0, padx=5, pady=5)

            # Create and display the length label
            self.length_label = Label(
                self.left_frame, text=f"Information: \n{self.length}"
            )
            self.length_label.grid(row=4, column=0, padx=5, pady=5)

    #def show_bellman_ford_path(self):
    def show_centralized_path(self):
        try:
            start = int(self.origin_node_entry.get())
            end = int(self.destination_node_entry.get())
        except ValueError:
            print(
                "Error Invalid origin or destination node.")
            return

       # old code
       # dist, path = nx.single_source_bellman_ford(self.graph, start)

        # new code
        central_alg = CentralizedAlg(self.graph)

        path, dist = central_alg.find_shortest_path(start, end)

        print(path)
        print(dist)

        self.path = path
        self.length = dist

        self.show_path_info()


        if not path:
            print("Error No path exists between the selected nodes.")
            return

        # Highlight the path on the graph
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        print(f"path edges:{path_edges}")

        node_colors = [
            'red' if node in path else 'gray' for node in self.graph.nodes()]
        edge_colors = [
            'red' if edge in path_edges else 'gray' for edge in self.graph.edges()]
        nx.draw(self.graph, self.pos, with_labels=True, node_color=node_colors, node_size=300, edge_color=edge_colors,
                ax=self.ax)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(
            self.graph, self.pos, edge_labels=edge_labels, ax=self.ax)

        self.canvas.draw()

    def show_decentralized_path(self):
            print("in decentralized algo")
            try:
                start = int(self.origin_node_entry.get())
                end = int(self.destination_node_entry.get())
            except ValueError:
                print(
                    "Error Invalid origin or destination node.")
                return

        # old code
        # dist, path = nx.single_source_bellman_ford(self.graph, start)

            # new code
            #central_alg = CentralizedAlg(self.graph)

            print("okay instantiating object")
            algorithm = DecentralizedAlg(self.graph)
            result = algorithm.find_shortest_path(start, end)

            dist = result[0]
            print(f"distance is {dist}")

            path = result[1]
            print(path)
            print(f"type of path is {type(path)}")
            path = path.split(",")
            path = list(map(int, path))
            print("new path")
            print(path)

            self.path = path
            self.length = algorithm.printVectorTable()
            print("vector table:")
            print(self.length)

            self.show_path_info()


            if not path:
                print("Error No path exists between the selected nodes.")
                return

            # Highlight the path on the graph
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            print(f"path edges:{path_edges}")

            node_colors = [
                'red' if node in path else 'gray' for node in self.graph.nodes()]
            edge_colors = [
                'red' if edge in path_edges else 'gray' for edge in self.graph.edges()]
            nx.draw(self.graph, self.pos, with_labels=True, node_color=node_colors, node_size=300, edge_color=edge_colors,
                    ax=self.ax)
            edge_labels = nx.get_edge_attributes(self.graph, 'weight')
            nx.draw_networkx_edge_labels(
                self.graph, self.pos, edge_labels=edge_labels, ax=self.ax)

            self.canvas.draw()       


if __name__ == "__main__":
    root = Tk()
    app = GUI(root)
    root.mainloop()
