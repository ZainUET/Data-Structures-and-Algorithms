// Question 1:Implement Kruskal Algorithms. Input is given as a weighted graph and output should be a MST using Kruskal Algorithm. 
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Edge {
    int src, dest, weight;
};

class Graph {
    int V; 
    vector<Edge> edges;
    
public:
    Graph(int V) {
        this->V = V;
    }
    
    void addEdge(int src, int dest, int weight) {
        Edge edge = {src, dest, weight};
        edges.push_back(edge);
    }
    
    int find(vector<int>& parent, int i) {
        if (parent[i] == i)
            return i;
        return parent[i] = find(parent, parent[i]); 
    }
    
    void unionSets(vector<int>& parent, vector<int>& rank, int x, int y) {
        int xroot = find(parent, x);
        int yroot = find(parent, y);
        
        if (rank[xroot] < rank[yroot])
            parent[xroot] = yroot;
        else if (rank[xroot] > rank[yroot])
            parent[yroot] = xroot;
        else {
            parent[yroot] = xroot;
            rank[xroot]++;
        }
    }
        void kruskalMST() {
        sort(edges.begin(), edges.end(), [](Edge a, Edge b) {
            return a.weight < b.weight;
        });
        
        vector<int> parent(V);
        vector<int> rank(V, 0);
        vector<Edge> result; 
        int e = 0; 
        int i = 0; 
        
        for (int v = 0; v < V; v++)
            parent[v] = v;
        
        while (e < V - 1 && i < edges.size()) {
            Edge next_edge = edges[i++];
            
            int x = find(parent, next_edge.src);
            int y = find(parent, next_edge.dest);
            
            if (x != y) {
                result.push_back(next_edge);
                unionSets(parent, rank, x, y);
                e++;
            }
        }
        
        cout << "Edges in the Minimum Spanning Tree:\n";
        int minCost = 0;
        for (Edge edge : result) {
            cout << edge.src << " -- " << edge.dest << " == " << edge.weight << endl;
            minCost += edge.weight;
        }
        cout << "Minimum Spanning Tree Cost: " << minCost << endl;
    }
};

int main() {
    Graph g(4);
    
    g.addEdge(0, 1, 10);
    g.addEdge(0, 2, 6);
    g.addEdge(0, 3, 5);
    g.addEdge(1, 3, 15);
    g.addEdge(2, 3, 4);
    
    
    g.kruskalMST();
    
    return 0;
}