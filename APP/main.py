from fastapi import FastAPI,Request,Depends,HTTPException,status
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.extension import _rate_limit_exceeded_handler
from models import (UsuarioCreate,UsuarioUpdate,Salida,UsuarioSalida,
                    CarreraCreate,CarreraUpdate,DocenteCarreraCreate,DocenteCarreraUpdate,
                    DocenteCreate,DocenteSalida,DocenteUpdate,CarreraSalida,
                    HabilidadCreate,HabilidadUpdate,HabilidadSalida,HabilidadesVigentesSalida,
                    AsignacionesSalida,Usuario)
from dao import Conexion,UsuarioDAO,CarreraDAO,DocenteDAO,DocenteCarreraDAO,HabilidadDAO
from security import RoleChecker
import uvicorn

app=FastAPI()
limiter=Limiter(key_func=get_remote_address)
app.state.limiter=limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

# Inicio

@app.get("/",tags=["Inicio"],summary="Home")
def home():
    return "Bienvenido a la APIRest de Proyecto BD"

# Usuarios

@app.post("/usuarios",tags=["Usuarios"],summary="Crear Usuario",response_model=Salida)
@limiter.limit("10/minute")
async def crearUsuario(request:Request,usuario:UsuarioCreate,
                       _:Usuario=Depends(RoleChecker(["Admin"]))):
    usuarioDAO=UsuarioDAO(request.app.cn.db)
    return usuarioDAO.agregar(usuario)

@app.get("/usuarios/{idUsuario}",tags=["Usuarios"],summary="Consultar Usuario",response_model=UsuarioSalida)
@limiter.limit("10/minute")
async def consultarUsuario(request:Request,idUsuario:int,
                           _:Usuario=Depends(RoleChecker(["Admin","Coordinador","Docente"]))):
    usuarioDAO=UsuarioDAO(request.app.cn.db)
    return usuarioDAO.consultaPorID(idUsuario)

@app.put("/usuarios/{idUsuario}",tags=["Usuarios"],summary="Modificar Usuario",response_model=Salida)
@limiter.limit("10/minute")
async def modificarUsuario(request:Request,idUsuario:int,usuario:UsuarioUpdate,
                           _:Usuario=Depends(RoleChecker(["Admin"]))):
    usuarioDAO=UsuarioDAO(request.app.cn.db)
    return usuarioDAO.modificar(idUsuario,usuario)

@app.delete("/usuarios/{idUsuario}",tags=["Usuarios"],summary="Cancelar Usuario",response_model=Salida)
@limiter.limit("10/minute")
async def cancelarUsuario(request:Request,idUsuario:int,
                          _:Usuario=Depends(RoleChecker(["Admin"]))):
    usuarioDAO=UsuarioDAO(request.app.cn.db)
    return usuarioDAO.cancelar(idUsuario)

# Docentes

@app.post("/docentes",tags=["Docentes"],summary="Crear Docente",response_model=Salida)
@limiter.limit("10/minute")
async def crearDocente(request:Request,docente:DocenteCreate,
                       _:Usuario=Depends(RoleChecker(["Admin","Coordinador"]))):
    docenteDAO=DocenteDAO(request.app.cn.db)
    return docenteDAO.agregar(docente)

@app.get("/docentes/{idDocente}",tags=["Docentes"],summary="Consultar Docente",response_model=DocenteSalida)
@limiter.limit("10/minute")
async def consultarDocente(request:Request,idDocente:int,
                           _:Usuario=Depends(RoleChecker(["Admin","Coordinador","Docente"]))):
    docenteDAO=DocenteDAO(request.app.cn.db)
    return docenteDAO.consultaPorID(idDocente)

