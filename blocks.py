import enum
from manim import (
    Ellipse,
    Polygon,
    Rectangle,
    VGroup,
    Text,
    WHITE,
    BLUE,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    ORIGIN,
    PI,
)
import numpy as np
from typing import List
from basics import Pin, PinSide, PinType, VGroupLogicBase, VGroupLogicObjectBase
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


class ALUZ(VGroupLogicObjectBase):
    """Starting with classic ALU Shape, adds text and lines."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shape = ClassicALUZShape(**kwargs)
        self.label = (
            Text("ALU", font_size=36, color=WHITE)
            .move_to(self.shape.get_center())
            .shift(DOWN * 0.65)
        )
        self.input0_pin = Pin(
            pin_side=PinSide.LEFT,
            label="in0",
            show_label=True,
            font_size=30,
            pin_type=PinType.INPUT,
        ).shift(self.shape.get_input0_start())
        self.input1_pin = Pin(
            pin_side=PinSide.LEFT,
            label="in1",
            show_label=True,
            font_size=30,
            pin_type=PinType.INPUT,
        ).shift(self.shape.get_input1_start())
        self.result_pin = Pin(
            pin_side=PinSide.RIGHT,
            label="result",
            show_label=True,
            font_size=30,
            pin_type=PinType.OUTPUT,
        ).shift(self.shape.get_result_start())
        self.zero_pin = Pin(
            pin_side=PinSide.RIGHT,
            label="zero",
            show_label=True,
            color=BLUE,
            font_size=26,
            pin_type=PinType.OUTPUT,
        ).shift(self.shape.get_zero_start())

        self.add(
            self.shape,
            self.input0_pin,
            self.input1_pin,
            self.result_pin,
            self.zero_pin,
            self.label,
        )

    def get_input0_connection(self) -> Pin:
        return self.input0_pin

    def get_input1_connection(self) -> Pin:
        return self.input1_pin

    def get_result_connection(self) -> Pin:
        return self.result_pin

    def get_zero_connection(self) -> Pin:
        return self.zero_pin

    def get_bottom_coordinate(self) -> np.ndarray:
        return (self.shape.get_vertices()[0] + self.shape.get_vertices()[1]) / 2

    def dim_all(self):
        super().dim_all()
        self.shape.set_stroke(opacity=self.dim_value)
        self.label.set_opacity(self.dim_value)
        self.input0_pin.set_opacity(self.dim_value)
        self.input1_pin.set_opacity(self.dim_value)
        self.result_pin.set_opacity(self.dim_value)
        self.zero_pin.set_opacity(self.dim_value)

    def undim_all(self):
        super().undim_all()
        self.shape.set_stroke(opacity=1)
        self.label.set_opacity(1)
        self.input0_pin.set_opacity(1)
        self.input1_pin.set_opacity(1)
        self.result_pin.set_opacity(1)
        self.zero_pin.set_opacity(1)


class Adder(VGroupLogicObjectBase):
    """Creates an Adder block."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shape = ClassicALUZShape(**kwargs)
        self.label = (
            Text("Adder", font_size=36, color=WHITE)
            .move_to(self.shape.get_center())
            .shift(DOWN * 0.65)
        )
        self.input0_pin = Pin(
            pin_side=PinSide.LEFT,
            label="in0",
            show_label=False,
            font_size=30,
            pin_type=PinType.INPUT,
        ).shift(self.shape.get_input0_start())
        self.input1_pin = Pin(
            pin_side=PinSide.LEFT,
            label="in1",
            show_label=False,
            font_size=30,
            pin_type=PinType.INPUT,
        ).shift(self.shape.get_input1_start())
        self.result_pin = Pin(
            pin_side=PinSide.RIGHT,
            label="result",
            show_label=False,
            font_size=30,
            pin_type=PinType.OUTPUT,
        ).shift(self.shape.get_result_start())
        self.add(
            self.shape, self.label, self.input0_pin, self.input1_pin, self.result_pin
        )

    def get_input0_connection(self) -> Pin:
        return self.input0_pin

    def get_input1_connection(self) -> Pin:
        return self.input1_pin

    def get_result_connection(self) -> Pin:
        return self.result_pin

    def dim_all(self):
        super().dim_all()
        self.shape.set_stroke(opacity=self.dim_value)
        self.label.set_opacity(self.dim_value)
        self.input0_pin.set_opacity(self.dim_value)
        self.input1_pin.set_opacity(self.dim_value)
        self.result_pin.set_opacity(self.dim_value)

    def undim_all(self):
        super().undim_all()
        self.shape.set_stroke(opacity=1)
        self.label.set_opacity(1)
        self.input0_pin.set_opacity(1)
        self.input1_pin.set_opacity(1)
        self.result_pin.set_opacity(1)


