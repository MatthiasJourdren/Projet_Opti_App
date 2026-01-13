import sys
import os
import random
import time

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.model.graph import Graph
from src.model.utils import write_solution
from src.local_search.tsp_local_search import local_search_2opt

def randomized_nearest_neighbor(graph, alpha=0.1):
    n = graph.n
    visited = [False] * n
    # Start at a random node
    start_node = random.randint(0, n - 1)
    current_node = start_node
    visited[current_node] = True
    path = [current_node]
    cost = 0

    for _ in range(n - 1):
        candidates = []
        min_dist = float('inf')
        max_dist = float('-inf')

        # Find all unvisited neighbors and their distances
        for neighbor in range(n):
            if not visited[neighbor]:
                dist = graph.get_weight(current_node, neighbor)
                candidates.append((neighbor, dist))
                if dist < min_dist:
                    min_dist = dist
                if dist > max_dist:
                    max_dist = dist
        
        if not candidates:
             break

        # Filter by RCL
        # threshold = min_dist + alpha * (max_dist - min_dist)
        # Using simple percent deviation might be safer if max is huge, but standard is range.
        threshold = min_dist + alpha * (max_dist - min_dist)
        
        rcl = [c for c in candidates if c[1] <= threshold]
        
        if not rcl:
            # Should not happen given logic, but fall back to best
            rcl = [min(candidates, key=lambda x: x[1])]

        # Pick random from RCL
        next_node, dist = random.choice(rcl)
            
        visited[next_node] = True
        path.append(next_node)
        cost += dist
        current_node = next_node

    # Return to start
    cost += graph.get_weight(current_node, path[0])
    
    return path, cost

def grasp_ls(graph, max_iterations=50, alpha=0.2):
    best_tour = []
    best_cost = float('inf')
    
    # Time limit could be added
    
    for i in range(max_iterations):
        # Phase 1: Constructive
        candidate_tour, candidate_cost = randomized_nearest_neighbor(graph, alpha)
        
        # Phase 2: Local Search
        improved_tour, improved_cost = local_search_2opt(graph, candidate_tour)
        
        if improved_cost < best_cost:
            best_cost = improved_cost
            best_tour = improved_tour
            # print(f"New best found at iteration {i}: {best_cost}")
            
    return best_tour, best_cost

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/grasp/tsp_grasp_ls.py <input_file>")
        sys.exit(1)

    input_filepath = sys.argv[1]
    # Set seed for reproducibility if needed, or leave random
    # random.seed(42) 
    
    try:
        graph = Graph.load_from_file(input_filepath)
        
        # Parameters (could be args)
        # alpha and max_iterations can be tuned.
        tour, cost = grasp_ls(graph, max_iterations=20, alpha=0.3)
        
        print(f"Tour: {tour}")
        print(f"Cost: {cost}")
        
        write_solution(input_filepath, "grasp_ls", tour, cost)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
