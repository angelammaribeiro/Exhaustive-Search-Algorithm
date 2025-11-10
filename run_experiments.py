"""
Computational Experiments Script

Runs exhaustive search and greedy heuristic algorithms on all generated graphs
and collects performance metrics.
"""

import time
import json
import os
from pathlib import Path
from graph_loader import load_graph_for_matching, list_available_graphs, get_graph_info
from exhaustive_search import exhaustive_search_matching
from greedy_heuristic import greedy_matching


def run_experiment_on_graph(graph_file, graphs_dir='graphs'):
    """
    Run both algorithms on a single graph and collect metrics.
    
    Args:
        graph_file: Name of graph JSON file
        graphs_dir: Directory containing graph files
    
    Returns:
        Dictionary with experiment results
    """
    filepath = os.path.join(graphs_dir, graph_file)
    
    # Load graph
    g = load_graph_for_matching(filepath)
    info = get_graph_info(filepath)
    
    # Extract graph parameters from filename
    # Format: graph_nX_dY.json
    parts = graph_file.replace('.json', '').split('_')
    n_vertices = int(parts[1][1:])  # Remove 'n' prefix
    density = parts[2][1:]  # Remove 'd' prefix
    
    result = {
        'filename': graph_file,
        'vertices': n_vertices,
        'edges': info['edges'],
        'density': density,
        'max_edges': n_vertices * (n_vertices - 1) // 2
    }
    
    # Skip exhaustive search for large graphs (too slow)
    max_edges_for_exhaustive = 20
    
    if info['edges'] <= max_edges_for_exhaustive:
        # Run exhaustive search
        try:
            start_time = time.time()
            ex_matching, ex_weight = exhaustive_search_matching(g)
            ex_time = time.time() - start_time
            
            result['exhaustive'] = {
                'weight': ex_weight,
                'time_ms': ex_time * 1000,
                'num_edges_in_matching': len(ex_matching),
                'matching': ex_matching
            }
        except Exception as e:
            result['exhaustive'] = {'error': str(e)}
    else:
        result['exhaustive'] = {'skipped': 'Too many edges for exhaustive search'}
    
    # Run greedy heuristic
    try:
        start_time = time.time()
        gr_matching, gr_weight = greedy_matching(g)
        gr_time = time.time() - start_time
        
        result['greedy'] = {
            'weight': gr_weight,
            'time_ms': gr_time * 1000,
            'num_edges_in_matching': len(gr_matching),
            'matching': gr_matching
        }
        
        # Calculate quality if exhaustive was run
        if 'exhaustive' in result and 'weight' in result['exhaustive']:
            ex_weight = result['exhaustive']['weight']
            if ex_weight > 0:
                result['greedy']['quality_percent'] = (gr_weight / ex_weight) * 100
                result['greedy']['speedup'] = result['exhaustive']['time_ms'] / gr_time if gr_time > 0 else 0
            else:
                result['greedy']['quality_percent'] = 100.0
    except Exception as e:
        result['greedy'] = {'error': str(e)}
    
    return result


