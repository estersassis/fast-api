from fastapi import APIRouter, Depends, HTTPException
from fastapi import FastAPI, Depends, status, Response, HTTPException
from .. import schemas, models, hashing, database, oaut2
from sqlalchemy.orm import Session
from typing import List
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)
get_db = database.get_db

@router.get('/', response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(oaut2.get_current_user)):
    return blog.get_all(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blogs(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oaut2.get_current_user)):
   return blog.create(request, db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy_blogs(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oaut2.get_current_user)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return Response('done')

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blogs(id, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oaut2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {id} is not available")   
    blog.update(request.dict())
    db.commit()
    return "updated"

@router.get('/{id}',status_code=200, response_model=schemas.ShowBlog)
def get_blog_per_id(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oaut2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {id} is not available")
    return blog
