import pandas as pd
from pyvis.network import Network

# Загрузка данных из CSV
df = pd.read_csv("scenario_network.csv")

# Создаем граф
net = Network(notebook=True, directed=True, cdn_resources='remote')

# Добавляем узлы
nodes = df[["NodeID", "NodeDescription"]].drop_duplicates()
for _, row in nodes.iterrows():
    net.add_node(row["NodeID"], label=f"Node {row['NodeID']}", title=row["NodeDescription"])

# Добавляем ребра
for _, row in df.iterrows():
    # Проверяем, что оба узла (NodeID и NextNodeID) существуют в графе
    if row["NodeID"] in net.get_nodes() and row["NextNodeID"] in net.get_nodes():
        # Формируем метку ребра с весами эмоций
        edge_label = (
            f"Радость: {row['Joy']}, "
            f"Грусть: {row['Sadness']}, "
            f"Злость: {row['Anger']}, "
            f"Страх: {row['Fear']}, "
            f"Спокойствие: {row['Calm']}"
        )
        net.add_edge(
            row["NodeID"],
            row["NextNodeID"],
            label=edge_label,
            value=max(row[["Joy", "Sadness", "Anger", "Fear", "Calm"]]),  # Вес для визуализации
        )
    else:
        print(f"Пропущено ребро: {row['NodeID']} -> {row['NextNodeID']} (один из узлов отсутствует)")

# Характеристики агента
agent_stats = {
    "optimism": 0.8,  # Оптимизм
    "pessimism": 0.3,  # Пессимизм
    "aggression": 0.5,  # Агрессивность
    "fear": 0.2,  # Пугливость
    "indifference": 0.1,  # Равнодушие
}

# Сопоставление характеристик агента и эмоций
emotion_mapping = {
    "optimism": "Joy",
    "pessimism": "Sadness",
    "aggression": "Anger",
    "fear": "Fear",
    "indifference": "Calm",
}

# Определение доминирующей характеристики агента
dominant_stat = max(agent_stats, key=agent_stats.get)
target_emotion = emotion_mapping[dominant_stat]

# Функция для выбора ребра
def choose_edge(df, current_node, target_emotion):
    # Фильтруем ребра, исходящие из текущего узла
    available_edges = df[df["NodeID"] == current_node]
    if available_edges.empty:
        return None
    # Выбираем ребро с максимальным весом целевой эмоции
    chosen_edge = available_edges.loc[available_edges[target_emotion].idxmax()]
    return chosen_edge

# Агент начинает с узла 1
current_node = 1
path = [current_node]

# Симулируем перемещение агента
for _ in range(3):  # Агент делает 3 шага
    chosen_edge = choose_edge(df, current_node, target_emotion)
    if chosen_edge is not None:
        next_node = chosen_edge["NextNodeID"]
        path.append(next_node)
        current_node = next_node
    else:
        break

# Визуализация пути агента
for node in net.nodes:
    if node["id"] in path:
        node["color"] = "green"  # Подсветка узлов, через которые прошел агент

for edge in net.edges:
    if edge["from"] in path and edge["to"] in path:
        edge["color"] = "red"  # Подсветка ребер, по которым прошел агент

# Сохраняем граф в HTML и открываем в браузере
net.show("agent_path.html")