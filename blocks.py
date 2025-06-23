from manim import (
    Polygon,
    VGroup,
    Text,
    Line,
    Dot,
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
            pin_side=PinSide.LEFT, label="in0", show_label=True
        ).shift(self.alu_shape.get_input0_start())
        self.input1_pin = Pin(
            pin_side=PinSide.LEFT, label="in1", show_label=True
        ).shift(self.alu_shape.get_input1_start())
        self.result_pin = Pin(
            pin_side=PinSide.RIGHT, label="result", show_label=True
        ).shift(self.alu_shape.get_result_start())
        self.zero_pin = Pin(
            pin_side=PinSide.RIGHT, label="zero", show_label=True, color=BLUE
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
        for i, input in enumerate(range(self.num_inputs)):
            self.inputs.append(Pin(pin_side=PinSide.LEFT).shift(UP * step * (i + 1)))
            label = Text(f"{i}", font_size=14, color=WHITE).next_to(
                self.inputs[i], RIGHT * step
            )
            self.add(label)
        self.outputs.append(
            Pin(pin_side=PinSide.RIGHT, label=f"{i}").shift(
                UP * (height / 2) + RIGHT * step
            )
        )
        start = (self.shape.get_vertices()[0] + self.shape.get_vertices()[1]) / 2
        self.inputs.append(Pin(pin_side=PinSide.BOTTOM, label="sel").shift(start))

        self.add(*self.inputs, *self.outputs)
