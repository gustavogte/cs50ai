# CS50 AI with python 2024

## Search

- Tile puzzle
- Maze solving -> Driving direcctions

### Terms

- agent; entity than perceives the problem and act upon that. Ejem. car, person.
- state: some configuration of the agent and its environment.
- initial state: where the agent begins.
- actions: choices that can be made in a state.
- function Actions(*s*) returns a set of actions than can be executed in a state *s*.

#### Transition Model

- Result(s,a) returns the state resulting from action *a* in state *s*.
- state space: the set of all states reachable from the initial state by any sequence of actions.
  - -> a graph with arrows an nodes.

#### Goal Test

- Way to determine whether a given state is a goal state.

#### Path Cost

- Numerical cost associated with a given path.
- A cost for each action. In some cases the actions can have different costs, other times they can have the same cost.

#### Resume Search problem

- initial state
- actions
- trasition model (how state and actions are realted to each other) Result(state, -> actions) = x
- State Space (all states reachable form initial state by any sequence of actions) -> **graph** 
- goal test
- path cost function
  - => get the optimal solutiion (with the lowest path cost)

### Node

A data structure that keeps track of 4 values:

1. state
2. parent node
3. an action (applied to parent to get this node)
4. path cost (from initial state to node)

### Frontier

The frontier, the mechanism that “manages” the nodes. The frontier starts by containing an initial state and an empty set of explored items, and then repeats the following actions until a solution is reached.


### Approach (Revised)

To avoid going back and foward to the same already visited node.
So we add an explored set to the frontier.

Now we have: **frontier** and **explored set**

#### Frontier is a Datastructure

  - Stack
  - Queue

####

- Start with the frontier that contains the initial state -> *the frontier is Data structure
- Start with an empty explored set.
- Repeat
  - If the frontier is empty, then no solution.
  - **Remove node from the frontier**
  - If node contains goal state, return the solution.
  - Add the node to the explored set.
  - Expand the node, add resulting nodes to the frontier if they aren't already in the frontier or the explored set.

- stack (data structure) (list)
- last-in first-out (data type)

### Depth-First Search (DFS)

- Uses a Stack
 => Depth-First Search -> always expands the deepest node in the frontier.
- When it hit a dead end it back up to that point and look again.
- Eventually it will find the solution, because it will explore everything.
- I could not be the most efficient solution.

### Breadth-First Search (BFS)

**Doesn't now any information Uninformed Search No problem specific knowlodge** 

- Uses a queue
  - Explore the closer path first (the shallower one)
  => first-in first-out
  - It always find the optimal path at the end.

### Greedy Best-First Search (GBFS)

**Informed Search, search algorithm that expands the node that is closest to the goal, as estimated by heuristic function h(n)**

- Herustic is an estimated how far away we are from the goal, but is estimated only not guarantee.
- We need a good heuristic.
- It is not always the optimal solution.

### A* Star Search

- Search algorithm that expands node with lowest value of g(n) + h(n)
  - g(n) = cost to reach node
  - h(n) = estimated cost to goal

  => Solves the problem of not getting the optimal solution.

  => Optimal only if some conditions
    1. h(n) is admissible (never overestimates the true cost)
    2. h(n) is consistent (for every node *n* and successor *n'* with step cost *c,h(n)<=h(n')+c)*

  => **THE IMPORTANT PART IS CHOOSING THE RIGHT HEURISTIC**

## Adversarial Search

- There are at least to agents
- They are competing against you

### Minimax

- MAX (X) aims to maximize the score
- MIN (O) aims to minimize the score

### Game functions (tic tac toe/gato) 255,169 possible games

- S0: initial state
- PLAYER(s): returns which player to move in state *s*
- ACTIONS(s): returns legal moves in state *s*
- RESULT(s,a): returnst state afte action *a* taken in stat *s* => transition model
- TERMINAL(s): checks if state *s* is a terminal state
- UTILITY(s): final numerical value of state *s*

### Alpha-Beta Pruning

- Try to optimize the Minimax algorith, more efficient
- Chess games possibilities 10 exp 29000 => to big for the computer
  => Depth-Limited Minimax

### Depth-Limited Minimax

- Include Evaluation function, than estimates the expected utility of the game for a given state
 => The better the evaluation function is the better the AI can predict the result

