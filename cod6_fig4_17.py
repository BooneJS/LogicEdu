from manim import (
    Scene,
    VGroup,
    FadeIn,
    Create,
    WHITE,
    LEFT,
)
from blocks import *
from basics import create_grid, ConnectorLine


class Cod6Fig417(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_objects = VGroup()

    def add_object(self, obj):
        self.all_objects.add(obj)

    def dim_all(self):
        for obj in self.all_objects:
            obj.dim_all()
        self.wait(1)

    def undim_all(self):
        for obj in self.all_objects:
            print(obj)
            obj.undim_all()
        self.wait(1)

    def construct(self):
        grid = create_grid()
        self.play(FadeIn(grid))

        # Introduce PC
        pc_block = PC(color=WHITE)
        self.add_object(pc_block)
        self.play(FadeIn(pc_block))

        self.wait(1)
        self.play(pc_block.animate.shift(LEFT * 6.5).scale(0.5))
        self.wait(1)

        # Introduce PC+4 Adder
        self.dim_all()
        adder_plus4 = AdderPlus4(color=WHITE)
        self.add_object(adder_plus4)
        self.play(Create(adder_plus4))
        self.wait(1)
        self.play(adder_plus4.animate.scale(0.3).shift(LEFT * 4.8 + UP * 2.9))
        self.undim_all()
        pc_out_pin = pc_block.get_output_by_label("PC")
        if pc_out_pin is None:
            raise ValueError("PC output pin not found")
        pc_to_pcplus4_bus = ConnectorLine(
            start_pin=pc_out_pin,
            end_pin=adder_plus4.get_input0_connection(),
            manhatten=True,
        )
        self.add_object(pc_to_pcplus4_bus)
        self.play(Create(pc_to_pcplus4_bus))
        self.wait(1)

        # Introduce Instruction Memory
        self.dim_all()
        imem = InstructionMemory(color=WHITE)
        self.add_object(imem)
        self.play(Create(imem))
        self.wait(1)
        scale_factor = 0.8
        raddr_pin = imem.get_input_by_label("RAddr")
        if raddr_pin is None:
            raise ValueError("RAddr input pin not found")
        down_shift = scale_factor * (
            raddr_pin.line.get_end()[1] - pc_out_pin.dot.get_center()[1]
        )
        left_shift = raddr_pin.line.get_end()[0] - pc_out_pin.dot.get_center()[0]
        self.play(
            imem.animate.scale(scale_factor).shift(
                LEFT * left_shift + DOWN * down_shift
            )
        )
        self.undim_all()
        self.wait(1)
