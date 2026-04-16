import csv
from collections import Counter
import math
import random

def read_data(filename, sample_size=None):
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)
        if sample_size and len(data) > sample_size:
            print(f"\nTotal rows in file: {len(data)}")
            data = random.sample(data, sample_size)
            print(f"Randomly selected {sample_size} rows for analysis")
        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def print_sampled_data(data):
    if not data: return
    columns = list(data[0].keys())
    col_widths = {col: max(len(col), max(len(str(row[col])) for row in data)) for col in columns}
    print("\n" + "="*100 + "\nRANDOMLY SELECTED DATA\n" + "="*100)
    header = " | ".join(col.ljust(col_widths[col]) for col in columns)
    print(header + "\n" + "-" * len(header))
    for row in data:
        print(" | ".join(str(row[col]).ljust(col_widths[col]) for col in columns))
    print("="*100 + f"\nTotal rows displayed: {len(data)}\n")

def get_column_values(data, column):
    return [row[column] for row in data]

def get_unique_values(data, column):
    return list(set(get_column_values(data, column)))

def filter_data(data, column, value):
    return [row for row in data if row[column] == value]

def entropy_before_split(data, target_column):
    target_values = get_column_values(data, target_column)
    total_count = len(target_values)
    value_counts = Counter(target_values)
    entropy = 0.0
    calculation_steps = []

    print(f"\nEntropy Before Split (for {target_column}):")
    print(f"Total samples: {total_count}")

    for value, count in value_counts.items():
        prob = count / total_count
        log_val = math.log2(prob) if prob > 0 else 0
        entropy -= prob * log_val
        calculation_steps.append(f"({count}/{total_count} * {log_val:.4f})")
        # Change 2: Display calculation for probability and log2
        print(f"  Class '{value}': {count} samples, probability = {count}/{total_count} ({prob:.4f}), log2({prob:.4f}) = {log_val:.4f}")

    # Change 1: Display how total entropy value comes
    calc_str = " + ".join(calculation_steps)
    print(f"Total Entropy Calculation: -[{calc_str}]")
    print(f"Total Entropy = {entropy:.4f}")
    return entropy

def entropy_after_split(data, attribute, target_column):
    total_count = len(data)
    attribute_values = get_unique_values(data, attribute)
    weighted_entropy = 0.0
    weighted_calc_steps = []

    print(f"\nEntropy After Split on '{attribute}':")
    for value in attribute_values:
        subset = filter_data(data, attribute, value)
        sub_count = len(subset)
        weight = sub_count / total_count

        print(f"\n  Value '{value}': {sub_count} samples (weight = {sub_count}/{total_count} = {weight:.4f})")
        sub_entropy = entropy_before_split(subset, target_column)
        weighted_entropy += weight * sub_entropy
        weighted_calc_steps.append(f"({sub_count}/{total_count} * {sub_entropy:.4f})")

    # Change 1: Display how weighted entropy value comes
    weighted_str = " + ".join(weighted_calc_steps)
    print(f"\nWeighted Entropy Calculation for '{attribute}': {weighted_str}")
    print(f"Weighted Entropy for '{attribute}' = {weighted_entropy:.4f}")
    return weighted_entropy

def information_gain(data, attribute, target_column):
    print(f"\n{'='*60}\nCalculating Information Gain for Attribute: '{attribute}'\n{'='*60}")
    ent_parent = entropy_before_split(data, target_column)
    ent_children = entropy_after_split(data, attribute, target_column)
    gain = ent_parent - ent_children
    print(f"\nInformation Gain for '{attribute}' = {ent_parent:.4f} - {ent_children:.4f} = {gain:.4f}")
    print(f"{'='*60}\n")
    return gain

def build_tree(data, target_column, attributes):
    target_values = get_column_values(data, target_column)
    if len(set(target_values)) == 1: return target_values[0]
    if not attributes: return Counter(target_values).most_common(1)[0][0]

    gains = {attr: information_gain(data, attr, target_column) for attr in attributes}
    best_attr = max(gains, key=gains.get)
    tree = {best_attr: {}}
    remaining = [a for a in attributes if a != best_attr]

    for val in get_unique_values(data, best_attr):
        subset = filter_data(data, best_attr, val)
        tree[best_attr][val] = build_tree(subset, target_column, remaining)
    return tree

