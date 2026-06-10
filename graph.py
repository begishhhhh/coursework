import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

DATA_FOLDER = 'C:/Users/User/Desktop/курсовая/50/'
OUTPUT_FOLDER = 'C:/Users/User/Desktop/курсовая/50/graphs/'

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# TICKERS = ['SBER', 'GAZP', 'LKOH', 'ROSN', 'YDEX',
#            'MGNT', 'NLMK', 'GMKN', 'VTBR', 'PLZL']
# SECTOR_COLORS = {
#     # Финансы (синий)
#     'SBER': 'blue', 'VTBR': 'blue',
#     # Нефтегаз (красный)
#     'GAZP': 'red', 'LKOH': 'red', 'ROSN': 'red',
#     # Металлургия (зеленый)
#     'NLMK': 'green', 'GMKN': 'green',
#     # Ритейл
#     'MGNT': 'gold',
#     # IT/Технологии
#     'YDEX': 'purple',
#     # Драгоценные металлы
#     'PLZL': 'yellow'
# }

TICKERS = ['SBER', 'VTBR', 'GAZP', 'LKOH', 'ROSN',
    'NLMK', 'GMKN', 'MGNT', 'YDEX', 'PLZL',
    'TATN', 'SNGS', 'SNGSP',
    'CHMF', 'MAGN', 'ALRS', 'RASP',
    'MOEX', 'BSPB',
    'IRAO', 'FEES', 'HYDR',
    'LENT', 'MVID', 'FIXR', 'BELU',
    'MTSS', 'RTKM', 'RTKMP',
    'PHOR', 'AKRN', 'KZOS',
    'AFLT', 'URAL', 'TRMK', 'KMAZ',
    'PIKK', 'LSRG', 'SMLT',
    'LIFE', 'APTK',
    'AFKS', 'CNRU', 'OZON',
    'ENPG', 'BANE', 'TRNFP',
    'T', 'SELG', 'ASTR']

SECTOR_COLORS = {
    # Финансы (синий)
    'SBER': 'blue', 'VTBR': 'blue', 'MOEX': 'blue', 'BSPB': 'blue', 'T': 'blue',
    # Нефтегаз (красный)
    'GAZP': 'red', 'LKOH': 'red', 'ROSN': 'red', 'TATN': 'red', 'SNGS': 'red', 'SNGSP': 'red', 'BANE': 'red',
    # Металлургия (зеленый)
    'NLMK': 'green', 'GMKN': 'green', 'CHMF': 'green', 'MAGN': 'green', 'ALRS': 'green', 'RASP': 'green',
    # Энергетика (оранжевый)
    'IRAO': 'orange', 'FEES': 'orange', 'HYDR': 'orange', 'ENPG': 'orange',
    # Ритейл (фиолетовый)
    'MGNT': 'purple', 'LENT': 'purple', 'MVID': 'purple', 'FIXR': 'purple', 'BELU': 'purple',
    # Телеком (голубой)
    'MTSS': 'cyan', 'RTKM': 'cyan', 'RTKMP': 'cyan',
    # Химия (розовый)
    'PHOR': 'pink', 'AKRN': 'pink', 'KZOS': 'pink',
    # Машиностроение (коричневый)
    'AFLT': 'brown', 'URAL': 'brown', 'TRMK': 'brown', 'KMAZ': 'brown',
    # Девелопмент (желтый)
    'PIKK': 'gold', 'LSRG': 'gold', 'SMLT': 'gold',
    # IT/Технологии (темно-синий)
    'YDEX': 'navy', 'AFKS': 'navy', 'CNRU': 'navy', 'OZON': 'navy', 'ASTR': 'navy',
    # Фарма (салатовый)
    'LIFE': 'lightgreen', 'APTK': 'lightgreen',
    # Драгоценные металлы (золотой)
    'PLZL': 'darkorange',
    # Лесопромышленность (оливковый)
    'SELG': 'olive',
    # Транспорт (серый)
    'TRNFP': 'gray',
}

# ЗАГРУЗКА МАТРИЦ КОРРЕЛЯЦИЙ
corr_matrices = {}
corr_types = ['pearson', 'spearman', 'kendall']

for corr_type in corr_types:
    filepath = os.path.join(DATA_FOLDER, f'correlation_{corr_type}.csv')
    if os.path.exists(filepath):
        corr_matrices[corr_type] = pd.read_csv(filepath, index_col=0)
    else:
        print(f"Файл {filepath} не найден")
        exit()


# ФУНКЦИИ ДЛЯ ПОСТРОЕНИЯ ГРАФОВ
def build_graph(corr_matrix, threshold=0.3):
    G = nx.Graph()
    G.add_nodes_from(TICKERS)

    tickers_list = list(corr_matrix.columns)

    for i in range(len(tickers_list)):
        for j in range(i + 1, len(tickers_list)):
            corr_value = corr_matrix.iloc[i, j]
            condition = corr_value > threshold

            if condition:
                G.add_edge(tickers_list[i], tickers_list[j],
                           weight=corr_value,
                           raw_corr=corr_value)
    return G


def draw_graph(G, title, filename, pos=None):
    plt.figure(figsize=(12, 8))

    if pos is None:
        pos = nx.spring_layout(G, seed=42, k=2, iterations=50)
    node_colors = [SECTOR_COLORS.get(node, 'gray') for node in G.nodes()]
    node_sizes = [300 + 100 * G.degree(node) for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                           node_color=node_colors, alpha=0.8)

    if G.number_of_edges() > 0:
        edges = G.edges(data=True)
        weights = [d['weight'] * 3 for (u, v, d) in edges]
        nx.draw_networkx_edges(G, pos, width=weights, alpha=0.5)

    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    plt.title(title, size=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, filename), dpi=300, bbox_inches='tight')
    plt.show()

    return pos


corr_type = 'pearson'  # 'pearson', 'spearman', 'kendall'
corr_matrix = corr_matrices[corr_type]
thresholds = [0.9]

for thresh in thresholds:
    G = build_graph(corr_matrix, threshold=thresh)
    print(f"\n🔹 Порог {thresh}: {G.number_of_edges()} ребер")

    if G.number_of_edges() > 0:
        draw_graph(G,
                   f'Сеть акций (порог={thresh}, {corr_type})',
                   f'graph_thresh_{thresh}_{corr_type}.png')


# MST
distance_matrix = 1 - abs(corr_matrix)
G_complete = nx.Graph()
for i in range(len(TICKERS)):
    for j in range(i + 1, len(TICKERS)):
        G_complete.add_edge(TICKERS[i], TICKERS[j],
                            weight=distance_matrix.iloc[i, j])
MST = nx.minimum_spanning_tree(G_complete)

plt.figure(figsize=(12, 8))
pos_mst = nx.spring_layout(MST, seed=42)

node_colors = [SECTOR_COLORS.get(node, 'gray') for node in MST.nodes()]

nx.draw_networkx_nodes(MST, pos_mst, node_size=500, node_color=node_colors, alpha=0.9)
nx.draw_networkx_edges(MST, pos_mst, width=2, alpha=0.7)
nx.draw_networkx_labels(MST, pos_mst, font_size=10)

plt.title(f'MST на основе {corr_type}', size=14)
plt.axis('off')
plt.savefig(os.path.join(OUTPUT_FOLDER, f'mst_{corr_type}.png'), dpi=300)
plt.show()
