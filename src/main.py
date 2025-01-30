from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from setup_config import settings

from .modules.chat.routers import chat_router


app = FastAPI(
    title="App Chat bot",
    version="v1.0",
    docs_url=f"/{settings.PATH_API}/docs",
    redoc_url=f"/{settings.PATH_API}/redoc",
)


origins = [
    settings.CLIENT_ORIGIN,
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router.router, tags=['chat'], prefix=f'/{settings.PATH_API}/chat')
