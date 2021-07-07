from fastapi import APIRouter, Depends, HTTPException
from fastapi import FastAPI, Depends, status, Response, HTTPException
from .. import schemas, models, hashing, database
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()
get_db = database.get_db

@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_blogs(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy_blogs(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return Response('done')

@router.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blogs(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {id} is not available")   
    blog.update(request.dict())
    db.commit()
    return "updated"

@router.get('/blog/{id}',status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def get_blog_per_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {id} is not available")
    return blog
