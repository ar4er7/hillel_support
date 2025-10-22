import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client  # replaces "requests" library for django tests
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
def test_user_creation_success(client: Client):
    payload = {
        "email": "masha_TEST@mail.com",
        "password": "1234",
        "first_name": "masha_TEST",
        "last_name": "Doe",
    }

    response = client.post(path="/users/", data=payload)
    user: User = User.objects.get(id=1)  # type: ignore

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert user.first_name == payload["first_name"]

    response_2 = client.get(path="/users/")
    get_users_data = response_2.json()

    assert response_2.status_code == status.HTTP_200_OK
    assert get_users_data["results"][0]["email"] == payload["email"]


# @pytest.fixture
# def john() -> str:
#     return "John"

# def test_username_injection(john):  # here we inject the fixruture's object
#     assert john == "John"  # here we use it


# def strange_calculator(a, b):
#     if a > b:
#         return a + b
#     else:
#         return a - b

# @pytest.mark.parametrize(  # naming arguments(a,b) and the relult(expected)
#     "a,b,expected",
#     [
#         (20, 10, 30),  # value a, b and expected result
#         (1, 5, -4),
#         (0, 1, -1),
#     ],
# )
# def test_strange_calculator(a, b, expected):  # the expected passed to compare
#     assert strange_calculator(a, b) == expected
