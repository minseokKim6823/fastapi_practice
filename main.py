from fastapi import FastAPI
from model.settings import create_db_and_tables
from controller.board_router import router as board_router


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(board_router)