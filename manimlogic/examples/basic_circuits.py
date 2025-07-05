"""
Basic circuit examples using ManimLogic.

This example demonstrates how to create simple digital logic circuits
using ManimLogic components.
"""

from manim import Scene, Create, FadeIn, VGroup
from manimlogic import (
    AND2,
    OR2,
    INV,
    ConnectorLine,
    create_grid,
    dim_all_objects,
    undim_all_objects,
)


class BasicLogicGates(Scene):
    """Example showing basic logic gates."""

    def construct(self):
        # Create a grid background
        grid = create_grid()
        self.play(FadeIn(grid))

        # Create logic gates
        and_gate = AND2()
        or_gate = OR2()
        not_gate = INV()

        # Position gates
        and_gate.move_to((-3, 1, 0))
        or_gate.move_to((0, 1, 0))
        not_gate.move_to((3, 1, 0))

        # Animate gates appearing
        gates = VGroup(and_gate, or_gate, not_gate)
        self.play(Create(gates))
        self.wait(1)

        # Show dimming functionality
        dim_all_objects(self, gates)
        undim_all_objects(self, gates)


class SimpleCircuit(Scene):
    """Example showing a simple circuit with connections."""

    def construct(self):
        # Create grid
        grid = create_grid()
        self.play(FadeIn(grid))

        # Create components
        and_gate = AND2().move_to((-2, 0, 0))
        or_gate = OR2().move_to((2, 0, 0))

        # Create components
        self.play(Create(and_gate), Create(or_gate))
        self.wait(1)

        # Connect them
        wire = ConnectorLine(
            start_pin=and_gate.get_output_connection(),
            end_pin=or_gate.get_input0_connection(),
            manhatten=True,
        )
        self.play(Create(wire))
        self.wait(2)
