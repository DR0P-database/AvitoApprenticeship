from fastapi import HTTPException


def verify_token(token, is_user=False):
    if token is None or not token:
        raise HTTPException(
            status_code=401, detail='Пользователь не авторизован')
    if token != 'admin_token' and (not is_user or token != 'user_token'):
        raise HTTPException(
            status_code=403, detail='Пользователь не имеет доступа')