@app.put("/docentes/{idDocente}",tags=["Docentes"],summary="Modificar Docente",response_model=Salida)
@limiter.limit("10/minute")
async def modificarDocente(request:Request,idDocente:int,docente:DocenteUpdate,
                           user:Usuario=Depends(RoleChecker(["Admin","Coordinador","Docente"]))):
    if user.rol=="Docente":
        cursor=request.app.cn.db.cursor(dictionary=True)
        cursor.execute("select idDocente from docentes where idUsuario=%s",(user.idUsuario,))
        doc=cursor.fetchone()
        cursor.close()
        if not doc or doc["idDocente"]!=idDocente:
            raise HTTPException(status.HTTP_403_FORBIDDEN,detail="Sin autorización.")
    docenteDAO=DocenteDAO(request.app.cn.db)
    return docenteDAO.modificar(idDocente,docente)

@app.delete("/docentes/{idDocente}",tags=["Docentes"],summary="Cancelar Docente",response_model=Salida)
@limiter.limit("10/minute")
async def cancelarDocente(request:Request,idDocente:int,
                          _:Usuario=Depends(RoleChecker(["Admin"]))):
    docenteDAO=DocenteDAO(request.app.cn.db)
    return docenteDAO.cancelar(idDocente)

# Carreras

@app.post("/carreras",tags=["Carreras"],summary="Crear Carrera",response_model=Salida)
@limiter.limit("10/minute")
async def crearCarrera(request:Request,carrera:CarreraCreate,
                       _:Usuario=Depends(RoleChecker(["Admin","Coordinador"]))):
    carreraDAO=CarreraDAO(request.app.cn.db)
    return carreraDAO.agregar(carrera)

@app.get("/carreras/{idCarrera}",tags=["Carreras"],summary="Consultar Carrera",response_model=CarreraSalida)
@limiter.limit("10/minute")
async def consultarCarrera(request:Request,idCarrera:int,
                           _:Usuario=Depends(RoleChecker(["Admin","Coordinador","Docente"]))):
    carreraDAO=CarreraDAO(request.app.cn.db)
    return carreraDAO.consultaPorID(idCarrera)

@app.put("/carreras/{idCarrera}",tags=["Carreras"],summary="Modificar Carrera",response_model=Salida)
@limiter.limit("10/minute")
async def modificarCarrera(request:Request,idCarrera:int,carrera:CarreraUpdate,
                           _:Usuario=Depends(RoleChecker(["Admin","Coordinador"]))):
    carreraDAO=CarreraDAO(request.app.cn.db)
    return carreraDAO.modificar(idCarrera,carrera)

@app.delete("/carreras/{idCarrera}",tags=["Carreras"],summary="Cancelar Carrera",response_model=Salida)
@limiter.limit("10/minute")
async def cancelarCarrera(request:Request,idCarrera:int,
                          _:Usuario=Depends(RoleChecker(["Admin"]))):
    carreraDAO=CarreraDAO(request.app.cn.db)
    return carreraDAO.cancelar(idCarrera)

# Docentes-Carreras

@app.post("/docentes-carreras",tags=["Docentes-Carreras"],summary="Crear Asignacion",response_model=Salida)
@limiter.limit("10/minute")
async def crearAsignacion(request:Request,asignacion:DocenteCarreraCreate,
                          _:Usuario=Depends(RoleChecker(["Admin","Coordinador"]))):
    docenteCarreraDAO=DocenteCarreraDAO(request.app.cn.db)
    return docenteCarreraDAO.agregar(asignacion)

@app.get("/docentes-carreras/{idDocente}",tags=["Docentes-Carreras"],summary="Consultar Asignaciones",response_model=AsignacionesSalida)
@limiter.limit("10/minute")
async def consultarAsignaciones(request:Request,idDocente:int,
                                _:Usuario=Depends(RoleChecker(["Admin","Coordinador","Docente"]))):
    docenteCarreraDAO=DocenteCarreraDAO(request.app.cn.db)
    return docenteCarreraDAO.consultaPorDocente(idDocente)

