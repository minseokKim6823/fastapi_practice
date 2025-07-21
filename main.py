from fastapi import FastAPI

from controller.template_container_router import router as template_container_router
from model.settings import create_db_and_tables
from service.update_time_service import register_timestamp_events
from controller.template_router import router as template_router
from controller.template_run_router import router as template_run_router
from controller.template_group_router import router as template_group_router
from boundary_ocr.controller.classify_router import router as classify_router
from boundary_ocr.controller.boundary_router import router as boundary_router

app = FastAPI(root_path="/template")


@app.on_event("startup")
def on_startup():
    register_timestamp_events()
    create_db_and_tables()

app.include_router(template_router)
app.include_router(template_group_router)
app.include_router(template_container_router)
# app.include_router(login_router)
# app.include_router(account_router)
app.include_router(template_run_router)
app.include_router(classify_router)
app.include_router(boundary_router)