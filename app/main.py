from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db import get_db, Base, engine
from app.models import Image
from app import schemas, crud
from app.utils import upload_file_to_s3, generate_clean_filename
from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME, AWS_REGION
from app.crud import delete_image
import boto3

import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

@app.post("/projects", response_model=schemas.ProjectOut)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project)

@app.get("/projects", response_model=list[schemas.ProjectOut])
def list_all_projects(db: Session = Depends(get_db)):
    return crud.list_projects(db)

@app.get("/images", response_model=list[schemas.ImageOut])
def get_images(project_id: int, db: Session = Depends(get_db)):
    return crud.get_images_for_project(db, project_id)


@app.delete("/images/{image_id}")
def delete_image_endpoint(image_id: int, db: Session = Depends(get_db)):
    # Fetch the image record from the database
    image = db.query(Image).filter(Image.image_id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Extract the S3 object key from the image URL

    image_url_parts = image.image_url.split("/")
    s3_key = "/".join(image_url_parts[3:])

    # Delete the image from S3
    try:
        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete image from S3: {e}")

    # Delete the image record from the database
    deleted_image = delete_image(db, image_id)
    if not deleted_image:
        raise HTTPException(status_code=500, detail="Failed to delete image record from database")

    return {"detail": "Image deleted successfully", "image_id": image_id}

@app.post("/images/upload", response_model=schemas.ImageOut)
async def upload_image(project_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):

    project = db.query(crud.models.Project).filter_by(project_id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    new_filename = generate_clean_filename(file.filename)

    file_content = await file.read()
    content_type = file.content_type

    # Upload to S3
    img_url = upload_file_to_s3(file_content, content_type, new_filename)

    # Store URL in DB
    image_data = schemas.ImageCreate(project_id=project_id, image_url=img_url)
    db_image = crud.create_image(db, image_data)
    return db_image

@app.post("/annotations", response_model=schemas.AnnotationOut)
def create_annotation(annotation: schemas.AnnotationCreate, db: Session = Depends(get_db)):
    return crud.create_annotation(db, annotation)

@app.get("/annotations", response_model=list[schemas.AnnotationOut])
def get_annotations(project_id: int, db: Session = Depends(get_db)):
    return crud.get_annotations_for_project(db, project_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
