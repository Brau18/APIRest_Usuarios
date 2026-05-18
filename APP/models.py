from pydantic import BaseModel,Field
from datetime import date
from typing import Optional
class UsuarioCreate(BaseModel):
    nombre:str
    apellidoPaterno:str
    apellidoMaterno:str
    telefono:str
    RFC:str
    CURP:str
    correo:str
    contrasena:str
class UsuarioUpdate(BaseModel):
    nombre:Optional[str]=None
    apellidoPaterno:Optional[str]=None
    apellidoMaterno:Optional[str]=None
    telefono:Optional[str]=None
    correo:Optional[str]=None
class Usuario(BaseModel):
    idUsuario:int
    nombre:str
    apellidoPaterno:str
    apellidoMaterno:str
    telefono:str
    RFC:str
    CURP:str
    correo:str
    activo:int
    fechaRegistro:date
class Salida(BaseModel):
    codigo:int
    mensaje:str
class UsuarioSalida(Salida):
    usuario:Usuario|None=None
class CarreraCreate(BaseModel):
    nombreCarrera:str
    descripcion:Optional[str]=None
class CarreraUpdate(BaseModel):
    nombreCarrera:Optional[str]=None
    descripcion:Optional[str]=None
