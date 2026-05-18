import mysql.connector
from models import UsuarioCreate,UsuarioUpdate,Salida,UsuarioSalida,CarreraCreate,CarreraUpdate
from datetime import date
DBHOST='localhost'
DBPORT=3306
DBUSER='root'
DBPASSWORD='root123'
DATABASE='proyecto_api_rest'
class Conexion:
    _conexion=None
    def __init__(self):
        try:
            self._conexion=mysql.connector.connect(
                host=DBHOST,port=DBPORT,user=DBUSER,
                password=DBPASSWORD,database=DATABASE
            )
            print(f"Conectado con la BD: {DATABASE}")
        except Exception as ex:
            print(f"Error al conectar con la BD a causa de: {ex}")
    def cerrar(self):
        try:
            self._conexion.close()
            print(f'Conexion cerrada con la BD:{DATABASE}')
        except Exception as ex:
            print(f"Error al cerrar con la BD a causa de: {ex}")
    @property
    def db(self):
        return self._conexion

class UsuarioDAO:
    def __init__(self,db):
        self.db=db
    def agregar(self,usuario:UsuarioCreate):
        salida=Salida(codigo=0,mensaje="")
        try:
            if len(usuario.RFC)!=13:
                salida.codigo=400
                salida.mensaje="El RFC debe tener 13 caracteres"
                return salida
            if len(usuario.CURP)!=18:
                salida.codigo=400
                salida.mensaje="El CURP debe tener 18 caracteres"
                return salida
            cursor=self.db.cursor(dictionary=True)
            cursor.execute(f"select idUsuario from usuarios where correo='{usuario.correo}'")
            if cursor.fetchone():
                salida.codigo=400
                salida.mensaje="El correo ya está registrado"
                cursor.close()
                return salida
            cursor.execute(
                f"insert into usuarios(nombre,apellidoPaterno,apellidoMaterno,telefono,RFC,CURP,correo,contrasena,activo,fechaRegistro) values('{usuario.nombre}','{usuario.apellidoPaterno}','{usuario.apellidoMaterno}','{usuario.telefono}','{usuario.RFC}','{usuario.CURP}','{usuario.correo}','{usuario.contrasena}',1,'{date.today()}')"
            )
            self.db.commit()
            salida.codigo=201
            salida.mensaje="Usuario creado exitosamente con id:"+str(cursor.lastrowid)
            cursor.close()
        except Exception as ex:
            salida.codigo=500
            salida.mensaje=f"Error:{ex}"
        return salida
    def consultaPorID(self,idUsuario:int):
        salida=UsuarioSalida(codigo=0,mensaje="",usuario=None)
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute(f"select idUsuario,nombre,apellidoPaterno,apellidoMaterno,telefono,RFC,CURP,correo,activo,fechaRegistro from usuarios where idUsuario={idUsuario}")
            usuario=cursor.fetchone()
            if usuario:
                salida.codigo=200
                salida.mensaje="Consulta del usuario"
                salida.usuario=usuario
            else:
                salida.codigo=404
                salida.mensaje="Usuario no encontrado"
            cursor.close()
        except Exception as ex:
            salida.codigo=500
            salida.mensaje=f"Error:{ex}"
        return salida
    def modificar(self,idUsuario:int,usuario:UsuarioUpdate):
        salida=Salida(codigo=0,mensaje="")
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute(f"select * from usuarios where idUsuario={idUsuario}")
            usuarioRec=cursor.fetchone()
            if not usuarioRec:
                salida.codigo=404
                salida.mensaje="Usuario no encontrado"
                cursor.close()
                return salida
            if usuarioRec['activo']==0:
                salida.codigo=400
                salida.mensaje="El usuario no se encuentra activo"
                cursor.close()
                return salida
            data=usuario.model_dump(exclude_unset=True)
            if not data:
                salida.codigo=400
                salida.mensaje="Debes proporcionar un valor a modificar"
                cursor.close()
                return salida
            if 'correo' in data:
                cursor.execute(f"select idUsuario from usuarios where correo='{data['correo']}' and idUsuario!={idUsuario}")
                if cursor.fetchone():
                    salida.codigo=400
                    salida.mensaje="El correo ya pertenece a otro usuario"
                    cursor.close()
                    return salida
            campos=",".join([f"{k}='{v}'" for k,v in data.items()])
            cursor.execute(f"update usuarios set {campos} where idUsuario={idUsuario}")
            self.db.commit()
            if cursor.rowcount>0:
                salida.codigo=200
                salida.mensaje=f"Usuario con id:{idUsuario} modificado exitosamente"
            else:
                salida.codigo=400
                salida.mensaje="No se pudo modificar el usuario"
            cursor.close()
        except Exception as ex:
            salida.codigo=500
            salida.mensaje=f"Error:{ex}"
        return salida
    def cancelar(self,idUsuario:int):
        salida=Salida(codigo=0,mensaje="")
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute(f"select * from usuarios where idUsuario={idUsuario}")
            usuarioRec=cursor.fetchone()
            if not usuarioRec:
                salida.codigo=404
                salida.mensaje="Usuario no encontrado"
                cursor.close()
                return salida
            if usuarioRec['activo']==0:
                salida.codigo=400
                salida.mensaje="El usuario ya se encuentra cancelado"
                cursor.close()
                return salida
            cursor.execute(f"update usuarios set activo=0 where idUsuario={idUsuario}")
            self.db.commit()
            salida.codigo=200
            salida.mensaje=f"Usuario con id:{idUsuario} cancelado exitosamente"
            cursor.close()
        except Exception as ex:
            salida.codigo=500
            salida.mensaje=f"Error:{ex}"
        return salida

