import py4j.GatewayServer;

public class FlowAlgorithmEntryPoint {

    private FlowAlgorithm flowAlgorithm;

    // Constructor to initialize FlowAlgorithm with vertex count
    public FlowAlgorithmEntryPoint(int vertexCount) {
        flowAlgorithm = new FlowAlgorithm(vertexCount);
    }

    // Method to reset the graph (useful when the vertex count changes)
    public void resetGraph(int vertexCount) {
        flowAlgorithm = new FlowAlgorithm(vertexCount);
    }

    // Method to add edges to the graph
    public void addEdge(int u, int v, int capacity) {
        flowAlgorithm.addEdge(u, v, capacity);
    }

    // Method to run Dinic's algorithm
    public int dinicMaxFlow(int source, int sink) {
        return flowAlgorithm.dinicMaxFlow(source, sink);
    }

    // Method to run Edmonds-Karp algorithm
    public int edmondsKarpMaxFlow(int source, int sink) {
        return flowAlgorithm.edmondsKarpMaxFlow(source, sink);
    }

    // Main method to start the Py4J Gateway server
    public static void main(String[] args) {
        FlowAlgorithmEntryPoint entryPoint = new FlowAlgorithmEntryPoint(0);
        GatewayServer server = new GatewayServer(entryPoint);
        server.start();
        System.out.println("Gateway server started...");
    }
}
