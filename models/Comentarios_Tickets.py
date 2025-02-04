from datetime import datetime
from utils.db import db

class ComentariosTickets(db.Model):
    __tablename__ = 'comentarios_tickets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comentario = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fk_ticket = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    fk_usuario = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    ticket = db.relationship('Tickets', backref='comentarios', lazy=True)
    usuario = db.relationship('Usuarios', backref='comentarios', lazy=True)
    