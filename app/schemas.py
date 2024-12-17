from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectOut(BaseModel):
    project_id: int
    name: str
    description: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True

class ImageCreate(BaseModel):
    project_id: int
    image_url: str

class ImageOut(BaseModel):
    image_id: int
    project_id: int
    image_url: str
    created_at: datetime
    class Config:
        orm_mode = True

class AnnotationCreate(BaseModel):
    image_id: int
    annotation_data: Any  # JSON object

class AnnotationOut(BaseModel):
    annotation_id: int
    image_id: int
    annotation_data: Any
    created_at: datetime
    class Config:
        orm_mode = True
