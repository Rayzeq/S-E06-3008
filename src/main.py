"""Main file implementing the Triangulator API.

API for calculating the triangulation of a 2D point set.
It retrieves the PointSet data from the PointSetManager service
using a PointSetID, performs the triangulation, and returns
the result in binary format.
"""

import requests  # noqa
from flask import Flask

app = Flask(__name__)


@app.route("/triangulation/<pointSetId>", methods=["GET"])
def get_triangulation(pointSetId: str):
    """Calculate triangulation for a PointSet.

    Requests the triangulation for a given PointSetID.
    The service will internally fetch the PointSet from the
    PointSetManager, compute the triangulation, and return
    the 'Triangles' structure in binary format.
    """
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
