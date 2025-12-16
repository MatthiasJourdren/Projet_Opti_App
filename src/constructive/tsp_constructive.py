import sys
import os

# Add src to python path to import model
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.model.graph import Graph
from src.model.utils import write_solution

def nearest_neighbor(graph):
    n = graph.n
    visited = [False] * n
    # Start at node 0
    current_node = 0
    visited[current_node] = True
    path = [current_node]
    cost = 0

    for _ in range(n - 1):
        best_dist = float('inf')
        next_node = -1
        
        for neighbor in range(n):
            if not visited[neighbor]:
                dist = graph.get_weight(current_node, neighbor)
                if dist < best_dist:
                    best_dist = dist
                    next_node = neighbor
        
        if next_node == -1:
            # Should not happen in a complete graph
            raise Exception("Graph is not connected or error in logic")
            
        visited[next_node] = True
        path.append(next_node)
        cost += best_dist
        current_node = next_node

    # Return to start
    cost += graph.get_weight(current_node, path[0])
    
    return path, cost

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/constructive/tsp_constructive.py <input_file>")
        sys.exit(1)

    input_filepath = sys.argv[1]
    try:
        graph = Graph.load_from_file(input_filepath)
        tour, cost = nearest_neighbor(graph)
        
        print(f"Tour: {tour}")
        print(f"Cost: {cost}")
        
        write_solution(input_filepath, "constructive", tour, cost)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
