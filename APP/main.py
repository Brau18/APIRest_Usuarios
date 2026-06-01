from fastapi import FastAPI,Request
from models import UsuarioCreate,UsuarioUpdate,Salida,UsuarioSalida,CarreraCreate,CarreraUpdate,DocenteCarreraCreate,DocenteCarreraUpdate,DocenteCreate,DocenteSalida,DocenteUpdate,CarreraSalida,HabilidadCreate,HabilidadUpdate,HabilidadSalida,HabilidadesVigentesSalida,AsignacionSalida
import uvicorn
from dao import Conexion,UsuarioDAO,CarreraDAO,DocenteDAO,DocenteCarreraDAO,HabilidadDAO
app=FastAPI()

@app.get("/",tags=["Inicio"],summary="Home")
def home():
    return "Bienvenido a la APIRest de Proyecto BD"
@app.post("/usuarios",tags=["Usuarios"],summary="Crear Usuario",response_model=Salida)
async def crearUsuario(request:Request,usuario:UsuarioCreate)->Salida:
    usuarioDAO=UsuarioDAO(request.app.cn.db)
    return usuarioDAO.agregar(usuario)
@app.get("/usuarios/{idUsuario}",tags=["Usuarios"],summary="Consultar Usuario",response_model=UsuarioSalida)
def consultarUsuario(request:Request,idUsuario:int)->UsuarioSalida:
    usuarioDAO=UsuarioDAO(request.app.cn.db)
    return usuarioDAO.consultaPorID(idUsuario)
@app.put("/usuarios/{idUsuario}",tags=["Usuarios"],summary="Modificar Usuario",response_model=Salida)
def modificarUsuario(request:Request,idUsuario:int,usuario:UsuarioUpdate)->Salida:
    usuarioDAO=UsuarioDAO(request.app.cn.db)
    return usuarioDAO.modificar(idUsuario,usuario)
@app.delete("/usuarios/{idUsuario}",tags=["Usuarios"],summary="Cancelar Usuario",response_model=Salida)
def cancelarUsuario(request:Request,idUsuario:int)->Salida:
    usuarioDAO=UsuarioDAO(request.app.cn.db)
    return usuarioDAO.cancelar(idUsuario)
@app.post("/carreras",tags=["Carreras"],summary="Crear Carrera",response_model=Salida)
async def crearCarrera(request:Request,carrera:CarreraCreate)->Salida:
    carreraDAO=CarreraDAO(request.app.cn.db)
    return carreraDAO.agregar(carrera)
@app.put("/carreras/{idCarrera}",tags=["Carreras"],summary="Modificar Carrera",response_model=Salida)
def modificarCarrera(request:Request,idCarrera:int,carrera:CarreraUpdate)->Salida:
    carreraDAO=CarreraDAO(request.app.cn.db)
    return carreraDAO.modificar(idCarrera,carrera)
@app.delete("/carreras/{idCarrera}",tags=["Carreras"],summary="Cancelar Carrera",response_model=Salida)
def cancelarCarrera(request:Request,idCarrera:int)->Salida:
    carreraDAO=CarreraDAO(request.app.cn.db)
    return carreraDAO.cancelar(idCarrera)
@app.get("/carreras/{idCarrera}",tags=["Carreras"],summary="Consultar Carrera",response_model=CarreraSalida)
def consultarCarrera(request:Request,idCarrera:int)->CarreraSalida:
    carreraDAO=CarreraDAO(request.app.cn.db)
    return carreraDAO.consultaPorID(idCarrera)
@app.on_event('startup')
def startup():
    conexion=Conexion()
    app.cn=conexion
@app.on_event('shutdown')
def shutdown():
    app.cn.cerrar()
@app.post("/docentes",tags=["Docentes"],summary="Crear Docente",response_model=Salida)
async def crearDocente(request:Request,docente:DocenteCreate)->Salida:
    docenteDAO=DocenteDAO(request.app.cn.db)
    return docenteDAO.agregar(docente)
@app.get("/docentes/{idDocente}",tags=["Docentes"],summary="Consultar Docente",response_model=DocenteSalida)
def consultarDocente(request:Request,idDocente:int)->DocenteSalida:
    docenteDAO=DocenteDAO(request.app.cn.db)
    return docenteDAO.consultaPorID(idDocente)
