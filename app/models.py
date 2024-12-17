from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    images = relationship("Image", back_populates="project")

class Image(Base):
    __tablename__ = "images"
    image_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="images")
    annotations = relationship("Annotation", back_populates="image")

class Annotation(Base):
    __tablename__ = "annotations"
    annotation_id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.image_id"))
    annotation_data = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    image = relationship("Image", back_populates="annotations")
