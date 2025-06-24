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

from basics import ConnectorLine, GRID, grid_round
from blocks import *
from logic_gates import *


class DrawAnALU(Scene):
    def construct(self):
        alu = ALUZ()
        alu.scale(0.5).move_to(LEFT * 3 + DOWN)

        dff = DFF(variant=DFFVariant.DFF).scale(0.75)
        dff.move_to(LEFT * 5 + UP * 3)
        self.play(FadeIn(dff))

        dffr = DFF(variant=DFFVariant.DFF_R, bit_width=4).scale(0.75)
        dffr.move_to(LEFT * 5 + UP * 1)
        self.play(FadeIn(dffr))

        dffsr = DFF(variant=DFFVariant.DFF_SR).scale(0.75)
        dffsr.move_to(LEFT * 5 + DOWN * 1)
        self.play(FadeIn(dffsr))

        # mux = Mux()
        # mux.move_to(LEFT * 5 + DOWN * 1.5)
        # self.play(Create(mux))

        # mux = Mux(num_inputs=5)
        # mux.move_to(LEFT * 5 + UP * 1.50).scale(0.75)
        # self.play(Create(mux))

        # Add the shape to the scene and play a creation animation
        self.play(Create(alu))

        gates_vg = VGroup()

        base_loc = UP * 4.2
        scale = 0.75
        for i, gate in enumerate(all_gates):
            gate.scale(scale)
            gate.move_to(base_loc + DOWN * (i * (scale + 0.1)))
            gates_vg.add(gate)

        self.play(FadeIn(gates_vg.move_to(base_loc + DOWN * (i * 0.6))))

        wires = VGroup()
        wires.add(
            ConnectorLine(
                alu.get_result_connection(),
                gates_vg[0].get_input1_connection(),
                manhatten=True,
                x_axis_shift=GRID,
            ),
        )
        wires.add(
            ConnectorLine(
                alu.get_zero_connection(),
                gates_vg[0].get_input0_connection(),
                manhatten=True,
            ),
        )

        wires.add(
            ConnectorLine(
                dff.get_q_connection(),
                gates_vg[1].get_input0_connection(),
                manhatten=True,
            ),
        )

        self.play(Create(wires))

        self.wait(1)