def print_tree(tree, indent=""):
    if not isinstance(tree, dict):
        print(f" -> {tree}")
        return
    for attr, branches in tree.items():
        print(f"\n{indent}[{attr}]")
        for val, subtree in branches.items():
            print(f"{indent}  |-- {val}", end="")
            print_tree(subtree, indent + "  |   ")

def main():
    filename = input("Enter the input CSV filename: ").strip() or "data.csv"
    sample_input = input("Enter sample data size: ").strip()
    sample_size = int(sample_input) if sample_input.isdigit() else None

    data = read_data(filename, sample_size)
    if not data: return

    print_sampled_data(data)
    target_column = input("Enter target column name: ").strip()
    if target_column not in data[0]: return

    attributes = [col for col in data[0].keys() if col != target_column]

    print("\n" + "*"*70 + "\nGENERATING ENTIRE DECISION TREE STRUCTURE\n" + "*"*70)
    full_tree = build_tree(data, target_column, attributes)

    print("\n" + "="*70 + "\nFINAL DECISION TREE\n" + "="*70)
    print_tree(full_tree)
    print("\n" + "="*70)

if __name__ == "__main__":
    main()

[23bcs123@mepcolinux ex4]$python3 prog1.py
Enter the input CSV filename: ninp.csv
Enter sample data size: 10

====================================================================================================
RANDOMLY SELECTED DATA
====================================================================================================
Species | Green | Legs | Height | Smelly
----------------------------------------
Martins | No    | 3    | Small  | Yes
Martins | Yes   | 2    | Tall   | No
Martins | Yes   | 3    | Tall   | No
Martins | No    | 2    | Small  | Yes
Martins | Yes   | 3    | Tall   | No
Humans  | No    | 2    | Tall   | Yes
Humans  | No    | 2    | Small  | No
Humans  | No    | 2    | Tall   | No
Humans  | Yes   | 2    | Small  | No
Humans  | No    | 2    | Tall   | Yes
====================================================================================================
Total rows displayed: 10

Enter target column name: Species

**********************************************************************
GENERATING ENTIRE DECISION TREE STRUCTURE
**********************************************************************

============================================================
Calculating Information Gain for Attribute: 'Green'
============================================================

Entropy Before Split (for Species):
Total samples: 10
  Class 'Martins': 5 samples, probability = 5/10 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 5 samples, probability = 5/10 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(5/10 * -1.0000) + (5/10 * -1.0000)]
Total Entropy = 1.0000

Entropy After Split on 'Green':

  Value 'No': 6 samples (weight = 6/10 = 0.6000)

Entropy Before Split (for Species):
Total samples: 6
  Class 'Martins': 2 samples, probability = 2/6 (0.3333), log2(0.3333) = -1.5850
  Class 'Humans': 4 samples, probability = 4/6 (0.6667), log2(0.6667) = -0.5850
Total Entropy Calculation: -[(2/6 * -1.5850) + (4/6 * -0.5850)]
Total Entropy = 0.9183

  Value 'Yes': 4 samples (weight = 4/10 = 0.4000)

Entropy Before Split (for Species):
Total samples: 4
  Class 'Martins': 3 samples, probability = 3/4 (0.7500), log2(0.7500) = -0.4150
  Class 'Humans': 1 samples, probability = 1/4 (0.2500), log2(0.2500) = -2.0000
Total Entropy Calculation: -[(3/4 * -0.4150) + (1/4 * -2.0000)]
Total Entropy = 0.8113

Weighted Entropy Calculation for 'Green': (6/10 * 0.9183) + (4/10 * 0.8113)
Weighted Entropy for 'Green' = 0.8755

Information Gain for 'Green' = 1.0000 - 0.8755 = 0.1245
============================================================


============================================================
Calculating Information Gain for Attribute: 'Legs'
============================================================

