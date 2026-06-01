use proyecto_api_rest;

-- usuario admin
insert into usuarios(nombre,apellidoPaterno,apellidoMaterno,telefono,RFC,CURP,correo,contrasena,rol,activo,fechaRegistro) values
('Carlos','García','López','5551234567','GALC800101ABC','GALC800101HDFXXX01','admin@test.com','admin123','Admin',1,'2024-01-01');

-- usuario coordinador
insert into usuarios(nombre,apellidoPaterno,apellidoMaterno,telefono,RFC,CURP,correo,contrasena,rol,activo,fechaRegistro) values
('María','Rodríguez','Pérez','5559876543','ROPM900202DEF','ROPM900202MDFXXX02','coordinador@test.com','coord123','Coordinador',1,'2024-01-01');

-- usuario docente
insert into usuarios(nombre,apellidoPaterno,apellidoMaterno,telefono,RFC,CURP,correo,contrasena,rol,activo,fechaRegistro) values
('Luis','Martínez','Sánchez','5554561234','MASL950303GHI','MASL950303HDFXXX03','docente@test.com','doc123','Docente',1,'2024-01-01');
