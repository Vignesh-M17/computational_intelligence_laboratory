import random
import sys

SIZE = 0
world = []
agent_pos = [0, 0]
has_gold = False
wumpus_alive = True

# -------- CREATE WORLD (MODIFIED FOR AGENT POS & USER INPUT) --------
def create_world(size):
    global world, agent_pos
    world = [["" for _ in range(size)] for _ in range(size)]

    print(f"\n--- MANUAL WORLD SETUP (Indices 0 to {size-1}) ---")

    # 1. Place Agent
    while True:
        try:
            pos = input("Enter row and col for the Agent's Start (e.g., 0 0): ").split()
            ax, ay = int(pos[0]), int(pos[1])
            if 0 <= ax < size and 0 <= ay < size:
                agent_pos = [ax, ay]
                break
            else:
                print("Position out of bounds.")
        except:
            print("Invalid input. Enter two numbers.")

    # 2. Place Pits
    num_pits = int(input("Enter number of pits to place: "))
    for i in range(num_pits):
        while True:
            try:
                pos = input(f"Enter row and col for Pit {i+1} (e.g., 1 2): ").split()
                x, y = int(pos[0]), int(pos[1])
                if 0 <= x < size and 0 <= y < size and [x,y] != agent_pos and world[x][y] == "":
                    world[x][y] = "P"
                    break
                else:
                    print("Invalid position (Out of bounds, overlaps agent, or already occupied).")
            except:
                print("Please enter two numbers separated by a space.")

    # 3. Place Wumpus
    while True:
        try:
            pos = input("Enter row and col for the Wumpus: ").split()
            x, y = int(pos[0]), int(pos[1])
            if 0 <= x < size and 0 <= y < size and [x,y] != agent_pos and world[x][y] == "":
                world[x][y] = "W"
                break
            else:
                print("Invalid position.")
        except:
            print("Invalid input format.")

    # 4. Place Gold
    while True:
        try:
            pos = input("Enter row and col for the Gold: ").split()
            x, y = int(pos[0]), int(pos[1])
            if 0 <= x < size and 0 <= y < size and [x,y] != agent_pos and world[x][y] == "":
                world[x][y] = "G"
                break
            else:
                print("Invalid position.")
        except:
            print("Invalid input format.")

# -------- DISPLAY --------
def init_display():
    print("\nINITIAL WORLD VIEW")
    for i in range(SIZE):
        for j in range(SIZE):
            if [i,j] == agent_pos:
                print("A", end=" ")
            elif world[i][j] == "W":
                print("W", end=" ")
            elif world[i][j] == "P":
                print("P", end=" ")
            elif world[i][j] == "G":
                print("G", end=" ")
            else:
                print("_", end=" ")
        print()
    print("A = Agent\tW = Wumpus\tP = Pit\tG = Gold")

def display():
    print("\nCURRENT GRID")
    for i in range(SIZE):
        for j in range(SIZE):
            if [i,j] == agent_pos:
                print("A", end=" ")
            else:
                print("_", end=" ")
        print()
    print("A = Agent")

