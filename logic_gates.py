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
    DEGREES,
)
from manim.typing import Point3DLike
from basics import Pin, PinSide
from typing import List
import enum
import numpy as np


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
    """Creates shapes for logic gates per MIL-STD-806B."""

    @staticmethod
    def or_radius() -> float:
        return 0.8

    @staticmethod
    def gate_dim() -> float:
        return 0.8

    @staticmethod
    def arc2d_radius_to_angle(
        radius: float, chord_start: Point3DLike, chord_end: Point3DLike
    ) -> float:
        chord_len = np.linalg.norm(np.array(chord_start) - np.array(chord_end))
        return 2 * np.arcsin(chord_len / (2 * radius))

    @staticmethod
    def or_edge_len() -> float:
        return 0.3

    @staticmethod
    def buf_side_len() -> float:
        return 0.7

    @staticmethod
    def and_radius() -> float:
        return ShapeFactory.gate_dim() / 2

    @staticmethod
    def and_edge_len() -> float:
        return 0.6

    @staticmethod
    def edge_to_pin() -> float:
        return 0.15

    @staticmethod
    def between_pins(pin_count: int = 2) -> float:
        return 0.25 if pin_count > 2 else 0.5

    @staticmethod
    def ex_offset() -> float:
        return 0.15

    @staticmethod
    def pin_length() -> float:
        return 0.4

    @staticmethod
    def solve_for_y_intercept(radius: float, y: float) -> float:
        return np.sqrt(radius**2 - y**2)

    @staticmethod
    def create_shape(logic_type: LogicType, **kwargs) -> ArcPolygon:
        match logic_type:
            case LogicType.AND | LogicType.NAND:
                lower_arc_start = RIGHT * ShapeFactory.and_edge_len()
                midpoint = (
                    lower_arc_start
                    + RIGHT * ShapeFactory.and_radius()
                    + UP * ShapeFactory.and_radius()
                )
                upper_arc_end = lower_arc_start + LOGIC_UP
                lower_angle = ShapeFactory.arc2d_radius_to_angle(
                    ShapeFactory.and_radius(), lower_arc_start, midpoint
                )
                upper_angle = ShapeFactory.arc2d_radius_to_angle(
                    ShapeFactory.and_radius(), midpoint, upper_arc_end
                )
                return ArcPolygon(
                    ORIGIN,
                    lower_arc_start,
                    midpoint,
                    upper_arc_end,
                    LOGIC_UP,
                    arc_config=[
                        {"angle": 0},
                        {"angle": lower_angle},
                        {"angle": upper_angle},
                        {"angle": 0},
                        {"angle": 0},
                    ],
                    color=WHITE,
                    **kwargs,
                )
            case LogicType.OR | LogicType.NOR | LogicType.XOR | LogicType.XNOR:

                # OR's rear arc has 0 offset at midpoint, but 'left_shift' at the start/end.
                left_shift = LEFT * (
                    0.8
                    - ShapeFactory.solve_for_y_intercept(
                        ShapeFactory.or_radius(), ShapeFactory.gate_dim() / 2
                    )
                )
                return ArcPolygon(
                    left_shift,
                    RIGHT * ShapeFactory.or_edge_len(),
                    LOGIC_UP / 2 + RIGHT,
                    LOGIC_UP + RIGHT * ShapeFactory.or_edge_len(),
                    LOGIC_UP + left_shift,
                    arc_config=[
                        {"angle": 0},
                        {"radius": ShapeFactory.or_radius()},
                        {"radius": ShapeFactory.or_radius()},
                        {"angle": 0},
                        {"radius": -ShapeFactory.or_radius()},
                    ],
                    color=WHITE,
                    **kwargs,
                )
            case LogicType.BUF | LogicType.INV:
                buf_up = UP * ShapeFactory.buf_side_len() / 2
                buf_right = RIGHT * sqrt(
                    ShapeFactory.buf_side_len() ** 2
                    - (ShapeFactory.buf_side_len() / 2) ** 2
                )
                return ArcPolygon(
                    ORIGIN,
                    buf_up + buf_right,
                    UP * ShapeFactory.buf_side_len(),
                    arc_config=[
                        {"angle": 0},
                        {"angle": 0},
                        {"angle": 0},
                    ],
                    color=WHITE,
                    **kwargs,
                )


LOGIC_UP = UP * ShapeFactory.gate_dim()
LOGIC_DOWN = DOWN * ShapeFactory.gate_dim()


