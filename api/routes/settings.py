"""Routes for file operations.

Routes:
    - /settings: GET - Return a list of all settings.
    - /settings: POST - Update a setting by ID (request body is a setting name/value pair).
"""

from fastapi import APIRouter
from pydantic import BaseModel
from utils.logger import get_logger

from api.models.setting import Setting

logger = get_logger(__name__)
router = APIRouter()


# START Route models
class ProcessSettingRequest(BaseModel):
    """Model for a setting name."""

    name: str
    value: str


# END Route Models


# START Routes
@router.get("/settings", response_model=list[Setting])
def get_all_settings():
    """Return a list of all settings."""
    return Setting.get_settings()


@router.post("/settings")
def update_setting(request: ProcessSettingRequest):
    """Update a setting by ID."""
    name = request.name
    value = request.value

    setting = Setting(key=name, value=value)
    setting.save()
    return {"message": f"Setting {name} updated to {value}."}


# END Routes
