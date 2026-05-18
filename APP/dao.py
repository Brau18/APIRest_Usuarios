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

class DocenteDAO:
    def __init__(self,db):
        self.db=db
    def agregar(self,docente:DocenteCreate):
        salida={"codigo":0,"mensaje":""}
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute("select idUsuario from usuarios where idUsuario=%s",(docente.idUsuario,))
            if not cursor.fetchone():
                salida["codigo"]=404
                salida["mensaje"]="El usuario no existe"
                cursor.close()
                return salida
            cursor.execute("select idDocente from docentes where idUsuario=%s",(docente.idUsuario,))
            if cursor.fetchone():
                salida["codigo"]=400
                salida["mensaje"]="El usuario ya tiene un registro como docente"
                cursor.close()
                return salida
            if docente.fechaIngreso>date.today():
                salida["codigo"]=400
                salida["mensaje"]="La fecha de ingreso no puede ser una fecha futura"
                cursor.close()
                return salida
            tipos_permitidos=['Tiempo completo','Medio tiempo','Por horas','Interino']
            if docente.tipoContrato not in tipos_permitidos:
                salida["codigo"]=400
                salida["mensaje"]="El tipo de contrato no es un valor permitido"
                cursor.close()
                return salida
            cursor.execute(
                "insert into docentes(idUsuario,gradoEstudio,fechaIngreso,estadoLaboral,correoInstitucional,horasFrenteAlGrupo,horasDocencia,horasAdministrativas,tipoContrato) values(%s,%s,%s,'Activo',%s,%s,%s,%s,%s)",
                (docente.idUsuario,docente.gradoEstudio,docente.fechaIngreso,
                docente.correoInstitucional,docente.horasFrenteAlGrupo,docente.horasDocencia,
                docente.horasAdministrativas,docente.tipoContrato)
            )
            self.db.commit()
            salida["codigo"]=201
            salida["mensaje"]="Docente creado exitosamente con id:"+str(cursor.lastrowid)
            cursor.close()
        except Exception as ex:
            salida["codigo"]=500
            salida["mensaje"]=f"Error:{ex}"
        return salida
    def consultaPorID(self,idDocente:int):
        salida=DocenteSalida(codigo=0,mensaje="",docente=None)
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute("select * from docentes where idDocente=%s",(idDocente,))
            docente=cursor.fetchone()
            if docente:
                salida.codigo=200
                salida.mensaje="Consulta del docente"
                salida.docente=docente
            else:
                salida.codigo=404
                salida.mensaje="Docente no encontrado"
            cursor.close()
        except Exception as ex:
            salida.codigo=500
            salida.mensaje=f"Error:{ex}"
        return salida
    def modificar(self,idDocente:int,docente:DocenteUpdate):
        salida={"codigo":0,"mensaje":""}
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute("select * from docentes where idDocente=%s",(idDocente,))
            docenteRec=cursor.fetchone()
            if not docenteRec:
                salida["codigo"]=404
                salida["mensaje"]="Docente no encontrado"
                cursor.close()
                return salida
            if docenteRec['estadoLaboral']=='Inactivo':
                salida["codigo"]=400
                salida["mensaje"]="El docente no se encuentra activo"
                cursor.close()
                return salida
            data=docente.model_dump(exclude_unset=True)
            if not data:
                salida["codigo"]=400
                salida["mensaje"]="Debes proporcionar un valor a modificar"
                cursor.close()
                return salida
            if 'tipoContrato' in data:
                tipos_permitidos=['Tiempo completo','Medio tiempo','Por horas','Interino']
                if data['tipoContrato'] not in tipos_permitidos:
                    salida["codigo"]=400
                    salida["mensaje"]="El tipo de contrato no es un valor permitido"
                    cursor.close()
                    return salida
            campos=",".join([f"{k}=%s" for k in data.keys()])
            valores=list(data.values())
            valores.append(idDocente)
            cursor.execute(f"update docentes set {campos} where idDocente=%s",valores)
            self.db.commit()
            if cursor.rowcount>0:
                salida["codigo"]=200
                salida["mensaje"]=f"Docente con id:{idDocente} modificado exitosamente"
            else:
                salida["codigo"]=400
                salida["mensaje"]="No se pudo modificar el docente"
            cursor.close()
        except Exception as ex:
            salida["codigo"]=500
            salida["mensaje"]=f"Error:{ex}"
        return salida
    def cancelar(self,idDocente:int):
        salida={"codigo":0,"mensaje":""}
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute("select * from docentes where idDocente=%s",(idDocente,))
            docenteRec=cursor.fetchone()
            if not docenteRec:
                salida["codigo"]=404
                salida["mensaje"]="Docente no encontrado"
                cursor.close()
                return salida
            if docenteRec['estadoLaboral']=='Inactivo':
                salida["codigo"]=400
                salida["mensaje"]="El docente ya se encuentra cancelado"
                cursor.close()
                return salida
            cursor.execute("update docentes set estadoLaboral='Inactivo' where idDocente=%s",(idDocente,))
            self.db.commit()
            salida["codigo"]=200
            salida["mensaje"]=f"Docente con id:{idDocente} cancelado exitosamente"
            cursor.close()
        except Exception as ex:
            salida["codigo"]=500
            salida["mensaje"]=f"Error:{ex}"
        return salida

