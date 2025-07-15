# main.py

from fastapi import FastAPI
from routers import reports, channels, search

app = FastAPI(title="Telegram Analytics API")

app.include_router(reports.router)
app.include_router(channels.router)
app.include_router(search.router)
