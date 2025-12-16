import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.model.graph import Graph
from src.model.utils import write_solution
from src.constructive.tsp_constructive import nearest_neighbor

def two_opt_swap(route, i, k):
    """
    Performs a 2-opt swap by reversing the segment route[i:k+1].
    Indices are based on the route list.
    """
    new_route = route[0:i]
    new_route.extend(route[i:k+1][::-1])
    new_route.extend(route[k+1:])
    return new_route

def local_search_2opt(graph, initial_tour):
    best_tour = initial_tour
    improved = True
    
    n = len(best_tour)
    
    while improved:
        improved = False
        current_cost = graph.calculate_tour_cost(best_tour)
        
        # Iterate over all possible segments to reverse
        # Edges involved are (i-1, i) and (k, k+1)
        # We try to replace them with (i-1, k) and (i, k+1)
        # Nodes in tour: 0..n-1
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                new_tour = two_opt_swap(best_tour, i, k)
                new_cost = graph.calculate_tour_cost(new_tour)
                
                if new_cost < current_cost:
                    best_tour = new_tour
                    improved = True
                    # First improvement strategy
                    break 
            if improved:
                break
                
    return best_tour, graph.calculate_tour_cost(best_tour)

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
