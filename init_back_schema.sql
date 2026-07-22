-- ==============================================================================
-- Esquema de Base de Datos para PyroGuard AI - Backend Principal
-- Base de Datos: PostgreSQL (No requiere PostGIS, usamos tipos simples para coordenadas)
-- Nota Arquitectónica: La tabla de 'Usuarios' ha sido delegada al microservicio de Auth.
-- En esta base de datos solo guardamos los UUIDs (id_usuario, id_coordinador, etc.) como referencia suelta.
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Tabla de Brigadas
CREATE TABLE Brigadas (
    id_brigada UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL,
    id_coordinador UUID, -- Referencia al Auth Service
    activa BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT NOW()
);

-- Relación N a M: Brigadistas en Brigadas
CREATE TABLE Brigadistas_Brigada (
    id_brigada UUID REFERENCES Brigadas(id_brigada) ON DELETE CASCADE,
    id_usuario UUID, -- Referencia al Auth Service
    PRIMARY KEY (id_brigada, id_usuario)
);

-- 2. Tabla de Intervenciones (Asignación a Zonas en ML)
CREATE TABLE Intervenciones (
    id_intervencion UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_brigada UUID REFERENCES Brigadas(id_brigada) ON DELETE RESTRICT,
    id_zona UUID NOT NULL, -- Hace referencia a la BD del microservicio ML
    estado VARCHAR(50) NOT NULL CHECK (estado IN ('Pendiente', 'En Progreso', 'Completada', 'Cancelada')),
    observaciones TEXT,
    fecha_asignacion TIMESTAMP DEFAULT NOW(),
    fecha_completada TIMESTAMP
);

-- 3. Tabla de Observaciones de Campo (Por intervención)
CREATE TABLE Observaciones_Campo (
    id_observacion UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_intervencion UUID REFERENCES Intervenciones(id_intervencion) ON DELETE CASCADE,
    id_usuario UUID, -- Referencia al Auth Service
    notas TEXT NOT NULL,
    latitud DOUBLE PRECISION,
    longitud DOUBLE PRECISION,
    foto_url VARCHAR(255),
    creado_en TIMESTAMP DEFAULT NOW()
);

-- 4. Tabla de Reportes Ciudadanos (Público)
CREATE TABLE Reportes_Ciudadanos (
    id_reporte UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    descripcion TEXT NOT NULL,
    latitud DOUBLE PRECISION NOT NULL,
    longitud DOUBLE PRECISION NOT NULL,
    foto_url VARCHAR(255),
    estado VARCHAR(50) DEFAULT 'Pendiente' CHECK (estado IN ('Pendiente', 'Verificado', 'Falsa Alarma')),
    creado_en TIMESTAMP DEFAULT NOW()
);

-- 5. Tabla de Comunicados Oficiales
CREATE TABLE Comunicados (
    id_comunicado UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titulo VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    id_autor UUID, -- Referencia al Auth Service
    fecha_publicacion TIMESTAMP DEFAULT NOW(),
    fecha_vigencia TIMESTAMP NOT NULL
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_intervenciones_zona ON Intervenciones(id_zona);
CREATE INDEX idx_reportes_estado ON Reportes_Ciudadanos(estado);
CREATE INDEX idx_comunicados_vigencia ON Comunicados(fecha_vigencia);
