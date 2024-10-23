import streamlit as st
from py4j.java_gateway import JavaGateway
import os
import json
import tempfile

def generate_manim_script(vertices_data, edges_data, source_node, sink_node):
    return f"""
from manim import *

config.background_color = BLACK

class InternetDataFlowScene(Scene):
    def construct(self):
        vertices_info = {vertices_data}
        edges_info = {edges_data}
        source = {source_node}
        sink = {sink_node}
        
        vertex_color = "#1A1A1A"
        edge_color = "#666666"
        data_flow_color = "#FF0000"
        highlight_color = "#00FF00"
        
        vertices = dict()
        vertex_labels = dict()

        for i, pos in enumerate(vertices_info):
            color = data_flow_color if i in [source, sink] else vertex_color
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
        
        self.play(
            *[Create(v) for v in vertices.values()],
            *[Write(l) for l in vertex_labels.values()],
            run_time=2
        )
        
        for u, v, capacity in edges_info:
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
            
            mid_point = arrow.get_center()
            capacity_label = Text(
                str(capacity),
                color=BLACK,
                font_size=24
            ).next_to(mid_point, UP, buff=0.1)
            
            self.play(
                Create(arrow),
                Write(capacity_label),
                run_time=1
            )
        
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

class InternetPacketFlowVisualizer:
    def __init__(self):
        self.gateway = JavaGateway()
        self.flow_algorithm = self.gateway.entry_point
        
    def create_visualization(self, router_count, source, sink, routers, edges, algorithm):
        try:
            self.flow_algorithm.resetGraph(router_count)
            for u, v, capacity in edges:
                self.flow_algorithm.addEdge(u, v, capacity)
            
            max_flow = (self.flow_algorithm.dinicMaxFlow(source, sink) 
                        if algorithm == "Dinic" 
                        else self.flow_algorithm.edmondsKarpMaxFlow(source, sink))
            
            st.success(f"Maximum Packet Flow: **{max_flow}* *")
            
            temp_dir = tempfile.mkdtemp()
            script_path = os.path.join(temp_dir, "internet_packet_flow_visualization.py")
            
            script_content = generate_manim_script(routers, edges, source, sink)
            
            with open(script_path, "w") as f:
                f.write(script_content)
            
            cmd = f"manim -pqh {script_path} InternetPacketFlowScene"
            os.system(cmd)
            
            video_path = os.path.join(temp_dir, "media/videos/1080p60/InternetPacketFlowScene.mp4")
            if os.path.exists(video_path):
                with open(video_path, "rb") as f:
                    return f.read(), max_flow
            
            raise Exception("Animation generation failed")
                
        except Exception as e:
            raise Exception(f"Visualization error: {str(e)}")


def main():
    st.set_page_config(page_title="Internet Packet Flow Simulator", layout="centered", page_icon="🌐")
    
    st.title("🌐 Internet Packet Flow Simulator")
    st.markdown("### simulate maximum data flow in an internet-like network.")
    
    tab1, tab2 = st.tabs(["Custom Input", "Examples"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            router_count = st.number_input("Number of Routers", min_value=2, value=6)
            source = st.number_input("Source Router", min_value=0)
            sink = st.number_input("Sink Router", min_value=0)
            
            algorithm = st.selectbox("Routing Algorithm", ["Dinic", "Edmonds-Karp"])
            
            routers_input = st.text_area("Router Coordinates", value='[[-3, 1], [-1, 2], [1, 2], [3, 1]]')
            edges_input = st.text_area("Connections (Edges)", value='[[0, 1, 10], [1, 2, 15]]')
        
        with col2:
            st.markdown("### Packet Flow Visualization")
            
            if st.button("Simulate Packet Flow"):
                try:
                    routers = json.loads(routers_input)
                    edges = json.loads(edges_input)
                    
                    with st.spinner("Generating animation..."):
                        visualizer = InternetPacketFlowVisualizer()
                        video_bytes, max_flow = visualizer.create_visualization(
                            router_count,
                            source,
                            sink,
                            routers,
                            edges,
                            algorithm
                        )
                        
                        st.video(video_bytes)
                        
                except json.JSONDecodeError:
                    st.error("Invalid JSON format in input fields.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.header("Example Packet Flows")
        
        example_tab1, example_tab2 = st.tabs(["Example 1: Dinic's Algorithm", "Example 2: Edmonds-Karp"])
        
        with example_tab1:
            st.markdown("""
            ### Example 1: Packet Flow using Dinic's Algorithm
            
            This example demonstrates packet flow through a complex network using Dinic's algorithm.
            """)
            
            if st.button("Run Example 1"):
                with st.spinner("Generating Example 1 animation..."):
                    st.video("DinicVisualization.mp4")
                    
        
        with example_tab2:
            st.markdown("""
            ### Example 2: Packet Flow using Edmonds-Karp Algorithm
            
            This example showcases a different topology optimized for the Edmonds-Karp algorithm.
            """)
            
            if st.button("Run Example 2"):
                with st.spinner("Generating Example 2 animation..."):
                    st.video("EdmondsKarpVisualization.mp4")


if __name__ == "__main__":
    main()
