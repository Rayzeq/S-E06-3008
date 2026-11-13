"""Unit tests for the triangulation algorithm."""

from collections import Counter

import pytest

from models import Point
from triangulation import TriangulationError, in_circumcircle, triangulate


def test_in_circumcircle_inside():
    """Check that a point inside the circumcircle is detected."""
    a = Point(0, 0)
    b = Point(2, 0)
    c = Point(0, 2)

    p = Point(1, 1)
    assert in_circumcircle(p, a, b, c) is True


def test_in_circumcircle_outside():
    """Check that a point outside the circumcircle is rejected."""
    a = Point(0, 0)
    b = Point(2, 0)
    c = Point(0, 2)

    p = Point(3, 3)
    assert in_circumcircle(p, a, b, c) is False


def test_in_circumcircle_on_boundary():
    """Check that a point exactly on the circumcircle is not considered inside."""
    a = Point(0, 0)
    b = Point(2, 0)
    c = Point(0, 2)

    p = Point(2, 2)
    assert in_circumcircle(p, a, b, c) is False


def test_in_circumcircle_different_orientation():
    """Check that the result does not depend on the triangle orientation."""
    a = Point(0, 0)
    b = Point(0, 2)
    c = Point(2, 0)

    p_inside = Point(1, 1)
    p_outside = Point(3, 3)

    assert in_circumcircle(p_inside, a, b, c) is True
    assert in_circumcircle(p_outside, a, b, c) is False


def test_in_circumcircle_collinear_vertices():
    """Check that collinear triangle vertices do not define a circumcircle."""
    a = Point(0, 0)
    b = Point(1, 1)
    c = Point(2, 2)

    p = Point(1, 0)
    assert in_circumcircle(p, a, b, c) is False


def test_triangulate_zero_points():
    """Check that triangulating an empty point set raises an error."""
    with pytest.raises(TriangulationError):
        triangulate([])


def test_triangulate_one_point():
    """Check that triangulating a single point raises an error."""
    with pytest.raises(TriangulationError):
        triangulate([Point(0, 0)])


def test_triangulate_two_points():
    """Check that triangulating two points raises an error."""
    with pytest.raises(TriangulationError):
        triangulate([Point(0, 0), Point(1, 1)])


def test_triangulate_three_points():
    """Check that three non-aligned points produce a single triangle."""
    result = triangulate([Point(0, 0), Point(1, 0), Point(0, 1)])
    assert len(result) == 1
    assert {result[0].p1, result[0].p2, result[0].p3} == {0, 1, 2}


def test_triangulate_four_points():
    """Check that a square is split into two triangles sharing an edge."""
    points = [Point(0, 0), Point(2, 0), Point(0, 2), Point(2, 2)]
    result = triangulate(points)
    assert len(result) == 2
    # check whether we have 2 points appearing one time, and 2 points appearing 2 times
    assert sorted(
        Counter(
            point_index for t in result for point_index in (t.p1, t.p2, t.p3)
        ).values()
    ) == [1, 1, 2, 2]


def test_triangulate_with_a_duplicate_point():
    """Check that a duplicated point does not produce a degenerate triangle."""
    points = [Point(0, 0), Point(0, 0), Point(1, 0), Point(0, 1)]
    result = triangulate(points)

    assert len(result) == 1
    triangle = result[0]
    assert {
        (points[index].x, points[index].y)
        for index in (triangle.p1, triangle.p2, triangle.p3)
    } == {(0, 0), (1, 0), (0, 1)}


def test_triangulate_confused_points():
    """Check that a point set made of identical points raises an error."""
    points = [Point(1, 1), Point(1, 1), Point(1, 1)]
    with pytest.raises(TriangulationError):
        triangulate(points)


def test_triangulate_aligned_points():
    """Check that a set of aligned points raises an error."""
    points = [Point(0, 0), Point(1, 1), Point(2, 2)]
    with pytest.raises(TriangulationError):
        triangulate(points)
