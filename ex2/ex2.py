[23bcs123@mepcolinux ex2]$cat ex2.prn
Script started on Tue Feb 10 10:56:00 2026
[23bcs123@mepcolinux ex2]$cat pro1.py
class Graph:
    def __init__(self):
        self.adj = {}

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []
            print(f"Node {node} added")
        else:
            print("Node already exists")

    def delete_node(self, node):
        if node in self.adj:
            for i in self.adj:
                self.adj[i] = [x for x in self.adj[i] if x[0] != node]
            del self.adj[node]
            print(f"Node {node} deleted")
        else:
            print("Node not found")

    def add_edge(self, n1, n2, cost):
        if n1 in self.adj and n2 in self.adj:
            self.delete_edge(n1, n2)
            self.adj[n1].append((n2, cost))
            self.adj[n2].append((n1, cost))
            print(f"Edge {n1}-{n2} added with cost {cost}")
        else:
            print("Both nodes must exist")

    def delete_edge(self, n1, n2):
        if n1 in self.adj and n2 in self.adj:
            self.adj[n1] = [x for x in self.adj[n1] if x[0] != n2]
            self.adj[n2] = [x for x in self.adj[n2] if x[0] != n1]
        else:
            print("Nodes not found")

    def display(self):
        print("\nAdjacency List:")
        for i in self.adj:
            print(f"{i} -> {self.adj[i]}")

def a_star(graph, start, goal):
    if start not in graph.adj or goal not in graph.adj:
        print("Start or Goal node not found")
        return None

    print(f"\nEnter heuristic values (h) for reaching {goal}:")
    heuristics = {node: int(input(f"  h({node}): ")) for node in graph.adj}
    queue = [[heuristics[start], 0, start, [start]]]
    closed_list = []
    step = 1

    print("\n--- A* Search Traversal Steps ---")
    while queue:

        queue.sort(key=lambda x: x[0])


        open_list_display = [item[2] for item in queue]
        print(f"\nStep {step}")
        print(f"OPEN: {open_list_display}")
        print(f"CLOSED: {closed_list}")

        f_cost, g_cost, current, path = queue.pop(0)
        print(f"Selected: {current} g: {g_cost} h: {heuristics[current]} f: {f_cost}")

        if current == goal:
            print("Goal node found!")
            print(f"Final Path: {' -> '.join(path)}")
            print(f"Total Cost: {g_cost}")
            return path, g_cost

        if current not in closed_list:
            closed_list.append(current)

        for neighbor, weight in graph.adj[current]:
            if neighbor in closed_list:
                continue

            new_g = g_cost + weight
            new_f = new_g + heuristics[neighbor]


            found_in_queue = False
            for i in range(len(queue)):
                if queue[i][2] == neighbor:
                    found_in_queue = True
                    if new_g < queue[i][1]:
                        queue[i] = [new_f, new_g, neighbor, path + [neighbor]]
                    break

            if not found_in_queue:
                queue.append([new_f, new_g, neighbor, path + [neighbor]])

        step += 1

    print("Goal not found")
    return None
graph = Graph()
try:
    n_nodes = int(input("Enter number of nodes: "))
    for _ in range(n_nodes):
        graph.add_node(input("Enter node: "))

    n_edges = int(input("Enter number of edges: "))
    for _ in range(n_edges):
        u = input("Enter node 1: ")
        v = input("Enter node 2: ")
        c = int(input("Enter cost: "))
        graph.add_edge(u, v, c)
except ValueError:
    print("Invalid input, please enter numeric values for counts/costs.")
while True:
    print("\n--- MENU ---")
    print("1. Add Node     \n 2. Delete Node")
    print("3. Add Edge      \n4. Delete Edge")
    print("5. Display       \n6. A* Search")
    print("7. Exit")

    choice = input("Enter choice: ")
    if choice == '1':
        graph.add_node(input("Enter node: "))
    elif choice == '2':
        graph.delete_node(input("Enter node to delete: "))
    elif choice == '3':
        u, v, c = input("Node 1: "), input("Node 2: "), int(input("Cost: "))
        graph.add_edge(u, v, c)
    elif choice == '4':
        graph.delete_edge(input("Node 1: "), input("Node 2: "))
    elif choice == '5':
        graph.display()
    elif choice == '6':
        a_star(graph, input("Start Node: "), input("Goal Node: "))
    elif choice == '7':
        print("Exiting...")
        break
    else:
        print("Invalid choice")
