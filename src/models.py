"""Data structures used in the APIs."""

from dataclasses import dataclass


@dataclass
class Point:
    """A point, composed of its X and Y coordinates."""

    x: float
    y: float


@dataclass
class Triangle:
    """A triangle, defined by the index of its 3 points in a PointSet."""

    p1: int
    p2: int
    p3: int
