from fastapi.security import HTTPBasic,HTTPBasicCredentials
from fastapi import Depends,HTTPException,status
from dao import Conexion,UsuarioDAO
from models import Usuario

security=HTTPBasic()

def getUser(credenciales:HTTPBasicCredentials=Depends(security)):
    cn=Conexion()
    usuarioDAO=UsuarioDAO(cn.db)
    usuario=usuarioDAO.autenticar(credenciales.username,credenciales.password)
    cn.cerrar()
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate":"Basic"}
        )
    return usuario

class RoleChecker:
    def __init__(self,roles:list):
        self.roles_permitidos=roles
    def __call__(self,user:Usuario=Depends(getUser)):
        if user.rol not in self.roles_permitidos:
            raise HTTPException(status.HTTP_403_FORBIDDEN,detail="Sin autorización.")
        return user
