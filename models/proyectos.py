from utils.db import db

class Proyectos(db.Model):
    __tablename__ = 'proyectos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, nombre, descripcion, usuario_id):
        self.nombre = nombre
        self.descripcion = descripcion
        self.usuario_id = usuario_id
