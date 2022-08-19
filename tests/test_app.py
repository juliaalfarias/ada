from cryptography.fernet import Fernet, InvalidToken
import app as application
from app import UnauthorizedException, ForbiddenException
import json
import pytest
import psycopg2 as pg
import pandas as pd
from unittest import mock
from http import HTTPStatus

client = application.app.test_client()


class PostgreMock:
    def close(self):
        return True


@pytest.fixture
def mock_df():
    data = [1, 2, 3]
    df = pd.DataFrame(data, columns=["Numbers"])
    return df


@pytest.fixture
def expected_return_401():
    expected_return_401 = json.dumps(
        {
            "Result": "Failure",
            "Reason": "Missing API KEY.",
        }
    )
    return expected_return_401


@pytest.fixture
def expected_return_403():
    expected_return_403 = json.dumps(
        {
            "Result": "Failure",
            "Reason": "Wrong API KEY.",
        }
    )
    return expected_return_403


def test_error_handler():
    expected_return = json.dumps(
        {
            "Result": "Failure",
            "Reason": "Invalid request.",
        }
    )
    with application.app.test_request_context():
        response = application.error_handler(
            message="Invalid request.", status_code=HTTPStatus.BAD_REQUEST
        )
        assert response.data.decode("utf-8") == expected_return
        assert response.status_code == 400


def test_authentication_layer_success(mocker):
    mocker.patch.object(Fernet, "__init__", return_value=None)
    mocker.patch.object(Fernet, "decrypt", return_value="valid_api_key".encode())
    with application.app.test_request_context(headers={"api_key": "valid_api_key"}):
        application.authentication_layer()


def test_authentication_layer_unauthorized():
    with pytest.raises(UnauthorizedException):
        with application.app.test_request_context():
            application.authentication_layer()


def test_authentication_layer_forbidden(mocker):
    mocker.patch.object(Fernet, "__init__", side_effect=ForbiddenException)
    with pytest.raises(ForbiddenException):
        with application.app.test_request_context(headers={"api_key": "wrong_api_key"}):
            application.authentication_layer()


def test_authentication_layer_invalid_token():
    with pytest.raises(InvalidToken):
        with application.app.test_request_context(headers={"api_key": "wrong_api_key"}):
            application.authentication_layer()


def test_retrieve_data_from_scheduling_success(mocker, mock_df):
    mocker.patch.object(pg, "connect", return_value=PostgreMock())
    mocker.patch.object(pd, "read_sql", return_value=mock_df)
    with application.app.test_request_context():
        mock_df = application.retrieve_data_from_scheduling(
            object_id="object_id", object_name="object_name"
        )


def test_retrieve_data_from_scheduling_database_error(mocker):
    mocker.patch.object(pg, "connect", return_value=PostgreMock())
    mocker.patch.object(pd, "read_sql", side_effect=pg.DatabaseError)
    with pytest.raises(pg.DatabaseError):
        with application.app.test_request_context():
            application.retrieve_data_from_scheduling(
                object_id="object_id", object_name="object_name"
            )


def test_all_success(mocker, mock_df):
    expected_return = mock_df.to_json(orient="records")
    mocker.patch("app.authentication_layer", return_value=True)
    mocker.patch("app.retrieve_data_from_scheduling", return_value=mock_df)
    response = client.get("/all")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == expected_return


def test_all_unauthorized(mocker, expected_return_401):
    mocker.patch("app.authentication_layer", side_effect=UnauthorizedException)
    response = client.get("/all")
    assert response.status_code == 401
    assert response.data.decode("utf-8") == expected_return_401


def test_all_forbidden(mocker, expected_return_403):
    mocker.patch("app.authentication_layer", side_effect=ForbiddenException)
    response = client.get("/all")
    assert response.status_code == 403
    assert response.data.decode("utf-8") == expected_return_403


def test_all_invalid_token(mocker, expected_return_403):
    mocker.patch("app.authentication_layer", side_effect=InvalidToken)
    response = client.get("/all")
    assert response.status_code == 403
    assert response.data.decode("utf-8") == expected_return_403


def test_dag_id_success(mocker, mock_df):
    expected_return = mock_df.to_json(orient="records")
    mocker.patch("app.authentication_layer", return_value=True)
    mocker.patch("app.retrieve_data_from_scheduling", return_value=mock_df)
    response = client.get("/dag_id/test_dag_id")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == expected_return


def test_dag_id_unauthorized(mocker, expected_return_401):
    mocker.patch("app.authentication_layer", side_effect=UnauthorizedException)
    response = client.get("/dag_id/test_dag_id")
    assert response.status_code == 401
    assert response.data.decode("utf-8") == expected_return_401


def test_dag_id_forbidden(mocker, expected_return_403):
    mocker.patch("app.authentication_layer", side_effect=ForbiddenException)
    response = client.get("/dag_id/test_dag_id")
    assert response.status_code == 403
    assert response.data.decode("utf-8") == expected_return_403


def test_dag_id_invalid_token(mocker, expected_return_403):
    mocker.patch("app.authentication_layer", side_effect=InvalidToken)
    response = client.get("/dag_id/test_dag_id")
    assert response.status_code == 403
    assert response.data.decode("utf-8") == expected_return_403


def test_task_id_success(mocker, mock_df):
    expected_return = mock_df.to_json(orient="records")
    mocker.patch("app.authentication_layer", return_value=True)
    mocker.patch("app.retrieve_data_from_scheduling", return_value=mock_df)
    response = client.get("/task_id/test_task_id")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == expected_return


def test_task_id_unauthorized(mocker, expected_return_401):
    mocker.patch("app.authentication_layer", side_effect=UnauthorizedException)
    response = client.get("/task_id/test_task_id")
    assert response.status_code == 401
    assert response.data.decode("utf-8") == expected_return_401


def test_task_id_forbidden(mocker, expected_return_403):
    mocker.patch("app.authentication_layer", side_effect=ForbiddenException)
    response = client.get("/task_id/test_task_id")
    assert response.status_code == 403
    assert response.data.decode("utf-8") == expected_return_403


def test_task_id_invalid_token(mocker, expected_return_403):
    mocker.patch("app.authentication_layer", side_effect=InvalidToken)
    response = client.get("/task_id/test_task_id")
    assert response.status_code == 403
    assert response.data.decode("utf-8") == expected_return_403
