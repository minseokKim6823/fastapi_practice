from service import template_group_service
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session


from model.settings import get_session

router = APIRouter(prefix="/container", tags=["container"])