@app.put("/docentes/{idDocente}",tags=["Docentes"],summary="Modificar Docente",response_model=Salida)
def modificarDocente(request:Request,idDocente:int,docente:DocenteUpdate)->Salida:
    docenteDAO=DocenteDAO(request.app.cn.db)
    return docenteDAO.modificar(idDocente,docente)
@app.delete("/docentes/{idDocente}",tags=["Docentes"],summary="Cancelar Docente",response_model=Salida)
def cancelarDocente(request:Request,idDocente:int)->Salida:
    docenteDAO=DocenteDAO(request.app.cn.db)
    return docenteDAO.cancelar(idDocente)
@app.post("/docentes-carreras",tags=["Docentes-Carreras"],summary="Crear Asignacion",response_model=Salida)
async def crearAsignacion(request:Request,asignacion:DocenteCarreraCreate)->Salida:
    docenteCarreraDAO=DocenteCarreraDAO(request.app.cn.db)
    return docenteCarreraDAO.agregar(asignacion)
@app.put("/docentes-carreras/{idDocente}/{idCarrera}",tags=["Docentes-Carreras"],summary="Modificar Asignacion",response_model=Salida)
def modificarAsignacion(request:Request,idDocente:int,idCarrera:int,asignacion:DocenteCarreraUpdate)->Salida:
    docenteCarreraDAO=DocenteCarreraDAO(request.app.cn.db)
    return docenteCarreraDAO.modificar(idDocente,idCarrera,asignacion)
@app.delete("/docentes-carreras/{idDocente}/{idCarrera}",tags=["Docentes-Carreras"],summary="Cancelar Asignacion",response_model=Salida)
def cancelarAsignacion(request:Request,idDocente:int,idCarrera:int)->Salida:
    docenteCarreraDAO=DocenteCarreraDAO(request.app.cn.db)
    return docenteCarreraDAO.cancelar(idDocente,idCarrera)
@app.get("/docentes-carreras/{idDocente}/{idCarrera}",tags=["Docentes-Carreras"],summary="Consultar Asignacion",response_model=AsignacionSalida)
def consultarAsignacion(request:Request,idDocente:int,idCarrera:int)->AsignacionSalida:
    docenteCarreraDAO=DocenteCarreraDAO(request.app.cn.db)
    return docenteCarreraDAO.consultaPorID(idDocente,idCarrera)
@app.post("/habilidades",tags=["Habilidades"],summary="Crear Habilidad",response_model=Salida)
async def crearHabilidad(request:Request,habilidad:HabilidadCreate)->Salida:
    habilidadDAO=HabilidadDAO(request.app.cn.db)
    return habilidadDAO.agregar(habilidad)
@app.get("/habilidades/{idHabilidad}",tags=["Habilidades"],summary="Consultar Habilidad",response_model=HabilidadSalida)
def consultarHabilidad(request:Request,idHabilidad:int)->HabilidadSalida:
    habilidadDAO=HabilidadDAO(request.app.cn.db)
    return habilidadDAO.consultaPorID(idHabilidad)
@app.get("/habilidades/vigentes/{idDocente}",tags=["Habilidades"],summary="Consultar Habilidades Vigentes",response_model=HabilidadesVigentesSalida)
def consultarHabilidadesVigentes(request:Request,idDocente:int)->HabilidadesVigentesSalida:
    habilidadDAO=HabilidadDAO(request.app.cn.db)
    return habilidadDAO.consultaVigentes(idDocente)
@app.put("/habilidades/{idHabilidad}",tags=["Habilidades"],summary="Modificar Habilidad",response_model=Salida)
def modificarHabilidad(request:Request,idHabilidad:int,habilidad:HabilidadUpdate)->Salida:
    habilidadDAO=HabilidadDAO(request.app.cn.db)
    return habilidadDAO.modificar(idHabilidad,habilidad)
@app.delete("/habilidades/{idHabilidad}",tags=["Habilidades"],summary="Cancelar Habilidad",response_model=Salida)
def cancelarHabilidad(request:Request,idHabilidad:int)->Salida:
    habilidadDAO=HabilidadDAO(request.app.cn.db)
    return habilidadDAO.cancelar(idHabilidad)

if __name__ == '__main__':
   uvicorn.run("main:app",reload=True)
