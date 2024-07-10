from sqlalchemy import Column, String, Text

from app.models.abstract import AbstractModel


class CharityProject(AbstractModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
