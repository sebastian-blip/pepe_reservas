import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from config import get_config_env
from routers.auth.auth import auth_router


app = FastAPI(
    title='Reservas_pepe',
    version='0.1.0',
    docs_url=get_config_env().docs_url,
    redoc_url=get_config_env().redoc_url,
)

app.mount("/static", StaticFiles(directory="public/static",  html=True), name='static')

origins = get_config_env().URL_ALLLOWED_CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run(app)
