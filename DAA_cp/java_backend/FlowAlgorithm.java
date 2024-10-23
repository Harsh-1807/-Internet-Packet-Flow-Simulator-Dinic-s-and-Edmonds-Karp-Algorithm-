import java.util.*;

public class FlowAlgorithm {

    private int vertexCount;
    private List<List<Edge>> graph;

    // Constructor accepting the number of vertices
    public FlowAlgorithm(int vertexCount) {
        this.vertexCount = vertexCount;
        graph = new ArrayList<>(vertexCount);
        for (int i = 0; i < vertexCount; i++) {
            graph.add(new ArrayList<>());
        }
    }

    // Edge class to store capacity, flow, and reverse edge
    static class Edge {
        int to, flow, capacity;
        Edge reverse;

        public Edge(int to, int capacity) {
            this.to = to;
            this.capacity = capacity;
            this.flow = 0;
        }
    }

    // Add an edge to the graph (along with reverse edge)
    public void addEdge(int u, int v, int capacity) {
        Edge forwardEdge = new Edge(v, capacity);
        Edge backwardEdge = new Edge(u, 0);  
        forwardEdge.reverse = backwardEdge;
        backwardEdge.reverse = forwardEdge;
        graph.get(u).add(forwardEdge);
        graph.get(v).add(backwardEdge);
    }

  

    private int[] level;

    // BFS to build level graph
    private boolean bfsDinic(int source, int sink) {
        level = new int[vertexCount];
        Arrays.fill(level, -1);
        level[source] = 0;

        Queue<Integer> queue = new LinkedList<>();
        queue.add(source);

        while (!queue.isEmpty()) {
            int u = queue.poll();
            for (Edge edge : graph.get(u)) {
                if (level[edge.to] < 0 && edge.flow < edge.capacity) {
                    level[edge.to] = level[u] + 1;
                    queue.add(edge.to);
                }
            }
        }
        return level[sink] != -1;
    }

    // DFS for finding augmenting path
    private int dfsDinic(int u, int flow, int sink, int[] start) {
        if (u == sink) {
            return flow;
        }

        for (; start[u] < graph.get(u).size(); start[u]++) {
            Edge edge = graph.get(u).get(start[u]);
            if (level[edge.to] == level[u] + 1 && edge.flow < edge.capacity) {
                int currentFlow = Math.min(flow, edge.capacity - edge.flow);
                int tempFlow = dfsDinic(edge.to, currentFlow, sink, start);
                if (tempFlow > 0) {
                    edge.flow += tempFlow;
                    edge.reverse.flow -= tempFlow;
                    return tempFlow;
                }
            }
        }
        return 0;
    }

    // Dinic's max flow method
    public int dinicMaxFlow(int source, int sink) {
        int maxFlow = 0;
        while (bfsDinic(source, sink)) {
            int[] start = new int[vertexCount];
            int flow;
            while ((flow = dfsDinic(source, Integer.MAX_VALUE, sink, start)) > 0) {
                maxFlow += flow;
            }
        }
        return maxFlow;
    }

    
    // BFS for finding augmenting paths
    private boolean bfsEdmondsKarp(int[] parent, int source, int sink) {
        boolean[] visited = new boolean[vertexCount];
        Arrays.fill(visited, false);

        Queue<Integer> queue = new LinkedList<>();
        queue.add(source);
        visited[source] = true;
        parent[source] = -1;

        while (!queue.isEmpty()) {
            int u = queue.poll();

            for (Edge edge : graph.get(u)) {
                if (!visited[edge.to] && edge.capacity > edge.flow) {
                    queue.add(edge.to);
                    parent[edge.to] = u;
                    visited[edge.to] = true;

                    if (edge.to == sink) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    // Edmonds-Karp max flow method
    public int edmondsKarpMaxFlow(int source, int sink) {
        int maxFlow = 0;
        int[] parent = new int[vertexCount];

        while (bfsEdmondsKarp(parent, source, sink)) {
            int pathFlow = Integer.MAX_VALUE;

           
            for (int v = sink; v != source; v = parent[v]) {
                int u = parent[v];
                for (Edge edge : graph.get(u)) {
                    if (edge.to == v && edge.capacity > edge.flow) {
                        pathFlow = Math.min(pathFlow, edge.capacity - edge.flow);
                    }
                }
            }

           
            for (int v = sink; v != source; v = parent[v]) {
                int u = parent[v];
                for (Edge edge : graph.get(u)) {
                    if (edge.to == v) {
                        edge.flow += pathFlow;
                        edge.reverse.flow -= pathFlow;
                    }
                }
            }

            maxFlow += pathFlow;
        }

        return maxFlow;
    }
}
