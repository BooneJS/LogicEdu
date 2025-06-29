from manim import (
    BLUE,
    GREY,
    Circle,
    Dot,
    DOWN,
    LEFT,
    Line,
    ORIGIN,
    PI,
    RIGHT,
    Text,
    UP,
    VGroup,
    WHITE,
    NumberPlane,
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


class PinType(enum.Enum):
    INPUT = 1
    OUTPUT = 2


class VGroupLogicBase(VGroup):
    def __init__(self, **kwargs):
        self.dim_value = kwargs.pop("dim_value", 0.3)
        super().__init__(**kwargs)

    def dim_all(self):
        pass

    def undim_all(self):
        pass


class Pin(VGroupLogicBase):
    def __init__(self, **kwargs):
        self.inner_label = kwargs.pop("inner_label", True)
        self.label_str = kwargs.pop("label", "")
        self.show_label = kwargs.pop("show_label", False)
        self.pin_side = kwargs.pop("pin_side", PinSide.LEFT)
        self.pin_length = kwargs.pop("pin_length", 0.6)
        self.pin_type = kwargs.pop("pin_type", PinType.INPUT)
        self.dot_radius = kwargs.pop("dot_radius", 0.05)
        self.not_bubble_radius = kwargs.pop("not_bubble_radius", 0.12 / 2)
        self.bit_width = kwargs.pop("bit_width", 1)
        self.font_size = kwargs.pop("font_size", 14)
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
            self.bus_text = Text(
                f"{self.bit_width}", font_size=self.font_size, **kwargs
            ).next_to(self.bus_line, text_next_to)
            self.add(self.bus_line, self.bus_text)

        if self.show_label:
            self.label = Text(self.label_str, font_size=self.font_size, color=color)
            if self.inner_label:
                match self.pin_side:
                    case PinSide.LEFT:
                        self.label.next_to(self.line, RIGHT * 0.5)
                    case PinSide.RIGHT:
                        self.label.next_to(self.line, LEFT * 0.5)
                    case PinSide.TOP:
                        self.label.next_to(self.line, DOWN * 0.5)
                    case PinSide.BOTTOM:
                        self.label.next_to(self.line, UP * 0.5)
            else:
                match self.pin_side:
                    case PinSide.LEFT:
                        self.label.next_to(
                            self.line, UP, aligned_edge=RIGHT, buff=0.1
                        ).shift(LEFT * 0.1)
                    case PinSide.RIGHT:
                        self.label.next_to(
                            self.line, UP, aligned_edge=LEFT, buff=0.1
                        ).shift(RIGHT * 0.1)
                    case PinSide.TOP:
                        self.label.rotate(PI / 2.0)
                        self.label.next_to(
                            self.line, LEFT, aligned_edge=DOWN, buff=0.1
                        ).shift(UP * 0.1)
                    case PinSide.BOTTOM:
                        self.label.rotate(PI / 2.0)
                        self.label.next_to(
                            self.line, LEFT, aligned_edge=UP, buff=0.1
                        ).shift(DOWN * 0.1)

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

    def __str__(self):
        return f"Pin(label={self.label_str}, side={self.pin_side}, length={self.pin_length})"

    def dim_all(self):
        super().dim_all()
        self.line.set_opacity(self.dim_value)
        self.dot.set_opacity(self.dim_value)
        self.bus_line.set_opacity(self.dim_value)
        self.bus_text.set_opacity(self.dim_value)

    def undim_all(self):
        super().undim_all()
        self.line.set_opacity(1)
        self.dot.set_opacity(1)
        self.bus_line.set_opacity(1)
        self.bus_text.set_opacity(1)


class ConnectorLine(VGroupLogicBase):
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
        if manhatten is False:
            self.line = Line(start_pin.line.get_end(), end_pin.line.get_end(), **kwargs)
        else:
            # If one of the pins is TOP or BOTTOM, that pin's x-axis is the midpoint to get a vertical line.
            mid_x_axis = 0
            if start_pin.pin_side in [PinSide.TOP, PinSide.BOTTOM]:
                mid_x_axis = start_pin.line.get_end()[0]
            elif end_pin.pin_side in [PinSide.TOP, PinSide.BOTTOM]:
                mid_x_axis = end_pin.line.get_end()[0]
            else:
                mid_x_axis = (
                    np.round(
                        (start_pin.line.get_end()[0] + end_pin.line.get_end()[0]) / 2, 1
                    )
                    + x_axis_shift
                )

            # X-axis of midpoint, Y-axis of start_pin.
            mid_segment_start = ORIGIN + [mid_x_axis, start_pin.line.get_end()[1], 0]
            # X-axis of midpoint, Y-axis of end_pin.
            mid_segment_end = ORIGIN + [mid_x_axis, end_pin.line.get_end()[1], 0]
            self.line = VGroup(
                Line(start_pin.line.get_end(), mid_segment_start, **kwargs),
                Line(mid_segment_start, mid_segment_end, **kwargs),
                Line(mid_segment_end, end_pin.line.get_end(), **kwargs),
            )
        self.add(self.line)

    def dim_all(self):
        super().dim_all()
        for line in self.line:
            line.set_opacity(self.dim_value)

    def undim_all(self):
        super().undim_all()
        for line in self.line:
            line.set_opacity(1)


def create_grid() -> NumberPlane:
    """Create a NumberPlane object to represent the grid. x_range and y_range define the
    visible area of the grid. x_length and y_length define the spacing between the major grid lines (deltas).
    """
    return NumberPlane(
        x_range=[-7, 7, 0.5],  # Start, End, Step (delta between lines)
        y_range=[-4, 4, 0.5],  # Start, End, Step (delta between lines)
        x_length=14,  # Total length in x-direction
        y_length=8,  # Total length in y-direction
        # Configure the appearance of the grid lines
        axis_config={
            "color": BLUE,
            "stroke_width": 1,  # Thickness of the grid lines
            "stroke_opacity": 0.3,
        },  # Color of the axes (major lines)
        background_line_style={
            "stroke_color": BLUE,  # Color of the background grid lines
            "stroke_width": 1,  # Thickness of the grid lines
            "stroke_opacity": 0.3,  # Faintness/transparency of the grid lines (0.0 to 1.0)
        },
    )
