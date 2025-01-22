from utils.db import db
from models.Tickets import Tickets, Adjuntos

class TicketsQueries:

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
