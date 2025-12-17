import os
import math

def generate_trap_instance(n, filename):
    """
    Generates a TSP instance designed to trick the Nearest Neighbor heuristic.
    
    Strategy:
    - Nodes 0 to n-2 are arranged in a line with distance 1.
    - Node n-1 is far away from n-2 but close to 0.
    - However, 0 is closer to 1 than to n-1.
    
    Actually, a better trap for NN starting at 0:
    0 is close to 1 (dist 1), 1 is close to 2 (dist 1)... up to k.
    But this path leads to a dead end forcing a long jump.
    
    Let's construct a graph explicitly with coordinates or matrix. Matrix is easier for total control.
    
    Scenario:
    Points 0, 1, ..., n-2 are on a line: (0,0), (1,0), (2,0)...
    Point n-1 is at (0, 1000).
    
    NN from 0 will go 0 -> 1 -> 2 ... -> n-2.
    Then from n-2 must go to n-1. Distance is roughly sqrt((n-2)^2 + 1000^2).
    Then n-1 back to 0. Distance 1000.
    
    Optimal path might be 0 -> n-1 -> n-2 -> ... -> 1 -> 0 (or similar).
    Path 0 -> n-1 is dist 1000. n-1 -> n-2 is huge.
    
    Let's try a different trap.
    "Double Circle" or "Zig Zag".
    
    Simple NN Trap:
    A (start) --- 1 --- B --- 1 --- C ...
    A is also connected to Z with distance 1.1
    Z is connected to B with distance small?
    
    Let's use the explicit coordinate trap:
    Points on a line, plus one outlier.
    0: (0,0)
    1: (1,0)
    ...
    N-2: (N-2, 0)
    N-1: (0, 2)  <-- "Close" to 0, but 1 is closer (1 < 2).
    
    NN tour: 0 -> 1 -> 2 ... -> N-2 -> N-1 -> 0
    Cost approx: (N-2) * 1 + dist(N-2, N-1) + dist(N-1, 0)
    dist(N-2, N-1) = sqrt((N-2)^2 + 2^2) ≈ N-2
    dist(N-1, 0) = 2
    Total NN = (N-2) + (N-2) + 2 = 2N - 2.
    
    Optimal tour: 0 -> N-1 -> N-2 -> N-3 ... -> 1 -> 0
    Edges: (0, N-1)=2, (N-1, N-2)=sqrt((N-2)^2+2^2)≈N-2, (N-2, N-3)=1... (1,0)=1
    Total Opt = 2 + (N-2) + (N-3) * 1 + 1 = 2 + N-2 + N-3 + 1 = 2N - 2.
    Wait, this is the same.
    
    We need the return trip to be expensive for NN.
    
    Let's try:
    0: (0,0)
    1: (10, 0)
    2: (20, 0)
    ...
    k: (10k, 0)
    
    And a point X at (0, 5).
    NN from 0:
    dist(0, X) = 5
    dist(0, 1) = 10
    NN picks X.
    From X, where to go? 
    dist(X, 1) = sqrt(10^2 + 5^2) = 11.18
    dist(X, 2) = sqrt(20^2 + 5^2) = 20.6
    
    If we have points increasing in distance?
    
    Let's implement a known hard case: "The GR24 / P43 instances" or similar construction.
    Or simply random points consisting of clusters. NN jumps between clusters poorly.
    
    But let's stick to the "Line with Outlier" but tune weights manually.
    
    Adjacency Matrix Construction:
    Nodes 0..N-1.
    Edges (i, i+1) = 1 for i=0..N-2.
    Edge (N-1, 0) = 1000. (The return edge is expensive).
    Edge (i, j) otherwise = large.
    
    If we want to trick NN starting at 0:
    It picks 0->1 (cost 1).
    Then 1->2 (cost 1).
    ...
    Reaches N-2.
    Only choice left is N-1.
    N-2 -> N-1 (cost 1).
    path so far: 0..N-1. Cost: N-1.
    Now must close tour: N-1 -> 0. Cost 1000.
    Total: N-1 + 1000.
    
    Is there a better tour?
    Maybe 0 -> N-1 -> N-2 ... -> 1 -> 0?
    0->N-1 cost 1000. Same.
    
    We need a short cycle including 0 and N-1, bypassing the chain? No TSP must visit all.
    
    Correct trap:
    Points 0, 1, 2, 3.
    0-1: 1
    1-2: 1
    2-3: 1
    3-0: 10
    
    0-2: 1.5
    1-3: 1.5
    
    NN (start 0): 0->1->2->3->0. Cost 1+1+1+10 = 13.
    Opt: 0->2->1->3->0 ? 1.5 + 1 + 1.5 + 10 = 14. worse.
    Opt: 0->2->3->1->0 ? 1.5 + 1 + 1.5 + 1 = 5. YES.
    
    Generalize:
    Vertices 0..3 (N=4).
    Chain 0-1-2-3 with cost 1.
    Cross edges (0,2), (1,3) with cost 1.5.
    Return 3-0 cost large.
    
    Let's code this specific matrix generator for size N (even).
    Zipper pattern.
    0, 1, 2, 3, ... N-1
    Edges (i, i+1) = 1.
    Edges (i, i+2) = 0.5 (Cheaper to skip!)
    
    NN at 0 will see (0,1)=1 and (0,2)=0.5. It will pick 2.
    From 2, sees (2,3)=1, (2,4)=0.5. Picks 4.
    ... Goes 0 -> 2 -> 4 ... -> N-2 (or N-1).
    Then has to come back to pick up the odds 1, 3, 5...
    This zig-zag might be expensive if connections between Evens and Odds are costly elsewhere.
    
    Let's build "trap_v1":
    N nodes.
    dist(i, j) = |i-j| basically, but modifier.
    
    Actually, let's create a "Clusters" instance.
    Two clusters far apart. 
    A----B
    |    |
    D----C
    
    Let's execute the file content generation directly.
    I will generate a file "trap_chain.in" which implements the logic:
    Nodes 0..N-1.
    Start at 0.
    0->1 dist 10.
    0->2 dist 100.
    ...
    But actually a path 0 -> 2 -> 4 ... -> 1 -> 3 ... is better.
    
    Let's stick to a simple geometrical trap:
    "U-shape"
    Points (0,0), (1,0), (2,0) ... (10,0)
    Points (10,10), (9,10) ... (0,10)
    
    NN goes 0->1->...->10. Then 10->(10,10) is dist 10.
    Then (10,10)->...->(0,10).
    Then (0,10)->0 is dist 10.
    Total = 10*1 + 10 + 10*1 + 10 = 40.
    
    Alternative: Zig Zag?
    (0,0) -> (0,10) -> (1,0) -> (1,10)...
    Dist(0,0 to 0,10) = 10.
    Dist(0,0 to 1,0) = 1.
    
    If we space them:
    (0,0), (0, 1.1), (0, 2.2) ... NO.
    
    Let's use the tool to write a generator that produces a few distinct types.
    1. Random Uniform (Control).
    2. Clusters (2 groups far apart).
    
    The user wants "Identifier ou Créer des instances où les heuristiques échouent".
    
    I will write the script to generate:
    1. `trap_double_circle`: Inner circle and outer circle.
       NN stays on one circle then jumps. Optimal zig-zags if carefully spaced.
    
    """
    
    output_dir = "instances/pathological"
    os.makedirs(output_dir, exist_ok=True)
    
    # Instance 1: The "Bad NN" Example (Standard trap)
    # A path 0-1-2-3... where sticking to the path is locally good but globally bad?
    # Actually, let's just make random clusters, it usually hurts constructive.
    
    # Let's generate a 50 node instance with 2 clusters
    # Cluster 1: (0,0) to (10,10)
    # Cluster 2: (100,0) to (110,10)
    # NN might jump back and forth if a point in C2 is closer to current in C1 than rest of C1? No.
    # NN will finish C1 then go to C2. That's usually good.
    
    # What if we have a "Line with outlier"
    # 0..48 on (0,0) to (48,0).
    # 49 at (0, 100).
    # NN: 0->1->...->48 -> 49 (dist ~ sqrt(48^2+100^2)≈110) -> 0 (dist 100).
    # Total ~ 48 + 110 + 100 = 258.
    # Opt: 0 -> 49 -> ... no that's worse.
    
    # Let's write a simple random generator first and a 'trap' manually constructed matrix.
    
    # TRAP MATRIX for N=10 (Small enough to see)
    # 0 is start.
    # 0->1 cost 1.
    # 1->2 cost 1.
    # ...
    # 8->9 cost 1.
    # 9->0 cost 100.
    # This is a circle. NN is optimal here.
    
    # Let's write the Trap that forces a "Crossing"
    # We will generate a file with explicit matrix.
    pass

