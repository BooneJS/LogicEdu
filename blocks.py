import enum
from manim import (
    Dot,
    Ellipse,
    Line,
    Polygon,
    VGroup,
    Text,
    WHITE,
    BLUE,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    ORIGIN,
)
import numpy as np
from typing import List
from basics import Pin, PinSide
from logic_gates import ShapeFactory
import math


class ClassicALUZShape(Polygon):
    """Creates the classic ALU Shape."""

    def __init__(self, **kwargs):
        # Corners of the ALU shape
        alu_vertices = [
            [0, 0, 0],
            [2, 1, 0],
            [2, 3, 0],
            [0, 4, 0],
            [0, 2.5, 0],
            [0.5, 2, 0],
            [0, 1.5, 0],
            [0, 0, 0],
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


class ALUZ(VGroup):
    """Starting with classic ALU Shape, adds text and lines."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alu_shape = ClassicALUZShape()
        self.title = (
            Text("ALU", font_size=36, color=WHITE)
            .move_to(self.alu_shape.get_center())
            .shift(DOWN * 0.65)
        )
        self.input0_pin = Pin(
            pin_side=PinSide.LEFT, label="in0", show_label=True, font_size=30
        ).shift(self.alu_shape.get_input0_start())
        self.input1_pin = Pin(
            pin_side=PinSide.LEFT, label="in1", show_label=True, font_size=30
        ).shift(self.alu_shape.get_input1_start())
        self.result_pin = Pin(
            pin_side=PinSide.RIGHT, label="result", show_label=True, font_size=30
        ).shift(self.alu_shape.get_result_start())
        self.zero_pin = Pin(
            pin_side=PinSide.RIGHT,
            label="zero",
            show_label=True,
            color=BLUE,
            font_size=26,
        ).shift(self.alu_shape.get_zero_start())

        self.add(
            self.alu_shape,
            self.input0_pin,
            self.input1_pin,
            self.result_pin,
            self.zero_pin,
            self.title,
        )

    def get_input0_connection(self) -> Pin:
        return self.input0_pin

    def get_input1_connection(self) -> Pin:
        return self.input1_pin

    def get_result_connection(self) -> Pin:
        return self.result_pin

    def get_zero_connection(self) -> Pin:
        return self.zero_pin


class Mux(VGroup):
    """Creates a Mux block."""

    def __init__(self, **kwargs):
        self.num_inputs = kwargs.pop("num_inputs", 2)
        super().__init__(**kwargs)
        step = 0.25
        height = 2 * step + (self.num_inputs - 1) * step
        self.inputs: List[Pin] = []
        self.outputs: List[Pin] = []
        self.shape = Polygon(
            ORIGIN,
            UP * step + RIGHT * step,
            UP * (height - step) + RIGHT * step,
            UP * height,
            color=WHITE,
        )
        self.add(self.shape)
        for i in range(self.num_inputs):
            self.inputs.append(
                Pin(pin_side=PinSide.LEFT, font_size=14).shift(UP * step * (i + 1))
            )
            label = Text(
                f"{self.num_inputs - 1 - i}", font_size=14, color=WHITE
            ).next_to(self.inputs[i], RIGHT * step)
            self.add(label)
        self.outputs.append(
            Pin(pin_side=PinSide.RIGHT, label=f"{i}").shift(
                UP * (height / 2) + RIGHT * step
            )
        )
        start = (self.shape.get_vertices()[0] + self.shape.get_vertices()[1]) / 2
        self.inputs.append(Pin(pin_side=PinSide.BOTTOM, label="sel").shift(start))

        self.add(*self.inputs, *self.outputs)


class DFFVariant(enum.Enum):
    """Variant of DFF."""

    DFF = "DFF"
    DFF_R = "DFF_R"
    DFF_SR = "DFF_SR"


class DFF(VGroup):
    """Creates a DFF block."""

    def __init__(self, variant: DFFVariant = DFFVariant.DFF, **kwargs):
        bit_width = kwargs.pop("bit_width", 1)
        super().__init__(**kwargs)
        self.variant = variant
        clk_side = 0.3
        height_multiplier = 1.3  # DFF
        clk_triangle_bottom_height = 0.2  # DFF
        dq_height = UP * height_multiplier + DOWN * 0.3  # DFF
        match self.variant:
            case DFFVariant.DFF:
                pass
            case DFFVariant.DFF_R:
                height_multiplier = 1.5
                dq_height = UP * height_multiplier + DOWN * 0.3  # DFF
                clk_triangle_bottom_height = 0.4
            case DFFVariant.DFF_SR:
                height_multiplier = 1.7
                clk_triangle_bottom_height = 0.4
                dq_height = UP * height_multiplier + DOWN * 0.5
        right_triangle_height = np.sqrt(clk_side**2 - (clk_side / 2) ** 2)
        self.shape = Polygon(
            ORIGIN,
            RIGHT,
            RIGHT + height_multiplier * UP,
            height_multiplier * UP,
            UP * clk_triangle_bottom_height,
            UP * clk_triangle_bottom_height
            + UP * clk_side / 2
            + RIGHT * right_triangle_height,
            UP * (clk_triangle_bottom_height + clk_side),
            **kwargs,
        )
        self.add(self.shape)
        self.d_pin = Pin(
            pin_side=PinSide.LEFT, label="D", show_label=True, bit_width=bit_width
        )
        self.d_pin.shift(dq_height)
        self.q_pin = Pin(
            pin_side=PinSide.RIGHT, label="Q", show_label=True, bit_width=bit_width
        )

        self.q_pin.shift(dq_height + RIGHT)
        self.clk_pin = Pin(pin_side=PinSide.LEFT, label="clk", show_label=True)
        self.clk_pin.shift(UP * clk_triangle_bottom_height + UP * clk_side / 2)
        self.clk_pin.label.shift(RIGHT * right_triangle_height)
        self.add(self.d_pin, self.q_pin, self.clk_pin)
        if self.variant == DFFVariant.DFF_R or self.variant == DFFVariant.DFF_SR:
            self.r_pin = Pin(pin_side=PinSide.BOTTOM, label="R", show_label=True)
            self.r_pin.shift(RIGHT * 0.5)
            self.add(self.r_pin)
        if self.variant == DFFVariant.DFF_SR:
            self.s_pin = Pin(pin_side=PinSide.TOP, label="S", show_label=True)
            self.s_pin.shift(UP * self.shape.get_height() + RIGHT * 0.5)
            self.add(self.s_pin)

    def get_d_connection(self) -> Pin:
        return self.d_pin

    def get_q_connection(self) -> Pin:
        return self.q_pin

    def get_clk_connection(self) -> Pin:
        return self.clk_pin

    def get_r_connection(self) -> Pin:
        return self.r_pin

    def get_s_connection(self) -> Pin:
        return self.s_pin


class GenEllipse(VGroup):
    """Creates a generic ellipse block used for SignExtend, Control, etc."""

    def __init__(self, **kwargs):
        self.inner_label = kwargs.pop("inner_label", True)
        self.label = kwargs.pop("label", "GenEllipse")
        ellipse_height = kwargs.pop("height", 2)
        ellipse_width = kwargs.pop("width", 1)
        pins_info = kwargs.pop(
            "pins_info",
            [
                {
                    "pin_side": PinSide.LEFT,
                    "label": "in",
                    "bit_width": 1,
                    "show_label": False,
                },
                {
                    "pin_side": PinSide.LEFT,
                    "label": "out",
                    "bit_width": 1,
                    "show_label": False,
                },
            ],
        )
        super().__init__(**kwargs)

        self.shape = Ellipse(
            height=ellipse_height,
            width=ellipse_width,
            **kwargs,
        )
        self.add(self.shape)

        x_half = ellipse_width / 2
        y_half = ellipse_height / 2
        self.label_text = Text(f"{self.label}", font_size=24, **kwargs)
        self.add(self.label_text)

        pin_dirs = [pin for pin in PinSide]
        pin_gap = 0.3

        # Iterate through each direction to calculate placement
        for pin_dir in pin_dirs:

            filtered_pins = [
                pin_info for pin_info in pins_info if pin_info["pin_side"] == pin_dir
            ]
            pin_count = len(filtered_pins)
            # Calculate both y and x. Only one will be used in the loop below.
            pin_y_down_distance = ellipse_height / 2 - pin_gap * (pin_count - 1) / 2
            pin_x_over_distance = ellipse_width / 2 - pin_gap * (pin_count - 1) / 2

            for pin_info in filtered_pins:
                pin = Pin(**pin_info, **kwargs)
                match pin.pin_side:
                    case PinSide.LEFT:
                        y_shift = ellipse_height / 2 - pin_y_down_distance
                        x_shift = ellipse_width / 2 - pin_x_over_distance
                        pin.shift(LEFT * x_half + UP * y_shift)
                        pin.line.put_start_and_end_on(
                            pin.line.get_start()
                            + RIGHT
                            * GenEllipse.ellipse_x_intercepts(
                                ellipse_height, ellipse_width, y_shift
                            ),
                            pin.line.get_end(),
                        )
                    case PinSide.RIGHT:
                        y_shift = ellipse_height / 2 - pin_y_down_distance
                        pin.shift(RIGHT * x_half + UP * y_shift)
                        pin.line.put_start_and_end_on(
                            pin.line.get_start()
                            + LEFT
                            * GenEllipse.ellipse_x_intercepts(
                                ellipse_height, ellipse_width, y_shift
                            ),
                            pin.line.get_end(),
                        )
                    case PinSide.TOP:
                        pin.shift(
                            UP * y_half
                            + LEFT * ellipse_width / 2
                            + RIGHT * pin_x_over_distance
                        )
                    case PinSide.BOTTOM:
                        pin.shift(
                            DOWN * y_half
                            + LEFT * ellipse_width / 2
                            + RIGHT * pin_x_over_distance
                        )
                self.add(pin)
                pin_y_down_distance += pin_gap
                pin_x_over_distance += pin_gap

    @staticmethod
    def ellipse_x_intercepts(height, width, y) -> float:
        """Calculates pin.end given y for an ellipse."""
        a = width / 2
        b = height / 2
        inside = 1 - (y**2) / (b**2)
        if inside < 0:
            # No real x-intercepts at this y
            return 0
        x = a - a * math.sqrt(inside)
        return x


class SignExtend(GenEllipse):
    """Creates a SignExtend block."""

    def __init__(self, **kwargs):
        label = " Sign-\nExtend"
        ellipse_height = kwargs.pop("ellipse_height", 2)
        ellipse_width = kwargs.pop("ellipse_width", 1.2)
        pins_info = [
            {
                "pin_side": PinSide.LEFT,
                "label": "in",
                "bit_width": 16,
                "show_label": False,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "out",
                "bit_width": 32,
                "show_label": False,
            },
        ]
        super().__init__(label=label, pins_info=pins_info, **kwargs)


class Control(GenEllipse):
    """Creates a Control block."""

    def __init__(self, **kwargs):
        label = "Control"
        ellipse_height = kwargs.pop("ellipse_height", 3)
        ellipse_width = kwargs.pop("ellipse_width", 1)
        input_pin_length = 1.2
        output_pin_length = 1.0
        pin_kwargs = {
            "show_label": True,
            "inner_label": False,
        }
        pins_info = [
            {
                "pin_side": PinSide.LEFT,
                "label": "inst[31:26]",
                "bit_width": 6,
                "pin_length": input_pin_length,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "RegDst",
                "bit_width": 1,
                "pin_length": output_pin_length,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "Branch",
                "bit_width": 1,
                "pin_length": output_pin_length,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "MemRead",
                "bit_width": 1,
                "pin_length": output_pin_length,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "MemtoReg",
                "bit_width": 1,
                "pin_length": output_pin_length,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "ALUOp",
                "bit_width": 2,
                "pin_length": output_pin_length,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "MemWrite",
                "bit_width": 1,
                "pin_length": output_pin_length,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "ALUSrc",
                "bit_width": 1,
                "pin_length": output_pin_length,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "RegWrite",
                "bit_width": 1,
                "pin_length": output_pin_length,
                **pin_kwargs,
            },
        ]
        super().__init__(
            label=label,
            pins_info=pins_info,
            height=ellipse_height,
            width=ellipse_width,
            **kwargs,
        )
