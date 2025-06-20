from manim import *


class NAND2(VGroup):
    """Create a custom NAND2 shape."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.arcpolygon = ArcPolygon(
            ORIGIN,
            RIGHT,
            UP + RIGHT,
            UP,
            arc_config=[
                {"angle": 0},
                {
                    "angle": PI / 2,
                    "radius": 0.5,
                },
                {"angle": 0},
                {"angle": 0},
            ],
            color=WHITE,
        )
        self.input0 = Line(
            start=(ORIGIN + UP) / (3 / 2),
            end=(ORIGIN + UP) / (3 / 2) + LEFT * 0.25,
            color=WHITE,
        )
        self.input0_dot = Dot(
            self.input0.get_end(),
            color=WHITE,
            radius=0.05,
        )
        self.input1 = Line(
            start=(ORIGIN + UP) / 3,
            end=(ORIGIN + UP) / 3 + LEFT * 0.25,
            color=WHITE,
        )
        self.input1_dot = Dot(
            self.input1.get_end(),
            color=WHITE,
            radius=0.05,
        )
        self.add(
            self.arcpolygon, self.input0, self.input0_dot, self.input1, self.input1_dot
        )
