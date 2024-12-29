from django.shortcuts import get_object_or_404
from ninja import Router

from browniebrokedrftoninja.users.api.schema import UserSchema
from browniebrokedrftoninja.users.models import User

router = Router(tags=["users"])


@router.get('/', response=list[UserSchema])
def list_users(request):
    users_qs = User.objects.filter(username=request.user.username)
    return users_qs


@router.get('/{username}', response=UserSchema)
def retrieve_user(request, username: str):
    return get_object_or_404(User, username=username)


@router.get('/me', response=UserSchema)
def retrieve_current_user(request):
    return request.user


@router.patch('/{username}')
def update_user(request, username: str, data: UserSchema):
    ...
