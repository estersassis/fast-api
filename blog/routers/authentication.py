from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, hashing, database
from ..hashing import Hash
from sqlalchemy.orm import Session

get_db = database.get_db
router = APIRouter(
    prefix="/login",
    tags=['Login']
)

@router.post('/')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")   
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")  
    return user