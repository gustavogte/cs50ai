"""
Exercise 3: Finding a Path Between Two Nodes
Objective:
Implement a search algorithm (BFS) to find a path between two nodes in the graph.
Instructions:
1. Extend the Graph class from the previous exercise by adding a bfs(self, start, goal) method.
2. The bfs method should:
    - Accept two node names (start and goal) as parameters.
    - Use Breadth-First Search (BFS) to find a path from start to goal.
    - Return a list of node names representing the shortest path.
    - Return None if there is no path between the nodes.
3. Algorithm Implementation:
    - Start with a queue containing a tuple of (current_node, path_taken), where:
        - current_node is the node being explored.
        - path_taken is a list of names representing the path so far.
    - Use a visited set to avoid re-exploring nodes.
    - For each node, enqueue its neighbors along with the updated path.
    - If the goal node is found, return the path.
    - If the queue is empty and the goal is not found, return None.
"""
from collections import deque

class Node:
    def __init__(self, name:str):
        self.name = name
        self.neighbors = []

    #Use this method only inside the graph    
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def __str__(self):
        return self.name
    

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name:str) -> None:
        if name not in self.nodes:
            self.nodes[name] = Node(name)
    
    def add_edge(self, name1:str, name2:str) -> None:
        if name1 in self.nodes and name2 in self.nodes:
            node1 = self.nodes[name1]
            node2 = self.nodes[name2]
            if node1 not in node2.neighbors:
                node2.add_neighbor(node1)
            if node2 not in node1.neighbors:
                node1.add_neighbor(node2)
    
    def bfs(self, start:str, goal:str)-> list:
        if start not in self.nodes or goal not in self.nodes:
            return None
        # Object and neighbors
        queue_frontier = deque([(self.nodes[start], [start])])
        print(type('type'), type(queue_frontier))
        explored_set = set()
        while queue_frontier:
            node, path = queue_frontier.popleft()
            if node.name in explored_set:
                continue
            explored_set.add(node.name)
            for neighbor in node.neighbors:
                if neighbor.name not in explored_set:
                    queue_frontier.append((neighbor, path + [neighbor.name]))
            if node.name == goal:
                return path
        return None
    

    def show_graph(self)-> None:
        for name in self.nodes:
            print(name, "->", end=" ")
            for neighbor in self.nodes[name].neighbors:
                print(neighbor, end=", ")
            print()


# Test the implementation
g = Graph()  # Create an instance of Graph
g.add_node("Alice")  # Add node Alice
g.add_node("Bob")  # Add node Bob
g.add_node("Charlie")  # Add node Charlie
g.add_node("David")  # Add node David
g.add_edge("Alice", "Bob")  # Create a connection between Alice and Bob
g.add_edge("Bob", "Charlie")  # Create a connection between Bob and Charlie
g.add_edge("Charlie", "David")  # Create a connection between Charlie and David
# Test BFS search function
print(g.bfs("Alice", "David"))  # Expected output: [‘Alice’, ‘Bob’, ‘Charlie’, ‘David’]
print(g.bfs("Alice", "Charlie"))  # Expected output: [‘Alice’, ‘Bob’, ‘Charlie’]
print(g.bfs("Alice", "Eve"))  # Expected output: None (because Eve does not exist)



