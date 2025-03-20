from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Auto
from schemas import AutoCreate,AutoRead
from database import SessionLocal, engine, Base

#Crear la tabla en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Get
@app.get('/autos/', response_model=list[AutoRead])
def getAutos(db:Session = Depends(get_db)):
    autos = db.query(Auto).all()
    return autos

#GetForId
@app.get('/autos/{auto_id}',response_model=AutoRead)
def getAuto(auto_id:int, db:Session=Depends(get_db)):
    auto = db.query(Auto).filter(Auto.id == auto_id).first()
    if auto is None:
        raise HTTPException(status_code=404, detail='Auto not found')
    return auto

#Post
@app.post('/autos/add',response_model=AutoCreate)
def addAuto(auto:AutoCreate, db:Session=Depends(get_db)):
    new_auto = Auto(marca=auto.marca,modelo=auto.modelo,anio=auto.ano,precio=auto.preco)
    db.add(new_auto)
    db.commit()
    db.refresh(new_auto)
    return new_auto

#Put
@app.put('autos/update/{auto_id}', response_model=AutoCreate)
def updateAuto(auto_id:int, auto:AutoCreate, db:Session=Depends(get_db)):
    auto_update = db.query(Auto).filter(Auto.id == auto_id).first()

    if auto_update is None:
        return HTTPException(status_code=404,detail='Auto not found')

    auto_update.marca = auto.marca
    auto_update.modelo = auto.modelo
    auto_update.anio = auto.ano 
    auto_update.precio = auto.preco

    db.commit()
    db.refresh(auto_update)

    return auto_update

#Delete
@app.delete('/autos/delete/{auto_id}')
def deleteAuto(auto_id:int, db:Session=Depends(get_db)):
    auto_delete = db.query(Auto).filter(Auto.id == auto_id).first()

    if auto_delete is None:
        return HTTPException(status_code=404,detail='Auto not found')
    db.delete(auto_delete)
    db.commit()
    return {'message':'Auto deleted'}               