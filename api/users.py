from fastapi import APIRouter

router = APIRouter()


@router.get('/users/', tags=['users'])
async def create_user():
    pass


@router.get('/users/{username}', tags=['users'])
async def change_password(username: str):
    pass


@router.get('/users/login', tags=['users'])
async def login():
    pass
