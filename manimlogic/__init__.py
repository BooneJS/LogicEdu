"""
ManimLogic - Digital Logic Circuit Animation Library for Manim

A comprehensive library for creating educational animations of digital logic circuits,
computer architecture diagrams, and data flow visualizations.
"""

__version__ = "0.1.0"
__author__ = "BooneJS"
__email__ = "boonejs@me.com"

# Core components
from .core.basics import (
    Pin,
    PinSide,
    PinType,
    ConnectorLine,
    ArbitrarySegmentLine,
    create_grid,
    GRID,
)

# Logic gates
from .components.logic_gates import (
    AND2,
    OR2,
    INV,
    NAND2,
    NOR2,
    XOR2,
    XNOR2,
    LogicType,
    BinaryLogic,
    all_gates,
)

# Computer architecture components
from .components.blocks import (
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
)

# Utility functions
from .utils.animation_helpers import (
    dim_all_objects,
    undim_all_objects,
)

# Re-export commonly used components for convenience
__all__ = [
    # Core
    "Pin",
    "PinSide",
    "PinType",
    "ConnectorLine",
    "ArbitrarySegmentLine",
    "create_grid",
    "GRID",
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
    # Utilities
    "dim_all_objects",
    "undim_all_objects",
]
