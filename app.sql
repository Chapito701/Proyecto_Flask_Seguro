-- 1. Crear la base de datos
CREATE DATABASE IF NOT EXISTS app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE app;

-- 2. Estructura de la tabla (generada automáticamente por SQLAlchemy)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL
);
