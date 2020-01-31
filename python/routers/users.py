from fastapi import APIRouter

router = APIRouter()

@router.get('/users/find/all', tags=['users'])
async def get_all_users():
    return {'Users': 'A, B'}

@router.get('/users/find/one', tags=['users'])
async def get_one_user():
    return {'user_a': 'bbb'}
