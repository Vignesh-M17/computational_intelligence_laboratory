import csv
import math
import random
from collections import Counter

def euclidean(p1, p2):
    return math.sqrt(sum((p1[i] - p2[i])**2 for i in range(len(p1))))

def manhattan(p1, p2):
    return sum(abs(p1[i] - p2[i]) for i in range(len(p1)))

def get_min_max(data, n):
    mins = [min(row[i] for row in data) for i in range(n)]
    maxs = [max(row[i] for row in data) for i in range(n)]
    return mins, maxs

def get_zscore_params(data, n):
    means = [sum(row[i] for row in data)/len(data) for i in range(n)]
    stds = [math.sqrt(sum((row[i]-means[i])**2 for row in data)/len(data)) for i in range(n)]
    return means, stds

def read_csv(file):
    data = []
    try:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for r in reader:
                if not r: continue
                # Features to float, last column as class string
                row = [float(x) for x in r[:-1]] + [str(r[-1]).strip()]
                data.append(row)
        return data, len(header)-1
    except FileNotFoundError:
        print("File not found."); exit()

def main():
    file = input("Enter CSV file name: ")
    full_dataset, total_features = read_csv(file)
    n = int(input(f"Enter number of features to use (Total {total_features}): "))

    # --- 1. BALANCED SAMPLING (50/50 SPLIT) ---
    class_0 = [row for row in full_dataset if row[-1] == '0']
    class_1 = [row for row in full_dataset if row[-1] == '1']

    print(f"\n[INFO] Original File Stats -> Class '0': {len(class_0)}, Class '1': {len(class_1)}")

    if len(class_0) >= 75 and len(class_1) >= 75:
        sampled_0 = random.sample(class_0, 75)
        sampled_1 = random.sample(class_1, 75)
        raw_data = sampled_0 + sampled_1
        random.shuffle(raw_data)

        # Identify remaining data (Test Data)
        used_ids = {id(r) for r in raw_data}
        test_data = [r for r in full_dataset if id(r) not in used_ids]

        print(f"[SUCCESS] Training Data balanced: 75 of Class 0 & 75 of Class 1 (Total 150)")
    else:
        raw_data = full_dataset
        test_data = []
        print("[WARNING] Dataset too small or imbalanced to create 75/75 split. Using all data.")

    # --- 2. DISPLAY REMAINING DATA ---
    if test_data:
        print(f"\n--- REMAINING DATASET (NOT SELECTED FOR TRAINING: {len(test_data)} records) ---")
        print(f"{'Features':<35} | {'Actual Class'}")
        print("-" * 50)
        for row in test_data[:15]: # Displaying first 15 for brevity
            print(f"{str(row[:n]):<35} | {row[-1]}")
        if len(test_data) > 15:
            print(f"... and {len(test_data)-15} more records.")

    # Calculate normalization parameters from training set
    mins, maxs = get_min_max(raw_data, n)
    means, stds = get_zscore_params(raw_data, n)

    while True:
        print("\n" + "="*110)
        try:
            line = input(f"Enter unknown point ({n} values separated by space): ")
            unknown_raw = list(map(float, line.split()))
            if len(unknown_raw) != n: raise ValueError
        except ValueError:
            print(f"Error: Enter exactly {n} values."); continue

        dist_choice = input("Select Distance Metric (1: Euclidean, 2: Manhattan): ")
        dist_func = euclidean if dist_choice == '1' else manhattan
        norm_type = input("Select Normalization (1: Min-Max, 2: Z-Score, 3: None): ")

        # Normalize the unknown point
        if norm_type == '1':
            norm_unknown = [round((unknown_raw[i] - mins[i]) / (maxs[i] - mins[i] + 1e-9), 4) for i in range(n)]
        elif norm_type == '2':
            norm_unknown = [round((unknown_raw[i] - means[i]) / (stds[i] + 1e-9), 4) for i in range(n)]
        else:
            norm_unknown = unknown_raw

        # Prepare distances from training data
        processed_table = []
        for row in raw_data:
            orig_feat = row[:n]
            if norm_type == '1':
                norm_feat = [round((row[i] - mins[i]) / (maxs[i] - mins[i] + 1e-9), 4) for i in range(n)]
            elif norm_type == '2':
                norm_feat = [round((row[i] - means[i]) / (stds[i] + 1e-9), 4) for i in range(n)]
            else:
                norm_feat = orig_feat

            dist = dist_func(norm_feat, norm_unknown)
            processed_table.append({'orig': orig_feat, 'norm': norm_feat, 'dist': dist, 'class': row[-1]})

        k = int(input("\nEnter value of k: "))
        processed_table.sort(key=lambda x: x['dist'])
        neighbors = processed_table[:k]

        # --- 3. DISPLAY SELECTED NEIGHBOR DATA ---
        print(f"\n--- {k} NEAREST NEIGHBORS SELECTED ---")
        print(f"{'Rank':<5} | {'Original Value':<25} | {'Normalized Value':<25} | {'Distance':<10} | {'Class'}")
        print("-" * 110)
        for i, nbr in enumerate(neighbors, 1):
            orig_str = str([round(x, 2) for x in nbr['orig']])
            norm_str = str(nbr['norm'])
            print(f"{i:<5} | {orig_str:<25} | {norm_str:<25} | {nbr['dist']:.4f}     | {nbr['class']}")

        # Voting
        mode = input("\nWeighted or Unweighted (W/U): ").upper()
        if mode == 'U':
            votes = Counter([nbr['class'] for nbr in neighbors])
            prediction = votes.most_common(1)[0][0]
            print(f"Votes Count: {dict(votes)}")
        else:
            weights = {}
            for nbr in neighbors:
                w = 1 / (nbr['dist'] + 1e-9)
                weights[nbr['class']] = weights.get(nbr['class'], 0) + w
            prediction = max(weights, key=weights.get)
            formatted_weights = {k: round(v, 4) for k, v in weights.items()}
            print(f"Weighted Scores: {formatted_weights}")

        print(f"\nRESULT: Predicted Class for {unknown_raw} is -> {prediction}")

        if input("\nProcess another point? (Y/N): ").upper() != 'Y': break

