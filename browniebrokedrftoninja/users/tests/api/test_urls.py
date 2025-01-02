from django.urls import reverse, resolve

from browniebrokedrftoninja.users.models import User


def test_user_detail(user: User):
    assert (
        reverse("api:retrieve_user", kwargs={"username": user.username})
        == f"/api/users/{user.username}/"
    )
    assert resolve(f"/api/users/{user.username}/").view_name == "api:retrieve_user"


def test_user_list():
    assert reverse("api:list_users") == "/api/users/"
    assert resolve("/api/users/").view_name == "api:list_users"


def test_user_me():
    assert reverse("api:retrieve_user", kwargs={"username": "me"}) == "/api/users/me/"
    assert resolve("/api/users/me/").view_name == "api:retrieve_user"


def test_update_user():
    assert reverse("api:update_user", kwargs={"username": "me"}) == "/api/users/me/"
    assert resolve("/api/users/me/").view_name == "api:retrieve_user"
