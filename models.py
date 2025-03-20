from sqlalchemy import Column, Integer, String, Float
from database import Base

class Auto(Base):
    __tablename__ = 'autos'

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, index=True, nullable=False)
    modelo = Column(String, index=True, nullable=False)
    anio = Column(Integer, index=True, nullable=False)
    precio = Column(Float, index=True, nullable=False)
