"""Triangulation of a set of 2D points using the Bowyer-Watson algorithm."""

from models import Point, Triangle


class TriangulationError(Exception):
    """Exception raised if the triangulation fails."""


def in_circumcircle(p: Point, a: Point, b: Point, c: Point) -> bool:
    """Return whether point p lies inside the circumcircle of triangle abc."""
    ax, ay = a.x - p.x, a.y - p.y
    bx, by = b.x - p.x, b.y - p.y
    cx, cy = c.x - p.x, c.y - p.y

    det = (
        (ax**2 + ay**2) * (bx * cy - cx * by)
        - (bx**2 + by**2) * (ax * cy - cx * ay)
        + (cx**2 + cy**2) * (ax * by - bx * ay)
    )

    cross = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
    return det * cross > 0


def triangulate(points: list[Point]) -> list[Triangle]:
    """Return a triangulation of the input points."""
    if len(points) < 3:
        raise TriangulationError

    min_x = min(p.x for p in points)
    min_y = min(p.y for p in points)
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)

    dx, dy = max_x - min_x, max_y - min_y
    delta_max = max(dx, dy)
    mid_x, mid_y = (min_x + max_x) / 2, (min_y + max_y) / 2

    st_p1 = Point(mid_x - 20 * delta_max - 1, mid_y - delta_max - 1)
    st_p2 = Point(mid_x, mid_y + 20 * delta_max + 1)
    st_p3 = Point(mid_x + 20 * delta_max + 1, mid_y - delta_max - 1)

    pts = points + [st_p1, st_p2, st_p3]
    n = len(points)
    triangles = [Triangle(n, n + 1, n + 2)]

    for i in range(n):
        bad_triangles = []
        for t in triangles:
            if in_circumcircle(pts[i], pts[t.p1], pts[t.p2], pts[t.p3]):
                bad_triangles.append(t)

        polygon = []
        for t in bad_triangles:
            edges = [(t.p1, t.p2), (t.p2, t.p3), (t.p3, t.p1)]
            for edge in edges:
                shared = False
                for other_t in bad_triangles:
                    if t == other_t:
                        continue
                    other_edges = [
                        (other_t.p1, other_t.p2),
                        (other_t.p2, other_t.p3),
                        (other_t.p3, other_t.p1),
                    ]
                    if edge in other_edges or (edge[1], edge[0]) in other_edges:
                        shared = True
                        break
                if not shared:
                    polygon.append(edge)

        triangles = [t for t in triangles if t not in bad_triangles]

        for edge in polygon:
            triangles.append(Triangle(edge[0], edge[1], i))

    final_triangles = [t for t in triangles if t.p1 < n and t.p2 < n and t.p3 < n]

    # Aligned or confused points, can't form a triangle
    if not final_triangles:
        raise TriangulationError

    return final_triangles
