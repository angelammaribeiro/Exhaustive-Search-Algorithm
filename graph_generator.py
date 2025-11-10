"""
Graph Generator for Computational Experiments

Generates random weighted graphs with vertices as 2D points on XOY plane.
- Vertices: 2D points with integer coordinates between 1 and 500
- Vertices are not coincident and maintain minimum distance
- Edge weights: Euclidean distance between vertices
- Generates graphs with different edge densities (12.5%, 25%, 50%, 75%)

Student Number: 109061 (used as random seed)
"""

import random
import math
import networkx as nx
import json
import os
from pathlib import Path


STUDENT_NUMBER = 109061
MIN_COORD = 1
MAX_COORD = 500
MIN_DISTANCE = 10  # Minimum distance between vertices to avoid being too close


def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two 2D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def generate_vertices(n, seed):
    """
    Generate n vertices as 2D points that are neither coincident nor too close.
    
    Args:
        n: Number of vertices to generate
        seed: Random seed
    
    Returns:
        List of tuples (x, y) representing vertex coordinates
    """
    random.seed(seed)
    vertices = []
    max_attempts = 10000
    
    for i in range(n):
        attempts = 0
        while attempts < max_attempts:
            x = random.randint(MIN_COORD, MAX_COORD)
            y = random.randint(MIN_COORD, MAX_COORD)
            point = (x, y)
            
            # Check if point is not too close to existing vertices
            too_close = False
            for existing in vertices:
                if euclidean_distance(point, existing) < MIN_DISTANCE:
                    too_close = True
                    break
            
            if not too_close:
                vertices.append(point)
                break
            
            attempts += 1
        
        if attempts == max_attempts:
            raise ValueError(f"Could not place vertex {i} after {max_attempts} attempts")
    
    return vertices


def create_weighted_graph(vertices, edge_percentage, seed):
    """
    Create a weighted graph with specified edge density.
    
    Args:
        vertices: List of 2D point coordinates
        edge_percentage: Percentage of maximum possible edges (0.125, 0.25, 0.5, 0.75)
        seed: Random seed for edge selection
    
    Returns:
        NetworkX graph with weighted edges
    """
    n = len(vertices)
    max_edges = n * (n - 1) // 2  # Maximum edges in undirected graph
    num_edges = int(max_edges * edge_percentage)
    
    # Create graph and add vertices with position attributes
    G = nx.Graph()
    for i, (x, y) in enumerate(vertices):
        G.add_node(i, pos=(x, y), x=x, y=y)
    
    # Generate all possible edges with weights (Euclidean distances)
    possible_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            weight = euclidean_distance(vertices[i], vertices[j])
            possible_edges.append((i, j, weight))
    
    # Randomly select edges
    random.seed(seed)
    selected_edges = random.sample(possible_edges, min(num_edges, len(possible_edges)))
    
    # Add edges to graph
    for u, v, weight in selected_edges:
        G.add_edge(u, v, weight=weight)
    
    return G


def graph_to_dict(G):
    """
    Convert NetworkX graph to dictionary representation.
    
    Returns:
        Dictionary with graph information
    """
    graph_dict = {
        'num_vertices': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
        'vertices': {},
        'edges': []
    }
    
    # Store vertex information
    for node in G.nodes():
        graph_dict['vertices'][node] = {
            'x': G.nodes[node]['x'],
            'y': G.nodes[node]['y']
        }
    
    # Store edge information
    for u, v, data in G.edges(data=True):
        graph_dict['edges'].append({
            'u': u,
            'v': v,
            'weight': round(data['weight'], 2)
        })
    
    return graph_dict


