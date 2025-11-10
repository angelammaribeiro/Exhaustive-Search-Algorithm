# Maximum Weighted Matching - Exhaustive Search Algorithm

## 📋 Problem Description

This project implements and compares two algorithms to solve the **Maximum Weighted Matching Problem** for undirected graphs:

**Problem Statement:** Given an undirected graph G(V, E) with n vertices and m edges, where each edge has a weight, find a maximum weighted matching. A matching in G is a set of pairwise non-adjacent edges (no two edges share a common vertex). A maximum weighted matching is a matching for which the sum of the weights of its edges is as large as possible.

## 🎯 Algorithms Implemented

### 1. Exhaustive Search Algorithm
- **Approach:** Generates all possible subsets of edges (power set) and checks which ones form valid matchings
- **Time Complexity:** O(2^m × m), where m is the number of edges
- **Space Complexity:** O(m)
- **Guarantee:** Always finds the optimal solution

### 2. Greedy Heuristic
- **Approach:** Sorts edges by weight in descending order and greedily selects edges that don't conflict with already selected edges
- **Time Complexity:** O(m log m) - dominated by sorting
- **Space Complexity:** O(n + m)
- **Guarantee:** Finds a good solution quickly, but may not be optimal

## 📁 Project Structure

```
.
├── graph.py                  # Graph data structure implementation
├── exhaustive_search.py      # Exhaustive search algorithm
├── greedy_heuristic.py       # Greedy heuristic algorithm
├── test_algorithms.py        # Comprehensive test suite
└── README.md                 # This file
```

## 🚀 Usage

### Basic Example

```python
from graph import Graph
from exhaustive_search import exhaustive_search_matching
from greedy_heuristic import greedy_matching

# Create a graph
g = Graph()
g.add_edge(1, 2, 10)
g.add_edge(2, 3, 5)
g.add_edge(3, 4, 8)
g.add_edge(1, 4, 6)

# Find maximum weighted matching using exhaustive search
matching, weight = exhaustive_search_matching(g)
print(f"Optimal Matching: {matching}")
print(f"Total Weight: {weight}")

# Find matching using greedy heuristic
matching, weight = greedy_matching(g)
print(f"Greedy Matching: {matching}")
print(f"Total Weight: {weight}")
```

### Running Tests

```bash
# Run comprehensive test suite
python test_algorithms.py
```

## 📊 Experimental Results

### Test Results Summary

The algorithms were tested on 6 different graph configurations:

| Test Case                    | V | E | Optimal | Greedy | Quality |
|------------------------------|---|---|---------|--------|---------|
| Simple 4-vertex graph        | 4 | 4 | 18      | 18     | 100.0%  |
| Graph testing greedy opt.    | 4 | 5 | 18      | 18     | 100.0%  |
| Triangle graph               | 3 | 3 | 7       | 7      | 100.0%  |
| Complete graph K4            | 4 | 6 | 18      | 18     | 100.0%  |
| Path graph (6 vertices)      | 6 | 5 | 15      | 15     | 100.0%  |
| Bipartite graph              | 6 | 5 | 37      | 37     | 100.0%  |

**Overall Statistics:**
- Greedy found optimal solution in **6/6 cases (100%)**
- Average solution quality: **100.00%**
- Average speedup: **5.16x**

### Performance Benchmark

Performance comparison on random graphs (averaged over 5 trials):

| Vertices | Exhaustive (ms) | Greedy (ms) | Speedup    | Quality |
|----------|----------------|-------------|------------|---------|
| 3        | 0.020          | 0.007       | 2.76x      | 100.0%  |
| 4        | 0.018          | 0.008       | 2.20x      | 91.4%   |
| 5        | 0.020          | 0.006       | 3.10x      | 93.9%   |
| 6        | 0.057          | 0.005       | 11.34x     | 94.3%   |
| 7        | 1.364          | 0.006       | 211.93x    | 98.7%   |
| 8        | 0.915          | 0.008       | 110.24x    | 96.3%   |
| 9        | 48.159         | 0.018       | 2,671.87x  | 96.5%   |
| 10       | 173.206        | 0.027       | 6,395.05x  | 93.3%   |

### Key Observations

1. **Exponential Growth:** Exhaustive search time grows exponentially with graph size (growth factor ≈ 3.60)
2. **Greedy Efficiency:** Greedy heuristic maintains **95.6% average solution quality** while being orders of magnitude faster
3. **Scalability:** For 10 vertices, greedy is over **6,000x faster** than exhaustive search
4. **Practical Recommendation:** Use exhaustive search for small graphs (< 15 edges), greedy heuristic for larger graphs

### When Greedy Fails

Example graph where greedy produces a suboptimal solution:

```
Edges: (1,2):100, (1,3):99, (2,4):98, (3,4):50

Exhaustive: [(1,3), (2,4)] → Weight = 197
Greedy:     [(1,2), (3,4)] → Weight = 150 (76.14% optimal)
```

**Why?** Greedy selects edge (1,2) with weight 100 first, which blocks the optimal combination of (1,3) and (2,4).

## 🧪 Algorithm Details

### Exhaustive Search

The exhaustive search algorithm:
1. Generates all possible subsets of edges (2^m possibilities)
2. For each subset, checks if it forms a valid matching (no shared vertices)
3. Calculates the total weight of valid matchings
4. Returns the matching with maximum weight

**Pseudocode:**
```
function exhaustive_search(G):
    best_matching = []
    best_weight = 0
    
    for each subset S of edges in G:
        if is_valid_matching(S):
            weight = sum of weights in S
            if weight > best_weight:
                best_weight = weight
                best_matching = S
    
    return best_matching, best_weight
```

### Greedy Heuristic

The greedy heuristic algorithm:
1. Sorts all edges by weight in descending order
2. Iterates through edges in this order
3. Adds edge to matching if neither vertex has been used
4. Continues until all edges are considered

**Pseudocode:**
```
function greedy_matching(G):
    edges = sort(G.edges) by weight descending
    matching = []
    used_vertices = {}
    
    for each edge (u, v, w) in edges:
        if u not in used_vertices and v not in used_vertices:
            matching.add((u, v, w))
            used_vertices.add(u)
            used_vertices.add(v)
    
    return matching
```

## 🔍 Complexity Analysis

### Time Complexity

| Algorithm          | Best Case | Average Case | Worst Case |
|--------------------|-----------|--------------|------------|
| Exhaustive Search  | O(2^m)    | O(2^m × m)   | O(2^m × m) |
| Greedy Heuristic   | O(m log m)| O(m log m)   | O(m log m) |

### Space Complexity

| Algorithm          | Space Complexity |
|--------------------|------------------|
| Exhaustive Search  | O(m)             |
| Greedy Heuristic   | O(n + m)         |

Where:
- n = number of vertices
- m = number of edges

## 🎓 Educational Value

This project demonstrates:
- **Algorithm Design:** Contrasting exhaustive vs. heuristic approaches
- **Trade-offs:** Optimality vs. efficiency
- **Complexity Analysis:** Exponential vs. polynomial time
- **Graph Theory:** Matching problems and their applications
- **Testing & Validation:** Comprehensive test suite and benchmarking

## 🛠️ Requirements

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

## 📝 License

This project is for educational purposes as part of an Algorithm Analysis course.

## 👥 Author

Angela Maribeiro - Advanced Algorithms Course Project

## 🔗 References

- Matching Theory in Graph Theory
- Greedy Algorithms and Approximation
- Computational Complexity Theory
