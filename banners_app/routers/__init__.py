from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse

from ..schemas.banner_schemas import *
from ..orm.repository import BannerRepository
from ..modules.verify_token import verify_token