Entropy Before Split (for Species):
Total samples: 10
  Class 'Martins': 5 samples, probability = 5/10 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 5 samples, probability = 5/10 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(5/10 * -1.0000) + (5/10 * -1.0000)]
Total Entropy = 1.0000

Entropy After Split on 'Legs':

  Value '2': 7 samples (weight = 7/10 = 0.7000)

Entropy Before Split (for Species):
Total samples: 7
  Class 'Martins': 2 samples, probability = 2/7 (0.2857), log2(0.2857) = -1.8074
  Class 'Humans': 5 samples, probability = 5/7 (0.7143), log2(0.7143) = -0.4854
Total Entropy Calculation: -[(2/7 * -1.8074) + (5/7 * -0.4854)]
Total Entropy = 0.8631

  Value '3': 3 samples (weight = 3/10 = 0.3000)

Entropy Before Split (for Species):
Total samples: 3
  Class 'Martins': 3 samples, probability = 3/3 (1.0000), log2(1.0000) = 0.0000
Total Entropy Calculation: -[(3/3 * 0.0000)]
Total Entropy = 0.0000

Weighted Entropy Calculation for 'Legs': (7/10 * 0.8631) + (3/10 * 0.0000)
Weighted Entropy for 'Legs' = 0.6042

Information Gain for 'Legs' = 1.0000 - 0.6042 = 0.3958
============================================================


============================================================
Calculating Information Gain for Attribute: 'Height'
============================================================

Entropy Before Split (for Species):
Total samples: 10
  Class 'Martins': 5 samples, probability = 5/10 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 5 samples, probability = 5/10 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(5/10 * -1.0000) + (5/10 * -1.0000)]
Total Entropy = 1.0000

Entropy After Split on 'Height':

  Value 'Small': 4 samples (weight = 4/10 = 0.4000)

Entropy Before Split (for Species):
Total samples: 4
  Class 'Martins': 2 samples, probability = 2/4 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 2 samples, probability = 2/4 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(2/4 * -1.0000) + (2/4 * -1.0000)]
Total Entropy = 1.0000

  Value 'Tall': 6 samples (weight = 6/10 = 0.6000)

Entropy Before Split (for Species):
Total samples: 6
  Class 'Martins': 3 samples, probability = 3/6 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 3 samples, probability = 3/6 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(3/6 * -1.0000) + (3/6 * -1.0000)]
Total Entropy = 1.0000

Weighted Entropy Calculation for 'Height': (4/10 * 1.0000) + (6/10 * 1.0000)
Weighted Entropy for 'Height' = 1.0000

Information Gain for 'Height' = 1.0000 - 1.0000 = 0.0000
============================================================


============================================================
Calculating Information Gain for Attribute: 'Smelly'
============================================================

Entropy Before Split (for Species):
Total samples: 10
  Class 'Martins': 5 samples, probability = 5/10 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 5 samples, probability = 5/10 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(5/10 * -1.0000) + (5/10 * -1.0000)]
Total Entropy = 1.0000

Entropy After Split on 'Smelly':

  Value 'No': 6 samples (weight = 6/10 = 0.6000)

Entropy Before Split (for Species):
Total samples: 6
  Class 'Martins': 3 samples, probability = 3/6 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 3 samples, probability = 3/6 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(3/6 * -1.0000) + (3/6 * -1.0000)]
Total Entropy = 1.0000

  Value 'Yes': 4 samples (weight = 4/10 = 0.4000)

Entropy Before Split (for Species):
Total samples: 4
  Class 'Martins': 2 samples, probability = 2/4 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 2 samples, probability = 2/4 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(2/4 * -1.0000) + (2/4 * -1.0000)]
Total Entropy = 1.0000

Weighted Entropy Calculation for 'Smelly': (6/10 * 1.0000) + (4/10 * 1.0000)
Weighted Entropy for 'Smelly' = 1.0000

Information Gain for 'Smelly' = 1.0000 - 1.0000 = 0.0000
============================================================


