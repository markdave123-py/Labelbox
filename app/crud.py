from sqlalchemy.orm import Session
from app import models, schemas
from app.models import Image
import json

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(name=project.name, description=project.description)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_image(db: Session, image_id: int):
    image = db.query(Image).filter(Image.image_id == image_id).first()
    if not image:
        return None
    db.delete(image)
    db.commit()
    return image


def list_projects(db: Session):
    return db.query(models.Project).all()

def create_image(db: Session, image: schemas.ImageCreate):
    db_image = models.Image(
        project_id=image.project_id,
        image_url=image.image_url
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_images_for_project(db: Session, project_id: int):
    return db.query(models.Image).filter(models.Image.project_id == project_id).all()

def create_annotation(db: Session, annotation: schemas.AnnotationCreate):
    db_annotation = models.Annotation(
        image_id=annotation.image_id,
        annotation_data=json.dumps(annotation.annotation_data)
    )
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation

def get_annotations_for_project(db: Session, project_id: int):
    return (db.query(models.Annotation)
            .join(models.Image)
            .filter(models.Image.project_id == project_id)
            .all())
