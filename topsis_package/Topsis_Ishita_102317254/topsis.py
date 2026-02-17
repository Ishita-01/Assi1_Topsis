import sys
import pandas as pd
import numpy as np
import os

def error(msg):
    print(f"Error: {msg}")
    sys.exit(1)

def topsis(input_file, weights, impacts, output_file):
    # File check
    if not os.path.exists(input_file):
        error("Input file not found")

    df = pd.read_csv(input_file)

    if df.shape[1] < 3:
        error("Input file must contain three or more columns")

    data = df.iloc[:, 1:].values

    try:
        data = data.astype(float)
    except:
        error("From 2nd column to last column must contain numeric values only")

    weights = list(map(float, weights.split(',')))
    impacts = impacts.split(',')

    if len(weights) != data.shape[1]:
        error("Number of weights must be equal to number of criteria")

    if len(impacts) != data.shape[1]:
        error("Number of impacts must be equal to number of criteria")

    for i in impacts:
        if i not in ['+', '-']:
            error("Impacts must be either + or -")

 
    norm = data / np.sqrt((data ** 2).sum(axis=0))
    weighted = norm * weights
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted[:, i].max())
            ideal_worst.append(weighted[:, i].min())
        else:
            ideal_best.append(weighted[:, i].min())
            ideal_worst.append(weighted[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

   
    d_pos = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = d_neg / (d_pos + d_neg)

    df['Topsis Score'] = score
    df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)

    df.to_csv(output_file, index=False)
    print("TOPSIS calculation completed successfully")


