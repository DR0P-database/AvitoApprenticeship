from fastapi.responses import JSONResponse
from . import *


def verify_token(token, is_user_allow=False):
    if token is None or not token:
        raise HTTPException(
            status_code=401, detail='Пользователь не авторизован')
    if not is_user_allow or token != 'user_token':
        if token != 'admin_token':
            raise HTTPException(
                status_code=403, detail='Пользователь не имеет доступа')
        else:
            return True  # Токен для админа

    return False  # user_token или кого-то другого
