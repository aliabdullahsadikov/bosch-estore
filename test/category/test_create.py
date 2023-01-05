import random

from starlette import status

from test import test

fake_payload = {
    "name": "test_" + str(random.random()),
    "parent_id": 13
}


def test_create_without_token():
    response = test.post(
        "/api/v1/categories",
        data=fake_payload
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_create_with_token():
    pass


def test_create_incorrect_data():
    pass


def test_create_already_exist():
    pass

