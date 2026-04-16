from collections import deque
import heapq

class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, u, v, cost=1):
        if u not in self.graph:
            self.add_node(u)
        if v not in self.graph:
            self.add_node(v)
        self.graph[u].append((v, cost))
        self.graph[v].append((u, cost))

    def delete_node(self, node):
        if node in self.graph:
            del self.graph[node]
            for n in self.graph:
                self.graph[n] = [(v, c) for v, c in self.graph[n] if v != node]

    def delete_edge(self, u, v):
        if u in self.graph:
            self.graph[u] = [(x, c) for x, c in self.graph[u] if x != v]
        if v in self.graph:
            self.graph[v] = [(x, c) for x, c in self.graph[v] if x != u]

    def display_adjacency_list(self):
        print("\nadjacency list:")
        for node in self.graph:
            print(f"{node} -> {self.graph[node]}")

    def bfs_search(self, start, goal):
        if start not in self.graph:
            return None
        if start in goal:
            return [start]

        fringe = deque([start])
        visited = set([start])
        search_path = [start]

        print("\nBFS search:")
        while fringe:
            print("fringe:", list(fringe))
            current = fringe.popleft()
            print("expand:", current)

            for neighbor, _ in self.graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    search_path.append(neighbor)

                    if neighbor in goal:
                        return search_path

                    fringe.append(neighbor)

        # Return None if the goal was never reached
        return None

    def dfs_search(self, start, goal):
        if start not in self.graph:
            return None
        fringe = [start]
        visited = set([start])
        path_tracker = {start: [start]}
        print("\nDFS search:")
        while fringe:
            print("fringe:", fringe)
            current = fringe.pop()
            print("expand:", current)
            if current in goal:
                return path_tracker[current]
            for neighbor, _ in reversed(self.graph.get(current, [])):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path_tracker[neighbor] = path_tracker[current] + [neighbor]
                    fringe.append(neighbor)
        return None

    def ucs_search(self, start, goal):
        if start not in self.graph:
            return None, None
        fringe = [(0, start)]
        cost_so_far = {start: 0}
        path_tracker = {start: [start]}
        print("\nUCS search:")
        while fringe:
            print("fringe:", fringe)
            current_cost, current = heapq.heappop(fringe)
            print(f"expand: {current} (cost={current_cost})")
            if current in goal:
                return path_tracker[current], current_cost
            for neighbor, weight in self.graph.get(current, []):
                new_cost = current_cost + weight
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    path_tracker[neighbor] = path_tracker[current] + [neighbor]
                    heapq.heappush(fringe, (new_cost, neighbor))
        return None, None

g = Graph()
n_input = input("enter no. of nodes: ")
n = int(n_input) if n_input else 0
print("enter nodes:")
for i in range(n):
    g.add_node(input())

e_input = input("enter no. of edges: ")
e = int(e_input) if e_input else 0
print("enter edges (u v cost):")
for i in range(e):
    u, v, cost = input().split()
    g.add_edge(u, v, int(cost))

print("\t\t----- MENU -----\n")
print("1. BFS search\t2. DFS search\t3. UCS search\t4. add node\t5. add edge\t\n")
print("6. delete node\t7. delete edge\t8. display adjacency list\t9. exit\t\n")

