from utils.db import db
from models.Users import Usuarios
from datetime import datetime
class Tickets(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    comentario = db.Column(db.Text, nullable=True)
    fk_proyecto = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    fk_usuario = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    fk_usuario_cierre = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) 
    estado = db.Column(db.String(50), default='pendiente')
    categoria = db.Column(db.String(100), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_estimada = db.Column(db.DateTime, nullable=True)
    causal_cierre = db.Column(db.String(255), nullable=True)
    comentario_cierre = db.Column(db.Text, nullable=True)

    proyecto = db.relationship('Proyectos', backref='tickets', lazy=True)
    usuario = db.relationship('Usuarios', foreign_keys=[fk_usuario], backref='tickets_creados', lazy=True) 
    usuario_cierre = db.relationship('Usuarios', foreign_keys=[fk_usuario_cierre], backref='tickets_cerrados', lazy=True) 
    archivos = db.relationship('Adjuntos', backref='tickets', lazy=True)


    
    
class Adjuntos(db.Model):
    __tablename__ = 'ticket_archivos'  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)  
    ruta_archivo = db.Column(db.String(255), nullable=False)    
    fk_ticket = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)


