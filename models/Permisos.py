from utils.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Permisos(db.Model):
    __tablename__ = 'permisos'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    fk_grupo = db.Column(db.Integer, ForeignKey('grupos.id'))

    grupo = relationship('Grupos', backref='permisos')
