import sys
import os
import random
import time
import argparse

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.model.graph import Graph
from src.model.utils import write_solution
from src.local_search.tsp_local_search import local_search_2opt

def randomized_nearest_neighbor(graph, alpha=0.1):
    n = graph.n
    unvisited = list(range(n))
    
    # Start at a random node
    start_node = random.choice(unvisited)
    unvisited.remove(start_node)
    
    current_node = start_node
    path = [current_node]
    cost = 0

    dist_fn = graph.get_weight

    while unvisited:
        # Find distances to all unvisited neighbors
        candidates = []
        min_dist = float('inf')
        max_dist = float('-inf')

        for neighbor in unvisited:
            dist = dist_fn(current_node, neighbor)
            candidates.append((neighbor, dist))
            if dist < min_dist:
                min_dist = dist
            if dist > max_dist:
                max_dist = dist

        # Restricted Candidate List (RCL)
        threshold = min_dist + alpha * (max_dist - min_dist)
        rcl = [c for c in candidates if c[1] <= threshold]
        
        # Pick random from RCL
        next_node, dist = random.choice(rcl)
            
        path.append(next_node)
        unvisited.remove(next_node)
        cost += dist
        current_node = next_node

    # Return to start
    cost += dist_fn(current_node, path[0])
    
    return path, cost

def grasp_ls(graph, max_iterations=10, alpha=0.2, timeout=600):
    best_tour = []
    best_cost = float('inf')
    
    start_time = time.time()
    
    for i in range(max_iterations):
        if time.time() - start_time > timeout:
            # print(f"Timeout reached at iteration {i}")
            break
            
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
    parser = argparse.ArgumentParser(description="GRASP TSP Solver with Local Search")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("--timeout", type=int, default=600, help="Timeout in seconds")
    parser.add_argument("--iterations", type=int, default=10, help="Number of iterations")
    parser.add_argument("--alpha", type=float, default=0.3, help="RCL alpha parameter")
    args = parser.parse_args()
    
    try:
        graph = Graph.load_from_file(args.input_file)
        
        tour, cost = grasp_ls(graph, max_iterations=args.iterations, alpha=args.alpha, timeout=args.timeout)
        
        print(f"Tour: {tour}")
        print(f"Cost: {cost}")
        
        write_solution(args.input_file, "grasp_ls", tour, cost)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