============================================================
Calculating Information Gain for Attribute: 'Green'
============================================================

Entropy Before Split (for Species):
Total samples: 7
  Class 'Martins': 2 samples, probability = 2/7 (0.2857), log2(0.2857) = -1.8074
  Class 'Humans': 5 samples, probability = 5/7 (0.7143), log2(0.7143) = -0.4854
Total Entropy Calculation: -[(2/7 * -1.8074) + (5/7 * -0.4854)]
Total Entropy = 0.8631

Entropy After Split on 'Green':

  Value 'No': 5 samples (weight = 5/7 = 0.7143)

Entropy Before Split (for Species):
Total samples: 5
  Class 'Martins': 1 samples, probability = 1/5 (0.2000), log2(0.2000) = -2.3219
  Class 'Humans': 4 samples, probability = 4/5 (0.8000), log2(0.8000) = -0.3219
Total Entropy Calculation: -[(1/5 * -2.3219) + (4/5 * -0.3219)]
Total Entropy = 0.7219

  Value 'Yes': 2 samples (weight = 2/7 = 0.2857)

Entropy Before Split (for Species):
Total samples: 2
  Class 'Martins': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(1/2 * -1.0000) + (1/2 * -1.0000)]
Total Entropy = 1.0000

Weighted Entropy Calculation for 'Green': (5/7 * 0.7219) + (2/7 * 1.0000)
Weighted Entropy for 'Green' = 0.8014

Information Gain for 'Green' = 0.8631 - 0.8014 = 0.0617
============================================================


============================================================
Calculating Information Gain for Attribute: 'Height'
============================================================

Entropy Before Split (for Species):
Total samples: 7
  Class 'Martins': 2 samples, probability = 2/7 (0.2857), log2(0.2857) = -1.8074
  Class 'Humans': 5 samples, probability = 5/7 (0.7143), log2(0.7143) = -0.4854
Total Entropy Calculation: -[(2/7 * -1.8074) + (5/7 * -0.4854)]
Total Entropy = 0.8631

Entropy After Split on 'Height':

  Value 'Small': 3 samples (weight = 3/7 = 0.4286)

Entropy Before Split (for Species):
Total samples: 3
  Class 'Martins': 1 samples, probability = 1/3 (0.3333), log2(0.3333) = -1.5850
  Class 'Humans': 2 samples, probability = 2/3 (0.6667), log2(0.6667) = -0.5850
Total Entropy Calculation: -[(1/3 * -1.5850) + (2/3 * -0.5850)]
Total Entropy = 0.9183

  Value 'Tall': 4 samples (weight = 4/7 = 0.5714)

Entropy Before Split (for Species):
Total samples: 4
  Class 'Martins': 1 samples, probability = 1/4 (0.2500), log2(0.2500) = -2.0000
  Class 'Humans': 3 samples, probability = 3/4 (0.7500), log2(0.7500) = -0.4150
Total Entropy Calculation: -[(1/4 * -2.0000) + (3/4 * -0.4150)]
Total Entropy = 0.8113

Weighted Entropy Calculation for 'Height': (3/7 * 0.9183) + (4/7 * 0.8113)
Weighted Entropy for 'Height' = 0.8571

Information Gain for 'Height' = 0.8631 - 0.8571 = 0.0060
============================================================


============================================================
Calculating Information Gain for Attribute: 'Smelly'
============================================================

Entropy Before Split (for Species):
Total samples: 7
  Class 'Martins': 2 samples, probability = 2/7 (0.2857), log2(0.2857) = -1.8074
  Class 'Humans': 5 samples, probability = 5/7 (0.7143), log2(0.7143) = -0.4854
Total Entropy Calculation: -[(2/7 * -1.8074) + (5/7 * -0.4854)]
Total Entropy = 0.8631

Entropy After Split on 'Smelly':

  Value 'No': 4 samples (weight = 4/7 = 0.5714)

Entropy Before Split (for Species):
Total samples: 4
  Class 'Martins': 1 samples, probability = 1/4 (0.2500), log2(0.2500) = -2.0000
  Class 'Humans': 3 samples, probability = 3/4 (0.7500), log2(0.7500) = -0.4150
