import streamlit as st
from py4j.java_gateway import JavaGateway
import os
import json
import tempfile

def generate_manim_script(vertices_data, edges_data, source_node, sink_node):
    return f"""
from manim import *

config.background_color = WHITE

class FlowNetworkScene(Scene):
    def construct(self):
        # Initialize data
        vertices_info = {vertices_data}
        edges_info = {edges_data}
        source = {source_node}
        sink = {sink_node}
        
        # Setup styling
        vertex_color = "#1A1A1A"
        edge_color = "#666666"
        flow_color = "#FF0000"
        highlight_color = "#00FF00"
        
        # Create vertices and labels
        vertices = dict()
        vertex_labels = dict()
        
        # Create vertices
        for i, pos in enumerate(vertices_info):
            color = flow_color if i in [source, sink] else vertex_color
            vertices[i] = Dot(
                point=[pos[0], pos[1], 0],
                radius=0.15,
                color=color,
                stroke_width=2
            )
            vertex_labels[i] = Text(
                str(i),
                color=BLACK,
                font_size=24
            ).next_to(vertices[i], UP, buff=0.1)
        
        # Animate vertices creation
        self.play(
            *[Create(v) for v in vertices.values()],
            *[Write(l) for l in vertex_labels.values()],
            run_time=2
        )
        
        # Create and animate edges
        for u, v, capacity in edges_info:
            # Create arrow
            start = vertices[u].get_center()
            end = vertices[v].get_center()
            arrow = Arrow(
                start=start,
                end=end,
                buff=0.3,
                max_tip_length_to_length_ratio=0.15,
                stroke_width=2,
                color=edge_color
            )
            
            # Create capacity label
            mid_point = arrow.get_center()
            capacity_label = Text(
                str(capacity),
                color=BLACK,
                font_size=24
            ).next_to(mid_point, UP, buff=0.1)
            
            # Animate edge creation
            self.play(
                Create(arrow),
                Write(capacity_label),
                run_time=1
            )
        
        # Final animation for source and sink
        self.play(
            *[v.animate.scale(1.2) for v in [vertices[source], vertices[sink]]],
            run_time=0.5
        )
        self.play(
            *[v.animate.scale(1/1.2) for v in [vertices[source], vertices[sink]]],
            run_time=0.5
        )
        
        self.wait(1)
"""

class FlowNetworkVisualizer:
    def __init__(self):
        self.gateway = JavaGateway()
        self.flow_algorithm = self.gateway.entry_point
        
    def create_visualization(self, vertex_count, source, sink, vertices, edges, algorithm):
        try:
            # Initialize flow algorithm
            self.flow_algorithm.resetGraph(vertex_count)
            for u, v, capacity in edges:
                self.flow_algorithm.addEdge(u, v, capacity)
            
            # Calculate max flow using selected algorithm
            max_flow = (self.flow_algorithm.dinicMaxFlow(source, sink) 
                        if algorithm == "Dinic" 
                        else self.flow_algorithm.edmondsKarpMaxFlow(source, sink))
            
            st.success(f"Maximum Flow: **{max_flow}**")
            
            # Create temporary directory for Manim script execution
            temp_dir = tempfile.mkdtemp()
            script_path = os.path.join(temp_dir, "flow_visualization.py")
            
            # Generate Manim script content
            script_content = generate_manim_script(vertices, edges, source, sink)
            
            # Save generated script to file
            with open(script_path, "w") as f:
                f.write(script_content)
            
            # Run Manim to create video visualization
            cmd = f"manim -pqh {script_path} FlowNetworkScene"
            os.system(cmd)
            
            # Locate and return video file along with max flow value
            video_path = os.path.join(temp_dir, "media/videos/1080p60/FlowNetworkScene.mp4")
            if os.path.exists(video_path):
                with open(video_path, "rb") as f:
                    return f.read(), max_flow  # Return video bytes and max flow value
            
            raise Exception("Animation generation failed")
                
        except Exception as e:
            raise Exception(f"Visualization error: {str(e)}")

def main():
    st.set_page_config(page_title="Flow Network Animator", layout="wide")
    
    st.title("Flow Network Animator")
    
    # Create two columns for input and visualization display
    col1, col2 = st.columns([1, 2])
    
    with col1:
        vertex_count = st.number_input("Number of Vertices", min_value=2, value=6)
        source = st.number_input("Source Node", min_value=0)
        sink = st.number_input("Sink Node", min_value=0)
        
        algorithm = st.selectbox("Algorithm", ["Dinic", "Edmonds-Karp"])
        
        vertices_input = st.text_area("Vertex Coordinates", value='[[-3, 1], [-1, 2], [1, 2], [3, 1]]')
        
        edges_input = st.text_area("Edges", value='[[0, 1, 10], [1, 2, 15]]')
    
    with col2:
        st.markdown("### Network Visualization")

    
    if st.button("Generate Animation"):
       
        try:
            vertices = json.loads(vertices_input)
            edges = json.loads(edges_input)
            
            with st.spinner("Generating animation..."):
                visualizer = FlowNetworkVisualizer()
                video_bytes, max_flow = visualizer.create_visualization(
                    vertex_count,
                    source,
                    sink,
                    vertices,
                    edges,
                    algorithm
                )
                
                st.video(video_bytes)  # Display generated video visualization
                
                
                
        except json.JSONDecodeError:
            st.error("Invalid JSON format in input fields.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()