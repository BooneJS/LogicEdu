from manim import VGroup, Line, Dot, Scene, FadeIn, WHITE, LEFT, UP, DOWN, RIGHT
from blocks import *
from logic_gates import *


class ConnectorLine(VGroup):
    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        midpoint = (start + end) / 2
        self.line = Line(start, end, color=WHITE)
        self.dot = Dot(midpoint, color=WHITE, radius=0.05)
        self.add(self.line, self.dot)


class DrawAnALU(Scene):
    def construct(self):
        # Define the vertices of the custom polygon
        # Create the polygon using the defined vertices
        alu = ALUZ()
        alu_loc = LEFT * 5 + UP * 1.5

        # Add the shape to the scene and play a creation animation
        self.play(FadeIn(alu.outline_vg.move_to(alu_loc)))
        self.play(FadeIn(alu.title_vg.move_to(alu_loc)))

        gates_vg = VGroup()

        base_loc = UP * 4.3
        scale = 0.8
        for i, gate in enumerate(all_gates):
            gate.scale(scale)
            gate.move_to(base_loc + DOWN * (i * (scale + 0.1)))
            gates_vg.add(gate)

        self.play(FadeIn(gates_vg.move_to(base_loc + DOWN * (i * 0.6))))

        self.wait(1)
