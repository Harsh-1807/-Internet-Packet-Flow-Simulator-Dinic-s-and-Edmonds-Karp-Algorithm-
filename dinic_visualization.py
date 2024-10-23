from manim import *
from collections import deque

class DinicVisualization(Scene):
    def construct(self):
        VERTEX_COLOR = "#6495ED"
        EDGE_COLOR = "#808080"
        FLOW_COLOR = "#FF6B6B"
        PATH_COLOR = "#98FB98"
        BFS_COLOR = "#FFD700"
        
        title = Text("Dinic's Maximum Flow Algorithm", 
                    font="Arial",
                    color="#FFFFFF").scale(0.8).to_edge(UP)

        complexity = VGroup(
            Text("Time Complexity Analysis:", font="Arial", color="#FFD700").scale(0.4),
            Text("• O(V²E) for general graphs", font="Arial").scale(0.4),
            Text("• O(E√V) for unit capacity", font="Arial").scale(0.4),
            Text("• O(EV) for bipartite graphs", font="Arial").scale(0.4)
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.2)
        complexity.to_edge(RIGHT).shift(DOWN * 1.5)

        initial_pseudo = Code(
            code="""\
            function dinic(graph, source, sink):
                max_flow = 0
                while level_graph = bfs(residual):
                    while path = dfs(level_graph):
                        flow = min(path.capacities)
                        max_flow += flow
                        update_residual(path, flow)
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
            def dinic(G, s, t):
                flow = 0
                while True:
                    level = [-1] * len(G)
                    level[s] = 0
                    q = deque([s])
                    
                    while q:
                        u = q.popleft()
                        for v, cap in G[u].items():
                            if cap > 0 and level[v] < 0:
                                level[v] = level[u] + 1
                                q.append(v)
                    
                    if level[t] < 0: break
                    flow += blocking_flow(G, level, s, t)
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

        status_text = Text("Creating Level Graph", 
                          font="Arial",
                          color=BFS_COLOR).scale(0.6).to_edge(DOWN)
        self.play(Write(status_text))

        level_order = [
            ['s'],
            ['b', 'c'],
            ['d', 'e'],
            ['t']
        ]

        for level in level_order:
            self.play(
                *[vertex_objects[v].animate.set_color(BFS_COLOR) for v in level],
                run_time=0.8
            )
            self.wait(0.3)

        augmenting_paths = [
            [('s', 'b'), ('b', 'd'), ('d', 't')],
            [('s', 'c'), ('c', 'e'), ('e', 't')],
            [('s', 'b'), ('b', 'e'), ('e', 't')]
        ]

        flow_updates = {
            0: {'s-b': 4, 'b-d': 4, 'd-t': 4},
            1: {'s-c': 9, 'c-e': 9, 'e-t': 9},
            2: {'s-b': 6, 'b-e': 6, 'e-t': 10}
        }

        self.play(
            Transform(
                status_text,
                Text("Finding Augmenting Paths", 
                     font="Arial",
                     color=PATH_COLOR).scale(0.6).to_edge(DOWN)
            )
        )

        for path_idx, path in enumerate(augmenting_paths):
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
            self.play(path_edges.animate.set_color(EDGE_COLOR))

        final_text = Text("Maximum Flow: 19", 
                         font="Arial",
                         color="#98FB98").scale(0.7).to_edge(DOWN)
        
        self.play(Transform(status_text, final_text))

        self.play(
            *[vertex_objects[v].animate.set_color(VERTEX_COLOR) for v in vertices.keys()],
            run_time=1
        )

        self.wait(2)

        layered_text = VGroup(
            Text("Layer 1: BFS creates level graph", font="Arial").scale(0.3),
            Text("Layer 2: DFS finds blocking flow", font="Arial").scale(0.3),
            Text("Layer 3: Update residual graph", font="Arial").scale(0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        layered_text.to_edge(RIGHT).shift(UP)

        self.play(Write(layered_text))

        self.wait(3)

        self.play(FadeOut(layered_text, shift=UP), 
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
