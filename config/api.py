from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI

api = NinjaAPI(urls_namespace="api", docs_decorator=staff_member_required)

api.add_router("/users/", "browniebrokedrftoninja.users.api.views.router")
