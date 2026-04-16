import csv

def activation_function(yin):
    # Bipolar Step function: 1 if yin > 0, else -1
    # (Note: Using round to prevent Python floating point precision errors like 0.000000001)
    return 1 if round(yin, 4) > 0 else -1

def main():
    # 1. Read and parse the CSV file
    try:
        with open('input.csv', 'r') as f:
            reader = csv.reader(f)
            lines = [row for row in reader if row] # Skip empty lines
    except FileNotFoundError:
        print("Error: 'input.csv' not found.")
        return

    # Parse initial parameters (Row 2, index 1)
    params = lines[1]
    alpha = float(params[0])
    max_epochs = int(params[1])
    bias = float(params[2])

    # Extract all weights generically (from 4th column onwards)
    weights = [float(w) for w in params[3:]]
    num_inputs = len(weights)

    # Parse training data (Row 4 onwards, index 3+)
    data = []
    for row in lines[3:]:
        data.append([float(val) for val in row])

    # Setup dynamic table headers based on number of inputs
    x_headers = [f"x{i+1}" for i in range(num_inputs)]
    w_headers = [f"w{i+1}" for i in range(num_inputs)]

    header_cols = x_headers + ["target", "yin", "y=f(yin)"] + w_headers + ["bias"]
    header_str = "".join([f"{col:<10}" for col in header_cols])

    print("Neural Network Training ")
    print("-------------------------------------------------")

    # 2. Training Loop
    for epoch in range(1, max_epochs + 1):
        print(f"\n--- Epoch {epoch} ---")
        print(header_str)
        print("-" * len(header_str))

        weight_changed_in_epoch = False

        for row in data:
            # Separate inputs (x) from the target
            x = row[:-1]
            target = row[-1]

            # Calculate net input (yin)
            yin = sum(x[i] * weights[i] for i in range(num_inputs)) + bias

            # Apply bipolar activation function
            y = activation_function(yin)

            # Check if weight update is needed
            if y != target:
                # Bipolar Perceptron learning rule: w = w + alpha * target * x
                for i in range(num_inputs):
                    weights[i] = round(weights[i] + alpha * target * x[i], 4)
                bias = round(bias + alpha * target, 4)
                weight_changed_in_epoch = True

            # Format and print the row dynamically
            row_str = ""
            for xi in x:
                row_str += f"{xi:<10.0f}"

            row_str += f"{target:<10.0f}{yin:<10.2f}{y:<10.0f}"

            for wi in weights:
                row_str += f"{wi:<10.2f}"

            row_str += f"{bias:<10.2f}"
            print(row_str)

        # 3. Termination Condition
        if not weight_changed_in_epoch:
            print(f"\nTermination condition reached at Epoch {epoch}: No weight updates needed.")
            break
    else:
        print(f"\nTermination condition reached: Maximum epochs ({max_epochs}) completed.")

if __name__ == "__main__":
    main()
[23bcs123@mepcolinux ex7]$cat input.csv
learning_rate,max_epochs,bias,w1,w2
1,2,1,0.2,0.3
x1,x2,target
0,0,0
0,1,1
1,0,1
[23bcs123@mepcolinux ex7]$python3 prog.py
Neural Network Training
-------------------------------------------------

--- Epoch 1 ---
x1        x2        target    yin       y=f(yin)  w1        w2        bias
--------------------------------------------------------------------------------
0         0         0         1.00      1         0.20      0.30      1.00
0         1         1         1.30      1         0.20      0.30      1.00
1         0         1         1.20      1         0.20      0.30      1.00

--- Epoch 2 ---
x1        x2        target    yin       y=f(yin)  w1        w2        bias
--------------------------------------------------------------------------------
0         0         0         1.00      1         0.20      0.30      1.00
0         1         1         1.30      1         0.20      0.30      1.00
1         0         1         1.20      1         0.20      0.30      1.00

Termination condition reached: Maximum epochs (2) completed.
[23bcs123@mepcolinux ex7]$exit

Script done on Tue Apr  7 11:33:37 2026