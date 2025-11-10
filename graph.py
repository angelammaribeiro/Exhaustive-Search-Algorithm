"""
Graph data structure for representing undirected weighted graphs.
"""

class Graph:
    """
    Represents an undirected weighted graph.
    
    Attributes:
        vertices: Set of vertices in the graph
        edges: List of tuples (u, v, weight) representing edges
    """
    
    def __init__(self):
        """Initialize an empty graph."""
        self.vertices = set()
        self.edges = []
    
    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.
        
        Args:
            vertex: The vertex to add
        """
        self.vertices.add(vertex)
    
    def add_edge(self, u, v, weight):
        """
        Add an undirected weighted edge to the graph.
        
        Args:
            u: First vertex
            v: Second vertex
            weight: Weight of the edge
        """
        self.vertices.add(u)
        self.vertices.add(v)
        # Store edge as tuple (u, v, weight) where u < v for consistency
        if u < v:
            self.edges.append((u, v, weight))
        else:
            self.edges.append((v, u, weight))
    
    def get_vertices(self):
        """Return the set of vertices."""
        return self.vertices
    
    def get_edges(self):
        """Return the list of edges."""
        return self.edges
    
    def get_num_vertices(self):
        """Return the number of vertices."""
        return len(self.vertices)
    
    def get_num_edges(self):
        """Return the number of edges."""
        return len(self.edges)
    
    def __str__(self):
        """String representation of the graph."""
        result = f"Graph with {self.get_num_vertices()} vertices and {self.get_num_edges()} edges:\n"
        result += "Vertices: " + str(sorted(self.vertices)) + "\n"
        result += "Edges:\n"
        for u, v, weight in sorted(self.edges):
            result += f"  ({u}, {v}): {weight}\n"
        return result
