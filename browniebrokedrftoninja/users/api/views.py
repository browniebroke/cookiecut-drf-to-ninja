from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from ninja import Router

from browniebrokedrftoninja.users.api.schema import UserSchema, UpdateUserSchema
from browniebrokedrftoninja.users.models import User

router = Router(tags=["users"])


def _get_users_queryset(request) -> QuerySet[User]:
    return User.objects.filter(username=request.user.username)


@router.get("/", response=list[UserSchema])
def list_users(request):
    return _get_users_queryset(request)


@router.get("/{username}/", response=UserSchema)
def retrieve_user(request, username: str):
    if username == "me":
        return request.user
    else:
        users_qs = _get_users_queryset(request)
        return get_object_or_404(users_qs, username=username)


@router.patch("/{username}/", response=UserSchema)
def update_user(request, username: str, data: UpdateUserSchema):
    users_qs = _get_users_queryset(request)
    user = get_object_or_404(users_qs, username=username)
    user.name = data.name
    user.save()
    return user
