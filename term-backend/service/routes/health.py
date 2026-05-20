from fastapi import status
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class HealthAPI:
    @router.get(
        "/health",
        responses={
            status.HTTP_200_OK: {
                "description": "Successfully retrieved the health status of the service.",
                "content": {"application/json": {"example": {"status": "Ok"}}},
            }
        },
    )
    async def get(self) -> dict[str, str]:
        return {"status": "Ok"}
