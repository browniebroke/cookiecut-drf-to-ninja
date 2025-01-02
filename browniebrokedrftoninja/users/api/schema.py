from django.urls.base import reverse
from ninja import ModelSchema

from browniebrokedrftoninja.users.models import User


class UpdateUserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["name"]


class UserSchema(ModelSchema):
    url: str

    class Meta:
        model = User
        fields = ["username", "name"]

    @staticmethod
    def resolve_url(obj: User):
        return reverse("api:retrieve_user", kwargs={"username": obj.username})
