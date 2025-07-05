"""
Tests for core LogicEdu components.
"""

from logicedu.core import Pin, PinSide, PinType, ConnectorLine, create_grid, GRID


class TestPin:
    """Test Pin class functionality."""

    def test_pin_creation(self):
        """Test basic pin creation."""
        pin = Pin(pin_side=PinSide.LEFT, pin_type=PinType.INPUT, label="test")
        assert pin.pin_side == PinSide.LEFT
        assert pin.pin_type == PinType.INPUT
        assert pin.label_str == "test"

    def test_pin_dimensions(self):
        """Test pin dimension properties."""
        pin = Pin(pin_side=PinSide.RIGHT, pin_length=0.5)
        assert pin.pin_length == 0.5
        assert pin.dot_radius == 0.05


class TestConnectorLine:
    """Test ConnectorLine functionality."""

    def test_connector_creation(self):
        """Test basic connector creation."""
        start_pin = Pin(pin_side=PinSide.LEFT)
        end_pin = Pin(pin_side=PinSide.RIGHT)
        connector = ConnectorLine(start_pin=start_pin, end_pin=end_pin)
        assert connector is not None


class TestGrid:
    """Test grid utility functions."""

    def test_grid_creation(self):
        """Test grid creation."""
        grid = create_grid()
        assert grid is not None

    def test_grid_rounding(self):
        """Test grid rounding function."""
        from logicedu.core.basics import grid_round

        assert grid_round(1.234) == 1.2
        assert grid_round(0.567) == 0.6
