import sys
import os
import time
import argparse

# Add src to python path to import model
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.model.graph import Graph
from src.model.utils import write_solution

class TSPSolverExact:
    def __init__(self, graph):
        self.graph = graph
        self.n = graph.n
        
        # Heuristic optimization: Initialize with a greedy solution (Upper Bound)
        # instead of infinity, to facilitate earlier pruning.
        self.best_path, self.best_cost = self._initial_solution()
        
        self.visited = [False] * self.n
        self.visited[0] = True

        # Default 30 minutes timeout
        self.timeout = 600 
        self.start_time = None

    def solve(self, timeout=600):
        self.timeout = timeout
        self.start_time = time.time()
        try:
            # Path starts with node 0
            self._branch_and_bound([0], 0)
        except TimeoutError:
            pass # Return best found so far
        return self.best_path, self.best_cost

    def _initial_solution(self):
        """
        Generates an initial solution using a Nearest Neighbor heuristic.
        """
        visited = [False] * self.n
        current_node = 0
        visited[0] = True
        path = [0]
        cost = 0
        
        for _ in range(self.n - 1):
            next_node = -1
            min_dist = float('inf')
            for neighbor in range(self.n):
                if not visited[neighbor]:
                    dist = self.graph.get_weight(current_node, neighbor)
                    if dist < min_dist:
                        min_dist = dist
                        next_node = neighbor
            
            visited[next_node] = True
            path.append(next_node)
            cost += min_dist
            current_node = next_node
            
        cost += self.graph.get_weight(current_node, 0)
        return path, cost

    def _calculate_mst_cost(self, unvisited_nodes):
        """
        Calculates the weight of the Minimum Spanning Tree (MST) for the unvisited nodes
        using Prim's algorithm.
        """
        if not unvisited_nodes:
            return 0
            
        mst_cost = 0
        node_indices = list(unvisited_nodes)
        num_nodes = len(node_indices)
        
        # Map original node indices to 0..k
        local_visited = [False] * num_nodes
        min_dists = [float('inf')] * num_nodes
        min_dists[0] = 0 # Start with the first node in the set
        
        for _ in range(num_nodes):
            # Find min dist node
            u_local = -1
            min_val = float('inf')
            for i in range(num_nodes):
                if not local_visited[i] and min_dists[i] < min_val:
                    min_val = min_dists[i]
                    u_local = i
            
            if u_local == -1: 
                break # Should not happen if graph is connected
                
            local_visited[u_local] = True
            mst_cost += min_val
            
            # Update neighbors
            u_original = node_indices[u_local]
            for v_local in range(num_nodes):
                if not local_visited[v_local]:
                    v_original = node_indices[v_local]
                    weight = self.graph.get_weight(u_original, v_original)
                    if weight < min_dists[v_local]:
                        min_dists[v_local] = weight
                        
        return mst_cost

    def _lower_bound(self, last_node, unvisited_nodes, start_node=0):
        """
        Estimates the lower bound of completing the tour.
        LB = current_cost + MST(unvisited) + min_edge_to_enter_MST + min_edge_to_return_start
        """
        if not unvisited_nodes:
            return 0
            
        mst_cost = self._calculate_mst_cost(unvisited_nodes)
        
        # Min edge from last_node to any unvisited node
        min_to_mst = float('inf')
        for node in unvisited_nodes:
            w = self.graph.get_weight(last_node, node)
            if w < min_to_mst:
                min_to_mst = w
                
        # Min edge from any unvisited node back to start_node
        min_from_mst = float('inf')
        for node in unvisited_nodes:
            w = self.graph.get_weight(node, start_node)
            if w < min_from_mst:
                min_from_mst = w
                
        return mst_cost + min_to_mst + min_from_mst

    def _branch_and_bound(self, current_path, current_cost):
        if time.time() - self.start_time > self.timeout:
            raise TimeoutError() # Propagate up

        # Pruning based on simple cost
        if current_cost >= self.best_cost:
            return

        # Base case: valid complete tour
        if len(current_path) == self.n:
            last_node = current_path[-1]
            start_node = current_path[0]
            total_cost = current_cost + self.graph.get_weight(last_node, start_node)
            
            if total_cost < self.best_cost:
                self.best_cost = total_cost
                self.best_path = list(current_path)
                # print(f"New best found: {self.best_cost}") # Debug
            return

        # --- Stronger Pruning with Lower Bound ---
        last_node = current_path[-1]
        
        # Identify unvisited nodes efficiently
        # Since self.visited is global, we can just iterate.
        # But for MST function it needs a list/set.
        unvisited_nodes = [i for i in range(self.n) if not self.visited[i]]
        
        if unvisited_nodes:
            # Estimate remaining cost
            lb_remaining = self._lower_bound(last_node, unvisited_nodes)
            if current_cost + lb_remaining >= self.best_cost:
                return # PRUNE

        # --- Recursive Step with Heuristic Sorting ---
        
        # Candidates sorted by distance for greedy-first exploration
        candidates = []
        for next_node in unvisited_nodes:
            dist = self.graph.get_weight(last_node, next_node)
            candidates.append((dist, next_node))
            
        candidates.sort(key=lambda x: x[0])
        
        for weight, next_node in candidates:
            self.visited[next_node] = True
            self._branch_and_bound(current_path + [next_node], current_cost + weight)
            self.visited[next_node] = False

def main():
    parser = argparse.ArgumentParser(description="Exact TSP Solver (Branch and Bound)")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("--timeout", type=int, default=600, help="Timeout in seconds")
    args = parser.parse_args()

    try:
        graph = Graph.load_from_file(args.input_file)
        solver = TSPSolverExact(graph)
        best_path, best_cost = solver.solve(timeout=args.timeout)
        
        print(f"Optimal Tour: {best_path}")
        print(f"Optimal Cost: {best_cost}")
        
        write_solution(args.input_file, "exact", best_path, best_cost)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
