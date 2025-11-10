"""
Greedy heuristic algorithm for maximum weighted matching problem.
"""

from graph import Graph


def greedy_matching(graph):
    """
    Find a weighted matching using a greedy heuristic.
    
    The algorithm works as follows:
    1. Sort all edges in descending order by weight
    2. Iterate through edges in this order
    3. Add an edge to the matching if it doesn't conflict with already selected edges
       (i.e., neither of its vertices has been used)
    4. Continue until all edges have been considered
    
    Time Complexity: O(m log m) where m is the number of edges (dominated by sorting)
    Space Complexity: O(n + m) where n is the number of vertices
    
    Note: This is a heuristic and does not guarantee the optimal solution,
    but it runs much faster than exhaustive search.
    
    Args:
        graph: Graph object
    
    Returns:
        Tuple of (matching, weight) where:
        - matching is a list of edges in the greedy matching
        - weight is the total weight of the matching
    """
    edges = graph.get_edges()
    
    # Sort edges by weight in descending order
    sorted_edges = sorted(edges, key=lambda edge: edge[2], reverse=True)
    
    matching = []
    used_vertices = set()
    total_weight = 0
    
    # Iterate through edges in descending order of weight
    for u, v, weight in sorted_edges:
        # Check if both vertices are available (not used in the matching yet)
        if u not in used_vertices and v not in used_vertices:
            # Add this edge to the matching
            matching.append((u, v, weight))
            used_vertices.add(u)
            used_vertices.add(v)
            total_weight += weight
    
    return matching, total_weight


def greedy_matching_with_details(graph):
    """
    Find a weighted matching using greedy heuristic with detailed step information.
    
    This version provides more information about the decision-making process.
    
    Args:
        graph: Graph object
    
    Returns:
        Dictionary containing:
        - 'matching': list of edges in the matching
        - 'weight': total weight of the matching
        - 'steps': list of decision steps taken
    """
    edges = graph.get_edges()
    sorted_edges = sorted(edges, key=lambda edge: edge[2], reverse=True)
    
    matching = []
    used_vertices = set()
    total_weight = 0
    steps = []
    
    for u, v, weight in sorted_edges:
        if u not in used_vertices and v not in used_vertices:
            matching.append((u, v, weight))
            used_vertices.add(u)
            used_vertices.add(v)
            total_weight += weight
            steps.append({
                'action': 'added',
                'edge': (u, v, weight),
                'reason': 'Both vertices available'
            })
        else:
            conflict_vertices = []
            if u in used_vertices:
                conflict_vertices.append(u)
            if v in used_vertices:
                conflict_vertices.append(v)
            steps.append({
                'action': 'skipped',
                'edge': (u, v, weight),
                'reason': f'Vertex/vertices {conflict_vertices} already used'
            })
    
    return {
        'matching': matching,
        'weight': total_weight,
        'steps': steps
    }


if __name__ == "__main__":
    # Example usage
    g = Graph()
    g.add_edge(1, 2, 10)
    g.add_edge(2, 3, 5)
    g.add_edge(3, 4, 8)
    g.add_edge(1, 4, 6)
    
    print("Graph:")
    print(g)
    
    matching, weight = greedy_matching(g)
    print("\nMaximum Weighted Matching (Greedy Heuristic):")
    print(f"Edges: {matching}")
    print(f"Total Weight: {weight}")
    
    print("\n" + "="*50)
    print("Detailed Greedy Algorithm Steps:")
    print("="*50)
    result = greedy_matching_with_details(g)
    for i, step in enumerate(result['steps'], 1):
        print(f"\nStep {i}:")
        print(f"  Edge: {step['edge']}")
        print(f"  Action: {step['action']}")
        print(f"  Reason: {step['reason']}")
