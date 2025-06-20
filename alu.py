from manim import *


class ClassicALUShape(Polygon):
    """Creates the classic ALU Shape."""

    def __init__(self, **kwargs):
        # Corners of the ALU shape
        alu_vertices = [
            [1, 0, 0],
            [3, 1, 0],
            [3, 3, 0],
            [1, 4, 0],
            [1, 2.5, 0],
            [1.75, 2, 0],
            [1, 1.5, 0],
            [1, 0, 0],
        ]
        super().__init__(*alu_vertices, **kwargs)

    def get_input0_start(self):
        return (self.get_vertices()[3] + self.get_vertices()[4]) / 2.0

    def get_input1_start(self):
        return (self.get_vertices()[6] + self.get_vertices()[7]) / 2.0

    def get_result_start(self):
        return (self.get_vertices()[2] + self.get_vertices()[1]) / 2.0

    def get_zero_start(self):
        return (self.get_vertices()[2] + self.get_vertices()[1]) / 2.0 + (UP * 0.75)


class ALU(VGroup):
    """Starting with classic ALU Shape, adds text and lines."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alu_shape = ClassicALUShape()
        self.title = (
            Text("ALU", font_size=36, color=WHITE)
            .move_to(self.alu_shape.get_center())
            .shift(DOWN * 0.65)
        )
        self.input0 = Line(
            start=self.alu_shape.get_input0_start(),
            end=self.alu_shape.get_input0_start() + LEFT * 0.25,
            color=WHITE,
        )
        self.input0_dot = Dot(
            self.input0.get_end(),
            color=WHITE,
            radius=0.05,
        )
        self.input0_title = Text("in0", font_size=28, color=WHITE).move_to(
            self.alu_shape.get_input0_start() + RIGHT * 0.3
        )
        self.input1 = Line(
            start=self.alu_shape.get_input1_start(),
            end=(self.alu_shape.get_input1_start() + LEFT * 0.25),
            color=WHITE,
        )
        self.input1_dot = Dot(
            self.input1.get_end(),
            color=WHITE,
            radius=0.05,
        )
        # 1.35
        self.input1_title = Text("in1", font_size=28, color=WHITE).move_to(
            self.alu_shape.get_input1_start() + RIGHT * 0.3
        )
        self.result = Line(
            start=self.alu_shape.get_result_start(),
            end=(self.alu_shape.get_result_start() + RIGHT * 0.25),
            color=WHITE,
        )
        self.result_dot = Dot(
            self.result.get_end(),
            color=WHITE,
            radius=0.05,
        )
        self.result_title = Text("result", font_size=28, color=WHITE).move_to(
            self.alu_shape.get_result_start() + (LEFT * 0.5)
        )
        self.zero = Line(
            start=self.alu_shape.get_zero_start(),
            end=self.alu_shape.get_zero_start() + RIGHT * 0.25,
            color=BLUE,
        )
        self.zero_title = Text("zero", font_size=28, color=BLUE).move_to(
            self.alu_shape.get_zero_start() + (LEFT * 0.4)
        )
        self.zero_dot = Dot(
            self.zero.get_end(),
            color=BLUE,
            radius=0.05,
        )
        self.add(
            self.alu_shape,
            self.input0,
            self.input0_dot,
            self.input1,
            self.input1_dot,
            self.result,
            self.result_dot,
            self.zero,
            self.zero_dot,
        )
        self.add(
            self.title,
            self.input0_title,
            self.input1_title,
            self.result_title,
            self.zero_title,
        )

    def get_input0_connection(self):
        return self.input0_dot.get_center()

    def get_input1_connection(self):
        return self.input1_dot.get_center()

    def get_result_connection(self):
        return self.result.get_end()

    def get_zero_connection(self):
        return self.zero_dot.get_center()
