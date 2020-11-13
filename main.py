import uvicorn

from fastapi import FastAPI, Depends

from api import users, scheduler, admin
from database.database import db
from auth import Security, check_admin_role


app = FastAPI()
app.include_router(users.router,
                   prefix='/users'
                   )
app.include_router(scheduler.router,
                   prefix='/schedule',
                   dependencies=[Depends(Security.get_user_by_token)]
                   )
app.include_router(admin.router,
                   prefix='/admin',
                   dependencies=[Depends(check_admin_role)]
                   )


@app.on_event("shutdown")
async def shutdown():
    if db.is_connected:
        await db.disconnect()


if __name__ == '__main__':
    uvicorn.run("main:app", port=80, reload=True)
