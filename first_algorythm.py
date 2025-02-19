import pandas as pd
import networkx as nx

class Agent:
    def __init__(self, optimism, pessimism, aggressiveness, fearfulness, indifference):
        self.traits = {
            'optimism': optimism,
            'pessimism': pessimism,
            'aggressiveness': aggressiveness,
            'fearfulness': fearfulness,
            'indifference': indifference
        }
    
    def choose_next_node(self, current_node, graph):
        neighbors = list(graph.neighbors(current_node))
        if not neighbors:
            return None  # Если нет доступных переходов
        
        best_node = None
        best_score = float('-inf')
        
        for neighbor in neighbors:
            edge_data = graph[current_node][neighbor]
            
            score = sum(self.traits[trait] * edge_data.get(trait, 0) for trait in self.traits)
            
            if score > best_score:
                best_score = score
                best_node = neighbor
        
        return best_node

# Загружаем сценарную сеть из CSV

def load_scenario_network(scenario_network):
    df = pd.read_csv("scenario_network.csv")
    G = nx.DiGraph()
    
    for _, row in df.iterrows():
        G.add_edge(row['source'], row['target'],
                   optimism=row.get('optimism', 0),
                   pessimism=row.get('pessimism', 0),
                   aggressiveness=row.get('aggressiveness', 0),
                   fearfulness=row.get('fearfulness', 0),
                   indifference=row.get('indifference', 0))
    
    return G