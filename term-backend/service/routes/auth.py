from fastapi_restful.inferring_router import InferringRouter

from service.dependencies import get_auth_backend, get_fastapi_users

router = InferringRouter()

fastapi_users = get_fastapi_users()
auth_backend = get_auth_backend()
current_superuser = fastapi_users.current_user(active=True, superuser=True)


router.include_router(fastapi_users.get_auth_router(auth_backend, requires_verification=False))