Total Entropy Calculation: -[(1/4 * -2.0000) + (3/4 * -0.4150)]
Total Entropy = 0.8113

  Value 'Yes': 3 samples (weight = 3/7 = 0.4286)

Entropy Before Split (for Species):
Total samples: 3
  Class 'Martins': 1 samples, probability = 1/3 (0.3333), log2(0.3333) = -1.5850
  Class 'Humans': 2 samples, probability = 2/3 (0.6667), log2(0.6667) = -0.5850
Total Entropy Calculation: -[(1/3 * -1.5850) + (2/3 * -0.5850)]
Total Entropy = 0.9183

Weighted Entropy Calculation for 'Smelly': (4/7 * 0.8113) + (3/7 * 0.9183)
Weighted Entropy for 'Smelly' = 0.8571

Information Gain for 'Smelly' = 0.8631 - 0.8571 = 0.0060
============================================================


============================================================
Calculating Information Gain for Attribute: 'Height'
============================================================

Entropy Before Split (for Species):
Total samples: 5
  Class 'Martins': 1 samples, probability = 1/5 (0.2000), log2(0.2000) = -2.3219
  Class 'Humans': 4 samples, probability = 4/5 (0.8000), log2(0.8000) = -0.3219
Total Entropy Calculation: -[(1/5 * -2.3219) + (4/5 * -0.3219)]
Total Entropy = 0.7219

Entropy After Split on 'Height':

  Value 'Small': 2 samples (weight = 2/5 = 0.4000)

Entropy Before Split (for Species):
Total samples: 2
  Class 'Martins': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(1/2 * -1.0000) + (1/2 * -1.0000)]
Total Entropy = 1.0000

  Value 'Tall': 3 samples (weight = 3/5 = 0.6000)

Entropy Before Split (for Species):
Total samples: 3
  Class 'Humans': 3 samples, probability = 3/3 (1.0000), log2(1.0000) = 0.0000
Total Entropy Calculation: -[(3/3 * 0.0000)]
Total Entropy = 0.0000

Weighted Entropy Calculation for 'Height': (2/5 * 1.0000) + (3/5 * 0.0000)
Weighted Entropy for 'Height' = 0.4000

Information Gain for 'Height' = 0.7219 - 0.4000 = 0.3219
============================================================


============================================================
Calculating Information Gain for Attribute: 'Smelly'
============================================================

Entropy Before Split (for Species):
Total samples: 5
  Class 'Martins': 1 samples, probability = 1/5 (0.2000), log2(0.2000) = -2.3219
  Class 'Humans': 4 samples, probability = 4/5 (0.8000), log2(0.8000) = -0.3219
Total Entropy Calculation: -[(1/5 * -2.3219) + (4/5 * -0.3219)]
Total Entropy = 0.7219

Entropy After Split on 'Smelly':

  Value 'No': 2 samples (weight = 2/5 = 0.4000)

Entropy Before Split (for Species):
Total samples: 2
  Class 'Humans': 2 samples, probability = 2/2 (1.0000), log2(1.0000) = 0.0000
Total Entropy Calculation: -[(2/2 * 0.0000)]
Total Entropy = 0.0000

  Value 'Yes': 3 samples (weight = 3/5 = 0.6000)

Entropy Before Split (for Species):
Total samples: 3
  Class 'Martins': 1 samples, probability = 1/3 (0.3333), log2(0.3333) = -1.5850
  Class 'Humans': 2 samples, probability = 2/3 (0.6667), log2(0.6667) = -0.5850
Total Entropy Calculation: -[(1/3 * -1.5850) + (2/3 * -0.5850)]
Total Entropy = 0.9183

Weighted Entropy Calculation for 'Smelly': (2/5 * 0.0000) + (3/5 * 0.9183)
Weighted Entropy for 'Smelly' = 0.5510

Information Gain for 'Smelly' = 0.7219 - 0.5510 = 0.1710
============================================================


============================================================
Calculating Information Gain for Attribute: 'Smelly'
============================================================

