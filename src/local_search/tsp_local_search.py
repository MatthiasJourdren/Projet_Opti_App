import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.model.graph import Graph
from src.model.utils import write_solution
from src.constructive.tsp_constructive import nearest_neighbor

def local_search_2opt(graph, initial_tour):
    """
    Optimized 2-opt local search that uses incremental cost calculation.
    Complexity: O(n^2) per restart.
    """
    best_tour = list(initial_tour)
    n = len(best_tour)
    current_cost = graph.calculate_tour_cost(best_tour)
    improved = True
    
    dist = graph.get_weight
    
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                # We pick edges (i-1, i) and (j, j_next)
                # And try to replace them with (i-1, j) and (i, j_next)
                # Note: this reverse the segment tour[i...j]
                
                j_next = (j + 1) % n
                
                # Non-adjacent edges requirement
                if j_next == i - 1:
                    continue
                    
                # delta = cost_new - cost_old
                delta = dist(best_tour[i-1], best_tour[j]) + dist(best_tour[i], best_tour[j_next]) \
                      - dist(best_tour[i-1], best_tour[i]) - dist(best_tour[j], best_tour[j_next])
                
                if delta < -1e-9:
                    # Apply swap (reverse segment)
                    best_tour[i:j+1] = best_tour[i:j+1][::-1]
                    current_cost += delta
                    improved = True
                    break # First improvement strategy
            if improved:
                break
                
    return best_tour, current_cost

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/local_search/tsp_local_search.py <input_file>")
        sys.exit(1)

    input_filepath = sys.argv[1]
    try:
        graph = Graph.load_from_file(input_filepath)
        
        # Initial solution using Nearest Neighbor
        initial_tour, initial_cost = nearest_neighbor(graph)
        # print(f"Initial Cost: {initial_cost}")
        
        best_tour, best_cost = local_search_2opt(graph, initial_tour)
        
        print(f"Tour: {best_tour}")
        print(f"Cost: {best_cost}")
        
        write_solution(input_filepath, "local_search", best_tour, best_cost)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
