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
from basics import *
from typing import List
import enum


class LogicType(enum.Enum):
    AND = "AND"
    NAND = "NAND"
    OR = "OR"
    NOR = "NOR"
    XOR = "XOR"
    XNOR = "XNOR"
    BUF = "BUF"
    INV = "INV"


class ShapeFactory:

    @staticmethod
    def create_shape(logic_type: LogicType, **kwargs):
        y_intercept = kwargs.pop(
            "y_intercept", sqrt(1 - ((1 / 4) ** 2)) - sqrt(1 - ((1 / 2) ** 2)) + 0.03
        )
        edge_length = kwargs.pop("edge_length", 0.25 + y_intercept)
        rear_angle = kwargs.pop("rear_angle", -PI / 2)
        bubble_angle = kwargs.pop("bubble_angle", PI / 4)

        match logic_type:
            case LogicType.AND | LogicType.NAND:
                return ArcPolygon(
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
            case LogicType.OR | LogicType.NOR | LogicType.XOR | LogicType.XNOR:
                return ArcPolygon(
                    UP + LEFT * y_intercept,
                    ORIGIN + LEFT * y_intercept,
                    RIGHT * edge_length,
                    UP * 0.5 + RIGHT,
                    UP + RIGHT * edge_length,
                    arc_config=[
                        {
                            "angle": rear_angle,
                        },
                        {"angle": 0},
                        {
                            "angle": bubble_angle,
                        },
                        {
                            "angle": bubble_angle,
                        },
                        {"angle": 0},
                    ],
                    color=WHITE,
                )
            case LogicType.BUF | LogicType.INV:
                return Polygon(ORIGIN, RIGHT + UP * 0.5, UP, color=WHITE)


class UnaryLogic(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.xor_shift_right = kwargs.pop("xor_shift_right", 0.15)
        self.or_radius = kwargs.pop("or_radius", 0.75)
        self.pin_length = kwargs.pop("pin_length", 0.4)
        self.inputs: List[Pin] = []
        self.outputs: List[Pin] = []
        self.inputs.append(Pin(pin_side=PinSide.LEFT, color=WHITE).shift(UP / 2))
        self.outputs.append(
            Pin(pin_side=PinSide.RIGHT, color=WHITE).shift(UP / 2 + RIGHT)
        )
        self.add(*self.inputs)
        self.add(*self.outputs)
        self.shape = ShapeFactory.create_shape(LogicType.INV)
        self.add(self.shape)

    def invert_output(self):
        self.outputs[0].add_invert()

    def get_input_connection(self, index: int):
        return self.inputs[index].get_connection()

    def get_output_connection(self, index: int = 0):
        return self.outputs[index].get_connection()

    def get_input_count(self):
        return len(self.inputs)

    def get_output_count(self):
        return len(self.outputs)


class BinaryLogic(VGroup):
    def __init__(self, logic_type: LogicType, **kwargs):
        self.num_inputs = kwargs.pop("num_inputs", 2)
        super().__init__(**kwargs)
        self.logic_type = logic_type
        self.rear_angle = kwargs.pop(
            "rear_angle", -PI / 2
        )  # OR symbol with concave back
        self.bubble_angle = kwargs.pop(
            "bubble_angle", PI / 4
        )  # OR symbol with acute angled nose
        self.y_intercept = sqrt(1 - ((1 / 4) ** 2)) - sqrt(1 - ((1 / 2) ** 2)) + 0.03
        self.xor_shift_right = kwargs.pop("xor_shift_right", 0.15)
        self.or_radius = kwargs.pop("or_radius", 0.75)
        self.pin_length = kwargs.pop("pin_length", 0.4)
        self.inputs: List[Pin] = []
        self.outputs: List[Pin] = []
        self.inputs.append(Pin(pin_side=PinSide.LEFT, color=WHITE).shift(UP / (4 / 3)))
        self.inputs.append(Pin(pin_side=PinSide.LEFT, color=WHITE).shift(UP / 4))
        self.outputs.append(
            Pin(pin_side=PinSide.RIGHT, color=WHITE).shift(UP / 2 + RIGHT)
        )
        self.add(*self.inputs)
        self.add(*self.outputs)
        self.shape = ShapeFactory.create_shape(self.logic_type)
        self.add(self.shape)

        # Handle Inverting output and Exclusive OR Inputs
        match self.logic_type:
            case LogicType.NAND | LogicType.NOR | LogicType.XNOR:
                self.invert_output()
            case LogicType.XOR | LogicType.XNOR:
                self.ex_inputs()

    def invert_output(self):
        self.outputs[0].add_invert()

    def ex_inputs(self):
        ex = ArcBetweenPoints(
            start=UP + LEFT * self.y_intercept + LEFT * self.xor_shift_right,
            end=LEFT * self.y_intercept + LEFT * self.xor_shift_right,
            angle=self.rear_angle,
        )
        self.add(ex)
        new_start = self.inputs[0].line.get_start() + LEFT * self.xor_shift_right
        self.inputs[0].line.put_start_and_end_on(
            new_start, self.inputs[0].line.get_end()
        )
        new_start = self.inputs[1].line.get_start() + LEFT * self.xor_shift_right
        self.inputs[1].line.put_start_and_end_on(
            new_start, self.inputs[1].line.get_end()
        )

    def get_input0_connection(self):
        """Return the input0 dot center."""
        return self.inputs[0].get_connection()

    def get_input1_connection(self):
        """Return the input1 dot center."""
        return self.inputs[0].get_connection()

    def get_output_connection(self):
        """Return the output dot center."""
        return self.outputs[0].get_connection()

    def get_input_count(self):
        return len(self.inputs)

    def get_output_count(self):
        return len(self.outputs)


class AND2(BinaryLogic):
    """Create a custom AND2 shape."""

    def __init__(self, **kwargs):
        super().__init__(LogicType.AND, **kwargs)


class NAND2(AND2):
    """Create a custom NAND2 shape from AND2."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.invert_output()


class OR2(BinaryLogic):
    """Create a custom OR2 shape."""

    def __init__(self, **kwargs):
        self.num_inputs = kwargs.pop("num_inputs", 2)
        super().__init__(LogicType.OR, **kwargs)


class NOR2(OR2):
    """Create a custom NOR2 shape from OR2."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invert_output()


class XOR2(OR2):
    """Create a custom XOR2 shape from OR2."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ex_inputs()


class XNOR2(XOR2):
    """Create a custom XNOR shape from XOR2."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invert_output()


class BUF(UnaryLogic):
    """Create a custom Inv shape."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class INV(BUF):
    """Create a custom INV shape from BUF."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invert_output()


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
