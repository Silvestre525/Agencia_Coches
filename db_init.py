import time
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Auto
from sqlalchemy.exc import OperationalError

def seed_data(db: Session):
    """Inserta autos de prueba si la tabla está vacía."""
    
    
    if db.query(Auto).count() == 0:
        print("— Insertando datos de prueba (seed data)...")
        
        autos_test = [
            Auto(marca="Toyota", modelo="Corolla", anio=2022, precio=25000.00),
            Auto(marca="Ford", modelo="Focus", anio=2021, precio=19000.50),
            Auto(marca="Chevrolet", modelo="Cruze", anio=2023, precio=28000.00),
        ]
        
        db.add_all(autos_test)
        db.commit()
        print("— 3 autos de prueba insertados exitosamente.")
    else:
        print("— La tabla 'autos' ya contiene datos, omitiendo seed data.")


def initialize_db_and_seed():
    """Maneja el bucle de reintento, crea tablas e inserta datos."""
    print("Intentando conectar a la DB y crear tablas...")
    
    max_retries = 10
    retry_delay = 2 

    for i in range(max_retries):
        try:
            
            Base.metadata.create_all(bind=engine)
            print("Conexión exitosa y tablas verificadas/creadas.")
            
            
            db = SessionLocal()
            seed_data(db)
            db.close()
            
            return 
        
        except OperationalError as e:
            
            print(f"Error de conexión a la DB (Intento {i+1}/{max_retries}): {e}")
            if i < max_retries - 1:
                time.sleep(retry_delay)
            else:
                
                raise e
        except Exception as e:
            
            print(f"Error de inicialización (Intento {i+1}/{max_retries}): {e}")
            if i < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise e