from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    project_type: str
    maturity: str
    status: str
    description: Optional[str] = None
    readme_path: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_date: date

    model_config = ConfigDict(from_attributes=True) 