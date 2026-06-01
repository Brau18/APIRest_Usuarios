from pydantic import BaseModel,Field
from datetime import date
from typing import Optional,List
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
class DocenteCreate(BaseModel):
    idUsuario:int
    gradoEstudio:str
    fechaIngreso:date
    correoInstitucional:str
    horasFrenteAlGrupo:int=Field(...,ge=0)
    horasDocencia:int=Field(...,ge=0)
    horasAdministrativas:int=Field(...,ge=0)
    tipoContrato:str
class DocenteUpdate(BaseModel):
    gradoEstudio:Optional[str]=None
    estadoLaboral:Optional[str]=None
    correoInstitucional:Optional[str]=None
    horasFrenteAlGrupo:Optional[int]=Field(None,ge=0)
    horasDocencia:Optional[int]=Field(None,ge=0)
    horasAdministrativas:Optional[int]=Field(None,ge=0)
    tipoContrato:Optional[str]=None
class Docente(BaseModel):
    idDocente:int
    idUsuario:int
    gradoEstudio:str
    fechaIngreso:date
    estadoLaboral:str
    correoInstitucional:str
    horasFrenteAlGrupo:int
    horasDocencia:int
    horasAdministrativas:int
    tipoContrato:str
class DocenteSalida(BaseModel):
    codigo:int
    mensaje:str
    docente:Docente|None=None
class Carrera(BaseModel):
    idCarrera:int
    nombreCarrera:str
    descripcion:str|None=None
    activo:int
class CarreraSalida(BaseModel):
    codigo:int
    mensaje:str
    carrera:Carrera|None=None
class DocenteCarreraCreate(BaseModel):
    idDocente:int
    idCarrera:int
class DocenteCarreraUpdate(BaseModel):
    idCarrera:int
    fechaAsignacion:date
class HabilidadCreate(BaseModel):
    idDocente:int
    nombreCurso:str
    tipoCertificado:str
    institucionEmisora:str
    fechaObtencion:date
    fechaVigencia:date
    descripcion:Optional[str]=None
    nivel:str
class HabilidadUpdate(BaseModel):
    nombreCurso:Optional[str]=None
    tipoCertificado:Optional[str]=None
    institucionEmisora:Optional[str]=None
    fechaVigencia:Optional[date]=None
    descripcion:Optional[str]=None
    nivel:Optional[str]=None
class Habilidad(BaseModel):
    idHabilidad:int
    idDocente:int
    nombreCurso:str
    tipoCertificado:str
    institucionEmisora:str
    fechaObtencion:date
    fechaVigencia:date
    descripcion:str|None=None
    nivel:str
    activo:int
class HabilidadSalida(BaseModel):
    codigo:int
    mensaje:str
    habilidad:Habilidad|None=None
class HabilidadVigente(BaseModel):
    idHabilidad:int
    nombreCurso:str
    tipoCertificado:str
    fechaVigencia:date
    nivel:str
class HabilidadesVigentesSalida(BaseModel):
    codigo:int
    mensaje:str
    habilidades:List[HabilidadVigente]|None=None
class Asignacion(BaseModel):
    idDocente:int
    idCarrera:int
    fechaAsignacion:date
    nombreDocente:str
    nombreCarrera:str
class AsignacionSalida(BaseModel):
    codigo:int
    mensaje:str
    asignacion:Asignacion|None=None
