from collections import Counter

import pytest

from models import Point
from triangulation import TriangulationError, triangulate


def test_triangulate_zero_points():
    with pytest.raises(TriangulationError):
        triangulate([])


def test_triangulate_one_point():
    with pytest.raises(TriangulationError):
        triangulate([Point(0, 0)])


def test_triangulate_two_points():
    with pytest.raises(TriangulationError):
        triangulate([Point(0, 0), Point(1, 1)])


def test_triangulate_three_points():
    result = triangulate([Point(0, 0), Point(1, 0), Point(0, 1)])
    assert len(result) == 1


def test_triangulate_four_points():
    points = [Point(0, 0), Point(2, 0), Point(0, 2), Point(2, 2)]
    result = triangulate(points)
    assert len(result) == 2
    # check whether we have 2 points appearing one time, and 2 points appearing 2 times
    assert sorted(
        Counter(
            point_index for t in result for point_index in (t.p1, t.p2, t.p3)
        ).values()
    ) == [1, 1, 2, 2]


def test_triangulate_confused_points():
    points = [Point(1, 1), Point(1, 1), Point(1, 1)]
    result = triangulate(points)
    assert len(result) == 1
    assert result[0].p1 != result[0].p2 != result[0].p3


def test_triangulate_aligned_points():
    points = [Point(0, 0), Point(1, 1), Point(2, 2)]
    result = triangulate(points)
    assert len(result) == 1
    assert result[0].p1 != result[0].p2 != result[0].p3
