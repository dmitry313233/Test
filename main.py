from fastapi_users import FastAPIUsers
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.database import User, get_async_session
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate


app = FastAPI(
    title="GPT App"
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(   # Создаем роутеры для входа и вахода пользователя
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(   # Создаём роутер для регистрации пользователя
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/user/{user_id}")
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.get(User, user_id)  # извлекаем пользователя из базы данных по его id
    if user:
        user_data = {
            "username": user.username,
            "email": user.email
        }
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User not found")
