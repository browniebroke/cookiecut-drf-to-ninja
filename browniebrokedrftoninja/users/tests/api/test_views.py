import pytest
from django.test import Client
from django.urls import reverse_lazy

from browniebrokedrftoninja.users.models import User
from browniebrokedrftoninja.users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


@pytest.fixture()
def user():
    return UserFactory()


def test_list_users_as_anonymous_user(client: Client):
    response = client.get(reverse_lazy("api:list_users"))

    assert response.status_code == 200
    assert response.json() == []


def test_list_users_as_authenticated_user(client: Client, user: User):
    client.force_login(user)
    # Another user, excluded from the response
    UserFactory()

    response = client.get(reverse_lazy("api:list_users"))

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": user.name,
            "url": f"/api/users/{user.username}/",
            "username": user.username,
        },
    ]


@pytest.mark.parametrize("username", [None, "me"])
def test_retrieve_user(client: Client, user: User, username: str | None):
    client.force_login(user)
    username = username or user.username

    response = client.get(
        reverse_lazy("api:retrieve_user", kwargs={"username": username})
    )

    assert response.status_code == 200
    assert response.json() == {
        "name": user.name,
        "url": f"/api/users/{user.username}/",
        "username": user.username,
    }


def test_retrieve_another_user(client: Client, user: User):
    client.force_login(user)
    user_2 = UserFactory()

    response = client.get(
        reverse_lazy("api:retrieve_user", kwargs={"username": user_2.username})
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_update_user(client: Client):
    user = UserFactory(name="Old", username="old")
    client.force_login(user)

    response = client.patch(
        reverse_lazy("api:update_user", kwargs={"username": "old"}),
        data='{"name": "New Name"}',
        content_type="application/json",
    )

    assert response.status_code == 200, response.json()
    assert response.json() == {
        "name": "New Name",
        "url": "/api/users/old/",
        "username": "old",
    }
