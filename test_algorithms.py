"""
Test cases for maximum weighted matching algorithms.
"""

import time
from graph import Graph
from exhaustive_search import exhaustive_search_matching, exhaustive_search_matching_optimized
from greedy_heuristic import greedy_matching


def create_test_graph_1():
    """Simple graph with 4 vertices."""
    g = Graph()
    g.add_edge(1, 2, 10)
    g.add_edge(2, 3, 5)
    g.add_edge(3, 4, 8)
    g.add_edge(1, 4, 6)
    return g, "Simple 4-vertex graph"


def create_test_graph_2():
    """Graph where greedy might not find optimal solution."""
    g = Graph()
    g.add_edge(1, 2, 10)
    g.add_edge(2, 3, 9)
    g.add_edge(3, 4, 8)
    g.add_edge(1, 3, 7)
    g.add_edge(2, 4, 6)
    return g, "Graph testing greedy optimality"


def create_test_graph_3():
    """Triangle graph."""
    g = Graph()
    g.add_edge('A', 'B', 5)
    g.add_edge('B', 'C', 7)
    g.add_edge('A', 'C', 6)
    return g, "Triangle graph"


def create_test_graph_4():
    """Complete graph K4."""
    g = Graph()
    g.add_edge(1, 2, 8)
    g.add_edge(1, 3, 5)
    g.add_edge(1, 4, 9)
    g.add_edge(2, 3, 7)
    g.add_edge(2, 4, 6)
    g.add_edge(3, 4, 10)
    return g, "Complete graph K4"


def create_test_graph_5():
    """Path graph with 6 vertices."""
    g = Graph()
    g.add_edge(1, 2, 3)
    g.add_edge(2, 3, 8)
    g.add_edge(3, 4, 5)
    g.add_edge(4, 5, 7)
    g.add_edge(5, 6, 4)
    return g, "Path graph with 6 vertices"


def create_test_graph_6():
    """Bipartite graph."""
    g = Graph()
    g.add_edge('A1', 'B1', 12)
    g.add_edge('A1', 'B2', 8)
    g.add_edge('A2', 'B1', 7)
    g.add_edge('A2', 'B2', 15)
    g.add_edge('A3', 'B3', 10)
    return g, "Bipartite graph"


def create_test_graph_7():
    """Larger graph for performance testing."""
    g = Graph()
    # Create a graph with 10 vertices
    for i in range(1, 10):
        g.add_edge(i, i+1, i * 2)
    g.add_edge(1, 5, 20)
    g.add_edge(2, 6, 18)
    g.add_edge(3, 7, 16)
    g.add_edge(4, 8, 14)
    g.add_edge(5, 9, 12)
    return g, "Larger graph (10 vertices)"


def run_test(graph, description):
    """
    Run both algorithms on a test graph and compare results.
    
    Args:
        graph: Graph object to test
        description: Description of the test case
    """
    print("\n" + "="*70)
    print(f"TEST: {description}")
    print("="*70)
    print(f"\nGraph Statistics:")
    print(f"  Vertices: {graph.get_num_vertices()}")
    print(f"  Edges: {graph.get_num_edges()}")
    print(f"\nEdges:")
    for u, v, w in sorted(graph.get_edges(), key=lambda x: x[2], reverse=True):
        print(f"  ({u}, {v}): {w}")
    
    # Run exhaustive search
    print("\n--- Exhaustive Search ---")
    start_time = time.time()
    exhaustive_matching, exhaustive_weight = exhaustive_search_matching(graph)
    exhaustive_time = time.time() - start_time
    print(f"Matching: {exhaustive_matching}")
    print(f"Total Weight: {exhaustive_weight}")
    print(f"Execution Time: {exhaustive_time:.6f} seconds")
    
    # Run greedy heuristic
    print("\n--- Greedy Heuristic ---")
    start_time = time.time()
    greedy_matching_result, greedy_weight = greedy_matching(graph)
    greedy_time = time.time() - start_time
    print(f"Matching: {greedy_matching_result}")
    print(f"Total Weight: {greedy_weight}")
    print(f"Execution Time: {greedy_time:.6f} seconds")
    
    # Compare results
    print("\n--- Comparison ---")
    if greedy_weight == exhaustive_weight:
        print("✓ Greedy found the OPTIMAL solution!")
        optimality = 100.0
    else:
        optimality = (greedy_weight / exhaustive_weight * 100) if exhaustive_weight > 0 else 0
        print(f"✗ Greedy is suboptimal: {greedy_weight}/{exhaustive_weight} = {optimality:.2f}%")
    
    if exhaustive_time > 0:
        speedup = exhaustive_time / greedy_time if greedy_time > 0 else float('inf')
        print(f"Speedup: {speedup:.2f}x faster with greedy")
    
    return {
        'description': description,
        'vertices': graph.get_num_vertices(),
        'edges': graph.get_num_edges(),
        'exhaustive_weight': exhaustive_weight,
        'exhaustive_time': exhaustive_time,
        'greedy_weight': greedy_weight,
        'greedy_time': greedy_time,
        'optimality': optimality
    }


def main():
    """Run all test cases."""
    print("\n" + "="*70)
    print("MAXIMUM WEIGHTED MATCHING - ALGORITHM COMPARISON")
    print("="*70)
    
    # Create test graphs
    test_cases = [
        create_test_graph_1(),
        create_test_graph_2(),
        create_test_graph_3(),
        create_test_graph_4(),
        create_test_graph_5(),
        create_test_graph_6(),
    ]
    
    results = []
    for graph, description in test_cases:
        result = run_test(graph, description)
        results.append(result)
    
    # Summary
    print("\n\n" + "="*70)
    print("SUMMARY OF ALL TESTS")
    print("="*70)
    print(f"\n{'Test Case':<35} {'V':<4} {'E':<4} {'Optimal':<8} {'Greedy':<8} {'Quality':<10}")
    print("-"*70)
    
    for r in results:
        print(f"{r['description']:<35} {r['vertices']:<4} {r['edges']:<4} "
              f"{r['exhaustive_weight']:<8} {r['greedy_weight']:<8} {r['optimality']:.1f}%")
    
    # Overall statistics
    optimal_count = sum(1 for r in results if r['optimality'] == 100.0)
    avg_optimality = sum(r['optimality'] for r in results) / len(results)
    avg_speedup = sum(r['exhaustive_time'] / r['greedy_time'] for r in results if r['greedy_time'] > 0) / len(results)
    
    print("\n" + "="*70)
    print("OVERALL STATISTICS")
    print("="*70)
    print(f"Greedy found optimal solution in: {optimal_count}/{len(results)} cases ({optimal_count/len(results)*100:.1f}%)")
    print(f"Average solution quality: {avg_optimality:.2f}%")
    print(f"Average speedup: {avg_speedup:.2f}x")


if __name__ == "__main__":
    main()
