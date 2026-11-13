"""Unit tests for the binary serialization and deserialization functions."""

import struct

import pytest

from models import Point, Triangle
from serialization import (
    SerializationError,
    deserialize_point_set,
    serialize_triangles,
)


class TestPointSet:
    """Tests for deserializing a PointSet from its binary representation."""

    def test_deserialize_empty_bytes(self):
        """Check that an empty payload is rejected."""
        with pytest.raises(SerializationError):
            deserialize_point_set(b"")

    def test_deserialize_3_bytes(self):
        """Check that a payload shorter than the length header is rejected."""
        with pytest.raises(SerializationError):
            deserialize_point_set(b"\x00\x00\x00")

    def test_deserialize_zero_points(self):
        """Check that an empty point set is deserialized to an empty list."""
        assert deserialize_point_set(b"\x00\x00\x00\x00") == []

    def test_deserialize_points_count_mismatch(self):
        """Check that a missing point payload is rejected."""
        with pytest.raises(SerializationError):
            deserialize_point_set(b"\x01\x00\x00\x00")

    def test_deserialize_superfluous_data(self):
        """Check that trailing bytes after the announced points are rejected."""
        with pytest.raises(SerializationError):
            deserialize_point_set(b"\x00\x00\x00\x00\x00")

    def test_deserialize_missing_y_coordinate(self):
        """Check that a point missing its Y coordinate is rejected."""
        with pytest.raises(SerializationError):
            deserialize_point_set(b"\x01\x00\x00\x00\x3f\x80\x00\x00")

    def test_deserialize_missing_two_bytes(self):
        """Check that a truncated point is rejected."""
        with pytest.raises(SerializationError):
            deserialize_point_set(b"\x01\x00\x00\x00\x3f\x80\x00\x00\xbf\x80")

    def test_deserialize_valid_one_point(self):
        """Check that a valid one-point payload is deserialized correctly."""
        result = deserialize_point_set(
            b"\x01\x00\x00\x00\x00\x00\x80\x3f\x00\x00\x80\xbf"
        )
        assert result == [Point(1.0, -1.0)]

    def test_deserialize_valid_five_points(self):
        """Check that a valid five-point payload is deserialized correctly."""
        result = deserialize_point_set(
            b"\x05\x00\x00\x00\
\x00\x00\x80\x3f\x00\x00\x80\xbf\
\x00\x00\xc0\x40\x00\x00\xe0\x40\
\x00\x00\x20\xc1\x00\x00\x00\x3f\
\x00\x00\x80\x40\x00\x00\xc0\xbf\
\x00\x00\x00\x41\x00\x00\x00\x00"
        )
        assert result == [
            Point(1.0, -1.0),
            Point(6.0, 7.0),
            Point(-10.0, 0.5),
            Point(4, -1.5),
            Point(8, 0),
        ]


class TestTriangles:
    """Tests for serializing a Triangles structure to its binary representation."""

    def test_serialize_zero_triangles(self):
        """Check that a Triangles with no triangle contains only the PointSet."""
        points = [Point(0, 0), Point(1, 1), Point(2, 2)]
        result = serialize_triangles(points, [])

        assert (
            result
            == b"\x03\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x80\x3f\x00\x00\x80\x3f\
\x00\x00\x00\x40\x00\x00\x00\x40\
\x00\x00\x00\x00"
        )

    def test_serialize_one_triangle(self):
        """Check that a single triangle is serialized in the expected format."""
        points = [Point(0, 0), Point(1, 0), Point(0, 1)]
        triangles = [Triangle(0, 1, 2)]
        result = serialize_triangles(points, triangles)

        assert (
            result
            == b"\x03\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x80\x3f\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x80\x3f\
\x01\x00\x00\x00\
\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00"
        )

    def test_serialize_multiple_triangles(self):
        """Check that several triangles are serialized in the expected format."""
        points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)]
        triangles = [Triangle(0, 1, 2), Triangle(1, 3, 2), Triangle(0, 1, 3)]
        result = serialize_triangles(points, triangles)

        expected = (
            struct.pack("<L", len(points))
            + b"".join(struct.pack("<ff", point.x, point.y) for point in points)
            + struct.pack("<L", len(triangles))
            + b"".join(
                struct.pack("<LLL", triangle.p1, triangle.p2, triangle.p3)
                for triangle in triangles
            )
        )
        assert result == expected
