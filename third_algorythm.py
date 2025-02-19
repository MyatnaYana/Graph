from pyvis.network import Network
import random

# Создаем граф
net = Network(notebook=True, directed=True)

# Добавляем узлы (состояния)
nodes = [
    {"id": 1, "label": "Node 1", "title": "Описание состояния 1"},
    {"id": 2, "label": "Node 2", "title": "Описание состояния 2"},
    {"id": 3, "label": "Node 3", "title": "Описание состояния 3"},
    {"id": 4, "label": "Node 4", "title": "Описание состояния 4"},
]

for node in nodes:
    net.add_node(node["id"], label=node["label"], title=node["title"])

# Добавляем ребра (связи между узлами)
edges = [
    {"from": 1, "to": 2, "label": "Радость: 0.9", "value": 0.9},
    {"from": 1, "to": 3, "label": "Грусть: 0.7", "value": 0.7},
    {"from": 1, "to": 4, "label": "Злость: 0.5", "value": 0.5},
    {"from": 2, "to": 3, "label": "Страх: 0.8", "value": 0.8},
    {"from": 3, "to": 4, "label": "Спокойствие: 0.6", "value": 0.6},
]

for edge in edges:
    net.add_edge(edge["from"], edge["to"], label=edge["label"], value=edge["value"])

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
    "optimism": "Радость",
    "pessimism": "Грусть",
    "aggression": "Злость",
    "fear": "Страх",
    "indifference": "Спокойствие",
}

# Определение доминирующей характеристики агента
dominant_stat = max(agent_stats, key=agent_stats.get)
target_emotion = emotion_mapping[dominant_stat]

# Выбор ребра с максимальным весом целевой эмоции
def choose_edge(edges, target_emotion):
    filtered_edges = [edge for edge in edges if target_emotion in edge["label"]]
    if filtered_edges:
        return max(filtered_edges, key=lambda x: x["value"])
    return None

# Агент начинает с узла 1
current_node = 1
path = [current_node]

# Симулируем перемещение агента
for _ in range(3):  # Агент делает 3 шага
    available_edges = [edge for edge in edges if edge["from"] == current_node]
    chosen_edge = choose_edge(available_edges, target_emotion)
    
    if chosen_edge:
        next_node = chosen_edge["to"]
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