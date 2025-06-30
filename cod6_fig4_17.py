from manim import (
    Scene,
    VGroup,
    FadeIn,
    Create,
    WHITE,
    BLUE,
    LEFT,
)
from blocks import PC, AdderPlus4, InstructionMemory, ControlUnit, RegisterFile, Mux
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
        self.play(Create(reg_write_wire))

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
        self.play(Create(read_reg1_wire))

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
        self.play(Create(read_reg2_wire))

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
        self.play(FadeIn(write_reg_mux))

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
        self.play(Create(write_reg_mux0_wire))

        # Connect inst to mux1
        write_reg_mux1_wire = ConnectorLine(
            start_pin=imem_inst_pin,
            end_pin=write_reg_mux.get_input_by_index(1),
            manhatten=True,
            axis_shift=-2 * GRID,
        )
        self.add_object(write_reg_mux1_wire)
        self.play(Create(write_reg_mux1_wire))

        # Connect mux0 to regfile
        regfile_mux2write_data_wire = ConnectorLine(
            start_pin=write_reg_mux.get_output_by_index(0),
            end_pin=regfile_write_reg_pin,
            manhatten=True,
            axis_shift=-2 * GRID,
        )
        self.add_object(regfile_mux2write_data_wire)
        self.play(Create(regfile_mux2write_data_wire))
        self.wait(1)

        # Manually route control.regdst to RegFile
        if True:
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
            self.play(Create(regdst_wire))
