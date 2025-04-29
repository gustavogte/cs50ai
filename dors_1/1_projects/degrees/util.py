class Node():
    #state = actors_name, parent = node, action = movie 
    def __init__(self, state:str, parent, action:str) -> None:
        self.state = state # actor
        self.parent = parent # node
        self.action = action # movie



# DFS (LIFO)
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    # Check if the actor is in the frontier
    def contains_state(self, state:str)-> bool:
        for node in self.frontier:
            if node.state == state:
                return True
        return False
        #return any(node.state == state for node in self.frontier)
        

    def empty(self):
        if len(self.frontier) == 0:
            return True
        return False 
        #return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            #remove the last item
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

# For BFS (FIFO)
class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
