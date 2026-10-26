#!/usr/bin/env python3
"""
Geometry Calculator - Enhanced Version

A calculator for computing areas and perimeters of common shapes.
Supports multiple shapes with error handling, logging, and CLI output.
Designed for testing in a CI/CD pipeline.
"""
import argparse
import json
import logging
import math
import sys
from functools import wraps
from typing import Tuple, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def validate_positive(func):
    """Decorator to validate that numeric arguments are positive."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args[1:]:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Argument must be non-negative, got {arg}")
        return func(*args, **kwargs)
    return wrapper


class GeometryCalculator:
    """A calculator for common geometric calculations."""

    @validate_positive
    def area_rectangle(self, length, width):
        result = length * width
        logger.info(f"area_rectangle({length}, {width}) = {result}")
        return round(result, 4)

    @validate_positive
    def perimeter_rectangle(self, length, width):
        result = 2 * (length + width)
        logger.info(f"perimeter_rectangle({length}, {width}) = {result}")
        return round(result, 4)

    @validate_positive
    def area_triangle(self, base, height):
        result = (base * height) / 2
        logger.info(f"area_triangle({base}, {height}) = {result}")
        return round(result, 4)

    @validate_positive
    def area_circle(self, radius):
        result = math.pi * (radius ** 2)
        logger.info(f"area_circle({radius}) = {result}")
        return round(result, 4)

    @validate_positive
    def circumference_circle(self, radius):
        result = 2 * math.pi * radius
        logger.info(f"circumference_circle({radius}) = {result}")
        return round(result, 4)

    @validate_positive
    def area_square(self, side):
        result = side ** 2
        logger.info(f"area_square({side}) = {result}")
        return round(result, 4)

    @validate_positive
    def area_trapezoid(self, base1, base2, height):
        result = ((base1 + base2) / 2) * height
        logger.info(f"area_trapezoid({base1}, {base2}, {height}) = {result}")
        return round(result, 4)


OPERATIONS = {
    'rect-area': ('Rectangle Area', 'area_rectangle', 2),
    'rect-perim': ('Rectangle Perimeter', 'perimeter_rectangle', 2),
    'tri-area': ('Triangle Area', 'area_triangle', 2),
    'circle-area': ('Circle Area', 'area_circle', 1),
    'circle-circ': ('Circle Circumference', 'circumference_circle', 1),
    'square-area': ('Square Area', 'area_square', 1),
    'trapezoid-area': ('Trapezoid Area', 'area_trapezoid', 3),
}


def main():
    parser = argparse.ArgumentParser(
        description="Geometry Calculator - Compute areas and perimeters.",
        epilog="""Examples:
  calc.py rect-area 5 3          Area of rectangle
  calc.py circle-area 7         Area of circle
  calc.py tri-area 4 6          Area of triangle
  calc.py trapezoid-area 5 3 4  Area of trapezoid
  calc.py --all 5               All shapes with dimension 5
  calc.py --json circle-area 7  JSON output"""
    )
    parser.add_argument('operation', nargs='?', help='Operation to perform')
    parser.add_argument('values', nargs='*', type=float, help='Numeric values')
    parser.add_argument('--all', '-a', type=float, metavar='N', help='Compute all shapes')
    parser.add_argument('--json', '-j', action='store_true', help='JSON output')
    parser.add_argument('--list', '-l', action='store_true', help='List operations')

    args = parser.parse_args()
    calc = GeometryCalculator()

    if args.list:
        print("Available operations:")
        for op_id, (name, _, _) in OPERATIONS.items():
            print(f"  {op_id}: {name}")
        return

    if args.all is not None:
        results = {
            'rectangle_area': calc.area_rectangle(args.all, args.all * 2),
            'triangle_area': calc.area_triangle(args.all, args.all),
            'circle_area': calc.area_circle(args.all),
            'circle_circumference': calc.circumference_circle(args.all),
            'square_area': calc.area_square(args.all),
            'trapezoid_area': calc.area_trapezoid(args.all, args.all * 2, args.all),
        }
        print(json.dumps(results, indent=2) if args.json else "Results with dimension " + str(args.all) + ":")
        if not args.json:
            for k, v in results.items():
                print(f"  {k}: {v}")
        return

    if args.operation and args.operation in OPERATIONS:
        name, method_name, expected = OPERATIONS[args.operation]
        if len(args.values) != expected:
            print(f"Error: '{args.operation}' requires {expected} value(s)")
            return
        result = getattr(calc, method_name)(*args.values)
        if args.json:
            print(json.dumps({"operation": args.operation, "result": result, "values": args.values}))
        else:
            print(f"{name}: {result}")
    elif args.operation:
        print(f"Unknown operation: {args.operation}")
        print("Use --list to see available operations.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
