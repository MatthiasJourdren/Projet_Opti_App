import pandas as pd
import matplotlib
# Force Agg backend to avoid MacOS threading issues with GUI
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

def plot_per_algorithm_performance(df, output_dir):
    """
    Generates a dual-axis plot (Cost bar, Time line) for each algorithm.
    """
    algorithms = df['Algorithm'].unique()
    
    for algo in algorithms:
        algo_df = df[df['Algorithm'] == algo].sort_values('Instance')
        
        if algo_df.empty:
            continue
            
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Plot Cost on primary y-axis (Bar chart)
        sns.barplot(
            data=algo_df,
            x='Instance',
            y='Cost',
            ax=ax1,
            color='skyblue',
            alpha=0.6,
            label='Cost'
        )
        ax1.set_xlabel('Instance', fontsize=12)
        ax1.set_ylabel('Cost', color='blue', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
        
        # Plot Time on secondary y-axis (Line chart)
        ax2 = ax1.twinx()
        sns.lineplot(
            data=algo_df,
            x='Instance',
            y='Time',
            ax=ax2,
            color='red',
            marker='o',
            linewidth=2,
            label='Time'
        )
        ax2.set_ylabel('Time (s)', color='red', fontsize=12)
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.set_ylim(bottom=0)

        plt.title(f"Performance Analysis: {algo}", fontsize=16)
        plt.tight_layout()
        
        plot_path = os.path.join(output_dir, f"performance_{algo}.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"Saved performance plot for {algo} to {plot_path}")

def plot_per_instance_performance(df, output_dir):
    """
    Generates a dual-axis plot (Cost bar, Time line) for each instance.
    """
    instances = df['Instance'].unique()
    
    for instance in instances:
        inst_df = df[df['Instance'] == instance].sort_values('Algorithm')
        
        if inst_df.empty:
            continue
            
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Plot Cost on primary y-axis (Bar chart)
        sns.barplot(
            data=inst_df,
            x='Algorithm',
            y='Cost',
            ax=ax1,
            color='skyblue',
            alpha=0.6,
            label='Cost'
        )
        ax1.set_xlabel('Algorithm', fontsize=12)
        ax1.set_ylabel('Cost', color='blue', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='blue')
        
        # Plot Time on secondary y-axis (Line chart)
        ax2 = ax1.twinx()
        sns.lineplot(
            data=inst_df,
            x='Algorithm',
            y='Time',
            ax=ax2,
            color='red',
            marker='o',
            linewidth=2,
            label='Time'
        )
        ax2.set_ylabel('Time (s)', color='red', fontsize=12)
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.set_ylim(bottom=0)

        plt.title(f"Performance Analysis: {instance}", fontsize=16)
        plt.tight_layout()
        
        plot_path = os.path.join(output_dir, f"instance_{instance}.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"Saved performance plot for {instance} to {plot_path}")

def plot_benchmark_results(csv_path, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load data
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_path}")
        return
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Filter for successful runs only for Cost comparison
    success_df = df[df['Status'] == 'Success'].copy()
    
    if success_df.empty:
        print("No successful runs found to plot.")
        return

    # Ensure Cost is numeric
    success_df['Cost'] = pd.to_numeric(success_df['Cost'], errors='coerce')
    success_df['Time'] = pd.to_numeric(success_df['Time'], errors='coerce')
    
    # --- Plot 1: Cost Comparison ---
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")
    
    # Create grouped bar chart
    chart_cost = sns.barplot(
        data=success_df, 
        x="Instance", 
        y="Cost", 
        hue="Algorithm", 
        palette="viridis"
    )
    
    plt.title("Comparison of Signal Cost by Algorithm", fontsize=16)
    plt.ylabel("Cost (Lower is Better)", fontsize=12)
    plt.xlabel("Instance", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title="Algorithm", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    cost_plot_path = os.path.join(output_dir, "comparison_cost.png")
    plt.savefig(cost_plot_path)
    print(f"Saved cost comparison plot to {cost_plot_path}")
    plt.close()

    # --- Plot 2: Time Comparison ---
    plt.figure(figsize=(12, 6))
    
    chart_time = sns.barplot(
        data=success_df, 
        x="Instance", 
        y="Time", 
        hue="Algorithm", 
        palette="rocket"
    )
    
    plt.title("Comparison of Execution Time by Algorithm", fontsize=16)
    plt.ylabel("Time (seconds)", fontsize=12)
    plt.xlabel("Instance", fontsize=12)
    plt.yscale("log") 
    plt.xticks(rotation=45)
    plt.legend(title="Algorithm", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    time_plot_path = os.path.join(output_dir, "comparison_time.png")
    plt.savefig(time_plot_path)
    print(f"Saved time comparison plot to {time_plot_path}")
    plt.close()

    # --- Plot 3: Per-Algorithm Performance ---
    print("\nGenerating per-algorithm performance plots...")
    plot_per_algorithm_performance(success_df, output_dir)

    # --- Plot 4: Per-Instance Performance ---
    print("\nGenerating per-instance performance plots...")
    plot_per_instance_performance(success_df, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Plot benchmark results")
    parser.add_argument("--csv", default="results/results.csv", help="Path to results CSV file")
    parser.add_argument("--output", default="results/plots", help="Directory to save plots")
    args = parser.parse_args()

    plot_benchmark_results(args.csv, args.output)

if __name__ == "__main__":
    main()
