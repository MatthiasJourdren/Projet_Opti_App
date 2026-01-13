import sys
import os
import subprocess
import re
import csv
import time
import argparse

# Configuration
ALGORITHMS = {
    "Exact": "src/exact/tsp_exact.py",
    "Constructive": "src/constructive/tsp_constructive.py",
    "LocalSearch": "src/local_search/tsp_local_search.py",
    "GRASP_LS": "src/grasp/tsp_grasp_ls.py"
}

def get_algorithm_command(algo_name, instance_path):
    script_path = ALGORITHMS[algo_name]
    return [sys.executable, script_path, instance_path]

def run_algorithm(algo_name, instance_path, timeout=60):
    command = get_algorithm_command(algo_name, instance_path)
    start_time = time.time()
    try:
        # Run the command with a timeout
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        duration = time.time() - start_time
        
        if result.returncode != 0:
            return {"status": "Error", "time": duration, "cost": None, "error": result.stderr}

        # Parse cost from output
        # Expecting "Cost: <number>"
        match = re.search(r"Cost:\s*([0-9.]+)", result.stdout)
        if match:
            cost = float(match.group(1))
            return {"status": "Success", "time": duration, "cost": cost}
        else:
             return {"status": "ParseError", "time": duration, "cost": None, "error": "Cost not found in stdout"}

    except subprocess.TimeoutExpired:
        return {"status": "Timeout", "time": timeout, "cost": None}
    except Exception as e:
        return {"status": "Exception", "time": 0, "cost": None, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Benchmark TSP algorithms")
    parser.add_argument("--instances", default="Data", help="Directory containing .in files")
    parser.add_argument("--output", default="results.csv", help="Output CSV file")
    parser.add_argument("--max-instances", type=int, default=None, help="Max number of instances to test per algorithm")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds per run")
    args = parser.parse_args()

    # Find instances
    instance_files = []
    if os.path.isdir(args.instances):
        for root, dirs, files in os.walk(args.instances):
            for file in files:
                if file.endswith(".in"):
                    instance_files.append(os.path.join(root, file))
    else:
        print(f"Error: {args.instances} is not a directory.")
        return

    # Sort for consistent order
    instance_files.sort()
    
    if args.max_instances:
        instance_files = instance_files[:args.max_instances]

    print(f"Found {len(instance_files)} instances. Starting benchmark...")

    results = []

    # Prepare CSV
    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['Instance', 'Algorithm', 'Status', 'Time', 'Cost', 'Error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for instance in instance_files:
            instance_name = os.path.basename(instance)
            print(f"\nProcessing {instance_name}...")
            
            for algo_name in ALGORITHMS:
                print(f"  Running {algo_name}...", end=" ", flush=True)
                
                # For exact method, likely skip large instances if logic requires, but we rely on timeout for now
                
                res = run_algorithm(algo_name, instance, timeout=args.timeout)
                
                print(f"{res['status']} ({res['time']:.2f}s) Cost: {res['cost']}")
                
                row = {
                    'Instance': instance_name,
                    'Algorithm': algo_name,
                    'Status': res['status'],
                    'Time': f"{res['time']:.4f}",
                    'Cost': res['cost'],
                    'Error': res.get('error', '')
                }
                writer.writerow(row)
                results.append(row)

    print(f"\nBenchmark complete. Results saved to {args.output}")

if __name__ == "__main__":
    main()