# -------- SENSOR & PERCEPTION (MODIFIED FOR SAFE MOVES) --------
def sensor():
    x,y = agent_pos
    perceptions = []

    print("\n--- AGENT PERCEPTION ---")
    print(f"Current Position: {agent_pos}")

    if world[x][y] == "G":
        perceptions.append("Glitter")

    breeze = False
    smell = False
    safe_moves = []

    # Check neighbors for sensors and evaluate SAFETY
    for label, dx, dy in [("Up", -1, 0), ("Down", 1, 0), ("Left", 0, -1), ("Right", 0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            # A move is safe if it's not a Pit and not a live Wumpus
            is_pit = (world[nx][ny] == "P")
            is_wumpus = (world[nx][ny] == "W" and wumpus_alive)

            if not is_pit and not is_wumpus:
                safe_moves.append(f"{label} ({nx}, {ny})")

            if is_pit:
                breeze = True
            if is_wumpus:
                smell = True

    if breeze: perceptions.append("Breeze")
    if smell: perceptions.append("Smell")

    if not perceptions:
        print("Perceiving: Safe (Nothing detected)")
    else:
        print(f"Perceiving: {', '.join(perceptions)}")

    # Display only SAFE possible moves
    if safe_moves:
        print(f"Possible SAFE Move Locations: {', '.join(safe_moves)}")
    else:
        print("Possible SAFE Move Locations: NONE (Trapped!)")
    print("------------------------")

# -------- MOVE --------
def move(dx, dy):
    global agent_pos
    x = agent_pos[0] + dx
    y = agent_pos[1] + dy
    if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
        print("\nBUMP WALL")
        display()
        return
    agent_pos = [x,y]
    check()
    display()
    sensor()

# -------- CHECK --------
def check():
    global has_gold
    x,y = agent_pos
    if world[x][y] == "P":
        display()
        print("Fell in PIT GAME OVER")
        sys.exit()
    if world[x][y] == "W" and wumpus_alive:
        display()
        print("WUMPUS killed you GAME OVER")
        sys.exit()
    if world[x][y] == "G":
        print("GOLD FOUND")

# -------- GRAB --------
def grab():
    global has_gold
    x,y = agent_pos
    if world[x][y] == "G":
        has_gold = True
        world[x][y] = ""
        print("GOLD GRABBED. Game Cleared")
        sys.exit()
    else:
        print("No gold here!")
    display()
    sensor()

# -------- SHOOT --------
def shoot():
    global wumpus_alive
    print("\nArrow fired!")
    hit = False
    for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx = agent_pos[0]+dx
        ny = agent_pos[1]+dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            if world[nx][ny] == "W":
                print("SCREEEAM! WUMPUS IS DEAD")
                world[nx][ny] = ""
                wumpus_alive = False
                hit = True
                break
    if not hit:
        print("Arrow missed...")
    display()
    sensor()

# -------- MAIN --------
def main():
    global SIZE
    print("WUMPUS WORLD (Manual Setup)")
    try:
        SIZE = int(input("Enter grid size: "))
    except ValueError:
        print("Defaulting to size 4")
        SIZE = 4

    create_world(SIZE)
    init_display()
    display()
    sensor()
    while True:
        print("\nControls: W (Up), S (Down), A (Left), D (Right), G (Grab), F (Shoot), E (Exit)")
        key = input("Action: ").upper()
        if key == "W":
            move(-1,0)
        elif key == "S":
            move(1,0)
        elif key == "A":
            move(0,-1)
        elif key == "D":
            move(0,1)
        elif key == "G":
            grab()
        elif key == "F":
            shoot()
        elif key == "E":
            if has_gold:
                print("YOU WON!")
            else:
                print("EXITED")
            break
        else:
            print("Invalid Input")

if __name__ == "__main__":
    main()

[23bcs123@mepcolinux ex5]$python3 p1.py
WUMPUS WORLD (Manual Setup)
Enter grid size: 4

--- MANUAL WORLD SETUP (Indices 0 to 3) ---
Enter row and col for the Agent's Start (e.g., 0 0): 3 0
Enter number of pits to place: 2
Enter row and col for Pit 1 (e.g., 1 2): 1 0
Enter row and col for Pit 2 (e.g., 1 2): 3 3
Enter row and col for the Wumpus: 1 3
Enter row and col for the Gold: 0 2

INITIAL WORLD VIEW
_ _ G _
P _ _ W
_ _ _ _
A _ _ P
A = Agent       W = Wumpus      P = Pit G = Gold

CURRENT GRID
_ _ _ _
_ _ _ _
_ _ _ _
A _ _ _
A = Agent

--- AGENT PERCEPTION ---
Current Position: [3, 0]
Perceiving: Safe (Nothing detected)
Possible SAFE Move Locations: Up (2, 0), Right (3, 1)
------------------------

Controls: W (Up), S (Down), A (Left), D (Right), G (Grab), F (Shoot), E (Exit)
Action: w

CURRENT GRID
_ _ _ _
_ _ _ _
A _ _ _
_ _ _ _
A = Agent

--- AGENT PERCEPTION ---
Current Position: [2, 0]
Perceiving: Breeze
Possible SAFE Move Locations: Down (3, 0), Right (2, 1)
------------------------

Controls: W (Up), S (Down), A (Left), D (Right), G (Grab), F (Shoot), E (Exit)
Action: d

CURRENT GRID
_ _ _ _
_ _ _ _
_ A _ _
_ _ _ _
A = Agent

--- AGENT PERCEPTION ---
Current Position: [2, 1]
Perceiving: Safe (Nothing detected)
Possible SAFE Move Locations: Up (1, 1), Down (3, 1), Left (2, 0), Right (2, 2)
------------------------

Controls: W (Up), S (Down), A (Left), D (Right), G (Grab), F (Shoot), E (Exit)
Action: d

CURRENT GRID
_ _ _ _
_ _ _ _
_ _ A _
_ _ _ _
A = Agent

--- AGENT PERCEPTION ---
Current Position: [2, 2]
Perceiving: Safe (Nothing detected)
Possible SAFE Move Locations: Up (1, 2), Down (3, 2), Left (2, 1), Right (2, 3)
------------------------

Controls: W (Up), S (Down), A (Left), D (Right), G (Grab), F (Shoot), E (Exit)
Action: w

CURRENT GRID
_ _ _ _
_ _ A _
_ _ _ _
_ _ _ _
A = Agent

--- AGENT PERCEPTION ---
Current Position: [1, 2]
Perceiving: Smell
Possible SAFE Move Locations: Up (0, 2), Down (2, 2), Left (1, 1)
------------------------

Controls: W (Up), S (Down), A (Left), D (Right), G (Grab), F (Shoot), E (Exit)
Action: w
GOLD FOUND

CURRENT GRID
_ _ A _
_ _ _ _
_ _ _ _
_ _ _ _
A = Agent

--- AGENT PERCEPTION ---
Current Position: [0, 2]
Perceiving: Glitter
Possible SAFE Move Locations: Down (1, 2), Left (0, 1), Right (0, 3)
------------------------

Controls: W (Up), S (Down), A (Left), D (Right), G (Grab), F (Shoot), E (Exit)
Action: g
GOLD GRABBED. Game Cleared
[23bcs123@mepcolinux ex5]$exit

Script done on Tue Mar 17 10:23:35 2026