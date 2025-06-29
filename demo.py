from manim import (
    VGroup,
    Line,
    Dot,
    Scene,
    FadeIn,
    WHITE,
    LEFT,
    UP,
    DOWN,
    RIGHT,
    Create,
)

from basics import ConnectorLine, GRID, create_grid
from blocks import *
from logic_gates import *


class Demo(Scene):
    def construct(self):

        grid = create_grid()
        self.play(FadeIn(grid))

        alu = ALUZ()
        alu.scale(0.5).move_to(LEFT * 3 + DOWN)

        dff = DFF(variant=DFFVariant.DFF).scale(0.75)
        dff.move_to(LEFT * 6 + UP * 3)
        self.play(FadeIn(dff))

        dffr = DFF(variant=DFFVariant.DFF_R, bit_width=4).scale(0.75)
        dffr.move_to(LEFT * 6 + UP * 1)
        self.play(FadeIn(dffr))

        dffsr = DFF(variant=DFFVariant.DFF_SR).scale(0.75)
        dffsr.move_to(LEFT * 6 + DOWN * 1)
        self.play(FadeIn(dffsr))

        mux = Mux()
        mux.move_to(LEFT * 3 + UP * 1)
        self.play(Create(mux))

        mux = Mux(num_inputs=5)
        mux.move_to(LEFT * 4.5 + UP * 2).scale(0.75)
        self.play(Create(mux))

        # Add the shape to the scene and play a creation animation
        self.play(Create(alu))

        gates_vg = VGroup()

        base_loc = LEFT + UP * 5.2
        scale = 0.5
        for i, gate in enumerate(all_gates):
            gate.scale(scale)
            gate.move_to(base_loc + DOWN * (i * (scale + 0.1)))
            gates_vg.add(gate)

        self.play(FadeIn(gates_vg.move_to(base_loc + DOWN * (i * 0.6))))

        sign_extend = SignExtend(color=WHITE).scale(0.5).move_to(RIGHT + UP * 3)
        self.play(FadeIn(sign_extend))

        shift_left2 = (
            ShiftLeft(amount=2, color=WHITE).scale(0.75).move_to(RIGHT * 2.0 + UP * 2.5)
        )
        self.play(FadeIn(shift_left2))

        control = Control(color=BLUE).scale(0.75).move_to(DOWN * 2.5)
        self.play(Create(control))

        alu_control = AluControl(color=BLUE).scale(0.5).move_to(RIGHT * 1.5 + DOWN * 0)
        self.play(Create(alu_control))

        pc_block = PC(color=WHITE).move_to(RIGHT * 2.5 + DOWN * 2.5)
        self.play(Create(pc_block))

        imem = InstructionMemory(color=WHITE).move_to(RIGHT * 2.5 + DOWN)
        self.play(Create(imem))

        dmem = DataMemory(color=WHITE).move_to(RIGHT * 4.5 + UP * 3)
        self.play(Create(dmem))

        registers = RegisterFile(color=WHITE).move_to(RIGHT * 5 + DOWN * 2.2)
        self.play(Create(registers))

        wires = VGroup()

        try:
            aluop_output = control.get_output_by_label("ALUOp")
            aluop_input = alu_control.get_input_by_label("ALUOp")

            if aluop_output is None:
                print("Warning: Could not find 'ALUOp' output pin in control block")
                return
            if aluop_input is None:
                print("Warning: Could not find 'ALUOp' input pin in alu_control block")
                return

            wires.add(
                ConnectorLine(
                    aluop_output,
                    aluop_input,
                    manhatten=True,
                )
            )
        except Exception as e:
            print(f"Error creating ALUOp connector line: {e}")

        wires.add(
            ConnectorLine(
                alu.get_result_connection(),
                gates_vg[0].get_input1_connection(),
                manhatten=True,
                x_axis_shift=GRID,
            ),
        )
        wires.add(
            ConnectorLine(
                alu.get_zero_connection(),
                gates_vg[0].get_input0_connection(),
                manhatten=True,
            ),
        )

        wires.add(
            ConnectorLine(
                dff.get_q_connection(),
                gates_vg[1].get_input0_connection(),
                manhatten=True,
            ),
        )

        self.play(Create(wires))

        self.wait(1)
