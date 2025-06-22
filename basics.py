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
)
import enum


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
        self.not_bubble_radius = kwargs.pop("not_bubble_radius", 0.15 / 2)
        self.bus_width = kwargs.pop("bus_width", 1)
        super().__init__(**kwargs)
        color = kwargs.get("color", WHITE)

        match self.pin_side:
            case PinSide.LEFT:
                end = LEFT * self.pin_length
            case PinSide.RIGHT:
                end = RIGHT * self.pin_length
            case PinSide.TOP:
                end = UP * self.pin_length
            case PinSide.BOTTOM:
                end = DOWN * self.pin_length

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
        if self.show_label:
            self.label = Text(self.label, font_size=28, color=color).next_to(
                self.line, RIGHT * 0.5
            )
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

    def get_connection(self):
        return self.line.get_end()
