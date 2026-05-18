create database proyecto_api_rest;

use proyecto_api_rest;

-- ============================================================
-- CREACIÓN DE TABLAS
-- ============================================================

create table usuarios (
    idUsuario int not null auto_increment primary key,
    nombre varchar(100) not null,
    apellidoPaterno varchar(100) not null,
    apellidoMaterno varchar(100) not null,
    telefono varchar(20) not null,
    RFC char(13) not null,
    CURP char(18) not null,
    correo varchar(150) not null,
    contrasena varchar(255) not null,
    activo tinyint(1) not null,
    fechaRegistro date not null
);

create table docentes (
    idDocente int not null auto_increment primary key,
    idUsuario int not null,
    gradoEstudio varchar(100) not null,
    fechaIngreso date not null,
    estadoLaboral varchar(50) not null,
    correoInstitucional varchar(150) not null,
    horasFrenteAlGrupo int not null,
    horasDocencia int not null,
    horasAdministrativas int not null,
    tipoContrato varchar(50) not null
);

create table habilidades (
    idHabilidad int not null auto_increment primary key,
    idDocente int not null,
    nombreCurso varchar(200) not null,
    tipoCertificado varchar(100) not null,
    institucionEmisora varchar(150) not null,
    fechaObtencion date not null,
    fechaVigencia date not null,
    descripcion text,
    nivel varchar(20) not null,
    activo tinyint(1) not null
);

create table carreras (
    idCarrera int not null auto_increment primary key,
    nombreCarrera varchar(200) not null,
    descripcion text,
    activo tinyint(1) not null
);

create table docentes_carreras (
    idDocente int not null,
    idCarrera int not null,
    fechaAsignacion date not null,
    primary key (idDocente, idCarrera)
);

-- ============================================================
-- UNIQUE
-- ============================================================

alter table usuarios add constraint uq_usuarios_correo unique (correo);
alter table usuarios add constraint uq_usuarios_RFC unique (RFC);
alter table usuarios add constraint uq_usuarios_CURP unique (CURP);

alter table docentes add constraint uq_docentes_idUsuario unique (idUsuario);

alter table carreras add constraint uq_carreras_nombre unique (nombreCarrera);

-- ============================================================
-- FOREIGN KEYS
-- ============================================================

alter table docentes add constraint fk_docentes_usuario foreign key (idUsuario) references usuarios(idUsuario);

alter table habilidades add constraint fk_habilidades_docente foreign key (idDocente) references docentes(idDocente);

alter table docentes_carreras add constraint fk_dc_docente foreign key (idDocente) references docentes(idDocente);
alter table docentes_carreras add constraint fk_dc_carrera foreign key (idCarrera) references carreras(idCarrera);

-- ============================================================
-- CHECKS
-- ============================================================

alter table usuarios add constraint chk_RFC check (char_length(RFC) = 13);
alter table usuarios add constraint chk_CURP check (char_length(CURP) = 18);

alter table docentes add constraint chk_horasFrenteAlGrupo check (horasFrenteAlGrupo >= 0);
alter table docentes add constraint chk_horasDocencia check (horasDocencia >= 0);
alter table docentes add constraint chk_horasAdministrativas check (horasAdministrativas >= 0);
alter table docentes add constraint chk_estadoLaboral check (estadoLaboral in ('Activo', 'Inactivo'));
alter table docentes add constraint chk_tipoContrato check (tipoContrato in ('Tiempo completo', 'Medio tiempo', 'Por horas', 'Interino'));

alter table habilidades add constraint chk_nivel check (nivel in ('básico', 'intermedio', 'avanzado'));
alter table habilidades add constraint chk_fechaVigencia check (fechaVigencia > fechaObtencion);

-- ============================================================
-- DEFAULTS
-- ============================================================

alter table usuarios alter column activo set default 1;

alter table docentes alter column estadoLaboral set default 'Activo';
alter table docentes alter column horasFrenteAlGrupo set default 0;
alter table docentes alter column horasDocencia set default 0;
alter table docentes alter column horasAdministrativas set default 0;

alter table habilidades alter column activo set default 1;

alter table carreras alter column activo set default 1;