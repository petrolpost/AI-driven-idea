import datetime
from sqlalchemy import Column, Integer, String, Date, Text
from pydantic import BaseModel, ConfigDict
from .database import Base # Import Base from database.py

# SQLAlchemy Model
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    project_type = Column(String)
    maturity = Column(String)
    status = Column(String)
    description = Column(Text)
    readme_path = Column(String, nullable=False, unique=True)
    created_date = Column(Date, default=datetime.date.today)

# Pydantic Schemas
class ProjectBase(BaseModel):
    name: str
    project_type: str | None = None
    maturity: str | None = None
    status: str | None = None
    description: str | None = None
    readme_path: str
    created_date: datetime.date | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

