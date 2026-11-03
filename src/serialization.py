"""Ensemble de fonctions pour sérialiser et désérialiser les données de l'API."""

import struct

from models import Point, Triangle


class SerializationError(Exception):
    """Exception raised if the serialization or deserialization fails."""


def deserialize_point_set(data: bytes) -> list[Point]:
    """Deserialize a PointSet from its API format."""
    if len(data) < 4:
        raise SerializationError

    (length,) = struct.unpack("<L", data[:4])
    data = data[4:]

    if len(data) != length * 8:
        raise SerializationError

    points = []
    for i in range(length):
        byte_index = i * 8
        (x, y) = struct.unpack("<ff", data[byte_index : byte_index + 8])
        points.append(Point(x, y))

    return points


def serialize_triangles(points: list[Point], triangles: list[Triangle]) -> bytes:
    """Serialize a Triangles (including the inner PointSet) to the API format."""
    result = b""

    result += struct.pack("<L", len(points))
    for point in points:
        result += struct.pack("<ff", point.x, point.y)

    result += struct.pack("<L", len(triangles))
    for triangle in triangles:
        result += struct.pack("<LLL", triangle.p1, triangle.p2, triangle.p3)

    return result
