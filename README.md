# Projet Optimization - TSP

## Team

- Name: Team X (Replace with actual team ID/Name if known)

## Structure

- `src/`: Source code
  - `model/`: Graph model and shared utilities
  - `exact/`: Branch and Bound algorithm
  - `constructive/`: Constructive heuristic
  - `local_search/`: Local search heuristic
  - `grasp/`: GRASP meta-heuristic
- `instances/`: Test instances and results
- `report/`: Project report

## Usage

Each algorithm can be run from the command line from the root of the project.

### Exact Method

```bash
python3 src/exact/tsp_exact.py <path_to_instance>
```

Example:

```bash
python3 src/exact/tsp_exact.py instances/exact/test.in
```

### Constructive Heuristic

```bash
python3 src/constructive/tsp_constructive.py Data/17.in
```

### Local Search

```bash
python3 src/local_search/tsp_local_search.py Data/17.in
```

### GRASP

```bash
python3 src/grasp/tsp_grasp.py Data/17.in
```

> [!NOTE]
> Ensure you are using `python3`. The `Data` directory contains additional instances you can test with.

## Input Format

The input file must contain `n` (number of vertices) on the first line, followed by the `n` rows of the adjacency matrix.

## Output Format

The program will generate a file named `{input_filename}_{method}.out` in the same directory as the input file, containing the tour and the total cost.
