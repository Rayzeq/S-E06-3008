import pytest

from models import Point, Triangle
from serialization import (
    SerializationError,
    deserialize_point_set,
    serialize_triangles,
)


class TestPointSet:
    def test_deserialize_empty_bytes(self):
        with pytest.raises(SerializationError):
            deserialize_point_set(b"")

    def test_deserialize_3_bytes(self):
        with pytest.raises(SerializationError):
            deserialize_point_set(b"\x00\x00\x00")

    def test_deserialize_zero_points(self):
        assert deserialize_point_set(b"\x00\x00\x00\x00") == []

    def test_deserialize_points_count_mismatch(self):
        with pytest.raises(SerializationError):
            deserialize_point_set(b"\x01\x00\x00\x00")

    def test_deserialize_superfluous_data(self):
        with pytest.raises(SerializationError):
            deserialize_point_set(b"\x00\x00\x00\x00\x00")

    def test_deserialize_missing_y_coordinate(self):
        with pytest.raises(SerializationError):
            deserialize_point_set(b"\x01\x00\x00\x00\x3f\x80\x00\x00")

    def test_deserialize_missing_two_bytes(self):
        with pytest.raises(SerializationError):
            deserialize_point_set(b"\x01\x00\x00\x00\x3f\x80\x00\x00\xbf\x80")

    def test_deserialize_valid_one_point(self):
        result = deserialize_point_set(
            b"\x01\x00\x00\x00\x3f\x80\x00\x00\xbf\x80\x00\x00"
        )
        assert result == [Point(1.0, -1.0)]

    def test_deserialize_valid_five_points(self):
        result = deserialize_point_set(
            b"\x05\x00\x00\x00\
\x3f\x80\x00\x00\xbf\x80\x00\x00\
\x40\xc0\x00\x00\x40\xe0\x00\x00\
\xc1\x20\x00\x00\x3f\x00\x00\x00\
\x40\x80\x00\x00\xbf\xc0\x00\x00\
\x41\x00\x00\x00\x00\x00\x00\x00"
        )
        assert result == [
            Point(1.0, -1.0),
            Point(6.0, 7.0),
            Point(-10.0, 0.5),
            Point(4, -1.5),
            Point(8, 0),
        ]


class TestTriangles:
    def test_serialize_zero_triangles(self):
        points = [Point(0, 0), Point(1, 1), Point(2, 2)]
        result = serialize_triangles(points, [])

        assert (
            result
            == b"\x03\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x3f\x80\x00\x00\x3f\x80\x00\x00\
\x40\x00\x00\x00\x40\x00\x00\x00\
\x00\x00\x00\x00"
        )

    def test_serialize_one_triangle(self):
        points = [Point(0, 0), Point(1, 0), Point(0, 1)]
        triangles = [Triangle(0, 1, 2)]
        result = serialize_triangles(points, triangles)

        assert (
            result
            == b"\x03\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x3f\x80\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x3f\x80\x00\x00\
\x01\x00\x00\x00\
\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00"
        )
