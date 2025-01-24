from models.proyectos import Proyectos
from utils.db import db
from models.Tickets import Tickets

class ProyectosQueries:

    @staticmethod
    def obtener_proyectos(usuario_id, proyecto_id=None, nombre=None):
        query = Proyectos.query.filter_by(usuario_id=usuario_id)
        if proyecto_id:
            query = query.filter(Proyectos.id == proyecto_id)  
        if nombre:
            query = query.filter(Proyectos.nombre.like(f"%{nombre}%"))
        return query.all()


    @staticmethod
    def obtener_todos_proyectos():
        return Proyectos.query.all()
    
    @staticmethod
    def obtener_resumen_tickets(usuario_id):
        query = db.session.query(
            Tickets.fk_proyecto,
            Proyectos.nombre.label('proyecto_nombre'),
            db.func.count(db.case((Tickets.estado == 'abierto', 1))).label('abiertos'),
            db.func.count(db.case((Tickets.estado == 'pendiente', 1))).label('pendientes'),
            db.func.count(db.case((Tickets.estado == 'atendido', 1))).label('atendidos'),
            db.func.count(db.case((Tickets.estado == 'cerrado', 1))).label('cerrados'),
            db.func.count(db.case((Tickets.estado == 'devuelto', 1))).label('devueltos'),
        ).join(
            Proyectos, Tickets.fk_proyecto == Proyectos.id
        ).filter(
            Proyectos.usuario_id == usuario_id
        ).group_by(
            Tickets.fk_proyecto, Proyectos.nombre
        ).all()

        return query

        
        