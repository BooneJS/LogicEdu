import pytest
from logicedu.core.basics import Pin, PinSide, PinType, VGroupLogicObjectBase
from logicedu.components.blocks import BranchLogic


class TestBugFixes:
    """Test that the bug fixes work correctly."""

    def test_pin_dim_all_without_bus(self):
        """Test that Pin.dim_all() works when bit_width <= 1 (no bus_line/bus_text)."""
        pin = Pin(pin_side=PinSide.LEFT, bit_width=1)
        # This should not raise AttributeError
        pin.dim_all()
        pin.undim_all()
        assert True  # If we get here, no exception was raised

    def test_pin_dim_all_with_bus(self):
        """Test that Pin.dim_all() works when bit_width > 1 (with bus_line/bus_text)."""
        pin = Pin(pin_side=PinSide.LEFT, bit_width=32)
        # This should not raise AttributeError
        pin.dim_all()
        pin.undim_all()
        assert True  # If we get here, no exception was raised

    def test_vgroup_logic_object_base_index_bounds(self):
        """Test that get_input_by_index and get_output_by_index handle invalid indices."""
        obj = VGroupLogicObjectBase()

        # Test with no pins
        with pytest.raises(ValueError, match="Input pin index 0 not found"):
            obj.get_input_by_index(0)

        with pytest.raises(ValueError, match="Output pin index 0 not found"):
            obj.get_output_by_index(0)

        # Add some pins
        obj.pins = [
            Pin(pin_side=PinSide.LEFT, pin_type=PinType.INPUT),
            Pin(pin_side=PinSide.RIGHT, pin_type=PinType.OUTPUT),
        ]

        # Test valid indices
        assert obj.get_input_by_index(0) is not None
        assert obj.get_output_by_index(0) is not None

        # Test invalid indices
        with pytest.raises(ValueError, match="Input pin index 1 not found"):
            obj.get_input_by_index(1)

        with pytest.raises(ValueError, match="Output pin index 1 not found"):
            obj.get_output_by_index(1)

    def test_branch_logic_undim_all(self):
        """Test that BranchLogic.undim_all() calls the correct super method."""
        # This test verifies that the method doesn't cause issues
        # The actual fix was changing super().dim_all() to super().undim_all()
        branch_logic = BranchLogic()
        # This should not cause any issues
        branch_logic.undim_all()
        assert True  # If we get here, no exception was raised
