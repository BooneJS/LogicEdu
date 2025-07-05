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
    LaggedStart,
)
from manimlogic import (
    AluControl,
    ALUZ,
    PC,
    BranchLogic,
    AdderPlus4,
    InstructionMemory,
    DataMemory,
    ControlUnit,
    RegisterFile,
    Mux,
    SignExtend,
    create_grid,
    ConnectorLine,
    ArbitrarySegmentLine,
    GRID,
)
from manim import DOWN, UP


class Cod6Fig417(Scene):
    """
    Example showing the MIPS architecture from Chapter 6, Figure 4.17.

    This animation demonstrates the construction of a MIPS processor datapath,
    showing how components are added and connected step by step.

    Reference: Computer Organization and Design, 6th Edition (MIPS),
    David A. Patterson & John L. Hennessy,
    [Elsevier Book Companion Site](https://www.elsevier.com/books-and-journals/book-companion/9780128201091)
    """

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
        """Construct the MIPS processor datapath."""
        # Create a grid for debugging alignment
        # grid = create_grid()
        # self.play(FadeIn(grid))

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
        self.play(control.animate.scale(0.6).shift(LEFT * 2.7 + UP * 1.2))
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
            axis_shift=3 * GRID,
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
            FadeOut(temp_left_text),
            FadeOut(temp_bottom_text),
            FadeOut(temp_right_text),
            alu_control.animate.scale(0.5).next_to(alu, DOWN).shift(LEFT * 0.5),
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
            LaggedStart(
                Create(inst_to_alu_control_bus),
                Create(control_aluop_to_alu_control_bus),
                Create(alu_control_to_alu_bottom_bus),
                lag_ratio=0.5,
            )
        )
        self.wait(1)

        # Introduce Data Memory
        self.dim_all()
        dmem = DataMemory(color=WHITE)
        self.add_object(dmem)
        self.play(Create(dmem))
        self.wait(1)

        dmem_addr_pin = dmem.get_input_by_label("Addr")
        if dmem_addr_pin is None:
            raise ValueError("Addr input pin not found")
        dmem_readdata_pin = dmem.get_output_by_label("ReadData")
        if dmem_readdata_pin is None:
            raise ValueError("ReadData output pin not found")
        alu_result_pin = alu.get_result_connection()
        dmem_scale = 0.6
        self.wait(1)
        self.play(
            dmem.animate.scale(
                dmem_scale, about_point=dmem_addr_pin.dot.get_center()
            ).shift(
                alu_result_pin.dot.get_center()
                - dmem_addr_pin.dot.get_center()
                + RIGHT * 0.5
            ),
        )
        self.undim_all()
        self.wait(1)
        # Route wires/busses and add writeback mux
        wbmux = Mux(pin_length=0.3, color=WHITE).scale(0.6).flip(RIGHT)
        wbmux.shift(
            dmem_readdata_pin.dot.get_center()
            - wbmux.get_input_by_index(1).dot.get_center()
        )
        self.add_object(wbmux)
        alu_result_to_dmem_addr_bus = ConnectorLine(
            start_pin=alu_result_pin,
            end_pin=dmem_addr_pin,
            manhatten=False,
        )
        self.add_object(alu_result_to_dmem_addr_bus)

        control_memtoreg_pin = control.get_output_by_label("MemtoReg")
        if control_memtoreg_pin is None:
            raise ValueError("MemtoReg output pin not found")
        wbmux_memtoreg_pin = wbmux.get_input_by_label("sel")
        if wbmux_memtoreg_pin is None:
            raise ValueError("wbmux sel input pin not found")
        control_memtoreg_to_wbmux_bus = ConnectorLine(
            start_pin=control_memtoreg_pin,
            end_pin=wbmux_memtoreg_pin,
            manhatten=True,
            mid_axis=wbmux_memtoreg_pin.dot.get_center()[0],
            color=BLUE,
        )
        self.add_object(control_memtoreg_to_wbmux_bus)
        # ReadData2 to DMEM.WriteData
        dmem_write_data_pin = dmem.get_input_by_label("WriteData")
        if dmem_write_data_pin is None:
            raise ValueError("WriteData input pin not found")
        bottom_line_start = rf_to_alu_1_bus.line[1].get_end() + DOWN * 0.6
        regfile_read_data2_to_dmem_write_data_bus = ArbitrarySegmentLine(
            rf_to_alu_1_bus.line[1].get_end(),
            bottom_line_start,
            (
                dmem_write_data_pin.dot.get_center()[0],
                bottom_line_start[1],
                0,
            ),
            dmem_write_data_pin.dot.get_center(),
            color=WHITE,
        )
        self.add_object(regfile_read_data2_to_dmem_write_data_bus)

        control_memwrite_pin = control.get_output_by_label("MemWrite")
        if control_memwrite_pin is None:
            raise ValueError("MemWrite output pin not found")
        dmem_memwrite_pin = dmem.get_input_by_label("MemWrite")
        if dmem_memwrite_pin is None:
            raise ValueError("MemWrite input pin not found")
        control_memwrite_to_dmem_bus = ConnectorLine(
            start_pin=control_memwrite_pin,
            end_pin=dmem_memwrite_pin,
            manhatten=True,
            color=BLUE,
            mid_axis=dmem_memwrite_pin.dot.get_center()[0],
        )
        self.add_object(control_memwrite_to_dmem_bus)
        control_memread_pin = control.get_output_by_label("MemRead")
        if control_memread_pin is None:
            raise ValueError("MemRead output pin not found")
        dmem_memread_pin = dmem.get_input_by_label("MemRead")
        if dmem_memread_pin is None:
            raise ValueError("MemRead input pin not found")
        control_memread_to_dmem_bus = ConnectorLine(
            start_pin=control_memread_pin,
            end_pin=dmem_memread_pin,
            manhatten=True,
            axis_shift=12 * GRID,
            color=BLUE,
        )
        self.add_object(control_memread_to_dmem_bus)
        bottom_line_start = alu_result_pin.dot.get_center() + DOWN * 1.7
        alu_result_to_wbmux0_bus = ArbitrarySegmentLine(
            alu_result_pin.dot.get_center(),
            bottom_line_start,
            (
                wbmux.get_input_by_index(0).dot.get_center()[0],
                bottom_line_start[1],
                0,
            ),
            wbmux.get_input_by_index(0).dot.get_center(),
            color=WHITE,
        )
        self.add_object(alu_result_to_wbmux0_bus)
        regfile_write_data_pin = regfile.get_input_by_label("WriteData")
        if regfile_write_data_pin is None:
            raise ValueError("WriteData input pin not found")
        bottom_line_start = wbmux.get_output_by_index(0).dot.get_center() + DOWN * 2.5
        writeback_data_bus = ArbitrarySegmentLine(
            wbmux.get_output_by_index(0).dot.get_center(),
            bottom_line_start,
            (
                regfile_write_data_pin.dot.get_center()[0],
                bottom_line_start[1],
                0,
            ),
            regfile_write_data_pin.dot.get_center(),
            color=WHITE,
        )
        self.add_object(writeback_data_bus)
        self.play(
            LaggedStart(
                FadeIn(wbmux),
                Create(alu_result_to_dmem_addr_bus),
                Create(control_memtoreg_to_wbmux_bus),
                Create(control_memwrite_to_dmem_bus),
                Create(control_memread_to_dmem_bus),
                Create(alu_result_to_wbmux0_bus),
                Create(regfile_read_data2_to_dmem_write_data_bus),
                lag_ratio=0.5,
            )
        )
        self.play(Create(writeback_data_bus))
        self.wait(1)

        # Add Branch Logic
        self.dim_all()
        branch_logic = BranchLogic(color=WHITE)
        self.add_object(branch_logic)
        self.add_object(branch_logic)
        shift_branch_logic = RIGHT * 1.3 + UP * 2.2
        self.play(
            Create(branch_logic),
        )
        self.wait(1)
        self.play(branch_logic.animate.scale(0.6).shift(shift_branch_logic))
        self.wait(1)
        self.undim_all()

        # Wire the Branch Logic
        pcplus4_pin = adder_plus4.get_result_connection()
        branch_logic_pcplus4_pin = branch_logic.get_input_by_label("pcplus4")
        if branch_logic_pcplus4_pin is None:
            raise ValueError("BranchLogic.pcplus4 input pin not found")
        pcplus4_to_branch_logic_bus = ConnectorLine(
            start_pin=pcplus4_pin,
            end_pin=branch_logic_pcplus4_pin,
            manhatten=True,
        )
        self.add_object(pcplus4_to_branch_logic_bus)

        branch_logic_imm_pin = branch_logic.get_input_by_label("imm")
        if branch_logic_imm_pin is None:
            raise ValueError("BranchLogic.imm input pin not found")
        sign_extend_to_branch_logic_bus = ConnectorLine(
            start_pin=sign_extend.get_output_by_index(0),
            end_pin=branch_logic_imm_pin,
            manhatten=True,
        )
        self.add_object(sign_extend_to_branch_logic_bus)

        control_branch_pin = control.get_output_by_label("Branch")
        if control_branch_pin is None:
            raise ValueError("ControlUnit.Branch output pin not found")
        branch_logic_branch_pin = branch_logic.get_input_by_label("branch")
        if branch_logic_branch_pin is None:
            raise ValueError("BranchLogic.branch input pin not found")
        control_branch_to_branch_logic_bus = ConnectorLine(
            start_pin=control_branch_pin,
            end_pin=branch_logic_branch_pin,
            manhatten=True,
            color=BLUE,
            axis_shift=15 * GRID,
        )
        self.add_object(control_branch_to_branch_logic_bus)

        alu_zero_pin = alu.get_zero_connection()
        branch_logic_zero_pin = branch_logic.get_input_by_label("zero")
        if branch_logic_zero_pin is None:
            raise ValueError("BranchLogic.zero input pin not found")
        alu_zero_to_branch_logic_bus = ConnectorLine(
            start_pin=alu_zero_pin,
            end_pin=branch_logic_zero_pin,
            manhatten=True,
            color=BLUE,
        )
        self.add_object(alu_zero_to_branch_logic_bus)

        next_pc_bus_upper_line = (
            branch_logic.get_output_by_index(0).dot.get_center() + UP * 0.8
        )
        pc_input_pin = pc_block.get_input_by_index(0)
        next_pc_bus = ArbitrarySegmentLine(
            branch_logic.get_output_by_index(0).dot.get_center(),
            next_pc_bus_upper_line,
            (
                pc_input_pin.dot.get_center()[0],
                next_pc_bus_upper_line[1],
                0,
            ),
            pc_input_pin.dot.get_center(),
            color=WHITE,
        )
        self.add_object(next_pc_bus)
        self.play(
            LaggedStart(
                Create(pcplus4_to_branch_logic_bus),
                Create(sign_extend_to_branch_logic_bus),
                Create(control_branch_to_branch_logic_bus),
                Create(alu_zero_to_branch_logic_bus),
                Create(next_pc_bus),
                lag_ratio=0.3,
            )
        )
        self.wait(1)
        self.undim_all()
        self.wait(1)
