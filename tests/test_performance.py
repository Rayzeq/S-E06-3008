"""Performance tests for serialization and triangulation."""

import random
import struct
import time

import pytest

from models import Point, Triangle
from serialization import deserialize_point_set, serialize_triangles
from triangulation import triangulate


def random_points(count: int, seed: int = 42) -> list[Point]:
    """Return a reproducible list of random points."""
    rng = random.Random(seed)
    return [
        Point(rng.uniform(-1000, 1000), rng.uniform(-1000, 1000)) for _ in range(count)
    ]


def measure(operation):
    """Run an operation and return its result together with its duration."""
    start = time.perf_counter()
    result = operation()
    return result, time.perf_counter() - start


def print_measures(operation: str, size: int, elapsed: float) -> None:
    """Print a readable measurement line for the performance report."""
    print(f"\n{operation}: {size} elements in {elapsed:.4f}s")


@pytest.mark.perf
@pytest.mark.parametrize(
    "point_count",
    [10_000, 20_000, 30_000],
)
def test_serialize_triangles_performance(point_count):
    """Measure the serialization of Triangles for several sizes."""
    points = random_points(point_count)
    triangles = [Triangle(i, i + 1, i + 2) for i in range(point_count - 2)]

    data, elapsed = measure(lambda: serialize_triangles(points, triangles))

    print_measures("serialize_triangles", point_count, elapsed)

    expected_size = 4 + 8 * point_count + 4 + 12 * len(triangles)
    assert len(data) == expected_size


@pytest.mark.perf
@pytest.mark.parametrize(
    "point_count",
    [10_000, 100_000, 1_000_000],
)
def test_deserialize_point_set_performance(point_count):
    """Measure the deserialization of a PointSet for several sizes."""
    points = random_points(point_count)
    data = struct.pack("<L", point_count) + b"".join(
        struct.pack("<ff", point.x, point.y) for point in points
    )

    result, elapsed = measure(lambda: deserialize_point_set(data))

    print_measures("deserialize_point_set", point_count, elapsed)

    assert len(result) == point_count
    assert all(
        struct.pack("<ff", point.x, point.y) == struct.pack("<ff", decoded.x, decoded.y)
        for point, decoded in zip(points, result, strict=True)
    )


@pytest.mark.perf
@pytest.mark.parametrize(
    "point_count",
    [100, 500, 1_000],
)
def test_triangulate_random_points_performance(point_count):
    """Measure the triangulation of random point sets for several sizes."""
    points = random_points(point_count)

    triangles, elapsed = measure(lambda: triangulate(points))

    print_measures("triangulate (random)", point_count, elapsed)

    assert len(triangles) >= point_count - 2
    assert all(
        0 <= index < point_count
        for triangle in triangles
        for index in (triangle.p1, triangle.p2, triangle.p3)
    )


@pytest.mark.perf
@pytest.mark.parametrize(
    "side",
    [10, 20, 30],
)
def test_triangulate_grid_performance(side):
    """Measure the triangulation of a regular grid, which contains alignments."""
    points = [Point(x, y) for x in range(side) for y in range(side)]

    triangles, elapsed = measure(lambda: triangulate(points))

    print_measures("triangulate (grid)", side * side, elapsed)

    assert len(triangles) == 2 * (side - 1) ** 2