class CarreraDAO:
    def __init__(self,db):
        self.db=db
    def consultaPorID(self,idCarrera:int):
        salida=CarreraSalida(codigo=0,mensaje="",carrera=None)
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute("select * from carreras where idCarrera=%s",(idCarrera,))
            carrera=cursor.fetchone()
            if carrera:
                salida.codigo=200
                salida.mensaje="Consulta de la carrera"
                salida.carrera=carrera
            else:
                salida.codigo=404
                salida.mensaje="Carrera no encontrada"
            cursor.close()
        except Exception as ex:
            salida.codigo=500
            salida.mensaje=f"Error:{ex}"
        return salida

class DocenteCarreraDAO:
    def __init__(self,db):
        self.db=db
    def agregar(self,asignacion:DocenteCarreraCreate):
        salida={"codigo":0,"mensaje":""}
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute("select idDocente from docentes where idDocente=%s",(asignacion.idDocente,))
            if not cursor.fetchone():
                salida["codigo"]=404
                salida["mensaje"]="El docente no existe"
                cursor.close()
                return salida
            cursor.execute("select idCarrera from carreras where idCarrera=%s",(asignacion.idCarrera,))
            if not cursor.fetchone():
                salida["codigo"]=404
                salida["mensaje"]="La carrera no existe"
                cursor.close()
                return salida
            cursor.execute("select * from docentes_carreras where idDocente=%s and idCarrera=%s",
                        (asignacion.idDocente,asignacion.idCarrera))
            if cursor.fetchone():
                salida["codigo"]=400
                salida["mensaje"]="Ya existe una asignacion entre ese docente y esa carrera"
                cursor.close()
                return salida
            cursor.execute(
                "insert into docentes_carreras(idDocente,idCarrera,fechaAsignacion) values(%s,%s,%s)",
                (asignacion.idDocente,asignacion.idCarrera,date.today())
            )
            self.db.commit()
            salida["codigo"]=201
            salida["mensaje"]="Asignacion docente-carrera creada exitosamente"
            cursor.close()
        except Exception as ex:
            salida["codigo"]=500
            salida["mensaje"]=f"Error:{ex}"
        return salida
    def modificar(self,idDocente:int,idCarrera:int,asignacion:DocenteCarreraUpdate):
        salida={"codigo":0,"mensaje":""}
        try:
            cursor=self.db.cursor(dictionary=True)
            cursor.execute("select * from docentes_carreras where idDocente=%s and idCarrera=%s",
                        (idDocente,idCarrera))
            if not cursor.fetchone():
                salida["codigo"]=404
                salida["mensaje"]="La asignacion no existe"
                cursor.close()
                return salida
            cursor.execute("select idCarrera from carreras where idCarrera=%s and activo=1",(asignacion.idCarrera,))
            if not cursor.fetchone():
                salida["codigo"]=404
                salida["mensaje"]="La carrera destino no existe o no esta activa"
                cursor.close()
                return salida
            if asignacion.idCarrera!=idCarrera:
                cursor.execute("select * from docentes_carreras where idDocente=%s and idCarrera=%s",
                            (idDocente,asignacion.idCarrera))
                if cursor.fetchone():
                    salida["codigo"]=400
                    salida["mensaje"]="Ya existe una asignacion con la carrera destino para este docente"
                    cursor.close()
                    return salida
            cursor.execute("delete from docentes_carreras where idDocente=%s and idCarrera=%s",
                        (idDocente,idCarrera))
            cursor.execute(
                "insert into docentes_carreras(idDocente,idCarrera,fechaAsignacion) values(%s,%s,%s)",
                (idDocente,asignacion.idCarrera,asignacion.fechaAsignacion)
            )
            self.db.commit()
            salida["codigo"]=200
            salida["mensaje"]=f"Asignacion modificada exitosamente"
            cursor.close()
        except Exception as ex:
            salida["codigo"]=500
            salida["mensaje"]=f"Error:{ex}"
        return salida