if __name__ == "__main__":
    main()

[23bcs123@mepcolinux ex3]$python3 prog.py
Enter CSV file name: transfusion.data.csv
Enter number of features to use (Total 4): 4

[INFO] Original File Stats -> Class '0': 570, Class '1': 178
[SUCCESS] Training Data balanced: 75 of Class 0 & 75 of Class 1 (Total 150)

--- REMAINING DATASET (NOT SELECTED FOR TRAINING: 598 records) ---
Features                            | Actual Class
--------------------------------------------------
[2.0, 50.0, 12500.0, 98.0]          | 1
[0.0, 13.0, 3250.0, 28.0]           | 1
[1.0, 24.0, 6000.0, 77.0]           | 0
[4.0, 4.0, 1000.0, 4.0]             | 0
[2.0, 7.0, 1750.0, 14.0]            | 1
[1.0, 12.0, 3000.0, 35.0]           | 0
[5.0, 46.0, 11500.0, 98.0]          | 1
[4.0, 23.0, 5750.0, 58.0]           | 0
[2.0, 10.0, 2500.0, 28.0]           | 1
[1.0, 13.0, 3250.0, 47.0]           | 0
[2.0, 6.0, 1500.0, 15.0]            | 1
[2.0, 5.0, 1250.0, 11.0]            | 1
[2.0, 14.0, 3500.0, 48.0]           | 1
[2.0, 6.0, 1500.0, 15.0]            | 1
[2.0, 3.0, 750.0, 4.0]              | 1
... and 583 more records.

==============================================================================================================
Enter unknown point (4 values separated by space): 2 50 12500 98
Select Distance Metric (1: Euclidean, 2: Manhattan): 1
Select Normalization (1: Min-Max, 2: Z-Score, 3: None): 1

Enter value of k: 3

--- 3 NEAREST NEIGHBORS SELECTED ---
Rank  | Original Value            | Normalized Value          | Distance   | Class
--------------------------------------------------------------------------------------------------------------
1     | [2.0, 43.0, 10750.0, 86.0] | [0.0769, 1.0, 1.0, 0.875] | 0.2668     | 1
2     | [0.0, 26.0, 6500.0, 76.0] | [0.0, 0.5952, 0.5952, 0.7708] | 0.8436     | 1
3     | [11.0, 24.0, 6000.0, 64.0] | [0.4231, 0.5476, 0.5476, 0.6458] | 1.0059     | 0

Weighted or Unweighted (W/U): W
Weighted Scores: {'1': 4.933, '0': 0.9941}

RESULT: Predicted Class for [2.0, 50.0, 12500.0, 98.0] is -> 1

Process another point? (Y/N): Y

==============================================================================================================
Enter unknown point (4 values separated by space): 2 50 12500 98
Select Distance Metric (1: Euclidean, 2: Manhattan): 1
Select Normalization (1: Min-Max, 2: Z-Score, 3: None): 1

Enter value of k: 3

--- 3 NEAREST NEIGHBORS SELECTED ---
Rank  | Original Value            | Normalized Value          | Distance   | Class
--------------------------------------------------------------------------------------------------------------
1     | [2.0, 43.0, 10750.0, 86.0] | [0.0769, 1.0, 1.0, 0.875] | 0.2668     | 1
2     | [0.0, 26.0, 6500.0, 76.0] | [0.0, 0.5952, 0.5952, 0.7708] | 0.8436     | 1
3     | [11.0, 24.0, 6000.0, 64.0] | [0.4231, 0.5476, 0.5476, 0.6458] | 1.0059     | 0

Weighted or Unweighted (W/U): U
Votes Count: {'1': 2, '0': 1}

RESULT: Predicted Class for [2.0, 50.0, 12500.0, 98.0] is -> 1

Process another point? (Y/N): N
[23bcs123@mepcolinux ex3]$exit

Script done on Tue Feb 17 12:08:25 2026