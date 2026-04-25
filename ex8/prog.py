Script started on Mon Apr 20 15:51:39 2026
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target
X = df.iloc[:, :-1]
y = df.iloc[:, -1]
n_trees = int(input("Enter number of decision trees: "))
metric=input("entropy or gini impurity:")
splits = {
    "70-30": 0.3,
    "60-40": 0.4,
    "75-25": 0.25
}
results = []
conf_matrices = {}
for split_name, test_size in splits.items():
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    if(metric=="entropy"):
        model = RandomForestClassifier(n_estimators=n_trees, criterion='entropy',random_state=42)
    else:
        model = RandomForestClassifier(n_estimators=n_trees,random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    results.append([split_name, acc, prec, rec, f1])
    cm = confusion_matrix(y_test, y_pred)
    TN, FP, FN, TP = cm.ravel()
    conf_matrices[split_name] = (TN, FP, FN, TP)
print("\nFinal Results Table:\n")
print("{:<10} {:<10} {:<12} {:<10} {:<10}".format(
    "Split", "Accuracy", "Precision", "Recall", "F1-score"
))
for row in results:
    print("{:<10} {:.4f}     {:.4f}       {:.4f}     {:.4f}".format(*row))
print("\nConfusion Matrices:\n")
for split_name, (TN, FP, FN, TP) in conf_matrices.items():
    print(f"{split_name} Split:")
    print("            Predicted")
    print(f"Actual    TP={TP}   FN={FN}")
    print(f"          FP={FP}   TN={TN}\n")




Output:

PS C:\Users\VIGNESH\Downloads> python .\ensemble.py
Enter number of decision trees: 100
entropy or gini impurity:entropy

Final Results Table:

Split      Accuracy   Precision    Recall     F1-score
70-30      0.9708     0.9640       0.9907     0.9772
60-40      0.9737     0.9733       0.9865     0.9799
75-25      0.9720     0.9670       0.9888     0.9778

Confusion Matrices:

70-30 Split:
            Predicted
Actual    TP=107   FN=1
          FP=4   TN=59

60-40 Split:
            Predicted
Actual    TP=146   FN=2
          FP=4   TN=76

75-25 Split:
            Predicted
Actual    TP=88   FN=1
          FP=3   TN=51

PS C:\Users\VIGNESH\Downloads> python .\ensemble.py
Enter number of decision trees: 100
entropy or gini impurity:gini impurity

Final Results Table:

Split      Accuracy   Precision    Recall     F1-score
70-30      0.9708     0.9640       0.9907     0.9772
60-40      0.9781     0.9735       0.9932     0.9833
75-25      0.9650     0.9667       0.9775     0.9721

Confusion Matrices:

70-30 Split:
            Predicted
Actual    TP=107   FN=1
          FP=4   TN=59

60-40 Split:
            Predicted
Actual    TP=147   FN=1
          FP=4   TN=76

75-25 Split:
            Predicted
Actual    TP=87   FN=2
          FP=3   TN=51

[23bcs123@mepcolinux ex8]$exit

Script done on Mon Apr 20 15:51:41 2026