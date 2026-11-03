"""Main file implementing the Triangulator API.

API for calculating the triangulation of a 2D point set.
It retrieves the PointSet data from the PointSetManager service
using a PointSetID, performs the triangulation, and returns
the result in binary format.
"""

import requests
from flask import Flask, jsonify

from serialization import SerializationError, deserialize_point_set, serialize_triangles
from triangulation import TriangulationError, triangulate

POINTSET_MANAGER_BASE_URL = "https://localhost"

app = Flask(__name__)


@app.route("/triangulation/<pointSetId>", methods=["GET"])
def get_triangulation(pointSetId: str):
    """Calculate triangulation for a PointSet.

    Requests the triangulation for a given PointSetID.
    The service will internally fetch the PointSet from the
    PointSetManager, compute the triangulation, and return
    the 'Triangles' structure in binary format.
    """
    try:
        response = requests.get(f"{POINTSET_MANAGER_BASE_URL}/pointset/{pointSetId}")
    except requests.RequestException:
        return {
            "code": "NETWORK_ERROR",
            "message": "couldn't connect to PointSetManager",
        }, 503
    if not response.ok:
        return jsonify(response.json()), response.status_code

    try:
        points = deserialize_point_set(response.content)
    except SerializationError:
        return jsonify(
            {
                "code": "INVALID_POINTSET",
                "message": "PointSet data was invalid",
            }
        ), 500

    try:
        triangles = triangulate(points)
    except TriangulationError:
        return jsonify(
            {
                "code": "TRIANGULATION_ERROR",
                "message": "coulnd't triangulate points",
            }
        ), 500

    return serialize_triangles(points, triangles), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
