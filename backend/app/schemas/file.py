from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FileBase(BaseModel):
    filename: str
    size: int
    content_type: Optional[str] = None

class FileCreate(FileBase):
    file_path: str
    user_id: Optional[int] = None

class File(FileBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FileResponse(FileBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
