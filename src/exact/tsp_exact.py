import sys
import os
import time

# Add src to python path to import model
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.model.graph import Graph
from src.model.utils import write_solution

class TSPSolverExact:
    def __init__(self, graph):
        self.graph = graph
        self.n = graph.n
        self.best_cost = float('inf')
        self.best_path = []
        self.visited = [False] * self.n
        # Start at node 0
        self.visited[0] = True

        # Default 5 minutes timeout
        self.timeout = 300 
        self.start_time = None

    def solve(self, timeout=300):
        self.timeout = timeout
        self.start_time = time.time()
        try:
            # Path starts with node 0
            self._branch_and_bound([0], 0)
        except TimeoutError:
            print("Time limit reached")
        return self.best_path, self.best_cost

    def _branch_and_bound(self, current_path, current_cost):
        if time.time() - self.start_time > self.timeout:
            raise TimeoutError()

        # Pruning
        if current_cost >= self.best_cost:
            return

        # Base case: valid complete tour
        if len(current_path) == self.n:
            # Add cost to return to start
            last_node = current_path[-1]
            start_node = current_path[0]
            total_cost = current_cost + self.graph.get_weight(last_node, start_node)
            
            if total_cost < self.best_cost:
                self.best_cost = total_cost
                self.best_path = list(current_path)
            return

        # Recursive step
        last_node = current_path[-1]
        
        # Simple heuristic for bounding: 
        # If current_cost + minimum possible completion cost >= best_cost, prune.
        # But for basic B&B, just current_cost check is often the first step.
        # Let's start with basic DFS.
        
        for next_node in range(self.n):
            if not self.visited[next_node]:
                weight = self.graph.get_weight(last_node, next_node)
                
                self.visited[next_node] = True
                self._branch_and_bound(current_path + [next_node], current_cost + weight)
                self.visited[next_node] = False

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/exact/tsp_exact.py <input_file>")
        sys.exit(1)

    input_filepath = sys.argv[1]
    try:
        graph = Graph.load_from_file(input_filepath)
        solver = TSPSolverExact(graph)
        best_path, best_cost = solver.solve()
        
        print(f"Optimal Tour: {best_path}")
        print(f"Optimal Cost: {best_cost}")
        
        write_solution(input_filepath, "exact", best_path, best_cost)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
