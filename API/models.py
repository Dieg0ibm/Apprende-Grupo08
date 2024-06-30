#models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Historial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_miembro = db.Column(db.String(255))
    contacto_miembro = db.Column(db.String(255))
    descripcion_taller = db.Column(db.String(255))
    tipo = db.Column(db.String(50))
    enlaces_resultados = db.Column(db.Text)

class Propuestas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_miembro = db.Column(db.String(255))
    contacto_miembro = db.Column(db.String(255))
    titulo = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
    duracion = db.Column(db.Integer)  
    sesiones = db.Column(db.Integer)  
    objetivos = db.Column(db.Text)
    estado = db.Column(db.Integer)

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.String(255))