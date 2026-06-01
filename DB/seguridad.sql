use proyecto_api_rest;

-- columna rol en usuarios
alter table usuarios
    add column rol varchar(20) not null default 'Docente'
        check (rol in ('Admin', 'Coordinador', 'Docente'));

-- roles de base de datos
create role 'admin_role';
create role 'coordinador_role';
create role 'docente_role';

-- permisos admin_role
grant all privileges on proyecto_api_rest.* to 'admin_role';

-- permisos coordinador_role
grant select on proyecto_api_rest.usuarios to 'coordinador_role';
grant insert, update, select on proyecto_api_rest.docentes to 'coordinador_role';
grant insert, update, select on proyecto_api_rest.carreras to 'coordinador_role';
grant insert, update, select, delete on proyecto_api_rest.docentes_carreras to 'coordinador_role';
grant select on proyecto_api_rest.habilidades to 'coordinador_role';

-- permisos docente_role
grant select on proyecto_api_rest.usuarios to 'docente_role';
grant update, select on proyecto_api_rest.docentes to 'docente_role';
grant select on proyecto_api_rest.carreras to 'docente_role';
grant select on proyecto_api_rest.docentes_carreras to 'docente_role';
grant insert, update, select on proyecto_api_rest.habilidades to 'docente_role';

-- usuarios de base de datos
create user 'admin_user'@'localhost' identified by 'Admin@1234';
create user 'coordinador_user'@'localhost' identified by 'Coord@1234';
create user 'docente_user'@'localhost' identified by 'Doc@1234';

-- asignacion de roles
grant 'admin_role' to 'admin_user'@'localhost';
grant 'coordinador_role' to 'coordinador_user'@'localhost';
grant 'docente_role' to 'docente_user'@'localhost';

-- rol por defecto
set default role 'admin_role' for 'admin_user'@'localhost';
set default role 'coordinador_role' for 'coordinador_user'@'localhost';
set default role 'docente_role' for 'docente_user'@'localhost';

flush privileges;
