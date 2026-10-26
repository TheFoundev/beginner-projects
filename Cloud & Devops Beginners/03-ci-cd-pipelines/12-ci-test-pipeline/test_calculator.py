"""
Unit tests for the Geometry Calculator.

Run: python -m pytest test_calculator.py -v
Or locally: python -m pytest tests/ -v
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calculator import GeometryCalculator, OPERATIONS


@pytest.fixture
def calc():
    """Create a fresh calculator instance for each test."""
    return GeometryCalculator()


class TestRectangleArea:
    def test_rectangle_basic(self, calc):
        assert calc.area_rectangle(5, 3) == 15.0

    def test_rectangle_zero_width(self, calc):
        assert calc.area_rectangle(5, 0) == 0.0

    def test_rectangle_large(self, calc):
        assert calc.area_rectangle(100, 200) == 20000.0

    def test_rectangle_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.area_rectangle(-5, 3)

    def test_rectangle_float(self, calc):
        result = calc.area_rectangle(2.5, 4.0)
        assert result == 10.0


class TestRectanglePerimeter:
    def test_perimeter_basic(self, calc):
        assert calc.perimeter_rectangle(5, 3) == 16.0

    def test_perimeter_square(self, calc):
        assert calc.perimeter_rectangle(4, 4) == 16.0

    def test_perimeter_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.perimeter_rectangle(-1, 5)


class TestTriangleArea:
    def test_triangle_basic(self, calc):
        assert calc.area_triangle(4, 6) == 12.0

    def test_triangle_zero_height(self, calc):
        assert calc.area_triangle(10, 0) == 0.0

    def test_triangle_float(self, calc):
        assert calc.area_triangle(3.5, 8) == 14.0

    def test_triangle_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.area_triangle(5, -2)


class TestCircleArea:
    def test_circle_basic(self, calc):
        import math
        expected = round(math.pi * 49, 4)
        assert calc.area_circle(7) == expected

    def test_circle_zero_radius(self, calc):
        assert calc.area_circle(0) == 0.0

    def test_circle_negative_raises(self, calc):
        with pytest.raises(ValueError):
            calc.area_circle(-1)


class TestCircleCircumference:
    def test_circumference_basic(self, calc):
        import math
        expected = round(2 * math.pi * 5, 4)
        assert calc.circumference_circle(5) == expected

    def test_circumference_negative(self, calc):
        with pytest.raises(ValueError):
            calc.circumference_circle(-3)


class TestSquareArea:
    def test_square_basic(self, calc):
        assert calc.area_square(4) == 16.0

    def test_square_zero(self, calc):
        assert calc.area_square(0) == 0.0

    def test_square_large(self, calc):
        assert calc.area_square(100) == 10000.0

    def test_square_negative(self, calc):
        with pytest.raises(ValueError):
            calc.area_square(-3)


class TestTrapezoidArea:
    def test_trapezoid_basic(self, calc):
        result = calc.area_trapezoid(5, 3, 4)
        assert result == 16.0

    def test_trapezoid_parallelogram(self, calc):
        result = calc.area_trapezoid(5, 5, 3)
        assert result == 15.0

    def test_trapezoid_negative(self, calc):
        with pytest.raises(ValueError):
            calc.area_trapezoid(5, -3, 4)


class TestOperationsDict:
    def test_operations_count(self):
        assert len(OPERATIONS) >= 6

    def test_operations_have_required_keys(self):
        for op_id, (name, method, arity) in OPERATIONS.items():
            assert name
            assert hasattr(GeometryCalculator, method)
            assert arity > 0

    def test_all_rectangle_ops_present(self):
        assert 'rect-area' in OPERATIONS
        assert 'rect-perim' in OPERATIONS

    def test_circle_ops_present(self):
        assert 'circle-area' in OPERATIONS
        assert 'circle-circ' in OPERATIONS
