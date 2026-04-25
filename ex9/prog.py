Script started on Sat Apr 25 16:14:24 2026
from itertools import product

def normalize_distribution(dist):
    total = sum(dist.values())
    if total == 0:
        return dist
    return {k: v / total for k, v in dist.items()}


def print_distribution(dist, variables):
    print("\nFull Joint Probability Table:")
    print("-" * 60)
    print(" | ".join(variables) + " | Probability")
    print("-" * 60)
    for assignment, prob in dist.items():
        print(" | ".join(assignment) + f" | {prob:.6f}")
    print("-" * 60)


def matches(assignment, variables, conditions):
    for var, val in conditions.items():
        idx = variables.index(var)
        if assignment[idx] != val:
            return False
    return True


def marginal_probability(dist, variables, query_conditions):
    total = 0.0
    for assignment, prob in dist.items():
        if matches(assignment, variables, query_conditions):
            total += prob
    return total


def conditional_probability(dist, variables, query_conditions, given_conditions):
    combined = given_conditions.copy()
    combined.update(query_conditions)

    numerator = marginal_probability(dist, variables, combined)
    denominator = marginal_probability(dist, variables, given_conditions)

    if denominator == 0:
        return None
    return numerator / denominator


def bayes_rule(dist, variables, A, B):
    # P(A|B) = P(B|A) * P(A) / P(B)
    p_b_given_a = conditional_probability(dist, variables, B, A)
    p_a = marginal_probability(dist, variables, A)
    p_b = marginal_probability(dist, variables, B)

    if p_b == 0:
        return None

    return (p_b_given_a * p_a) / p_b


def parse_conditions(input_str):
    conditions = {}
    input_str = input_str.strip()

    if input_str == "":
        return conditions

    parts = input_str.split(",")
    for part in parts:
        var, val = part.split("=")
        conditions[var.strip()] = val.strip()
    return conditions

def simple_probability():
    print("\n==============================")
    print("1) SIMPLE PROBABILITY")
    print("==============================")
    print("Choose problem type:")
    print("1. Two Coins")
    print("2. Two Dice")

    choice = input("Enter choice (1/2): ").strip()

    if choice == '1':
        # Two Coins
        outcomes = ['HH', 'HT', 'TH', 'TT']
        total = len(outcomes)

        print("\nAvailable events for Two Coins:")
        print("1. At least one Head")
        print("2. Exactly one Head")
        print("3. Both Heads")
        print("4. At least one Tail")
        print("5. Both Tails")

        event_choice = input("Enter event choice (1-5): ").strip()

        if event_choice == '1':
            favorable = [o for o in outcomes if 'H' in o]
            event_name = "At least one Head"
        elif event_choice == '2':
            favorable = [o for o in outcomes if o.count('H') == 1]
            event_name = "Exactly one Head"
        elif event_choice == '3':
            favorable = [o for o in outcomes if o == 'HH']
            event_name = "Both Heads"
        elif event_choice == '4':
            favorable = [o for o in outcomes if 'T' in o]
            event_name = "At least one Tail"
        elif event_choice == '5':
            favorable = [o for o in outcomes if o == 'TT']
            event_name = "Both Tails"
        else:
            print("Invalid choice.")
            return

        probability = len(favorable) / total

        print("\nSample Space =", outcomes)
        print("Favorable Outcomes =", favorable)
        print(f"P({event_name}) = {len(favorable)}/{total} = {probability:.6f}")

    elif choice == '2':
        # Two Dice
        outcomes = list(product(range(1, 7), repeat=2))
        total = len(outcomes)

        print("\nAvailable events for Two Dice:")
        print("1. Sum = k")
        print("2. Doubles")
        print("3. At least one 6")
        print("4. Sum >= k")
        print("5. Sum <= k")

        event_choice = input("Enter event choice (1-5): ").strip()

        if event_choice == '1':
            k = int(input("Enter value of k: "))
            favorable = [o for o in outcomes if o[0] + o[1] == k]
            event_name = f"Sum = {k}"

        elif event_choice == '2':
            favorable = [o for o in outcomes if o[0] == o[1]]
            event_name = "Doubles"

        elif event_choice == '3':
            favorable = [o for o in outcomes if o[0] == 6 or o[1] == 6]
            event_name = "At least one 6"

        elif event_choice == '4':
            k = int(input("Enter value of k: "))
            favorable = [o for o in outcomes if o[0] + o[1] >= k]
            event_name = f"Sum >= {k}"

        elif event_choice == '5':
            k = int(input("Enter value of k: "))
            favorable = [o for o in outcomes if o[0] + o[1] <= k]
            event_name = f"Sum <= {k}"

        else:
            print("Invalid choice.")
            return

        probability = len(favorable) / total

        print("\nTotal Outcomes = 36")
        print("Favorable Outcomes =", favorable)
        print(f"P({event_name}) = {len(favorable)}/{total} = {probability:.6f}")

    else:
        print("Invalid choice.")