@app.put("/docentes-carreras/{idDocente}/{idCarrera}",tags=["Docentes-Carreras"],summary="Modificar Asignacion",response_model=Salida)
@limiter.limit("10/minute")
async def modificarAsignacion(request:Request,idDocente:int,idCarrera:int,asignacion:DocenteCarreraUpdate,
                              _:Usuario=Depends(RoleChecker(["Admin","Coordinador"]))):
    docenteCarreraDAO=DocenteCarreraDAO(request.app.cn.db)
    return docenteCarreraDAO.modificar(idDocente,idCarrera,asignacion)

@app.delete("/docentes-carreras/{idDocente}",tags=["Docentes-Carreras"],summary="Cancelar Asignacion",response_model=Salida)
@limiter.limit("10/minute")
async def cancelarAsignacion(request:Request,idDocente:int,
                             _:Usuario=Depends(RoleChecker(["Admin","Coordinador"]))):
    docenteCarreraDAO=DocenteCarreraDAO(request.app.cn.db)
    return docenteCarreraDAO.cancelarPorDocente(idDocente)

# Habilidades

@app.post("/habilidades",tags=["Habilidades"],summary="Crear Habilidad",response_model=Salida)
@limiter.limit("10/minute")
async def crearHabilidad(request:Request,habilidad:HabilidadCreate,
                         _:Usuario=Depends(RoleChecker(["Admin","Docente"]))):
    habilidadDAO=HabilidadDAO(request.app.cn.db)
    return habilidadDAO.agregar(habilidad)

@app.get("/habilidades/vigentes/{idDocente}",tags=["Habilidades"],summary="Consultar Habilidades Vigentes",response_model=HabilidadesVigentesSalida)
@limiter.limit("10/minute")
async def consultarHabilidadesVigentes(request:Request,idDocente:int,
                                       _:Usuario=Depends(RoleChecker(["Admin","Coordinador","Docente"]))):
    habilidadDAO=HabilidadDAO(request.app.cn.db)
    return habilidadDAO.consultaVigentes(idDocente)

@app.get("/habilidades/{idHabilidad}",tags=["Habilidades"],summary="Consultar Habilidad",response_model=HabilidadSalida)
@limiter.limit("10/minute")
async def consultarHabilidad(request:Request,idHabilidad:int,
                             _:Usuario=Depends(RoleChecker(["Admin","Coordinador","Docente"]))):
    habilidadDAO=HabilidadDAO(request.app.cn.db)
    return habilidadDAO.consultaPorID(idHabilidad)

@app.put("/habilidades/{idHabilidad}",tags=["Habilidades"],summary="Modificar Habilidad",response_model=Salida)
@limiter.limit("10/minute")
async def modificarHabilidad(request:Request,idHabilidad:int,habilidad:HabilidadUpdate,
                             user:Usuario=Depends(RoleChecker(["Admin","Docente"]))):
    if user.rol=="Docente":
        cursor=request.app.cn.db.cursor(dictionary=True)
        cursor.execute(
            "select h.idHabilidad from habilidades h join docentes d on h.idDocente=d.idDocente where h.idHabilidad=%s and d.idUsuario=%s",
            (idHabilidad,user.idUsuario)
        )
        hab=cursor.fetchone()
        cursor.close()
        if not hab:
            raise HTTPException(status.HTTP_403_FORBIDDEN,detail="Sin autorización.")
    habilidadDAO=HabilidadDAO(request.app.cn.db)
    return habilidadDAO.modificar(idHabilidad,habilidad)

@app.delete("/habilidades/{idHabilidad}",tags=["Habilidades"],summary="Cancelar Habilidad",response_model=Salida)
@limiter.limit("10/minute")
async def cancelarHabilidad(request:Request,idHabilidad:int,
                            _:Usuario=Depends(RoleChecker(["Admin"]))):
    habilidadDAO=HabilidadDAO(request.app.cn.db)
    return habilidadDAO.cancelar(idHabilidad)

# Startup / Shutdown

@app.on_event("startup")
def startup():
    conexion=Conexion()
    app.cn=conexion

@app.on_event("shutdown")
def shutdown():
    app.cn.cerrar()

if __name__=="__main__":
    uvicorn.run("main:app",reload=True)
