from unittest.mock import patch

import pytest
import requests

from main import app


@pytest.fixture
def client():
    app.config.update(
        {
            "TESTING": True,
        }
    )
    with app.test_client() as client:
        yield client


@patch("main.requests.get")
def test_api_pointset_manager_returns_400(mock_get, client):
    mock_get.return_value.status_code = 400
    mock_get.return_value.json = lambda: {
        "code": "INVALID_UUID",
        "message": "Invalid PointSet identifier",
    }

    response = client.get("/triangulation/123")
    assert response.status_code == 400
    assert response.json == {
        "code": "INVALID_UUID",
        "message": "Invalid PointSet identifier",
    }


@patch("main.requests.get")
def test_api_pointset_manager_returns_404(mock_get, client):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json = lambda: {
        "code": "NOT_FOUND",
        "message": "PointSet not found",
    }

    response = client.get("/triangulation/1234")
    assert response.status_code == 404
    assert response.json == {
        "code": "NOT_FOUND",
        "message": "PointSet not found",
    }


@patch("main.requests.get")
def test_api_pointset_manager_invalid_payload(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"not a valid PointSet"

    response = client.get("/triangulation/1234")
    assert response.status_code == 500
    assert response.json == {
        "code": "INVALID_POINTSET",
        "message": "PointSet data was invalid",
    }


@patch("main.requests.get")
def test_api_pointset_manager_triangulation_impossible(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"\x00\x00\x00\x00"

    response = client.get("/triangulation/1234")
    assert response.status_code == 500
    assert response.json == {
        "code": "TRIANGULATION_ERROR",
        "message": "coulnd't triangulate points",
    }


@patch("main.requests.get")
def test_api_pointset_manager_timeout(mock_get, client):
    mock_get.side_effect = requests.exceptions.Timeout

    response = client.get("/triangulation/1234")
    assert response.status_code == 503
    assert response.json == {
        "code": "NETWORK_ERROR",
        "message": "couldn't connect to PointSetManager",
    }


@patch("main.requests.get")
def test_api_success(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"\x03\x00\x00\x00" + (b"\x00\x00\x00\x00" * 6)

    response = client.get("/triangulation/1234")
    assert response.status_code == 200
    assert (
        response.data
        == mock_get.return_value.content
        + b"\x01\x00\x00\x00"
        + b"\x00\x00\x00\x00"
        + b"\x01\x00\x00\x00"
        + b"\x02\x00\x00\x00"
    )