def read_joint_distribution():
    print("\n==============================")
    print("2) FULL JOINT DISTRIBUTION")
    print("==============================")

    n = int(input("Enter number of variables (max 3): "))
    if n < 1 or n > 3:
        print("Only 1 to 3 variables allowed.")
        return None, None

    variables = []
    value_domains = []

    for i in range(n):
        var = input(f"Enter variable {i+1} name: ").strip()
        values = input(f"Enter possible values for {var} separated by space (e.g. T F): ").split()
        variables.append(var)
        value_domains.append(values)

    all_assignments = list(product(*value_domains))
    dist = {}

    print("\nEnter probability for each assignment:")
    for assignment in all_assignments:
        label = ", ".join([f"{variables[i]}={assignment[i]}" for i in range(n)])
        p = float(input(f"P({label}) = "))
        dist[assignment] = p

    total_prob = sum(dist.values())
    print(f"\nTotal probability entered = {total_prob:.6f}")

    if abs(total_prob - 1.0) > 1e-6:
        print("Probabilities do not sum to 1. Normalizing automatically...")
        dist = normalize_distribution(dist)

    print_distribution(dist, variables)
    return dist, variables

def knowledge_base_queries(dist, variables):
    print("\n==============================")
    print("3) KB QUERIES")
    print("==============================")
    print("\nQuery Types:")
    print("1. Marginal Probability   P(A)")
    print("2. Conditional Probability P(A|B)")
    print("3. Bayes Rule              P(A|B)")
    print("4. Exit")
    while True:
        choice = input("Enter choice (1/2/3/4): ").strip()

        if choice == '1':
            q = input("Enter event A (e.g. Rain=T or Rain=T,GrassWet=T): ")
            q_cond = parse_conditions(q)

            try:
                result = marginal_probability(dist, variables, q_cond)
                print(f"P({q}) = {result:.6f}")

            except:
                print("Invalid query.")

        elif choice == '2':
            q = input("Enter event A (e.g. GrassWet=T): ")
            g = input("Enter given event B (e.g. Rain=T): ")

            try:
                q_cond = parse_conditions(q)
                g_cond = parse_conditions(g)

                result = conditional_probability(dist, variables, q_cond, g_cond)

                if result is None:
                    print("Undefined (denominator is 0).")
                else:
                    print(f"P({q} | {g}) = {result:.6f}")

            except:
                print("Invalid query.")

        elif choice == '3':
            a = input("Enter event A (e.g. Rain=T): ")
            b = input("Enter event B (e.g. GrassWet=T): ")

            try:
                a_cond = parse_conditions(a)
                b_cond = parse_conditions(b)

                result = bayes_rule(dist, variables, a_cond, b_cond)

                if result is None:
                    print("Undefined (P(B)=0).")
                else:
                    print(f"P({a} | {b}) using Bayes Rule = {result:.6f}")
                query_count += 1
            except:
                print("Invalid query.")

        elif choice == '4':
            '''if query_count < 6:
                print("You must perform at least 6 queries before exiting.")
            else:'''
            print("Exiting KB query section.")
            break

        else:
            print("Invalid choice.")

