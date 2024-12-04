from utils.db import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .Roles import Roles

class Usuarios(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fk_rol = db.Column(db.Integer, ForeignKey('roles.id'), nullable=False)

    rol = relationship('Roles', backref='usuarios')

    def __init__(self, nombre, password, fk_rol):
        self.nombre = nombre
        self.password = password
        self.fk_rol = fk_rol
