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
    source_url: Optional[str] = None  # 引用原文URL

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_date: date

    model_config = ConfigDict(from_attributes=True)