def create_trap_50(filepath):
    """
    Generates a 50-node instance.
    Points 0..48 on a line: (0,0), (2,0), (4,0)...
    Point 49 is 'bait'.
    
    Actually, let's rely on the geometric 'Double Circle' which is known to be tricky.
    Inner circle radius R1, Outer radius R2.
    Angle separation same.
    """
    n = 20 # Small example
    coords = []
    # Inner circle
    for i in range(10):
        theta = 2 * math.pi * i / 10
        coords.append((10 * math.cos(theta), 10 * math.sin(theta)))
    
    # Outer circle, slightly offset rotation?
    for i in range(10):
        theta = 2 * math.pi * i / 10
        coords.append((20 * math.cos(theta), 20 * math.sin(theta)))
        
    # Write as full matrix
    write_instance(filepath, coords)

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def write_instance(filepath, coords):
    n = len(coords)
    with open(filepath, 'w') as f:
        f.write(f"{n}\n")
        for i in range(n):
            row = []
            for j in range(n):
                d = dist(coords[i], coords[j])
                row.append(f"{d:.2f}")
            f.write(" ".join(row) + "\n")
    print(f"Generated {filepath}")

if __name__ == "__main__":
    os.makedirs("instances/pathological", exist_ok=True)
    create_trap_50("instances/pathological/double_circle_20.in")
    
    # Also generate a random one for comparison
    import random
    coords = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(20)]
    write_instance("instances/pathological/random_20.in", coords)
