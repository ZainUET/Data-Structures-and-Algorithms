import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KDTree

train = pd.read_csv("Train.csv")
test = pd.read_csv("Test.csv")

label_col = "TYPE"
feature_cols = [c for c in train.columns if c != label_col]

test_has_label = label_col in test.columns

train[feature_cols] = train[feature_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
if test_has_label:
    test[feature_cols] = test[feature_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
else:
    test = test[feature_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

disease_to_int = {lab: i+1 for i, lab in enumerate(sorted(train[label_col].unique()))}
int_to_disease = {v:k for k,v in disease_to_int.items()}
train['LabelNum'] = train[label_col].map(disease_to_int)

for col in feature_cols:
    plt.figure(figsize=(6,3))
    plt.scatter(train.index, train['LabelNum'], c=train[col], cmap='coolwarm', alpha=0.6)
    plt.yticks(list(int_to_disease.keys()), [int_to_disease[i] for i in int_to_disease.keys()])
    plt.xlabel("Samples")
    plt.ylabel("Disease")
    plt.title(f"{col} vs Disease (color=Symptom)")
    plt.tight_layout()
    plt.show()

def euclidean_distance(x, y):
    return np.sqrt(np.sum((x - y) ** 2))

X_train = train[feature_cols].values.astype(float)
y_train = train[label_col].values
X_test = test[feature_cols].values.astype(float)

def predict_1nn_vectorized(X_train, y_train, X_test):
    preds = []
    for i in range(X_test.shape[0]):
        x = X_test[i]
        d2 = np.sum((X_train - x) ** 2, axis=1)
        idx = np.argmin(d2)
        preds.append(y_train[idx])
    return np.array(preds)

preds = predict_1nn_vectorized(X_train, y_train, X_test)
test['Predicted_TYPE'] = preds

if test_has_label:
    acc = np.mean(test['Predicted_TYPE'] == test[label_col])
    print(f"Accuracy: {acc*100:.2f}%")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)
preds_scaled = predict_1nn_vectorized(X_train_scaled, y_train, X_test_scaled)
if test_has_label:
    acc_scaled = np.mean(preds_scaled == test[label_col].values)
    print(f"Scaled accuracy: {acc_scaled*100:.2f}%")

part1 = train.copy()
part2 = train[feature_cols].copy()
preds_on_part2 = predict_1nn_vectorized(part1[feature_cols].values.astype(float), part1[label_col].values, part2.values.astype(float))
accuracy_part2 = np.mean(preds_on_part2 == part1[label_col].values)
print(f"Self-labeling accuracy: {accuracy_part2*100:.2f}%")

tree = KDTree(X_train)
_, idxs = tree.query(X_test, k=1)
preds_kdtree = y_train[idxs.flatten()]
if test_has_label:
    acc_kdtree = np.mean(preds_kdtree == test[label_col].values)
    print(f"KDTree accuracy: {acc_kdtree*100:.2f}%")

import time

for col in feature_cols:
    plt.figure(figsize=(6,3))
    plt.scatter(train.index, train['LabelNum'], c=train[col], cmap='coolwarm', alpha=0.6)
    plt.yticks(list(int_to_disease.keys()), [int_to_disease[i] for i in int_to_disease.keys()])
    plt.xlabel("Samples")
    plt.ylabel("Disease")
    plt.title(f"{col} vs Disease (color=Symptom)")
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(1)
    plt.close()
