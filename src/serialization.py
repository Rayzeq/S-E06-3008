"""Ensemble de fonctions pour sérialiser et désérialiser les données de l'API."""

from models import Point, Triangle


class SerializationError(Exception):
    """Exception raised if the serialization or deserialization fails."""


def deserialize_point_set(data: bytes) -> list[Point]:
    """Deserialize a PointSet from its API format."""
    ...


def serialize_triangles(points: list[Point], triangles: list[Triangle]) -> bytes:
    """Serialize a Triangles (including the inner PointSet) to the API format."""
    ...