[23bcs123@mepcolinux ex2]$python3 prog.py
Enter number of nodes: 7
Enter node: Arad
Node Arad added
Enter node: Sibiu
Node Sibiu added
Enter node: Timisoara
Node Timisoara added
Enter node: Fagaras
Node Fagaras added
Enter node: Rimnicu Vilcea
Node Rimnicu Vilcea added
Enter node: Pitesti
Node Pitesti added
Enter node: Bucharest
Node Bucharest added
Enter number of edges: 7
Enter node 1: Arad
Enter node 2: Sibiu
Enter cost: 140
Edge Arad-Sibiu added with cost 140
Enter node 1: Arad
Enter node 2: Timisoara
Enter cost: 118
Edge Arad-Timisoara added with cost 118
Enter node 1: Sibiu
Enter node 2: Fagaras
Enter cost: 99
Edge Sibiu-Fagaras added with cost 99
Enter node 1: Sibiu
Enter cost: 80
Edge Sibiu-Rimnicu Vilcea added with cost 80
Enter node 1: Fagaras
Enter node 2: Bucharest
Enter cost: 211
Edge Fagaras-Bucharest added with cost 211
Enter node 1: Rimnicu Vilcea
Enter node 2: Pitesti
Enter cost: 97
Edge Rimnicu Vilcea-Pitesti added with cost 97
Enter node 1: Pitesti
Enter node 2: Bucharest
Enter cost: 101
Edge Pitesti-Bucharest added with cost 101

--- MENU ---
1. Add Node
 2. Delete Node
3. Add Edge
4. Delete Edge
5. Display
6. A* Search
7. Exit
Enter choice: 5

Adjacency List:
Arad -> [('Sibiu', 140), ('Timisoara', 118)]
Sibiu -> [('Arad', 140), ('Fagaras', 99), ('Rimnicu Vilcea', 80)]
Timisoara -> [('Arad', 118)]
Fagaras -> [('Sibiu', 99), ('Bucharest', 211)]
Rimnicu Vilcea -> [('Sibiu', 80), ('Pitesti', 97)]
Pitesti -> [('Rimnicu Vilcea', 97), ('Bucharest', 101)]
Bucharest -> [('Fagaras', 211), ('Pitesti', 101)]

--- MENU ---
1. Add Node
 2. Delete Node
3. Add Edge
4. Delete Edge
5. Display
6. A* Search
7. Exit
Enter choice: 6
Start Node: Arad
Goal Node: Bucharest

Enter heuristic values (h) for reaching Bucharest:
  h(Arad): 366
  h(Sibiu): 253
  h(Timisoara): 329
  h(Fagaras): 178
  h(Rimnicu Vilcea): 193
  h(Pitesti): 98
  h(Bucharest): 0

--- A* Search Traversal Steps ---

Step 1
OPEN ['Arad']
CLOSED []
Selected: Arad g: 0 h: 366 f: 366

Step 2
OPEN ['Sibiu', 'Timisoara']
CLOSED ['Arad']
Selected: Sibiu g: 140 h: 253 f: 393

Step 3
OPEN ['Rimnicu Vilcea', 'Fagaras', 'Timisoara']
CLOSED ['Arad', 'Sibiu']
Selected: Rimnicu Vilcea g: 220 h: 193 f: 413

Step 4
OPEN ['Pitesti', 'Fagaras', 'Timisoara']
CLOSED ['Arad', 'Sibiu', 'Rimnicu Vilcea']
Selected: Pitesti g: 317 h: 98 f: 415

Step 5
OPEN ['Fagaras', 'Bucharest', 'Timisoara']
CLOSED ['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti']
Selected: Fagaras g: 239 h: 178 f: 417

Step 6
OPEN ['Bucharest', 'Timisoara']
CLOSED ['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Fagaras']
Selected: Bucharest g: 418 h: 0 f: 418
Goal node found!
Final Path: Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest
Total Cost: 418

--- MENU ---
1. Add Node
 2. Delete Node
3. Add Edge
4. Delete Edge
5. Display
6. A* Search
7. Exit
Enter choice: 7
Exiting...
[23bcs123@mepcolinux ex2]$exit

Script done on Tue Feb 10 10:56:06 2026