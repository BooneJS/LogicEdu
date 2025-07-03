from manim import (
    Scene,
    VGroup,
    FadeIn,
    FadeOut,
    Create,
    WHITE,
    BLUE,
    LEFT,
    RIGHT,
    Text,
)
from blocks import (
    AluControl,
    ALUZ,
    PC,
    AdderPlus4,
    InstructionMemory,
    ControlUnit,
    RegisterFile,
    Mux,
    SignExtend,
)
from basics import create_grid, ConnectorLine, DOWN, UP, GRID, ArbitrarySegmentLine


class Cod6Fig417(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_objects = VGroup()

    def add_object(self, *obj):
        self.all_objects.add(*obj)

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

        # Introduce Instruction Decode
        self.dim_all()
        control = ControlUnit(color=BLUE)
        self.add_object(control)
        self.play(Create(control))
        self.wait(1)
        self.play(control.animate.scale(0.6).shift(LEFT * 2.7 + UP * 1.5))
        self.undim_all()
        self.wait(1)
        imem_inst_pin = imem.get_output_by_label("Inst")
        if imem_inst_pin is None:
            raise ValueError("Inst bus not found")
        control_inst_pin = control.get_input_by_label("inst[31:26]")
        if control_inst_pin is None:
            raise ValueError("Inst input pin not found")
        inst_to_control_bus = ConnectorLine(
            start_pin=imem_inst_pin,
            end_pin=control_inst_pin,
            manhatten=True,
        )
        self.add_object(inst_to_control_bus)
        self.play(Create(inst_to_control_bus))

        # Introduce Register File
        self.dim_all()
        regfile = RegisterFile(color=WHITE)
        self.add_object(regfile)
        self.play(Create(regfile))
        self.wait(1)
        self.play(regfile.animate.scale(0.6).shift(LEFT * 1.8 + DOWN * 1))
        self.undim_all()
        self.wait(1)

        control_reg_write = control.get_output_by_label("RegWrite")
        if control_reg_write is None:
            raise ValueError("RegWrite output pin not found")
        regfile_reg_write = regfile.get_input_by_label("RegWrite")
        if regfile_reg_write is None:
            raise ValueError("RegWrite input pin not found")
        reg_write_wire = ConnectorLine(
            start_pin=control_reg_write,
            end_pin=regfile_reg_write,
            manhatten=True,
        )
        self.add_object(reg_write_wire)

        regfile_read_reg1_pin = regfile.get_input_by_label("ReadReg1")
        if regfile_read_reg1_pin is None:
            raise ValueError("ReadReg1 input pin not found")
        read_reg1_wire = ConnectorLine(
            start_pin=imem_inst_pin,
            end_pin=regfile_read_reg1_pin,
            manhatten=True,
            axis_shift=-6 * GRID,
        )
        self.add_object(read_reg1_wire)

        regfile_read_reg2_pin = regfile.get_input_by_label("ReadReg2")
        if regfile_read_reg2_pin is None:
            raise ValueError("ReadReg2 input pin not found")
        read_reg2_wire = ConnectorLine(
            start_pin=imem_inst_pin,
            end_pin=regfile_read_reg2_pin,
            manhatten=True,
            axis_shift=-6 * GRID,
        )
        self.add_object(read_reg2_wire)

        regfile_write_reg_pin = regfile.get_input_by_label("WriteReg")
        if regfile_write_reg_pin is None:
            raise ValueError("WriteReg input pin not found")
        write_reg_mux = Mux(pin_length=0.3, color=WHITE).scale(0.6).shift(LEFT * 3.3)
        mux_down_len = (
            write_reg_mux.get_output_by_index(0).dot.get_center()[1]
            - regfile_write_reg_pin.dot.get_center()[1]
        )
        write_reg_mux.shift(DOWN * mux_down_len)
        self.add_object(write_reg_mux)

        regfile_write_data_pin = regfile.get_input_by_label("WriteData")
        if regfile_write_data_pin is None:
            raise ValueError("WriteData input pin not found")

        # Connect inst to mux0
        write_reg_mux0_wire = ConnectorLine(
            start_pin=imem_inst_pin,
            end_pin=write_reg_mux.get_input_by_index(0),
            manhatten=True,
            axis_shift=-2 * GRID,
        )
        self.add_object(write_reg_mux0_wire)

        # Connect inst to mux1
        write_reg_mux1_wire = ConnectorLine(
            start_pin=imem_inst_pin,
            end_pin=write_reg_mux.get_input_by_index(1),
            manhatten=True,
            axis_shift=-2 * GRID,
        )
        self.add_object(write_reg_mux1_wire)

        # Connect mux0 to regfile
        regfile_mux2write_data_wire = ConnectorLine(
            start_pin=write_reg_mux.get_output_by_index(0),
            end_pin=regfile_write_reg_pin,
            manhatten=True,
            axis_shift=-2 * GRID,
        )
        self.add_object(regfile_mux2write_data_wire)
        self.wait(1)

        # Manually route control.regdst to RegFile
        upper_y = (UP * 0.5)[1]
        left_x = (LEFT * 2.5)[0]
        control_regdst_pin = control.get_output_by_label("RegDst")
        if control_regdst_pin is None:
            raise ValueError("RegDst output pin not found")
        rf_write_reg_pin = regfile.get_input_by_label("WriteReg")
        if rf_write_reg_pin is None:
            raise ValueError("WriteReg input pin not found")

        regdst_wire = ArbitrarySegmentLine(
            control_regdst_pin.dot.get_center(),
            (
                control_regdst_pin.dot.get_center()[0],
                control_regdst_pin.dot.get_center()[1] + upper_y,
                0,
            ),
            (
                control_regdst_pin.dot.get_center()[0] + left_x,
                control_regdst_pin.dot.get_center()[1] + upper_y,
                0,
            ),
            (
                control_regdst_pin.dot.get_center()[0] + left_x,
                write_reg_mux.get_input_by_index(2).dot.get_center()[1],
                0,
            ),
            write_reg_mux.get_input_by_index(2).dot.get_center(),
            color=BLUE,
        )
        self.add_object(regdst_wire)
        self.play(
            Create(reg_write_wire),
            Create(read_reg1_wire),
            Create(read_reg2_wire),
            FadeIn(write_reg_mux),
            Create(write_reg_mux0_wire),
            Create(write_reg_mux1_wire),
            Create(regfile_mux2write_data_wire),
            Create(regdst_wire),
        )
        self.wait(1)

        # Add Sign Extend
        self.dim_all()
        sign_extend = SignExtend(color=WHITE)
        self.add_object(sign_extend)
        self.play(Create(sign_extend))
        self.wait(1)
        self.play(sign_extend.animate.scale(0.6).shift(LEFT * 1.8 + DOWN * 2.3))
        self.undim_all()
        inst_sign_extend_bus = ConnectorLine(
            start_pin=imem_inst_pin,
            end_pin=sign_extend.get_input_by_index(0),
            manhatten=True,
            axis_shift=-7 * GRID,
        )
        self.add_object(inst_sign_extend_bus)
        self.play(Create(inst_sign_extend_bus))
        self.wait(1)

        # Introduce ALU
        self.dim_all()
        alu = ALUZ(color=WHITE)
        alu.shift(DOWN * alu.shape.get_height() / 2 + LEFT * alu.shape.get_width() / 2)
        alu_0_pin = alu.get_input0_connection()
        alu_1_pin = alu.get_input1_connection()
        regfile_read_data1_pin = regfile.get_output_by_label("ReadData1")
        if regfile_read_data1_pin is None:
            raise ValueError("ReadData1 input pin not found")
        regfile_read_data2_pin = regfile.get_output_by_label("ReadData2")
        if regfile_read_data2_pin is None:
            raise ValueError("ReadData2 input pin not found")
        self.add_object(alu)
        self.play(Create(alu))
        self.wait(1)

        alu_scale = 0.5
        # ALU scales around shape center, so go down Y distance between center and pin0 and then again Y height of readdata1.pin
        align_with_regfile_readdata1 = (
            alu_scale * (alu_0_pin.dot.get_center()[1] - alu.shape.get_center()[1])
            - regfile_read_data1_pin.dot.get_center()[1]
        )
        self.play(
            alu.animate.scale(alu_scale).shift(
                RIGHT * 0.7 + DOWN * align_with_regfile_readdata1
            )
        )
        self.undim_all()

        regfile_read_data1_wire = ConnectorLine(
            start_pin=regfile_read_data1_pin,
            end_pin=alu_0_pin,
            manhatten=False,
            axis_shift=-7 * GRID,
        )
        self.add_object(regfile_read_data1_wire)

        # Add ALU1 Mux
        alu_1_mux = Mux(pin_length=0.3, color=WHITE).scale(0.6)
        alu_1_mux_shift = (
            alu_1_pin.dot.get_center()
            - alu_1_mux.get_output_by_index(0).dot.get_center()
            + RIGHT * 0.2
        )
        alu_1_mux.shift(alu_1_mux_shift)
        self.add_object(alu_1_mux)

        # Wire the ALU
        rf_to_alu_1_bus = ConnectorLine(
            start_pin=regfile_read_data2_pin,
            end_pin=alu_1_mux.get_input_by_index(0),
            manhatten=True,
        )
        self.add_object(rf_to_alu_1_bus)
        sign_extend_alu1_bus = ConnectorLine(
            start_pin=sign_extend.get_output_by_index(0),
            end_pin=alu_1_mux.get_input_by_index(1),
            manhatten=True,
            axis_shift=2.8 * GRID,
        )
        self.add_object(sign_extend_alu1_bus)
        control_alu_src_pin = control.get_output_by_label("ALUSrc")
        if control_alu_src_pin is None:
            raise ValueError("ALUSrc output pin not found")
        alu_1_mux_sel_pin = alu_1_mux.get_input_by_label("sel")
        if alu_1_mux_sel_pin is None:
            raise ValueError("ALU1 Mux sel input pin not found")
        alu_src_wire = ConnectorLine(
            start_pin=control_alu_src_pin,
            end_pin=alu_1_mux_sel_pin,
            manhatten=True,
            color=BLUE,
            axis_shift=0 * GRID,
        )
        self.add_object(alu_src_wire)
        self.play(
            Create(regfile_read_data1_wire),
            FadeIn(alu_1_mux),
            Create(rf_to_alu_1_bus),
            Create(sign_extend_alu1_bus),
            Create(alu_src_wire),
        )
        self.wait(1)

        # Add ALUControl
        self.dim_all()
        alu_control = AluControl(color=BLUE, show_labels=False)
        self.add_object(alu_control)
        temp_left_text = Text("inst[5:0]", color=BLUE, font_size=18).next_to(
            alu_control.get_input_by_index(0), LEFT
        )
        temp_bottom_text = Text("ALUOp", color=BLUE, font_size=18).next_to(
            alu_control.get_input_by_index(1), DOWN
        )
        temp_right_text = Text("Decode", color=BLUE, font_size=18).next_to(
            alu_control.get_output_by_index(0), RIGHT
        )
        self.play(
            Create(alu_control),
            FadeIn(temp_left_text),
            FadeIn(temp_bottom_text),
            FadeIn(temp_right_text),
        )
        self.wait(1)
        self.play(
            alu_control.animate.scale(0.5).next_to(alu, DOWN).shift(LEFT * 0.5),
            FadeOut(temp_left_text),
            FadeOut(temp_bottom_text),
            FadeOut(temp_right_text),
        )
        self.wait(1)
        self.undim_all()

        # Wire the ALUControl - start with inst[5:0]
        alu_control_inst_pin = alu_control.get_input_by_label("inst[5:0]")
        if alu_control_inst_pin is None:
            raise ValueError("inst[5:0] input pin not found")
        bottom_line = inst_sign_extend_bus.line[0].get_end() + DOWN * 2.8
        inst_to_alu_control_bus = ArbitrarySegmentLine(
            imem_inst_pin.dot.get_center(),
            inst_sign_extend_bus.line[0].get_end(),
            bottom_line,
            (
                alu_control_inst_pin.dot.get_center()[0],
                bottom_line[1],
                0,
            ),
            alu_control_inst_pin.dot.get_center(),
            color=WHITE,
        )
        self.add_object(inst_to_alu_control_bus)
        control_aluop_pin = control.get_output_by_label("ALUOp")
        if control_aluop_pin is None:
            raise ValueError("ControlUnit.ALUOp output pin not found")
        alu_control_aluop_pin = alu_control.get_input_by_label("ALUOp")
        if alu_control_aluop_pin is None:
            raise ValueError("ALUControl.ALUOp input pin not found")
        alu_control_decode_pin = alu_control.get_output_by_label("decode")
        if alu_control_decode_pin is None:
            raise ValueError("ALUControl.decode output pin not found")
        control_aluop_to_alu_control_bus = ConnectorLine(
            start_pin=control_aluop_pin,
            end_pin=alu_control_aluop_pin,
            manhatten=True,
            axis_shift=2 * GRID,
            color=BLUE,
        )
        self.add_object(control_aluop_to_alu_control_bus)
        alu_control_to_alu_bottom_bus = ArbitrarySegmentLine(
            alu_control_decode_pin.dot.get_center(),
            (
                alu.get_bottom_coordinate()[0],
                alu_control_decode_pin.dot.get_center()[1],
                0,
            ),
            alu.get_bottom_coordinate(),
            color=BLUE,
        )
        self.add_object(alu_control_to_alu_bottom_bus)
        self.play(
            Create(inst_to_alu_control_bus),
            Create(control_aluop_to_alu_control_bus),
            Create(alu_control_to_alu_bottom_bus),
        )
        self.wait(1)
