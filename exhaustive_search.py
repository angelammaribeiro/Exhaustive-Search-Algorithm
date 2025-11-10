"""
Exhaustive search algorithm for maximum weighted matching problem.
"""

from itertools import combinations
from graph import Graph


def is_valid_matching(edges):
    """
    Check if a set of edges forms a valid matching.
    A matching is valid if no two edges share a common vertex.
    
    Args:
        edges: List of edges, where each edge is a tuple (u, v, weight)
    
    Returns:
        True if the edges form a valid matching, False otherwise
    """
    vertices_used = set()
    for u, v, _ in edges:
        if u in vertices_used or v in vertices_used:
            return False
        vertices_used.add(u)
        vertices_used.add(v)
    return True


def calculate_matching_weight(edges):
    """
    Calculate the total weight of a matching.
    
    Args:
        edges: List of edges, where each edge is a tuple (u, v, weight)
    
    Returns:
        Sum of weights of all edges in the matching
    """
    return sum(weight for _, _, weight in edges)


def exhaustive_search_matching(graph):
    """
    Find the maximum weighted matching using exhaustive search.
    
    This algorithm generates all possible subsets of edges and checks
    which ones form valid matchings. It returns the valid matching with
    the maximum total weight.
    
    Time Complexity: O(2^m * m) where m is the number of edges
    Space Complexity: O(m)
    
    Args:
        graph: Graph object
    
    Returns:
        Tuple of (best_matching, best_weight) where:
        - best_matching is a list of edges in the maximum weighted matching
        - best_weight is the total weight of the matching
    """
    edges = graph.get_edges()
    best_matching = []
    best_weight = 0
    
    # Generate all possible subsets of edges (power set)
    # We need to check all sizes from 0 to len(edges)
    for r in range(len(edges) + 1):
        # Generate all combinations of r edges
        for edge_subset in combinations(edges, r):
            # Check if this subset forms a valid matching
            if is_valid_matching(edge_subset):
                weight = calculate_matching_weight(edge_subset)
                if weight > best_weight:
                    best_weight = weight
                    best_matching = list(edge_subset)
    
    return best_matching, best_weight


def exhaustive_search_matching_optimized(graph):
    """
    Find the maximum weighted matching using optimized exhaustive search.
    
    This version uses pruning: it stops exploring larger subsets once
    we've found a matching that uses all possible vertices.
    
    Args:
        graph: Graph object
    
    Returns:
        Tuple of (best_matching, best_weight)
    """
    edges = graph.get_edges()
    best_matching = []
    best_weight = 0
    max_possible_edges = graph.get_num_vertices() // 2
    
    # Generate all possible subsets of edges
    for r in range(min(len(edges), max_possible_edges) + 1):
        for edge_subset in combinations(edges, r):
            if is_valid_matching(edge_subset):
                weight = calculate_matching_weight(edge_subset)
                if weight > best_weight:
                    best_weight = weight
                    best_matching = list(edge_subset)
    
    return best_matching, best_weight


if __name__ == "__main__":
    # Example usage
    g = Graph()
    g.add_edge(1, 2, 10)
    g.add_edge(2, 3, 5)
    g.add_edge(3, 4, 8)
    g.add_edge(1, 4, 6)
    
    print("Graph:")
    print(g)
    
    matching, weight = exhaustive_search_matching(g)
    print("\nMaximum Weighted Matching (Exhaustive Search):")
    print(f"Edges: {matching}")
    print(f"Total Weight: {weight}")
