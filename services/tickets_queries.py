from utils.db import db
from models.Tickets import Tickets, Adjuntos
from models.Comentarios_Tickets import ComentariosTickets

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
    def actualizar_estado(ticket_id, nuevo_estado):
        ticket = Tickets.query.get(ticket_id)
        if not ticket:
            return None
        ticket.estado = nuevo_estado
        db.session.commit()
        return ticket

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