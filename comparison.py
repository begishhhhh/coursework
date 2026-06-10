import pandas as pd
import numpy as np

def build_binary_graph(corr_matrix, threshold=0.3):
    tickers = corr_matrix.index
    n = len(tickers)
    adj_matrix = pd.DataFrame(0, index=tickers, columns=tickers)

    for i in range(n):
        for j in range(i + 1, n):
            if corr_matrix.iloc[i, j] > threshold:
                adj_matrix.iloc[i, j] = 1
                adj_matrix.iloc[j, i] = 1
    return adj_matrix

def compare_two_methods(adj1, adj2, name1, name2, threshold):
    tickers = adj1.index
    n = len(tickers)
    total_pairs = n * (n - 1) // 2

    same_edges = 0
    same_non_edges = 0
    diff = 0

    for i in range(n):
        for j in range(i + 1, n):
            val1 = adj1.iloc[i, j]
            val2 = adj2.iloc[i, j]

            if val1 == 1 and val2 == 1:
                same_edges += 1
            elif val1 == 0 and val2 == 0:
                same_non_edges += 1
            else:
                diff += 1

    total_same = same_edges + same_non_edges
    agreement = total_same / total_pairs if total_pairs > 0 else 0

    return {
        'threshold': threshold,
        'pair': f"{name1} - {name2}",
        'same_edges': same_edges,
        'same_non_edges': same_non_edges,
        'diff': diff
    }

corr_pearson = pd.read_csv('C:/Users/User/Desktop/курсовая/50/correlation_pearson.csv', index_col=0)
corr_spearman = pd.read_csv('C:/Users/User/Desktop/курсовая/50/correlation_spearman.csv', index_col=0)
corr_kendall = pd.read_csv('C:/Users/User/Desktop/курсовая/50/correlation_kendall.csv', index_col=0)

thresholds = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
results = []

for t in thresholds:
    adj_p = build_binary_graph(corr_pearson, t)
    adj_s = build_binary_graph(corr_spearman, t)
    adj_k = build_binary_graph(corr_kendall, t)

    results.append(compare_two_methods(adj_p, adj_s, "Pearson", "Spearman", t))
    results.append(compare_two_methods(adj_p, adj_k, "Pearson", "Kendall", t))
    results.append(compare_two_methods(adj_s, adj_k, "Spearman", "Kendall", t))

df_results = pd.DataFrame(results)
df_results.to_csv('C:/Users/User/Desktop/курсовая/50/methods_comparison_50.csv', index=False)