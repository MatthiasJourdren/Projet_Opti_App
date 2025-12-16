import os

class Graph:
    def __init__(self, n, adjacency_matrix):
        self.n = n
        self.adjacency_matrix = adjacency_matrix

    @staticmethod
    def load_from_file(filepath):
        """
        Loads a graph from a file with the specified format:
        n
        row_1
        ...
        row_n
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, 'r') as f:
            lines = f.readlines()
            
        # Parse n
        try:
            n = int(lines[0].strip())
        except ValueError:
            raise ValueError("First line must be the number of vertices (integer).")

        # Parse adjacency matrix
        adjacency_matrix = []
        for i in range(1, n + 1):
            if i >= len(lines):
                raise ValueError(f"Expected {n} rows for the matrix, found fewer.")
            
            row_str = lines[i].strip().split()
            # Convert to float or int. Weights usually int in TSP examples but float is safer generally.
            # Convert to float for generality, or int if strictly specified. Example uses ints.
            # Let's use float to be safe, but print as int if it is int.
            row = [float(x) for x in row_str]
            
            if len(row) != n:
                raise ValueError(f"Row {i} has {len(row)} elements, expected {n}.")
            
            adjacency_matrix.append(row)

        return Graph(n, adjacency_matrix)

    def get_weight(self, i, j):
        """Returns the weight of edge (i, j). 0-indexed internally."""
        # Adjust for 0-based indexing if input is 1-based? 
        # Usually input indices in file might be just values. 
        # Internally we will use 0 to n-1. 
        # The output requirement asks for indices. 
        # Let's assume internal logic uses 0..n-1.
        return self.adjacency_matrix[i][j]

    def calculate_tour_cost(self, tour):
        """Calculates the cost of a tour (list of vertex indices)."""
        cost = 0
        for i in range(len(tour)):
            u = tour[i]
            v = tour[(i + 1) % len(tour)]
            cost += self.get_weight(u, v)
        return cost
