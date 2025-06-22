from manim import (
    VGroup,
    Line,
    Dot,
    Scene,
    FadeIn,
    WHITE,
    LEFT,
    UP,
    DOWN,
    RIGHT,
    Create,
    ImageMobject,
)

from blocks import *
from logic_gates import *


class ConnectorLine(VGroup):
    def __init__(self, start_pin, end_pin, midpoint=None, **kwargs):
        super().__init__(**kwargs)
        if midpoint is None:
            midpoint = (start_pin.get_connection() + end_pin.get_connection()) / 2
        self.line = Line(
            start_pin.get_connection(), end_pin.get_connection(), color=WHITE
        )
        self.dot = Dot(midpoint, color=WHITE, radius=0.05)
        self.add(self.line, self.dot)


class DrawAnALU(Scene):
    def construct(self):
        # Define the vertices of the custom polygon
        # Create the polygon using the defined vertices
        alu = ALUZ()
        alu.scale(0.5).move_to(LEFT * 3 + DOWN)

        mux = Mux()
        mux.move_to(LEFT * 5 + DOWN * 1.5)
        self.play(Create(mux))

        mux = Mux(num_inputs=4)
        mux.move_to(LEFT * 5 + UP * 1.50)
        self.play(Create(mux))

        # Add the shape to the scene and play a creation animation
        self.play(Create(alu))

        gates_vg = VGroup()

        base_loc = UP * 4.2
        scale = 0.5
        for i, gate in enumerate(all_gates):
            gate.scale(scale)
            gate.move_to(base_loc + DOWN * (i * (scale + 0.1)))
            gates_vg.add(gate)

        self.play(FadeIn(gates_vg.move_to(base_loc + DOWN * (i * 0.6))))

        # connector_line = ConnectorLine(
        #     alu.get_output_connection(), gates_vg[0].get_input_connection()
        # )
        self.wait(1)
