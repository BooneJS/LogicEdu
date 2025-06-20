from manim import *
from alu import *
from logic_gates import *


class DrawAnALU(Scene):
    def construct(self):
        # Define the vertices of the custom polygon
        # Create the polygon using the defined vertices
        alu = ALU(color=BLUE)
        alu.move_to((-1, 0, 0))

        # Add the shape to the scene and play a creation animation
        self.play(Write(alu))
        self.play(alu.animate.scale(1.5))
        self.play(alu.animate.scale(1 / 1.5))

        nand2 = NAND2()
        self.play(Create(nand2.shift(DOWN * 2)))
        self.wait(1)