class CarreraDAO:
    def __init__(self,db):
        self.db=db
    def agregar(self,carrera:CarreraCreate):
        salida=Salida(codigo=0,mensaje="")
        try:
            if not carrera.nombreCarrera or carrera.nombreCarrera.strip()=="":
                salida.codigo=400
                salida.mensaje="El nombre de la carrera no puede estar vacío"
                return salida
            cursor=self.db.cursor(dictionary=True)
            cursor.execute(f"select idCarrera from carreras where nombreCarrera='{carrera.nombreCarrera}'")
            if cursor.fetchone():
                salida.codigo=400
                salida.mensaje="Ya existe una carrera con ese nombre"
                cursor.close()
                return salida
            cursor.execute(
                f"insert into carreras(nombreCarrera,descripcion,activo) values('{carrera.nombreCarrera}','{carrera.descripcion}',1)"
            )
            self.db.commit()
            salida.codigo=201
            salida.mensaje="Carrera creada exitosamente con id:"+str(cursor.lastrowid)
            cursor.close()
        except Exception as ex:
            salida.codigo=500
            salida.mensaje=f"Error:{ex}"
        return salida
    def modificar(self,idCarrera:int,carrera:CarreraUpdate):
        salida=Salida(codigo=0,mensaje="")
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute(f"select * from carreras where idCarrera={idCarrera}")
            carreraRec=cursor.fetchone()
            if not carreraRec:
                salida.codigo=404
                salida.mensaje="Carrera no encontrada"
                cursor.close()
                return salida
            data=carrera.model_dump(exclude_unset=True)
            if not data:
                salida.codigo=400
                salida.mensaje="Debes proporcionar un valor a modificar"
                cursor.close()
                return salida
            if 'nombreCarrera' in data:
                cursor.execute(f"select idCarrera from carreras where nombreCarrera='{data['nombreCarrera']}' and idCarrera!={idCarrera}")
                if cursor.fetchone():
                    salida.codigo=400
                    salida.mensaje="Ya existe otra carrera con ese nombre"
                    cursor.close()
                    return salida
            campos=",".join([f"{k}='{v}'" for k,v in data.items()])
            cursor.execute(f"update carreras set {campos} where idCarrera={idCarrera}")
            self.db.commit()
            if cursor.rowcount>0:
                salida.codigo=200
                salida.mensaje=f"Carrera con id:{idCarrera} modificada exitosamente"
            else:
                salida.codigo=400
                salida.mensaje="No se pudo modificar la carrera"
            cursor.close()
        except Exception as ex:
            salida.codigo=500
            salida.mensaje=f"Error:{ex}"
        return salida
    def cancelar(self,idCarrera:int):
        salida=Salida(codigo=0,mensaje="")
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute(f"select * from carreras where idCarrera={idCarrera}")
            carreraRec=cursor.fetchone()
            if not carreraRec:
                salida.codigo=404
                salida.mensaje="Carrera no encontrada"
                cursor.close()
                return salida
            if carreraRec['activo']==0:
                salida.codigo=400
                salida.mensaje="La carrera ya se encuentra cancelada"
                cursor.close()
                return salida
            cursor.execute(
                f"select dc.idDocente from docentes_carreras dc join docentes d on dc.idDocente=d.idDocente where dc.idCarrera={idCarrera} and d.estadoLaboral='Activo'"
            )
            if cursor.fetchone():
                salida.codigo=400
                salida.mensaje="No se puede cancelar la carrera, tiene docentes activos asignados"
                cursor.close()
                return salida
            cursor.execute(f"update carreras set activo=0 where idCarrera={idCarrera}")
            self.db.commit()
            salida.codigo=200
            salida.mensaje=f"Carrera con id:{idCarrera} cancelada exitosamente"
            cursor.close()
        except Exception as ex:
            salida.codigo=500
            salida.mensaje=f"Error:{ex}"
        return salida
