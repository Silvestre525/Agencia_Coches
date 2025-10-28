from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from models import Auto
from schemas import AutoCreate,AutoRead
from database import SessionLocal, engine, Base
from db_init import initialize_db_and_seed

app = FastAPI()
router = APIRouter(prefix="/api")

@app.on_event("startup")
def startup_event():
     initialize_db_and_seed()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Get
@router.get('/autos/', response_model=list[AutoRead], tags=["Autos"])
def getAutos(db:Session = Depends(get_db)):
    autos = db.query(Auto).all()
    return autos

#GetForId
@router.get('/autos/{auto_id}',response_model=AutoRead, tags=["Autos"])
def getAuto(auto_id:int, db:Session=Depends(get_db)):
    auto = db.query(Auto).filter(Auto.id == auto_id).first()
    if auto is None:
        raise HTTPException(status_code=404, detail='Auto not found')
    return auto

#Post
@router.post('/autos/',response_model=AutoRead, tags=["Autos"])
def addAuto(auto:AutoCreate, db:Session=Depends(get_db)):
    new_auto = Auto(marca=auto.marca,modelo=auto.modelo,anio=auto.anio,precio=auto.precio)
    db.add(new_auto)
    db.commit()
    db.refresh(new_auto)
    return new_auto

#Put
@router.put('/autos/{auto_id}', response_model=AutoRead, tags=["Autos"])
def updateAuto(auto_id:int, auto:AutoCreate, db:Session=Depends(get_db)):
    auto_update = db.query(Auto).filter(Auto.id == auto_id).first()

    if auto_update is None:
        raise HTTPException(status_code=404,detail='Auto not found')

    auto_data = auto.dict()
    for key, value in auto_data.items():
        setattr(auto_update, key, value)

    db.commit()
    db.refresh(auto_update)

    return auto_update

#Delete
@router.delete('/autos/{auto_id}', tags=["Autos"])
def deleteAuto(auto_id:int, db:Session=Depends(get_db)):
    auto_delete = db.query(Auto).filter(Auto.id == auto_id).first()

    if auto_delete is None:
        raise HTTPException(status_code=404,detail='Auto not found')
    db.delete(auto_delete)
    db.commit()
    return {'message':'Auto deleted'}

app.include_router(router)
