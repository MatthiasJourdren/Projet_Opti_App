import os

def write_solution(input_filepath, method_name, tour, cost):
    """
    Writes the solution to a file named {input_filename}_{method}.out
    
    Args:
        input_filepath: Path to the input file (to derive output name).
        method_name: Name of the method (exact, constructive, local_search, grasp).
        tour: List of vertex indices (internal 0-based).
        cost: Total cost of the tour.
    """
    # Derive output filename
    base_name = os.path.splitext(os.path.basename(input_filepath))[0]
    directory = os.path.dirname(input_filepath)
    output_filename = f"{base_name}_{method_name}.out"
    output_filepath = os.path.join(directory, output_filename)

    # Convert tour to 1-based indexing for output if the example suggests 1-based.
    # The example in the subject says:
    # "Cela correspond au cycle 1, 2, 3, 4, 1"
    # And the file content example is:
    # 1 2 3 4
    # So yes, output should be 1-based.
    
    tour_1_based = [str(node + 1) for node in tour]
    
    with open(output_filepath, 'w') as f:
        f.write(" ".join(tour_1_based) + "\n")
        # Format cost as int if it's an integer, else float
        if int(cost) == cost:
            f.write(f"{int(cost)}\n")
        else:
            f.write(f"{cost}\n")

    print(f"Solution written to {output_filepath}")
