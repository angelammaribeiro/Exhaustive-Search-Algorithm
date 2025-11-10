"""
Utility to load generated graphs and convert them for use with matching algorithms.
"""

import json
import os
from graph import Graph


def load_graph_for_matching(json_filename):
    """
    Load a graph from JSON file and convert to Graph object for matching algorithms.
    
    Args:
        json_filename: Path to JSON file
    
    Returns:
        Graph object compatible with exhaustive_search and greedy_heuristic
    """
    with open(json_filename, 'r') as f:
        graph_data = json.load(f)
    
    g = Graph()
    
    # Add edges with weights
    for edge in graph_data['edges']:
        g.add_edge(edge['u'], edge['v'], edge['weight'])
    
    return g


def list_available_graphs(graphs_dir='graphs'):
    """
    List all available graph files.
    
    Args:
        graphs_dir: Directory containing graph files
    
    Returns:
        List of graph filenames
    """
    if not os.path.exists(graphs_dir):
        return []
    
    json_files = [f for f in os.listdir(graphs_dir) if f.endswith('.json') and 'summary' not in f]
    return sorted(json_files)


def get_graph_info(json_filename):
    """
    Get information about a graph without loading it completely.
    
    Args:
        json_filename: Path to JSON file
    
    Returns:
        Dictionary with graph statistics
    """
    with open(json_filename, 'r') as f:
        graph_data = json.load(f)
    
    weights = [edge['weight'] for edge in graph_data['edges']]
    
    return {
        'vertices': graph_data['num_vertices'],
        'edges': graph_data['num_edges'],
        'min_weight': min(weights) if weights else 0,
        'max_weight': max(weights) if weights else 0,
        'avg_weight': sum(weights) / len(weights) if weights else 0
    }


if __name__ == "__main__":
    # Example usage
    print("Available graphs:")
    graphs = list_available_graphs()
    
    if graphs:
        print(f"Found {len(graphs)} graphs")
        for i, graph_file in enumerate(graphs[:5], 1):
            print(f"  {i}. {graph_file}")
            info = get_graph_info(os.path.join('graphs', graph_file))
            print(f"     V={info['vertices']}, E={info['edges']}, "
                  f"Weight range=[{info['min_weight']:.1f}, {info['max_weight']:.1f}]")
    else:
        print("No graphs found. Run graph_generator.py first.")
