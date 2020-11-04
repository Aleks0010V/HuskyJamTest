import uvicorn

from fastapi import FastAPI, Depends

from api import users, scheduler
from auth import oauth2_scheme

app = FastAPI()
app.include_router(users.router,
                   prefix='/users'
                   )
app.include_router(scheduler.router,
                   prefix='/schedule',
                   dependencies=[Depends(oauth2_scheme)]
                   )


if __name__ == '__main__':
    uvicorn.run("main:app", port=80, reload=True)
