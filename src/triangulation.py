from models import Point, Triangle


class TriangulationError(Exception):
    """Exception raised if the triangulation fails."""


def triangulate(points: list[Point]) -> list[Triangle]:
    """Return a triangulation of the input points."""
    ...
