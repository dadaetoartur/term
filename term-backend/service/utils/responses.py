from fastapi_users.router.common import ErrorModel

response_400 = {
    "description": "Недопустимые параметры запроса или нарушение ограничений.",
    "model": ErrorModel,
    "content": {
        "application/json": {
            "example": {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email",
                    }
                ]
            }
        }
    },
}

response_401 = {
    "description": "Отсутствует токен или пользователь неактивен.",
    "model": ErrorModel,
    "content": {"application/json": {"example": {"detail": "Not authenticated"}}},
}

response_403 = {
    "description": "Не является суперпользователем.",
    "model": ErrorModel,
    "content": {"application/json": {"example": {"detail": "Forbidden"}}},
}

response_404 = {
    "description": "Группа или пользователь не найдены.",
    "model": ErrorModel,
    "content": {"application/json": {"example": {"detail": "User not found"}}},
}

response_500 = {
    "description": "Внутренняя ошибка сервера - сервер столкнулся с неожиданным состоянием, "
    "которое помешало ему выполнить запрос.",
    "model": ErrorModel,
    "content": {"application/json": {"example": {"detail": "Internal server error"}}},
}
