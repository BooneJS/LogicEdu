"""
Component library for LogicEdu.

This module contains all the digital logic and computer architecture components:
- Logic gates (AND, OR, NOT, etc.)
- Computer architecture blocks (ALU, Register File, Memory, etc.)
- Data path elements (Multiplexers, Adders, etc.)
"""

from .logic_gates import (
    AND2,
    OR2,
    INV,
    NAND2,
    NOR2,
    XOR2,
    XNOR2,
    LogicType,
    BinaryLogic,
    ShapeFactory,
    LOGIC_UP,
    UnaryLogic,
    all_gates,
)

from .blocks import (
    ALUZ,
    RegisterFile,
    DataMemory,
    InstructionMemory,
    ControlUnit,
    AluControl,
    PC,
    AdderPlus4,
    BranchLogic,
    Mux,
    SignExtend,
    ShiftLeft,
    DFF,
    DFFVariant,
    Adder,
    GenEllipse,
)

__all__ = [
    # Logic gates
    "AND2",
    "OR2",
    "INV",
    "NAND2",
    "NOR2",
    "XOR2",
    "XNOR2",
    "LogicType",
    "BinaryLogic",
    "ShapeFactory",
    "LOGIC_UP",
    "UnaryLogic",
    "all_gates",
    # Architecture components
    "ALUZ",
    "RegisterFile",
    "DataMemory",
    "InstructionMemory",
    "ControlUnit",
    "AluControl",
    "PC",
    "AdderPlus4",
    "BranchLogic",
    "Mux",
    "SignExtend",
    "ShiftLeft",
    "DFF",
    "DFFVariant",
    "Adder",
    "GenEllipse",
]
