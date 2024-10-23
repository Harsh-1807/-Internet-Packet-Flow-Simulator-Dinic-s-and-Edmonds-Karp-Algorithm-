# Internet Packet Flow Simulator 🌐

A powerful network simulation tool that visualizes maximum packet flow through router networks using **Dinic's** and **Edmonds-Karp** algorithms. Built with **Java** backend for flow computations and **Streamlit** frontend for interactive visualization using **Manim**.

![Network Flow](https://img.shields.io/badge/Network-Flow-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Java](https://img.shields.io/badge/Java-8+-red)

## 🚀 Features

- Real-time visualization of packet flow through networks
- Implementation of both Dinic's and Edmonds-Karp algorithms
- Interactive network topology creation
- Performance comparison between algorithms
- Predefined example scenarios
- Custom router placement and edge definition
<img src="https://github.com/user-attachments/assets/0b2164fb-ba8e-4cf4-8514-a9425365b886" alt="image" width="600" height="400"/>


## 📋 Prerequisites

- Python 3.8 or higher
- Java 8 or higher
- Streamlit
- Manim (Community Edition)
- Py4J

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Harsh-1807/Internet-Packet-Flow-Simulator-Dinic-s-and-Edmonds-Karp-Algorithm.git
   cd packet-flow-simulator
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Running the Application

### Step 1: Start the Java Backend
```bash
cd DAA_cp/java_backend
java FlowAlgorithmEntryPoint
```

### Step 2: Launch the Streamlit Frontend
```bash
cd DAA_cp/python_frontend
streamlit run app.py
```

## 📖 Usage Guide

1. **Creating a Network**
   - Add routers by specifying coordinates
   - Define edges between routers
   - Set capacity for each connection

2. **Running Simulations**
   - Select your preferred algorithm
   - Click "Simulate Packet Flow"
   - View the visualization and results

3. **Using Examples**
   Navigate to the "Examples" tab to run predefined scenarios:
   - Basic Network (4 nodes)
   - Complex Network (8 nodes)
   - Custom Scenarios

## 📊 Example Outputs

```plaintext
Network Statistics:
- Maximum Flow: 23 packets/s
- Execution Time: 0.045s
- Path Count: 3
```

## 🔍 Algorithm Details

### Dinic's Algorithm
- Time Complexity: O(V²E)
- Optimized for networks with multiple paths
- Uses level graphs for faster augmentation

### Edmonds-Karp Algorithm
- Time Complexity: O(VE²)
- Based on Ford-Fulkerson method
- Uses BFS to find augmenting paths

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