def run_all_experiments(graphs_dir='graphs', output_dir='results'):
    """
    Run experiments on all generated graphs.
    
    Args:
        graphs_dir: Directory containing graph files
        output_dir: Directory to store results
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Get all graph files
    graph_files = list_available_graphs(graphs_dir)
    
    print("="*80)
    print("COMPUTATIONAL EXPERIMENTS")
    print("="*80)
    print(f"Total graphs to process: {len(graph_files)}")
    print(f"Results will be saved to: {output_dir}/")
    print("="*80)
    
    all_results = []
    
    for i, graph_file in enumerate(graph_files, 1):
        print(f"\n[{i}/{len(graph_files)}] Processing: {graph_file}")
        
        result = run_experiment_on_graph(graph_file, graphs_dir)
        all_results.append(result)
        
        # Print summary
        print(f"  Vertices: {result['vertices']}, Edges: {result['edges']} "
              f"(Density: {result['density']}%)")
        
        if 'exhaustive' in result and 'weight' in result['exhaustive']:
            print(f"  Exhaustive: weight={result['exhaustive']['weight']:.2f}, "
                  f"time={result['exhaustive']['time_ms']:.3f}ms")
        elif 'exhaustive' in result and 'skipped' in result['exhaustive']:
            print(f"  Exhaustive: {result['exhaustive']['skipped']}")
        
        if 'greedy' in result and 'weight' in result['greedy']:
            print(f"  Greedy: weight={result['greedy']['weight']:.2f}, "
                  f"time={result['greedy']['time_ms']:.3f}ms")
            if 'quality_percent' in result['greedy']:
                speedup_str = f"{result['greedy']['speedup']:.2f}x" if 'speedup' in result['greedy'] else "N/A"
                print(f"  Quality: {result['greedy']['quality_percent']:.2f}%, "
                      f"Speedup: {speedup_str}")
    
    # Save all results
    results_file = os.path.join(output_dir, 'experiment_results.json')
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n" + "="*80)
    print(f"All results saved to: {results_file}")
    print("="*80)
    
    # Generate summary statistics
    generate_summary_report(all_results, output_dir)
    
    return all_results


def generate_summary_report(results, output_dir='results'):
    """
    Generate a summary report of experimental results.
    
    Args:
        results: List of experiment results
        output_dir: Directory to store report
    """
    report_file = os.path.join(output_dir, 'experiment_summary.txt')
    
    with open(report_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("COMPUTATIONAL EXPERIMENTS - SUMMARY REPORT\n")
        f.write("="*80 + "\n\n")
        
        # Overall statistics
        total_graphs = len(results)
        exhaustive_run = sum(1 for r in results if 'exhaustive' in r and 'weight' in r['exhaustive'])
        greedy_run = sum(1 for r in results if 'greedy' in r and 'weight' in r['greedy'])
        
        f.write(f"Total graphs tested: {total_graphs}\n")
        f.write(f"Exhaustive search completed: {exhaustive_run}\n")
        f.write(f"Greedy heuristic completed: {greedy_run}\n\n")
        
        # Detailed table
        f.write("-"*80 + "\n")
        f.write(f"{'Vertices':<10} {'Density':<10} {'Edges':<10} {'Exhaustive':<15} "
                f"{'Greedy':<15} {'Quality':<10}\n")
        f.write("-"*80 + "\n")
        
        for r in results:
            vertices = f"{r['vertices']}"
            density = f"{r['density']}%"
            edges = f"{r['edges']}"
            
            if 'exhaustive' in r and 'weight' in r['exhaustive']:
                ex_weight = f"{r['exhaustive']['weight']:.2f}"
            else:
                ex_weight = "N/A"
            
            if 'greedy' in r and 'weight' in r['greedy']:
                gr_weight = f"{r['greedy']['weight']:.2f}"
                quality = f"{r['greedy'].get('quality_percent', 0):.1f}%" if 'quality_percent' in r['greedy'] else "N/A"
            else:
                gr_weight = "N/A"
                quality = "N/A"
            
            f.write(f"{vertices:<10} {density:<10} {edges:<10} {ex_weight:<15} "
                    f"{gr_weight:<15} {quality:<10}\n")
        
        # Performance statistics
        f.write("\n" + "="*80 + "\n")
        f.write("PERFORMANCE STATISTICS\n")
        f.write("="*80 + "\n\n")
        
        # Calculate averages
        results_with_both = [r for r in results 
                            if 'exhaustive' in r and 'weight' in r['exhaustive'] 
                            and 'greedy' in r and 'weight' in r['greedy']]
        
        if results_with_both:
            avg_quality = sum(r['greedy']['quality_percent'] for r in results_with_both) / len(results_with_both)
            speedups = [r['greedy']['speedup'] for r in results_with_both if 'speedup' in r['greedy']]
            avg_speedup = sum(speedups) / len(speedups) if speedups else 0
            optimal_count = sum(1 for r in results_with_both if r['greedy']['quality_percent'] >= 99.9)
            
            f.write(f"Average greedy quality: {avg_quality:.2f}%\n")
            if avg_speedup > 0:
                f.write(f"Average speedup: {avg_speedup:.2f}x\n")
            f.write(f"Greedy found optimal in: {optimal_count}/{len(results_with_both)} cases "
                   f"({optimal_count/len(results_with_both)*100:.1f}%)\n")
    
    print(f"Summary report saved to: {report_file}")


if __name__ == "__main__":
    results = run_all_experiments()
    
    print("\n" + "="*80)
    print("EXPERIMENTS COMPLETED!")
    print("="*80)
    print("\nResults saved in 'results/' directory:")
    print("  - experiment_results.json: Detailed results for all graphs")
    print("  - experiment_summary.txt: Human-readable summary report")
