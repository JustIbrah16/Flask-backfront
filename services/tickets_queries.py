from utils.db import db
from models.Tickets import Tickets, Adjuntos
from models.Comentarios_Tickets import ComentariosTickets
from models.proyectos import Proyectos
from models.Users import Usuarios
from datetime import datetime, timedelta
from flask import jsonify

class TicketsQueries:

    @staticmethod
    def obtener_tickets():
        return Tickets.query.all()   

    @staticmethod
    def crear_ticket(titulo, comentario, fk_proyecto, usuario_id, archivos, categoria, fecha_estimada):
        ticket = Tickets(
            titulo=titulo,
            comentario=comentario,
            fk_proyecto=fk_proyecto,
            fk_usuario=usuario_id,
            categoria = categoria,
            fecha_estimada = fecha_estimada

        )
        db.session.add(ticket)
        db.session.flush()

        for archivo in archivos:
            adjunto = Adjuntos(
                nombre_archivo=archivo['nombre_archivo'],  
                ruta_archivo=archivo['ruta_archivo'],      
                fk_ticket=ticket.id
            )
            db.session.add(adjunto)
    
        db.session.commit()
        return ticket
    

    @staticmethod
    def actualizar_estado(ticket_id, nuevo_estado, causal_cierre=None, comentario_cierre=None, usuario_id=None):
        ticket = Tickets.query.get(ticket_id)
        if not ticket:
            return None, "Ticket no encontrado", 404

        if ticket.estado == nuevo_estado:
            return ticket, "El estado del ticket ya es el especificado", 200

        if nuevo_estado == 'cerrado':
            if not causal_cierre or not comentario_cierre:
                return None, "Faltan datos para cerrar el ticket", 400

            ticket.causal_cierre = causal_cierre
            ticket.comentario_cierre = comentario_cierre
            ticket.fk_usuario_cierre = usuario_id

        ticket.estado = nuevo_estado
        db.session.commit()
        return ticket, "Estado actualizado correctamente", 200


    @staticmethod
    def cerrar_ticket(ticket_id, causal_cierre, comentarios_cierre):
        ticket = Tickets.query.get(ticket_id)
        if not ticket:
            return None
        ticket.estado = 'cerrado'
        ticket.causal_cierre = causal_cierre
        ticket.comentarios_cierre = comentarios_cierre
        db.session.commit()
        return ticket
    
    @staticmethod
    def agregar_comentario(ticket_id, comentario, usuario_id):
        nuevo_comentario = ComentariosTickets(
            comentario=comentario,
            fk_ticket=ticket_id,
            fk_usuario=usuario_id
        )
        db.session.add(nuevo_comentario)
        db.session.commit()
        return nuevo_comentario
    
    @staticmethod
    def filtrar_tickets(titulo=None, nombre_proyecto=None, nombre_usuario=None, estado=None, categoria=None, 
                         fecha_creacion=None, fecha_estimada=None, causal_cierre=None, comentario_cierre=None):
        query = Tickets.query

        if titulo:
            query = query.filter(Tickets.titulo.ilike(f"%{titulo}%"))
        if nombre_proyecto:
            query = query.join(Proyectos).filter(Proyectos.nombre.ilike(f"%{nombre_proyecto}%"))
        if nombre_usuario:
            query = query.join(Usuarios).filter(Usuarios.nombre.ilike(f"%{nombre_usuario}%"))
        if estado:
            query = query.filter(Tickets.estado.ilike(f"%{estado}%"))
        if categoria:
            query = query.filter(Tickets.categoria.ilike(f"%{categoria}%"))
        if causal_cierre:
            query = query.filter(Tickets.causal_cierre.ilike(f"%{causal_cierre}%"))
        if comentario_cierre:
            query = query.filter(Tickets.comentario_cierre.ilike(f"%{comentario_cierre}%"))
        if fecha_creacion:
            try:
                fecha_inicio = datetime.strptime(fecha_creacion, '%Y-%m-%d')
                fecha_fin = fecha_inicio + timedelta(days=1)
                query = query.filter(Tickets.fecha_creacion >= fecha_inicio, Tickets.fecha_creacion < fecha_fin)
            except ValueError:
                return {"error": "Formato de fecha de creación inválido. Use Año-Mes-Día"}, 400
        if fecha_estimada:
            try:
                fecha_estimada = datetime.strptime(fecha_estimada, '%Y-%m-%d')
                query = query.filter(Tickets.fecha_estimada == fecha_estimada)
            except ValueError:
                return {"error": "Formato de fecha estimada inválido. Use Año-Mes-Día"}, 400

        return query.all()