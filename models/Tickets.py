from utils.db import db
from models.Users import Usuarios

class Tickets(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    comentario = db.Column(db.Text, nullable=True)
    fk_proyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    fk_usuario = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    proyecto = db.relationship('Proyectos', backref='tickets', lazy=True)
    usuario = db.relationship('Usuarios', backref='tickets', lazy=True)
    archivos = db.relationship('Adjuntos', backref='tickets', lazy=True)
    
 

class Adjuntos(db.Model):
    __tablename__ = 'ticket_archivos'  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)  
    ruta_archivo = db.Column(db.String(255), nullable=False)    
    fk_ticket = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)


