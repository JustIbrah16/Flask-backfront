from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from utils.db import db

rol_permisos = Table(
    'rol_permisos',
    db.Model.metadata,
    Column('fk_rol', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('fk_permiso', Integer, ForeignKey('permisos.id'), primary_key=True)
)

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

    permisos = relationship('Permisos', secondary=rol_permisos, backref='roles')
