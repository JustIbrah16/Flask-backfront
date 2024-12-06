from models.proyectos import Proyectos
from utils.db import db

class ProyectosQueries:

    @staticmethod
    def obtener_proyectos(usuario_id, nombre=None):
        query = Proyectos.query.filter_by(usuario_id=usuario_id)
        if nombre:
            query = query.filter(Proyectos.nombre.like(f"%{nombre}%"))
        return query.all()

    @staticmethod
    def obtener_todos_proyectos():
        return Proyectos.query.all()
        
    
        