def main():
    while True:
        print("\n============================================")
        print("JOINT PROBABILITY / SIMPLE PROBABILITY / BAYES")
        print("==============================================")
        print("1. Simple Probability (User Input)")
        print("2. Full Joint Distribution + Bayes Rule")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            simple_probability()

        elif choice == '2':
            dist, variables = read_joint_distribution()
            if dist is not None:
                knowledge_base_queries(dist, variables)

        elif choice == '3':
            print("Program exited.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
[23bcs123@mepcolinux ex9]$python3 prog.py

============================================
JOINT PROBABILITY / SIMPLE PROBABILITY / BAYES
==============================================
1. Simple Probability (User Input)
2. Full Joint Distribution + Bayes Rule
3. Exit
Enter your choice: 2

==============================
2) FULL JOINT DISTRIBUTION
==============================
Enter number of variables (max 3): 3
Enter variable 1 name: Rain
Enter possible values for Rain separated by space (e.g. T F): T F
Enter variable 2 name: Sprinkler
Enter possible values for Sprinkler separated by space (e.g. T F): T F
Enter variable 3 name: Grasswet
Enter possible values for Grasswet separated by space (e.g. T F): T F

Enter probability for each assignment:
P(Rain=T, Sprinkler=T, Grasswet=T) = 0.2
P(Rain=T, Sprinkler=T, Grasswet=F) = 0.05
P(Rain=T, Sprinkler=F, Grasswet=T) = 0.25
P(Rain=T, Sprinkler=F, Grasswet=F) = 0.10
P(Rain=F, Sprinkler=T, Grasswet=T) = 0.15
P(Rain=F, Sprinkler=T, Grasswet=F) = 0.05
P(Rain=F, Sprinkler=F, Grasswet=T) = 0.10
P(Rain=F, Sprinkler=F, Grasswet=F) = 0.10

Total probability entered = 1.000000

Full Joint Probability Table:
------------------------------------------------------------
Rain | Sprinkler | Grasswet | Probability
------------------------------------------------------------
T | T | T | 0.200000
T | T | F | 0.050000
T | F | T | 0.250000
T | F | F | 0.100000
F | T | T | 0.150000
F | T | F | 0.050000
F | F | T | 0.100000
F | F | F | 0.100000
------------------------------------------------------------

==============================
3) KB QUERIES
==============================

Query Types:
1. Marginal Probability   P(A)
2. Conditional Probability P(A|B)
3. Bayes Rule              P(A|B)
4. Exit
Enter choice (1/2/3/4): 1
Enter event A (e.g. Rain=T or Rain=T,GrassWet=T): Rain=T
P(Rain=T) = 0.600000
Enter choice (1/2/3/4): 2
Enter event A (e.g. GrassWet=T): GrassWet=F
Enter given event B (e.g. Rain=T): Rain=T
Invalid query.
Enter choice (1/2/3/4):    2
Enter event A (e.g. GrassWet=T): Grasswet=T
Enter given event B (e.g. Rain=T): Rain=T
P(Grasswet=T | Rain=T) = 0.750000
Enter choice (1/2/3/4): 3
Enter event A (e.g. Rain=T): Rain=T
Enter event B (e.g. GrassWet=T): Grasswet=T
P(Rain=T | Grasswet=T) using Bayes Rule = 0.642857
Invalid query.
Enter choice (1/2/3/4): 1
Enter event A (e.g. Rain=T or Rain=T,GrassWet=T): Grasswet=T
P(Grasswet=T) = 0.700000
Enter choice (1/2/3/4): 4
Exiting KB query section.

============================================
JOINT PROBABILITY / SIMPLE PROBABILITY / BAYES
==============================================
1. Simple Probability (User Input)
2. Full Joint Distribution + Bayes Rule
3. Exit
Enter your choice: 1

==============================
1) SIMPLE PROBABILITY
==============================
Choose problem type:
1. Two Coins
2. Two Dice
Enter choice (1/2): 1

Available events for Two Coins:
1. At least one Head
2. Exactly one Head
3. Both Heads
4. At least one Tail
5. Both Tails
Enter event choice (1-5): 1

Sample Space = ['HH', 'HT', 'TH', 'TT']
Favorable Outcomes = ['HH', 'HT', 'TH']
P(At least one Head) = 3/4 = 0.750000

============================================
JOINT PROBABILITY / SIMPLE PROBABILITY / BAYES
==============================================
1. Simple Probability (User Input)
2. Full Joint Distribution + Bayes Rule
3. Exit
Enter your choice: 3
Program exited.
[23bcs123@mepcolinux ex9]$exit

Script done on Sat Apr 25 16:14:26 2026