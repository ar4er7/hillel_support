import requests


def test_user_creation_success():
    url = "http://localhost:8000/users/"
    payload = {
        "email": "masha_TEST@mail.com",
        "first_name": "masha_TEST",
        "last_name": "Doe",
        "password": "1234",
        "role": "senior",
    }

    response = requests.post(url, json=payload)

    user_id = response.json().get("id")
    assert user_id is not None, "ID пользователя не найден в ответе"

    assert response.status_code == 201