while True:
    choice = input("enter choice: ")
    if choice == "1":
        start_node = input("enter start node:")
        num_goals = int(input("enter no. of goal nodes:"))
        goal_nodes = []
        print("enter goal nodes: ")
        for i in range(num_goals):
            goal_nodes.append(input())
        search_path = g.bfs_search(start_node, goal_nodes)
        if search_path:
            print("search order:", " >> ".join(search_path))
        else:
            print("Error: goal not reachable from start node.")

    elif choice == "2":
        start_node = input("enter start node:")
        num_goals = int(input("enter no. of goal nodes:"))
        goal_nodes = []
        print("enter goal nodes: ")
        for i in range(num_goals):
            goal_nodes.append(input())
        path = g.dfs_search(start_node, goal_nodes)
        if path:
            print("path:", " >> ".join(path))
        else:
            print("Error: goal not reachable")

    elif choice == "3":
        start_node = input("enter start node:")
        num_goals = int(input("enter no. of goal nodes:"))
        goal_nodes = []
        print("enter goal nodes: ")
        for i in range(num_goals):
            goal_nodes.append(input())
        path, cost = g.ucs_search(start_node, goal_nodes)
        if path:
            print("path:", " >> ".join(path))
            print("cost:", cost)
        else:
            print("Error: goal not reachable")

    elif choice == "4":
        node = input("enter node to add: ")
        g.add_node(node)
        print("node", node, "has been added successfully.")

    elif choice == "5":
        u = input("node 1: ")
        v = input("node 2: ")
        cost = input("cost: ")
        g.add_edge(u, v, int(cost) if cost else 1)
        print("edge between", u, "and", v, "added.")

    elif choice == "6":
        node_to_del = input("enter the node to delete: ")
        g.delete_node(node_to_del)
        print("node", node_to_del, "has been deleted.")

    elif choice == "7":
        u = input("node 1: ")
        v = input("node 2: ")
        g.delete_edge(u, v)
        print("edge between", u, "and", v, "deleted.")

    elif choice == "8":
        g.display_adjacency_list()

    elif choice == "9":
        break
    else:
        print("invalid choice")

[23bcs123@mepcolinux ex1]$python3 prog1.py
enter no. of nodes: 7
enter nodes:
a
b
c
d
e
f
g
enter no. of edges: 6
enter edges (u v cost):
a b 1
a c 1
c d 1
c e 1
e f 1
e g 1
                ----- MENU -----

1. BFS search   2. DFS search   3. UCS search   4. add node     5. add edge

6. delete node  7. delete edge  8. display adjacency list       9. exit

enter choice: 1
enter start node:a
enter no. of goal nodes:1
enter goal nodes:
g

BFS search:
fringe: ['a']
expand: a
fringe: ['b', 'c']
expand: b
fringe: ['c']
expand: c
fringe: ['d', 'e']
expand: d
fringe: ['e']
expand: e
search order: a >> b >> c >> d >> e >> f >> g
enter choice: 2
enter start node:a
enter no. of goal nodes:1
enter goal nodes:
f

DFS search:
fringe: ['a']
expand: a
fringe: ['c', 'b']
expand: b
fringe: ['c']
expand: c
fringe: ['e', 'd']
expand: d
fringe: ['e']
expand: e
fringe: ['g', 'f']
expand: f
path: a >> c >> e >> f
enter choice: 9
[23bcs123@mepcolinux ex1]$python3 prog1.py
enter no. of nodes: 6
enter nodes:
a
b
c
d
e
f
enter no. of edges: 7
enter edges (u v cost):
a b 2
a c 1
a d 4
b d 5
c d 7
c f 3
d f 2
                ----- MENU -----

1. BFS search   2. DFS search   3. UCS search   4. add node     5. add edge

6. delete node  7. delete edge  8. display adjacency list       9. exit

enter choice: 3
enter start node:a
enter no. of goal nodes:1
enter goal nodes:
f

UCS search:
fringe: [(0, 'a')]
expand: a (cost=0)
fringe: [(1, 'c'), (2, 'b'), (4, 'd')]
expand: c (cost=1)
fringe: [(2, 'b'), (4, 'd'), (4, 'f')]
expand: b (cost=2)
fringe: [(4, 'd'), (4, 'f')]
expand: d (cost=4)
fringe: [(4, 'f')]
expand: f (cost=4)
path: a >> c >> f
cost: 4
enter choice: 9
[23bcs123@mepcolinux ex1]$exit

Script done on Tue Feb  3 10:00:27 2026