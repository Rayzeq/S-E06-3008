"""Integration tests for the Triangulator HTTP API."""

import pytest
import requests
import responses

from main import POINTSET_MANAGER_BASE_URL, app


@pytest.fixture
def client():
    """Provide a Flask test client for the Triangulator application."""
    app.config.update(
        {
            "TESTING": True,
        }
    )
    with app.test_client() as client:
        yield client


@responses.activate
def test_api_pointset_manager_returns_400(client):
    """Check that a PointSetManager 400 error is forwarded to the client."""
    responses.add(
        responses.GET,
        f"{POINTSET_MANAGER_BASE_URL}/pointset/123",
        status=400,
        json={
            "code": "INVALID_UUID",
            "message": "Invalid PointSet identifier",
        },
    )

    response = client.get("/triangulation/123")
    assert response.status_code == 400
    assert response.json == {
        "code": "INVALID_UUID",
        "message": "Invalid PointSet identifier",
    }


@responses.activate
def test_api_pointset_manager_returns_404(client):
    """Check that a PointSetManager 404 error is forwarded to the client."""
    responses.add(
        responses.GET,
        f"{POINTSET_MANAGER_BASE_URL}/pointset/1234",
        status=404,
        json={
            "code": "NOT_FOUND",
            "message": "PointSet not found",
        },
    )

    response = client.get("/triangulation/1234")
    assert response.status_code == 404
    assert response.json == {
        "code": "NOT_FOUND",
        "message": "PointSet not found",
    }


@responses.activate
def test_api_pointset_manager_invalid_payload(client):
    """Check that an invalid PointSet payload returns a 500 error."""
    responses.add(
        responses.GET,
        f"{POINTSET_MANAGER_BASE_URL}/pointset/1234",
        status=200,
        body=b"not a valid PointSet",
    )

    response = client.get("/triangulation/1234")
    assert response.status_code == 500
    assert response.json == {
        "code": "INVALID_POINTSET",
        "message": "PointSet data was invalid",
    }


@responses.activate
def test_api_pointset_manager_triangulation_impossible(client):
    """Check that a non-triangulable PointSet returns a 500 error."""
    responses.add(
        responses.GET,
        f"{POINTSET_MANAGER_BASE_URL}/pointset/1234",
        status=200,
        body=b"\x00\x00\x00\x00",
    )

    response = client.get("/triangulation/1234")
    assert response.status_code == 500
    assert response.json == {
        "code": "TRIANGULATION_ERROR",
        "message": "coulnd't triangulate points",
    }


@responses.activate
def test_api_pointset_manager_timeout(client):
    """Check that an unreachable PointSetManager returns a 503 error."""
    responses.add(
        responses.GET,
        f"{POINTSET_MANAGER_BASE_URL}/pointset/1234",
        body=requests.exceptions.Timeout(),
    )

    response = client.get("/triangulation/1234")
    assert response.status_code == 503
    assert response.json == {
        "code": "NETWORK_ERROR",
        "message": "couldn't connect to PointSetManager",
    }


@responses.activate
def test_api_success(client):
    """Check that a valid PointSet is triangulated and returned as binary."""
    mock_points = b"\x03\x00\x00\x00" + b"".join(
        b"\x00\x00\x00" + i.to_bytes(1) for i in range(6)
    )
    responses.add(
        responses.GET,
        f"{POINTSET_MANAGER_BASE_URL}/pointset/1234",
        body=mock_points,
        status=200,
    )

    response = client.get("/triangulation/1234")
    assert response.status_code == 200
    print(response.data.removeprefix(mock_points))
    assert (
        response.data
        == mock_points
        + b"\x01\x00\x00\x00"
        + b"\x01\x00\x00\x00"
        + b"\x00\x00\x00\x00"
        + b"\x02\x00\x00\x00"
    )