def save_graph(G, filename, output_dir='graphs'):
    """
    Save graph to JSON file.
    
    Args:
        G: NetworkX graph
        filename: Output filename (without extension)
        output_dir: Directory to store graph files
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Convert graph to dictionary
    graph_dict = graph_to_dict(G)
    
    # Save as JSON
    json_path = os.path.join(output_dir, f"{filename}.json")
    with open(json_path, 'w') as f:
        json.dump(graph_dict, f, indent=2)
    
    # Also save as adjacency matrix
    adj_matrix_path = os.path.join(output_dir, f"{filename}_adj_matrix.txt")
    with open(adj_matrix_path, 'w') as f:
        n = G.number_of_nodes()
        f.write(f"Adjacency Matrix ({n}x{n}):\n")
        f.write("   ")
        for i in range(n):
            f.write(f"{i:8}")
        f.write("\n")
        
        for i in range(n):
            f.write(f"{i:2} ")
            for j in range(n):
                if G.has_edge(i, j):
                    weight = G[i][j]['weight']
                    f.write(f"{weight:8.2f}")
                else:
                    f.write(f"{0:8.2f}")
            f.write("\n")
    
    print(f"  Saved: {json_path}")
    print(f"  Saved: {adj_matrix_path}")


def load_graph_from_json(filename):
    """
    Load graph from JSON file and convert to NetworkX graph.
    
    Args:
        filename: Path to JSON file
    
    Returns:
        NetworkX graph
    """
    with open(filename, 'r') as f:
        graph_dict = json.load(f)
    
    G = nx.Graph()
    
    # Add vertices
    for node_id, data in graph_dict['vertices'].items():
        G.add_node(int(node_id), x=data['x'], y=data['y'], pos=(data['x'], data['y']))
    
    # Add edges
    for edge in graph_dict['edges']:
        G.add_edge(edge['u'], edge['v'], weight=edge['weight'])
    
    return G


def generate_all_graphs(min_vertices=4, max_vertices=20, student_number=STUDENT_NUMBER):
    """
    Generate all graph instances for computational experiments.
    
    Args:
        min_vertices: Minimum number of vertices
        max_vertices: Maximum number of vertices
        student_number: Student number used as seed
    """
    edge_percentages = {
        '12.5': 0.125,
        '25': 0.25,
        '50': 0.50,
        '75': 0.75
    }
    
    print("="*80)
    print("GRAPH GENERATOR FOR COMPUTATIONAL EXPERIMENTS")
    print("="*80)
    print(f"Student Number (Seed): {student_number}")
    print(f"Vertex Range: {min_vertices} to {max_vertices}")
    print(f"Coordinate Range: [{MIN_COORD}, {MAX_COORD}]")
    print(f"Minimum Distance Between Vertices: {MIN_DISTANCE}")
    print(f"Edge Densities: {list(edge_percentages.keys())}%")
    print("="*80)
    
    summary = []
    
    for n in range(min_vertices, max_vertices + 1):
        print(f"\n--- Generating graphs with {n} vertices ---")
        
        # Generate vertex positions (same for all densities)
        vertices = generate_vertices(n, student_number + n)
        max_edges = n * (n - 1) // 2
        
        for density_name, density_value in edge_percentages.items():
            # Create seed that depends on both vertex count and density
            graph_seed = student_number + n * 1000 + int(float(density_name) * 10)
            
            # Create graph
            G = create_weighted_graph(vertices, density_value, graph_seed)
            
            # Generate filename
            filename = f"graph_n{n}_d{density_name}"
            
            print(f"\n  Graph: {filename}")
            print(f"    Vertices: {G.number_of_nodes()}")
            print(f"    Max possible edges: {max_edges}")
            print(f"    Actual edges: {G.number_of_edges()} ({density_name}%)")
            print(f"    Density: {density_value}")
            
            # Save graph
            save_graph(G, filename)
            
            # Add to summary
            summary.append({
                'filename': filename,
                'vertices': n,
                'edges': G.number_of_edges(),
                'max_edges': max_edges,
                'density': density_name
            })
    
    # Save summary
    summary_path = 'graphs/graph_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "="*80)
    print(f"Generation Complete! Total graphs: {len(summary)}")
    print(f"Summary saved to: {summary_path}")
    print("="*80)
    
    return summary


if __name__ == "__main__":
    # Generate graphs from 4 to 20 vertices
    summary = generate_all_graphs(min_vertices=4, max_vertices=20)
    
    # Display summary table
    print("\n" + "="*80)
    print("GRAPH SUMMARY TABLE")
    print("="*80)
    print(f"{'Vertices':<10} {'Density':<10} {'Edges':<10} {'Max Edges':<12} {'Filename':<30}")
    print("-"*80)
    
    for item in summary:
        print(f"{item['vertices']:<10} {item['density']+'%':<10} {item['edges']:<10} "
              f"{item['max_edges']:<12} {item['filename']:<30}")
