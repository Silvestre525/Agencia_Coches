from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Auto
from schemas import AutoCreate,AutoRead
from database import SessionLocal, engine, Base
import time

app = FastAPI()

@app.on_event("startup")
def startup_event():
    """Espera un momento (por si acaso) y crea las tablas."""
    print("Intentando conectar a la DB y crear tablas...")
    
    # Simple bucle de reintento en Python (más legible que shell)
    max_retries = 10
    retry_delay = 2  # segundos

    for i in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("Conexión exitosa y tablas verificadas/creadas.")
            return # Salir del bucle si es exitoso
        except Exception as e:
            print(f"Error de conexión a la DB (Intento {i+1}/{max_retries}): {e}")
            if i < max_retries - 1:
                time.sleep(retry_delay)
            else:
                # Si falla el último intento, levantamos la excepción fatal
                raise e


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
    new_auto = Auto(marca=auto.marca,modelo=auto.modelo,anio=auto.anio,precio=auto.preco)
    db.add(new_auto)
    db.commit()
    db.refresh(new_auto)
    return new_auto

#Put
@app.put('/autos/update/{auto_id}', response_model=AutoCreate)
def updateAuto(auto_id:int, auto:AutoCreate, db:Session=Depends(get_db)):
    auto_update = db.query(Auto).filter(Auto.id == auto_id).first()

    if auto_update is None:
        raise HTTPException(status_code=404,detail='Auto not found')

    auto_update.marca = auto.marca
    auto_update.modelo = auto.modelo
    auto_update.anio = auto.anio 
    auto_update.precio = auto.precio

    db.commit()
    db.refresh(auto_update)

    return auto_update

#Delete
@app.delete('/autos/delete/{auto_id}')
def deleteAuto(auto_id:int, db:Session=Depends(get_db)):
    auto_delete = db.query(Auto).filter(Auto.id == auto_id).first()

    if auto_delete is None:
        raise HTTPException(status_code=404,detail='Auto not found')
    db.delete(auto_delete)
    db.commit()
    return {'message':'Auto deleted'}               

