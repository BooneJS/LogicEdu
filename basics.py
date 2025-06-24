from manim import (
    VGroup,
    Line,
    Dot,
    Circle,
    WHITE,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    ORIGIN,
    Text,
    BLUE,
)
import enum
from manim.typing import Point3DLike
import numpy as np
from typing import List, Optional


GRID = 0.1


def grid_round(x: float) -> float:
    return np.round(x, 1)


class PinSide(enum.Enum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4


class Pin(VGroup):
    def __init__(self, **kwargs):
        self.label = kwargs.pop("label", "")
        self.show_label = kwargs.pop("show_label", False)
        self.pin_side = kwargs.pop("pin_side", PinSide.LEFT)
        self.pin_length = kwargs.pop("pin_length", 0.6)
        self.dot_radius = kwargs.pop("dot_radius", 0.05)
        self.not_bubble_radius = kwargs.pop("not_bubble_radius", 0.12 / 2)
        self.bit_width = kwargs.pop("bit_width", 1)
        self.font_size = kwargs.pop("font_size", 14)
        if self.font_size is not 14:
            print(f"Pin: {self.label} font_size: {self.font_size}")
        super().__init__(**kwargs)

        # bus starts -0.15 in from the end.
        bus_start = ORIGIN
        bus_end = ORIGIN
        color = kwargs.get("color", WHITE)

        slash_offset = 0.1
        text_next_to = RIGHT * slash_offset
        match self.pin_side:
            case PinSide.LEFT:
                end = LEFT * self.pin_length
                bus_start = end + RIGHT * slash_offset + UP * slash_offset
                bus_end = bus_start + 2 * DOWN * slash_offset + 2 * RIGHT * slash_offset
                text_next_to = UP * slash_offset
            case PinSide.RIGHT:
                end = RIGHT * self.pin_length
                bus_end = end + LEFT * slash_offset + DOWN * slash_offset
                bus_start = bus_end + 2 * LEFT * slash_offset + 2 * UP * slash_offset
                text_next_to = UP * slash_offset
            case PinSide.TOP:
                end = UP * self.pin_length
                bus_start = end + DOWN * slash_offset + LEFT * slash_offset
                bus_end = bus_start + 2 * DOWN * slash_offset + 2 * RIGHT * slash_offset
                text_next_to = LEFT * slash_offset
            case PinSide.BOTTOM:
                end = DOWN * self.pin_length
                bus_end = end + UP * slash_offset + RIGHT * slash_offset
                bus_start = bus_end + UP * slash_offset + 2 * LEFT * slash_offset
                text_next_to = LEFT * slash_offset

        # Pin line
        self.line = Line(
            start=ORIGIN,
            end=end,
            color=color,
        )
        self.dot = Dot(
            self.line.get_end(),
            color=color,
            radius=self.dot_radius,
        )
        self.add(self.line, self.dot)

        # Bus line
        if self.bit_width > 1:
            self.bus_line = Line(
                start=bus_start,
                end=bus_end,
                color=color,
            )
            self.bus_text = Text(f"{self.bit_width}", font_size=self.font_size).next_to(
                self.bus_line, text_next_to
            )
            self.add(self.bus_line, self.bus_text)

        if self.show_label:
            self.label = Text(self.label, font_size=self.font_size, color=color)
            # .next_to(
            #     self.line, RIGHT * 0.5
            # )
            match self.pin_side:
                case PinSide.LEFT:
                    self.label.next_to(self.line, RIGHT * 0.5)
                case PinSide.RIGHT:
                    self.label.next_to(self.line, LEFT * 0.5)
                case PinSide.TOP:
                    self.label.next_to(self.line, DOWN * 0.5)
                case PinSide.BOTTOM:
                    self.label.next_to(self.line, UP * 0.5)
            self.add(self.label)

    def add_invert(self, color=WHITE):
        self.circle = Circle(
            radius=self.not_bubble_radius,
            color=color,
        )
        if self.pin_side == PinSide.LEFT:
            self.circle.move_to(self.line.get_start() + LEFT * self.not_bubble_radius)
            new_start = self.line.get_start() + LEFT * self.not_bubble_radius * 2
        elif self.pin_side == PinSide.RIGHT:
            self.circle.move_to(self.line.get_start() + RIGHT * self.not_bubble_radius)
            new_start = self.line.get_start() + RIGHT * self.not_bubble_radius * 2
        elif self.pin_side == PinSide.TOP:
            self.circle.move_to(self.line.get_start() + UP * self.not_bubble_radius)
            new_start = self.line.get_start() + UP * self.not_bubble_radius * 2
        elif self.pin_side == PinSide.BOTTOM:
            self.circle.move_to(self.line.get_start() + DOWN * self.not_bubble_radius)
            new_start = self.line.get_start() + DOWN * self.not_bubble_radius * 2
        self.add(self.circle)
        self.line.put_start_and_end_on(new_start, self.line.get_end())


class ConnectorLine(VGroup):
    """ConnectorLine is used to connect two pins directly. If a mid_y_axis is provided,
    3 segments are created: the first and last traverse x-axis only, and the middle segment
    traverses y-axis only."""

    def __init__(
        self,
        start_pin: Pin,
        end_pin: Pin,
        **kwargs,
    ):
        manhatten: bool = kwargs.pop("manhatten", False)
        x_axis_shift: float = kwargs.pop("x_axis_shift", 0)
        super().__init__(**kwargs)
        print(f"ConnectorLine: {start_pin} to {end_pin}")
        if manhatten is False:
            self.line = Line(start_pin.line.get_end(), end_pin.line.get_end(), **kwargs)
        else:
            # midpoint = np.round(
            #     np.mean([start_pin.line.get_end(), end_pin.line.get_end()]), 1
            # )
            print(f"start_pin.line.get_end(): {start_pin.line.get_end()}")
            print(f"end_pin.line.get_end(): {end_pin.line.get_end()}")
            mid_x_axis = (
                np.round(
                    (start_pin.line.get_end()[0] + end_pin.line.get_end()[0]) / 2, 1
                )
                + x_axis_shift
            )

            print(f"midpoint: {mid_x_axis}")
            # X-axis of midpoint, Y-axis of start_pin.
            mid_segment_start = ORIGIN + [mid_x_axis, start_pin.line.get_end()[1], 0]
            # X-axis of midpoint, Y-axis of end_pin.
            mid_segment_end = ORIGIN + [mid_x_axis, end_pin.line.get_end()[1], 0]
            print(f"mid_segment_start: {mid_segment_start}")
            print(f"mid_segment_end: {mid_segment_end}")
            self.line = VGroup(
                Line(start_pin.line.get_end(), mid_segment_start, **kwargs),
                Line(mid_segment_start, mid_segment_end, **kwargs),
                Line(mid_segment_end, end_pin.line.get_end(), **kwargs),
            )
        self.add(self.line)
