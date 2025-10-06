from fastapi import FastAPI

import api.routes as api

app = FastAPI()

app.include_router(api.router)