class AdderPlus4(Adder):
    """Creates PC+4 Adder"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plus4_text = Text("'d4", font_size=36, color=WHITE).next_to(
            self.get_input1_connection(), LEFT
        )
        self.add(self.plus4_text)
        self.shift(
            DOWN * (self.shape.get_height() / 2) + LEFT * (self.shape.get_width() / 2)
        )

    def dim_all(self):
        super().dim_all()
        self.plus4_text.set_opacity(self.dim_value)

    def undim_all(self):
        super().undim_all()
        self.plus4_text.set_opacity(1)


class Mux(VGroupLogicObjectBase):
    """Creates a Mux block."""

    def __init__(self, **kwargs):
        self.num_inputs = kwargs.pop("num_inputs", 2)
        self.pin_length = kwargs.pop("pin_length", 0.5)
        super().__init__(**kwargs)
        step = 0.25
        height = 2 * step + (self.num_inputs - 1) * step
        self.shape = Polygon(
            ORIGIN,
            UP * step + RIGHT * step,
            UP * (height - step) + RIGHT * step,
            UP * height,
            color=WHITE,
        )
        self.add(self.shape)
        for i in range(self.num_inputs):
            self.pins.append(
                Pin(
                    pin_side=PinSide.LEFT,
                    font_size=14,
                    pin_length=self.pin_length,
                    pin_type=PinType.INPUT,
                ).shift(UP * step * (self.num_inputs - i))
            )
            label = Text(f"{i}", font_size=14, color=WHITE).next_to(
                self.pins[i], RIGHT * step
            )
            self.add(label)
        self.pins.append(
            Pin(
                pin_side=PinSide.RIGHT,
                label=f"{i}",
                pin_length=self.pin_length,
                pin_type=PinType.OUTPUT,
            ).shift(UP * (height / 2) + RIGHT * step)
        )
        start = (self.shape.get_vertices()[0] + self.shape.get_vertices()[1]) / 2
        self.pins.append(
            Pin(
                pin_side=PinSide.BOTTOM,
                label="sel",
                pin_length=self.pin_length,
                pin_type=PinType.INPUT,
            ).shift(start)
        )

        self.add(*self.pins)

    def dim_all(self):
        super().dim_all()
        self.shape.set_stroke(opacity=self.dim_value)
        for pin in self.pins:
            pin.set_opacity(self.dim_value)

    def undim_all(self):
        super().undim_all()
        self.shape.set_stroke(opacity=1)
        for pin in self.pins:
            pin.set_opacity(1)


class DFFVariant(enum.Enum):
    """Variant of DFF."""

    DFF = "DFF"
    DFF_R = "DFF_R"
    DFF_SR = "DFF_SR"


class DFF(VGroupLogicObjectBase):
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
        width_multiplier = 0.8
        self.shape = Polygon(
            ORIGIN,
            RIGHT * width_multiplier,
            RIGHT * width_multiplier + height_multiplier * UP,
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

        self.q_pin.shift(dq_height + RIGHT * width_multiplier)
        self.clk_pin = Pin(
            pin_side=PinSide.LEFT, label="clk", show_label=True, font_size=18
        )
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


class GenEllipse(VGroupLogicObjectBase):
    """Creates a generic ellipse block used for SignExtend, Control, etc."""

    def __init__(self, **kwargs):
        self.inner_label = kwargs.pop("inner_label", True)
        self.label_text = kwargs.pop("label_text", "GenEllipse")
        ellipse_height = kwargs.pop("height", 2)
        ellipse_width = kwargs.pop("width", 1)
        pins_info = kwargs.pop(
            "pins_info",
            [
                {
                    "pin_side": PinSide.LEFT,
                    "pin_type": PinType.INPUT,
                    "label": "in",
                    "bit_width": 1,
                    "show_label": False,
                },
                {
                    "pin_side": PinSide.RIGHT,
                    "pin_type": PinType.OUTPUT,
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
        self.label = Text(f"{self.label_text}", font_size=24, **kwargs).rotate(PI / 2)
        self.add(self.label)

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
                        self.pins.append(pin)
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
                        self.pins.append(pin)
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
                        self.pins.append(pin)
                        pin.shift(
                            UP * y_half
                            + LEFT * ellipse_width / 2
                            + RIGHT * pin_x_over_distance
                        )
                    case PinSide.BOTTOM:
                        self.pins.append(pin)
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

    def dim_all(self):
        super().dim_all()
        self.shape.set_stroke(opacity=self.dim_value)
        self.label.set_opacity(self.dim_value)
        for pin in self.pins:
            pin.set_opacity(self.dim_value)

    def undim_all(self):
        super().undim_all()
        self.shape.set_stroke(opacity=1)
        self.label.set_opacity(1)
        for pin in self.pins:
            pin.set_opacity(1)


class SignExtend(GenEllipse):
    """Creates a SignExtend block."""

    def __init__(self, **kwargs):
        label_text = " Sign-\nExtend"
        ellipse_height = kwargs.pop("ellipse_height", 2)
        ellipse_width = kwargs.pop("ellipse_width", 1.2)
        pins_info = [
            {
                "pin_side": PinSide.LEFT,
                "label": "in",
                "bit_width": 16,
                "show_label": False,
                "pin_type": PinType.INPUT,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "out",
                "bit_width": 32,
                "show_label": False,
                "pin_type": PinType.OUTPUT,
            },
        ]
        super().__init__(label_text=label_text, pins_info=pins_info, **kwargs)


class ControlUnit(GenEllipse):
    """Creates a Control block."""

    def __init__(self, **kwargs):
        label_text = "Control"
        ellipse_height = kwargs.pop("ellipse_height", 3)
        ellipse_width = kwargs.pop("ellipse_width", 1)
        input_pin_length = 1.3
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
                "pin_type": PinType.INPUT,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "RegDst",
                "bit_width": 1,
                "pin_length": output_pin_length,
                "pin_type": PinType.OUTPUT,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "Branch",
                "bit_width": 1,
                "pin_length": output_pin_length,
                "pin_type": PinType.OUTPUT,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "MemRead",
                "bit_width": 1,
                "pin_length": output_pin_length,
                "pin_type": PinType.OUTPUT,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "MemtoReg",
                "bit_width": 1,
                "pin_length": output_pin_length,
                "pin_type": PinType.OUTPUT,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "ALUOp",
                "bit_width": 1,
                "pin_length": output_pin_length,
                "pin_type": PinType.OUTPUT,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "MemWrite",
                "bit_width": 1,
                "pin_length": output_pin_length,
                "pin_type": PinType.OUTPUT,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "ALUSrc",
                "bit_width": 1,
                "pin_length": output_pin_length,
                "pin_type": PinType.OUTPUT,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "RegWrite",
                "bit_width": 1,
                "pin_length": output_pin_length,
                "pin_type": PinType.OUTPUT,
                **pin_kwargs,
            },
        ]
        super().__init__(
            label_text=label_text,
            pins_info=pins_info,
            height=ellipse_height,
            width=ellipse_width,
            **kwargs,
        )


class AluControl(GenEllipse):
    """Creates a ALU Control block."""

    def __init__(self, **kwargs):
        label_text = "  ALU\nControl"
        ellipse_height = kwargs.pop("ellipse_height", 2)
        ellipse_width = kwargs.pop("ellipse_width", 1.2)
        show_labels = kwargs.pop("show_labels", False)
        pin_length = 1.0 if show_labels else 0.3
        pin_kwargs = {
            "show_label": show_labels,
            "inner_label": False,
            "pin_length": pin_length,
        }
        pins_info = [
            {
                "pin_side": PinSide.LEFT,
                "label": "inst[5:0]",
                "bit_width": 6,
                "pin_type": PinType.INPUT,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "decode",
                "bit_width": 1,
                "pin_type": PinType.OUTPUT,
                **pin_kwargs,
            },
            {
                "pin_side": PinSide.BOTTOM,
                "label": "ALUOp",
                "bit_width": 1,
                "pin_type": PinType.INPUT,
                **pin_kwargs,
            },
        ]
        super().__init__(label_text=label_text, pins_info=pins_info, **kwargs)


class ShiftLeft(GenEllipse):
    """Creates a ShiftLeft block."""

    def __init__(self, amount: int, **kwargs):
        label = f"Shift\nLeft {amount}"
        eight = kwargs.pop("ellipse_height", 2)
        ellipse_width = kwargs.pop("ellipse_width", 1.2)
        pins_info = [
            {
                "pin_side": PinSide.LEFT,
                "label": "in",
                "bit_width": 32,
                "pin_type": PinType.INPUT,
                "show_label": False,
            },
            {
                "pin_side": PinSide.RIGHT,
                "label": "out",
                "bit_width": 32,
                "pin_type": PinType.OUTPUT,
                "show_label": False,
            },
        ]
        super().__init__(label=label, pins_info=pins_info, **kwargs)


class GenRectangle(VGroupLogicObjectBase):
    """A generic block with a Rectangle and labeled pins."""

    def __init__(
        self,
        label: str,
        pins_info: list,
        **kwargs,
    ):
        self.rectangle_width = kwargs.pop("rectangle_width", 1)
        self.rectangle_height = kwargs.pop("rectangle_height", 2)

        super().__init__(**kwargs)

        # Draw the rectangle
        self.shape = Rectangle(
            width=self.rectangle_width,
            height=self.rectangle_height,
            color=kwargs.get("color", WHITE),
        )
        self.add(self.shape)

        # Add label at the center
        self.label = Text(label, font_size=18, color=kwargs.get("color", WHITE))
        self.label.move_to(self.shape.get_center())
        self.add(self.label)

        # Add pins
        for pin_info in pins_info:
            # Copy to avoid mutating the original dict
            pin_kwargs = dict(pin_info)
            pin_side = pin_kwargs.pop("pin_side")
            pin = Pin(pin_side=pin_side, **pin_kwargs, **kwargs)
            # Position the pin on the rectangle
            if pin_side == PinSide.LEFT:
                pin.shift(LEFT * (self.rectangle_width / 2))
            elif pin_side == PinSide.RIGHT:
                pin.shift(RIGHT * (self.rectangle_width / 2))
            elif pin_side == PinSide.TOP:
                pin.shift(UP * (self.rectangle_height / 2))
            elif pin_side == PinSide.BOTTOM:
                pin.shift(DOWN * (self.rectangle_height / 2))
            self.pins.append(pin)
            self.add(pin)

    def dim_all(self):
        super().dim_all()
        self.shape.set_stroke(opacity=self.dim_value)
        self.label.set_opacity(self.dim_value)
        for pin in self.pins:
            pin.set_opacity(self.dim_value)

    def undim_all(self):
        super().undim_all()
        self.shape.set_stroke(opacity=1)
        self.label.set_opacity(1)
        for pin in self.pins:
            pin.set_opacity(1)


class PC(GenRectangle):
    """Creates a PC block."""

    def __init__(self, **kwargs):
        pins_info = [
            {
                "pin_side": PinSide.LEFT,
                "pin_length": 0.5,
                "pin_type": PinType.INPUT,
                "label": "NextPC",
                "bit_width": 32,
                "show_label": False,
            },
            {
                "pin_side": PinSide.RIGHT,
                "pin_length": 0.5,
                "pin_type": PinType.OUTPUT,
                "label": "PC",
                "bit_width": 32,
                "show_label": False,
            },
        ]
        super().__init__(
            label="PC",
            pins_info=pins_info,
            rectangle_height=1.2,
            rectangle_width=0.4,
            **kwargs,
        )


class InstructionMemory(GenRectangle):
    """Creates an Instruction Memory block."""

    def __init__(self, **kwargs):
        pins_info = [
            {
                "pin_side": PinSide.LEFT,
                "pin_type": PinType.INPUT,
                "label": "RAddr",
                "bit_width": 32,
                "show_label": True,
            },
            {
                "pin_side": PinSide.RIGHT,
                "pin_type": PinType.OUTPUT,
                "label": "Inst",
                "bit_width": 32,
                "show_label": True,
            },
        ]
        super().__init__(
            label="IMEM",
            pins_info=pins_info,
            rectangle_height=1.5,
            rectangle_width=1.2,
            **kwargs,
        )
        self._get_input_pins()[0].shift(UP * ((self.rectangle_height / 2) - 0.3))
        self.label.shift(DOWN * (self.rectangle_height / 2 - 0.3))


class DataMemory(GenRectangle):
    """Creates an Data Memory block."""

    def __init__(self, **kwargs):
        pins_info = [
            {
                "pin_side": PinSide.LEFT,
                "pin_type": PinType.INPUT,
                "label": "Addr",
                "bit_width": 32,
                "show_label": True,
            },
            {
                "pin_side": PinSide.LEFT,
                "pin_type": PinType.INPUT,
                "label": "WriteData",
                "bit_width": 32,
                "show_label": True,
            },
            {
                "pin_side": PinSide.TOP,
                "pin_type": PinType.INPUT,
                "label": "MemWrite",
                "bit_width": 1,
                "show_label": True,
                "inner_label": False,
                "pin_length": 1.1,
            },
            {
                "pin_side": PinSide.RIGHT,
                "pin_type": PinType.OUTPUT,
                "label": "ReadData",
                "bit_width": 32,
                "show_label": True,
            },
        ]
        super().__init__(
            label="DMEM",
            pins_info=pins_info,
            rectangle_height=1.5,
            rectangle_width=1.2,
            **kwargs,
        )
        self._get_input_pins()[0].shift(UP * ((self.rectangle_height / 2) - 0.2))
        self._get_input_pins()[1].shift(DOWN * ((self.rectangle_height / 2) - 0.3))
        self._get_output_pins()[0].shift(UP * 0.3)
        self.label.shift(DOWN * (self.rectangle_height / 2 - 0.6))


class RegisterFile(GenRectangle):
    """Creates a Register File block."""

    def __init__(self, **kwargs):
        pins_info = [
            {
                "pin_side": PinSide.LEFT,
                "pin_type": PinType.INPUT,
                "label": "ReadReg1",
                "bit_width": 5,
                "show_label": True,
            },
            {
                "pin_side": PinSide.LEFT,
                "pin_type": PinType.INPUT,
                "label": "ReadReg2",
                "bit_width": 5,
                "show_label": True,
            },
            {
                "pin_side": PinSide.LEFT,
                "pin_type": PinType.INPUT,
                "label": "WriteReg",
                "bit_width": 5,
                "show_label": True,
            },
            {
                "pin_side": PinSide.LEFT,
                "pin_type": PinType.INPUT,
                "label": "WriteData",
                "bit_width": 32,
                "show_label": True,
            },
            {
                "pin_side": PinSide.TOP,
                "pin_type": PinType.INPUT,
                "label": "RegWrite",
                "bit_width": 1,
                "show_label": True,
                "inner_label": False,
                "pin_length": 0.9,
            },
            {
                "pin_side": PinSide.RIGHT,
                "pin_type": PinType.OUTPUT,
                "label": "ReadData1",
                "bit_width": 32,
                "show_label": True,
            },
            {
                "pin_side": PinSide.RIGHT,
                "pin_type": PinType.OUTPUT,
                "label": "ReadData2",
                "bit_width": 32,
                "show_label": True,
            },
        ]
        super().__init__(
            label="Registers",
            pins_info=pins_info,
            rectangle_height=2.5,
            rectangle_width=1.5,
            **kwargs,
        )
        lhs_offset = 0.3
        pin_increment = 0.5

        # Place LHS pins
        self._get_input_pins()[0].shift(UP * ((self.rectangle_height / 2) - lhs_offset))
        lhs_offset += pin_increment
        self._get_input_pins()[1].shift(UP * ((self.rectangle_height / 2) - lhs_offset))
        lhs_offset += pin_increment
        self._get_input_pins()[2].shift(UP * ((self.rectangle_height / 2) - lhs_offset))
        lhs_offset += pin_increment
        self._get_input_pins()[3].shift(UP * ((self.rectangle_height / 2) - lhs_offset))

        # Place RHS pins
        rhs_offset = 0.3 + pin_increment / 2 - 0.005
        self._get_output_pins()[0].shift(
            UP * ((self.rectangle_height / 2) - rhs_offset)
        )
        rhs_offset += pin_increment
        self._get_output_pins()[1].shift(
            UP * ((self.rectangle_height / 2) - rhs_offset)
        )
        self.label.shift(DOWN * (self.rectangle_height / 2 - 0.2) + RIGHT * 0.2)
