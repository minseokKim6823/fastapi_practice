from fastapi import FastAPI
from model.settings import create_db_and_tables
from controller.board_router import router as board_router
from controller.login_router import router as login_router
from controller.account_router import router as account_router


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(board_router)
app.include_router(login_router)
app.include_router(account_router)
