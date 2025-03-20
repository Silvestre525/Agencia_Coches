from pydantic import BaseModel


#Schema para el Post de un coche
class AutoCreate(BaseModel):
    marca = str
    modelo = str
    ano = int
    preco = float



#Schema para el Get de un coche
class Auto(BaseModel):
    id: int
    marca: str
    modelo: str
    ano: int
    preco: float

    class Config:
        from_atributes = True   #habilita la compatibilidad del ORM