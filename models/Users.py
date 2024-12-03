
from utils.db import db
from sqlalchemy import column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .Roles import Roles

class Usuarios(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    nombre = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    fk_rol = db.Column(db.Integer, ForeignKey('roles.id'), nullable = False)

    rol = relationship('Roles', backref='users')

    def __init__(self, nombre, password, fk_rol):
        self.nombre = nombre
        self.password = password,
        self.fk_rol = fk_rol