class UnaryLogic(VGroup):
    """Creates shapes for unary logic gates per MIL-STD-806B."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs: List[Pin] = []
        self.outputs: List[Pin] = []

        self.shape = ShapeFactory.create_shape(LogicType.INV)
        self.add(self.shape)

        self.inputs.append(
            Pin(pin_side=PinSide.LEFT, color=WHITE).shift(UP * self.get_height() / 2)
        )
        self.outputs.append(
            Pin(pin_side=PinSide.RIGHT, color=WHITE).shift(
                UP * self.get_height() / 2 + RIGHT * self.shape.get_width()
            )
        )
        self.add(*self.inputs)
        self.add(*self.outputs)

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

    def get_height(self):
        return self.shape.get_height()

    def dim_all(self):
        self.shape.set_stroke(opacity=0.1)
        for pin in self.inputs + self.outputs:
            pin.set_opacity(0.1)

    def undim_all(self):
        self.shape.set_stroke(opacity=1)
        for pin in self.inputs + self.outputs:
            pin.set_opacity(1)


class BinaryLogic(VGroup):
    def __init__(self, logic_type: LogicType, **kwargs):
        self.num_inputs = kwargs.pop("num_inputs", 2)
        super().__init__(**kwargs)
        self.logic_type = logic_type

        pin_starts = List[Point3DLike]
        outer_pin_intercept = 0  # AND shapes
        if self.logic_type == LogicType.OR:
            outer_pin_intercept = (
                ShapeFactory.or_radius()
                - ShapeFactory.solve_for_y_intercept(
                    ShapeFactory.or_radius(),
                    ShapeFactory.gate_dim() / 2 - ShapeFactory.edge_to_pin(),
                )
            )
        self.inputs: List[Pin] = []
        self.outputs: List[Pin] = []

        self.shape = ShapeFactory.create_shape(self.logic_type)
        self.add(self.shape)

        # Create Input Pins for 2 or 3 input gates.
        # Input 0 measures down from the top of the gate.
        self.inputs.append(
            Pin(pin_side=PinSide.LEFT, color=WHITE).shift(
                LOGIC_UP + DOWN * ShapeFactory.edge_to_pin()
            )
        )
        # If there's more than 2 inputs, add the second input to the middle
        if self.num_inputs > 2:
            self.inputs.append(
                Pin(pin_side=PinSide.LEFT, color=WHITE).shift(LOGIC_UP / 2)
            )

        # The last input measures up from the bottom of the gate.
        self.inputs.append(
            Pin(pin_side=PinSide.LEFT, color=WHITE).shift(
                UP * ShapeFactory.edge_to_pin()
            )
        )

        # Shorten the outermost input pins.
        self.inputs[0].line.put_start_and_end_on(
            self.inputs[0].line.get_start() + LEFT * outer_pin_intercept,
            self.inputs[0].line.get_end(),
        )
        self.inputs[self.num_inputs - 1].line.put_start_and_end_on(
            self.inputs[self.num_inputs - 1].line.get_start()
            + LEFT * outer_pin_intercept,
            self.inputs[self.num_inputs - 1].line.get_end(),
        )

        self.outputs.append(
            Pin(pin_side=PinSide.RIGHT, color=WHITE).shift(self.shape.arcs[1].get_end())
        )
        self.add(*self.inputs)
        self.add(*self.outputs)

        # Handle Inverting output and Exclusive OR Inputs
        match self.logic_type:
            case LogicType.NAND | LogicType.NOR | LogicType.XNOR:
                self.invert_output()
            case LogicType.XOR | LogicType.XNOR:
                self.ex_inputs()

    def invert_output(self):
        self.outputs[0].add_invert()

    def ex_inputs(self):
        left_shift = LEFT * (
            0.8
            - ShapeFactory.solve_for_y_intercept(
                ShapeFactory.or_radius(), ShapeFactory.gate_dim() / 2
            )
        )
        ex = ArcBetweenPoints(
            start=LOGIC_UP + left_shift,
            end=left_shift,
            radius=-ShapeFactory.or_radius(),
        ).shift(LEFT * ShapeFactory.ex_offset())
        self.add(ex)

        for pin in self.inputs:
            pin.line.put_start_and_end_on(
                pin.line.get_start() + LEFT * ShapeFactory.ex_offset(),
                pin.line.get_end(),
            )

    def get_input0_connection(self) -> Pin:
        """Return the input0 Pin."""
        return self.inputs[0]

    def get_input1_connection(self) -> Pin:
        """Return the input1 Pin."""
        return self.inputs[1]

    def get_output_connection(self) -> Pin:
        """Return the output Pin."""
        return self.outputs[0]

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
    AND2(num_inputs=2),
    NAND2(num_inputs=3),
    OR2(num_inputs=2),
    NOR2(num_inputs=3),
    XOR2(num_inputs=2),
    XNOR2(num_inputs=3),
    BUF(),
    INV(),
]
