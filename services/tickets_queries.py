from utils.db import db
from models.Tickets import Tickets, Adjuntos

class TicketsQueries:

    @staticmethod
    def crear_ticket(titulo, comentario, fk_proyecto, usuario_id, archivos):
        ticket = Tickets(
            titulo=titulo,
            comentario=comentario,
            fk_proyecto=fk_proyecto,
            fk_usuario=usuario_id  
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

