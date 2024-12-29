from ninja import NinjaAPI

api = NinjaAPI(urls_namespace="api")

api.add_router("/users/", "browniebrokedrftoninja.users.api.views.router")
