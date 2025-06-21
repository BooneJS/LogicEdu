from math import sqrt
from manim import (
    VGroup,
    Circle,
    RIGHT,
    LEFT,
    UP,
    DOWN,
    ORIGIN,
    WHITE,
    PI,
    ArcBetweenPoints,
    ArcPolygon,
    Polygon,
)
from manim._config.logger_utils import set_file_logger
from basics import *

xor_shift_right = 0.15
or_radius = 0.75
pin_length = 0.4


class UnaryLogic(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def invert_output(self, circle_loc, pin):
        self.circle = (
            Circle(radius=xor_shift_right / 2, color=WHITE)
            .move_to(circle_loc)
            .shift(RIGHT * xor_shift_right / 2)
        )
        self.add(self.circle)
        new_start = pin.line.get_start() + RIGHT * xor_shift_right
        pin.line.put_start_and_end_on(new_start, pin.line.get_end())

    def get_input0_connection(self):
        """Return the input0 dot center."""
        pass

    def get_output_connection(self):
        """Return the output dot center."""
        pass


class BinaryLogic(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bubble_radius = 1  # 1 for *OR, 0.5 for *AND

    def invert_pin(self, pin):
        pin.add_invert()

    def ex_inputs(self, input0_pin, input1_pin, angle):
        # TODO: y_intercept isn't always available
        arc = ArcBetweenPoints(
            start=UP + LEFT * self.y_intercept + LEFT * xor_shift_right,
            end=LEFT * self.y_intercept + LEFT * xor_shift_right,
            angle=angle,
        )
        self.add(arc)
        new_start = input0_pin.line.get_start() + LEFT * xor_shift_right
        input0_pin.line.put_start_and_end_on(new_start, input0_pin.line.get_end())
        new_start = input1_pin.line.get_start() + LEFT * xor_shift_right
        input1_pin.line.put_start_and_end_on(new_start, input1_pin.line.get_end())

    def get_input0_connection(self):
        """Return the input0 dot center."""
        pass

    def get_input1_connection(self):
        """Return the input1 dot center."""
        pass

    def get_output_connection(self):
        """Return the output dot center."""
        pass


class AND2(BinaryLogic):
    """Create a custom AND2 shape."""

    def __init__(self, **kwargs):
        self.num_inputs = kwargs.pop("num_inputs", 2)
        super().__init__(**kwargs)
        self.arcpolygon = ArcPolygon(
            ORIGIN,
            RIGHT * 0.5,
            UP + RIGHT * 0.5,
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
        self.input0_pin = Pin(pin_side=PinSide.LEFT, color=WHITE).shift(UP / (4 / 3))
        self.input1_pin = Pin(pin_side=PinSide.LEFT, color=WHITE).shift(UP / 4)
        self.output_pin = Pin(pin_side=PinSide.RIGHT, color=WHITE).shift(UP / 2 + RIGHT)
        self.add(
            self.arcpolygon,
            self.input0_pin,
            self.input1_pin,
            self.output_pin,
        )

    def get_input0_connection(self):
        return self.input0_pin.get_connection()

    def get_input1_connection(self):
        return self.input1_pin.get_connection()

    def get_output_connection(self):
        return self.output_pin.get_connection()


class NAND2(AND2):
    """Create a custom NAND2 shape from AND2."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invert_pin(self.output_pin)


class OR2(BinaryLogic):
    """Create a custom OR2 shape."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(f"name of class: {type(self).__name__}")
        self.rear_angle = -PI / 2
        self.bubble_angle = PI / 4
        self.y_intercept = sqrt(1 - ((1 / 4) ** 2)) - sqrt(1 - ((1 / 2) ** 2)) + 0.03
        edge_length = 0.25 + self.y_intercept
        self.arcpolygon = ArcPolygon(
            UP + LEFT * self.y_intercept,
            ORIGIN + LEFT * self.y_intercept,
            RIGHT * edge_length,
            UP * 0.5 + RIGHT,
            UP + RIGHT * edge_length,
            arc_config=[
                {
                    "angle": self.rear_angle,
                },
                {"angle": 0},
                {
                    "angle": self.bubble_angle,
                },
                {
                    "angle": self.bubble_angle,
                },
                {"angle": 0},
            ],
            color=WHITE,
        )

        self.input0_pin = Pin(pin_side=PinSide.LEFT, color=WHITE).shift(UP / (4 / 3))
        self.input1_pin = Pin(pin_side=PinSide.LEFT, color=WHITE).shift(UP / 4)
        self.output_pin = Pin(pin_side=PinSide.RIGHT, color=WHITE).shift(UP / 2 + RIGHT)

        self.add(
            self.arcpolygon,
            self.input0_pin,
            self.input1_pin,
            self.output_pin,
        )

    def get_input0_connection(self):
        return self.input0_pin.get_connection()

    def get_input1_connection(self):
        return self.input1_pin.get_connection()

    def get_output_connection(self):
        return self.output_pin.get_connection()


class NOR2(OR2):
    """Create a custom NOR2 shape from OR2."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invert_pin(self.output_pin)


class XOR2(OR2):
    """Create a custom XOR2 shape from OR2."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ex_inputs(self.input0_pin, self.input1_pin, self.rear_angle)


class XNOR2(XOR2):
    """Create a custom XNOR shape from XOR2."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invert_pin(self.output_pin)


class BUF(UnaryLogic):
    """Create a custom Inv shape."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.triangle = Polygon(ORIGIN, RIGHT + UP * 0.5, UP, color=WHITE)
        self.input0_pin = Pin(pin_side=PinSide.LEFT, color=WHITE).shift(UP / 2)
        self.output_pin = Pin(pin_side=PinSide.RIGHT, color=WHITE).shift(UP / 2 + RIGHT)
        self.add(
            self.triangle,
            self.input0_pin,
            self.output_pin,
        )

    def invert_pin(self, pin):
        pin.add_invert()

    def get_input0_connection(self):
        return self.input0_pin.get_connection()

    def get_output_connection(self):
        return self.output_pin.get_connection()


class INV(BUF):
    """Create a custom INV shape from BUF."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invert_pin(self.output_pin)


all_gates = [
    AND2(),
    NAND2(),
    OR2(),
    NOR2(),
    XOR2(),
    XNOR2(),
    BUF(),
    INV(),
]
