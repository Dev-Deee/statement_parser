from fastapi import FastAPI

from statement_parser.config import health

app = FastAPI(title="Statement Parser")
app.include_router(health.router)