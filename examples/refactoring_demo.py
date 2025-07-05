#!/usr/bin/env python3
"""
Demo script showing the refactored components with get_input_by_index and get_output_by_index methods.
"""

from manim import Scene, Create, FadeIn, VGroup, LEFT, RIGHT, UP, DOWN
from logicedu.components.blocks import ALUZ, Adder, DFF, DFFVariant
from logicedu.components.logic_gates import AND2, OR2, BUF
from logicedu.core.basics import ConnectorLine


class RefactoringDemo(Scene):
    """Demonstrate the refactored components with new pin access methods."""

    def construct(self):
        # Create components
        alu = ALUZ().shift(LEFT * 4)
        adder = Adder().shift(RIGHT * 4)
        dff = DFF().shift(UP * 2)
        and_gate = AND2().shift(DOWN * 2)
        buf = BUF().shift(RIGHT * 2 + UP * 2)

        # Show components
        self.play(
            Create(alu), Create(adder), Create(dff), Create(and_gate), Create(buf)
        )
        self.wait(1)

        # Demonstrate get_input_by_index and get_output_by_index
        # ALU: input0 -> AND gate input0
        alu_input0 = alu.get_input_by_index(0)
        and_input0 = and_gate.get_input_by_index(0)
        wire1 = ConnectorLine(start_pin=alu_input0, end_pin=and_input0, manhatten=True)

        # ALU: result -> Adder input0
        alu_result = alu.get_output_by_index(0)
        adder_input0 = adder.get_input_by_index(0)
        wire2 = ConnectorLine(
            start_pin=alu_result, end_pin=adder_input0, manhatten=True
        )

        # DFF: Q -> BUF input
        dff_q = dff.get_output_by_index(0)
        buf_input = buf.get_input_by_index(0)
        wire3 = ConnectorLine(start_pin=dff_q, end_pin=buf_input, manhatten=True)

        # Show connections
        self.play(Create(wire1), Create(wire2), Create(wire3))
        self.wait(2)

        # Demonstrate DFF variants
        dff_r = DFF(variant=DFFVariant.DFF_R).shift(LEFT * 2 + DOWN * 2)
        dff_sr = DFF(variant=DFFVariant.DFF_SR).shift(RIGHT * 2 + DOWN * 2)

        self.play(Create(dff_r), Create(dff_sr))
        self.wait(1)

        # Show that DFF variants have different numbers of inputs
        print(
            f"DFF basic has {len([dff.get_input_by_index(i) for i in range(2)])} inputs"
        )
        print(
            f"DFF_R has {len([dff_r.get_input_by_index(i) for i in range(3)])} inputs"
        )
        print(
            f"DFF_SR has {len([dff_sr.get_input_by_index(i) for i in range(4)])} inputs"
        )

        self.wait(2)


if __name__ == "__main__":
    # This script can be run with: manim -pql examples/refactoring_demo.py RefactoringDemo
    pass