Entropy Before Split (for Species):
Total samples: 2
  Class 'Martins': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(1/2 * -1.0000) + (1/2 * -1.0000)]
Total Entropy = 1.0000

Entropy After Split on 'Smelly':

  Value 'No': 1 samples (weight = 1/2 = 0.5000)

Entropy Before Split (for Species):
Total samples: 1
  Class 'Humans': 1 samples, probability = 1/1 (1.0000), log2(1.0000) = 0.0000
Total Entropy Calculation: -[(1/1 * 0.0000)]
Total Entropy = 0.0000

  Value 'Yes': 1 samples (weight = 1/2 = 0.5000)

Entropy Before Split (for Species):
Total samples: 1
  Class 'Martins': 1 samples, probability = 1/1 (1.0000), log2(1.0000) = 0.0000
Total Entropy Calculation: -[(1/1 * 0.0000)]
Total Entropy = 0.0000

Weighted Entropy Calculation for 'Smelly': (1/2 * 0.0000) + (1/2 * 0.0000)
Weighted Entropy for 'Smelly' = 0.0000

Information Gain for 'Smelly' = 1.0000 - 0.0000 = 1.0000
============================================================


============================================================
Calculating Information Gain for Attribute: 'Height'
============================================================

Entropy Before Split (for Species):
Total samples: 2
  Class 'Martins': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(1/2 * -1.0000) + (1/2 * -1.0000)]
Total Entropy = 1.0000

Entropy After Split on 'Height':

  Value 'Small': 1 samples (weight = 1/2 = 0.5000)

Entropy Before Split (for Species):
Total samples: 1
  Class 'Humans': 1 samples, probability = 1/1 (1.0000), log2(1.0000) = 0.0000
Total Entropy Calculation: -[(1/1 * 0.0000)]
Total Entropy = 0.0000

  Value 'Tall': 1 samples (weight = 1/2 = 0.5000)

Entropy Before Split (for Species):
Total samples: 1
  Class 'Martins': 1 samples, probability = 1/1 (1.0000), log2(1.0000) = 0.0000
Total Entropy Calculation: -[(1/1 * 0.0000)]
Total Entropy = 0.0000

Weighted Entropy Calculation for 'Height': (1/2 * 0.0000) + (1/2 * 0.0000)
Weighted Entropy for 'Height' = 0.0000

Information Gain for 'Height' = 1.0000 - 0.0000 = 1.0000
============================================================


============================================================
Calculating Information Gain for Attribute: 'Smelly'
============================================================

Entropy Before Split (for Species):
Total samples: 2
  Class 'Martins': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(1/2 * -1.0000) + (1/2 * -1.0000)]
Total Entropy = 1.0000

Entropy After Split on 'Smelly':

  Value 'No': 2 samples (weight = 2/2 = 1.0000)

Entropy Before Split (for Species):
Total samples: 2
  Class 'Martins': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
  Class 'Humans': 1 samples, probability = 1/2 (0.5000), log2(0.5000) = -1.0000
Total Entropy Calculation: -[(1/2 * -1.0000) + (1/2 * -1.0000)]
Total Entropy = 1.0000

Weighted Entropy Calculation for 'Smelly': (2/2 * 1.0000)
Weighted Entropy for 'Smelly' = 1.0000

Information Gain for 'Smelly' = 1.0000 - 1.0000 = 0.0000
============================================================


======================================================================
FINAL DECISION TREE
======================================================================

[Legs]
  |-- 2
  |   [Green]
  |     |-- No
  |     |   [Height]
  |     |     |-- Small
  |     |     |   [Smelly]
  |     |     |     |-- No -> Humans
  |     |     |     |-- Yes -> Martins
  |     |     |-- Tall -> Humans
  |     |-- Yes
  |     |   [Height]
  |     |     |-- Small -> Humans
  |     |     |-- Tall -> Martins
  |-- 3 -> Martins

======================================================================
[23bcs123@mepcolinux ex4]$exit

Script done on Tue Mar  3 11:14:48 2026