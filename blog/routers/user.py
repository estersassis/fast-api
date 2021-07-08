from fastapi import APIRouter, Depends, HTTPException
from fastapi import FastAPI, Depends, status, Response, HTTPException
from .. import schemas, models, hashing, database
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/user",
    tags=['Users']
)
get_db = database.get_db

@router.post('/', response_model=schemas.ShowUser)
def create_user(request:schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypting(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get_user_per_id(id, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} doesn't exist")
    return user