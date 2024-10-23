from manim import *
from collections import deque

class EdmondsKarpVisualization(Scene):
    def construct(self):
        VERTEX_COLOR = "#6495ED"
        EDGE_COLOR = "#808080"
        FLOW_COLOR = "#FF6B6B"
        PATH_COLOR = "#98FB98"
        BFS_COLOR = "#FFD700"
        
        title = Text("Edmonds-Karp Maximum Flow Algorithm", 
                    font="Arial",
                    color="#FFFFFF").scale(0.8).to_edge(UP)

        complexity = VGroup(
            Text("Time Complexity Analysis:", font="Arial", color="#FFD700").scale(0.4),
            Text("• O(VE²) worst case", font="Arial").scale(0.4),
            Text("• O(V + E) per BFS", font="Arial").scale(0.4),
            Text("• At most O(VE) augmentations", font="Arial").scale(0.4)
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.2)
        complexity.to_edge(RIGHT).shift(DOWN * 1.5)

        initial_pseudo = Code(
            code="""\
            function edmonds_karp(graph, source, sink):
                max_flow = 0
                while path = bfs(residual):
                    path_flow = min(path.capacities)
                    max_flow += path_flow
                    update_residual(path, path_flow)
                return max_flow
            """,
            language="java",
            font="Monospace",
            style="monokai",
            background="window",
            font_size=24
        ).scale(0.5)
        initial_pseudo.move_to(ORIGIN)

        detailed_pseudo = Code(
            code="""\
            def edmonds_karp(G, s, t):
                flow = 0
                parent = [-1] * len(G)
                
                while True:
                    # BFS to find augmenting path
                    q = deque([s])
                    parent = [-1] * len(G)
                    parent[s] = s
                    
                    while q and parent[t] == -1:
                        u = q.popleft()
                        for v, cap in G[u].items():
                            if cap > 0 and parent[v] == -1:
                                parent[v] = u
                                q.append(v)
                    
                    if parent[t] == -1:
                        break
                        
                    # Find minimum residual capacity
                    path_flow = float('inf')
                    v = t
                    while v != s:
                        u = parent[v]
                        path_flow = min(path_flow, G[u][v])
                        v = u
                    
                    # Update residual graph
                    v = t
                    while v != s:
                        u = parent[v]
                        G[u][v] -= path_flow
                        G[v][u] += path_flow
                        v = u
                    
                    flow += path_flow
                
                return flow
            """,
            language="python",
            font="Monospace",
            style="monokai",
            background="window",
            font_size=20
        ).scale(0.6)
        detailed_pseudo.to_edge(LEFT)

        vertices = {
            's': (-2, 1, 0),
            'b': (0, 2, 0),
            'c': (0, 0, 0),
            'd': (2, 2, 0),
            'e': (2, 0, 0),
            't': (4, 1, 0)
        }
        
        edges = [
            ('s', 'b', 10),
            ('s', 'c', 10),
            ('b', 'c', 2),
            ('b', 'd', 4),
            ('b', 'e', 8),
            ('c', 'e', 9),
            ('d', 't', 10),
            ('e', 't', 10),
            ('d', 'e', 6)
        ]

        vertex_objects = {}
        vertex_labels = {}
        for v, pos in vertices.items():
            vertex_objects[v] = Circle(radius=0.25, 
                                     color=VERTEX_COLOR, 
                                     fill_opacity=0.3).move_to(pos)
            vertex_labels[v] = Text(v, 
                                  font="Arial",
                                  color=WHITE).scale(0.6).next_to(vertex_objects[v], DOWN, buff=0.1)

        edge_objects = {}
        capacity_labels = {}
        flow_labels = {}
        
        for u, v, cap in edges:
            start = vertex_objects[u].get_center()
            end = vertex_objects[v].get_center()
            
            edge_objects[(u, v)] = Arrow(start, end, 
                                       color=EDGE_COLOR,
                                       buff=0.3,
                                       max_tip_length_to_length_ratio=0.1)
            
            mid_point = edge_objects[(u, v)].get_center()
            
            capacity_labels[(u, v)] = Text(str(cap), 
                                         font="Arial",
                                         color=WHITE).scale(0.4).next_to(mid_point, UP, buff=0.1)
            
            flow_labels[(u, v)] = Text("0", 
                                     font="Arial",
                                     color=FLOW_COLOR).scale(0.4).next_to(capacity_labels[(u, v)], LEFT, buff=0.1)

        self.play(Write(title))
        self.play(Write(initial_pseudo))
        
        self.play(
            *[FadeIn(v, shift=DOWN*0.5) for v in vertex_objects.values()],
            *[FadeIn(l, shift=DOWN*0.5) for l in vertex_labels.values()],
            run_time=1.5
        )
        
        self.play(
            *[GrowArrow(e) for e in edge_objects.values()],
            *[FadeIn(l, shift=UP*0.3) for l in capacity_labels.values()],
            *[FadeIn(l, shift=UP*0.3) for l in flow_labels.values()],
            run_time=1.5
        )

        self.play(
            Transform(initial_pseudo, detailed_pseudo),
            Write(complexity),
            run_time=1.5
        )

        status_text = Text("Finding Augmenting Path via BFS", 
                          font="Arial",
                          color=BFS_COLOR).scale(0.6).to_edge(DOWN)
        self.play(Write(status_text))

        # BFS paths for Edmonds-Karp
        bfs_paths = [
            [('s', 'b'), ('b', 'd'), ('d', 't')],
            [('s', 'c'), ('c', 'e'), ('e', 't')],
            [('s', 'b'), ('b', 'e'), ('e', 't')],
            [('s', 'c'), ('c', 'e'), ('e', 't')]
        ]

        flow_updates = {
            0: {'s-b': 4, 'b-d': 4, 'd-t': 4},
            1: {'s-c': 8, 'c-e': 8, 'e-t': 8},
            2: {'s-b': 6, 'b-e': 6, 'e-t': 10},
            3: {'s-c': 10, 'c-e': 9, 'e-t': 10}
        }

        for path_idx, path in enumerate(bfs_paths):
            # Highlight BFS exploration
            explored_vertices = []
            for u, _ in path:
                if u not in explored_vertices:
                    self.play(
                        vertex_objects[u].animate.set_color(BFS_COLOR),
                        run_time=0.5
                    )
                    explored_vertices.append(u)
            
            path_edges = VGroup(*[edge_objects[e] for e in path])
            
            self.play(
                path_edges.animate.set_color(PATH_COLOR),
                Transform(
                    status_text,
                    Text(f"Augmenting Path {path_idx + 1}", 
                         font="Arial",
                         color=PATH_COLOR).scale(0.6).to_edge(DOWN)
                ),
                run_time=1
            )

            # Update flows
            for u, v in path:
                edge_key = f"{u}-{v}"
                if edge_key in flow_updates[path_idx]:
                    new_flow = flow_updates[path_idx][edge_key]
                    self.play(
                        Transform(
                            flow_labels[(u,v)],
                            Text(str(new_flow), 
                                 font="Arial",
                                 color=FLOW_COLOR).scale(0.4).next_to(capacity_labels[(u,v)], LEFT)
                        ),
                        run_time=0.5
                    )

            self.wait(0.5)
            
            # Reset colors
            self.play(
                path_edges.animate.set_color(EDGE_COLOR),
                *[vertex_objects[v].animate.set_color(VERTEX_COLOR) for v in explored_vertices],
                run_time=0.8
            )

        final_text = Text("Maximum Flow: 19", 
                         font="Arial",
                         color="#98FB98").scale(0.7).to_edge(DOWN)
        
        self.play(Transform(status_text, final_text))

        # Algorithm key points
        key_points = VGroup(
            Text("Algorithm Features:", font="Arial").scale(0.3),
            Text("• Uses BFS to find shortest augmenting paths", font="Arial").scale(0.3),
            Text("• Guarantees minimum number of edges in path", font="Arial").scale(0.3),
            Text("• Better practical performance than Ford-Fulkerson", font="Arial").scale(0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        key_points.to_edge(RIGHT).shift(UP)

        self.play(Write(key_points))
        self.wait(3)

        # Final cleanup
        self.play(
            FadeOut(key_points, shift=UP),
            FadeOut(final_text, shift=UP),
            FadeOut(status_text, shift=UP),
            FadeOut(complexity, shift=UP),
            FadeOut(initial_pseudo, shift=UP),
            FadeOut(detailed_pseudo, shift=UP),
            *[FadeOut(v) for v in vertex_objects.values()],
            *[FadeOut(l) for l in vertex_labels.values()],
            *[FadeOut(e) for e in edge_objects.values()],
            *[FadeOut(l) for l in capacity_labels.values()],
            *[FadeOut(l) for l in flow_labels.values()],
            run_time=1
        )

        self.play(FadeOut(title, shift=UP))

if __name__ == "__main__":
    scene = EdmondsKarpVisualization()
    scene.render()