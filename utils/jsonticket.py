from flask import Blueprint, session, jsonify, request, send_from_directory, url_for


def serializar_ticket(ticket):
    return {
        "id": ticket.id,
        "titulo": ticket.titulo,
        "comentario": ticket.comentario,
        "categoria": ticket.categoria,
        "fecha_creacion": ticket.fecha_creacion.strftime('%Y-%m-%d') if ticket.fecha_creacion else None,
        "fecha_estimada": ticket.fecha_estimada.strftime('%Y-%m-%d') if ticket.fecha_estimada else None,
        "causal_cierre": ticket.causal_cierre,
        "comentario_cierre": ticket.comentario_cierre,
        "estado": ticket.estado,
        "proyecto": ticket.proyecto.nombre,
        "usuario": ticket.usuario.nombre,
        "comentarios": [
            {
                "id": comentario.id,
                "comentario": comentario.comentario,
                "fecha_creacion": comentario.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
                "usuario": comentario.usuario.nombre
            }
            for comentario in ticket.comentarios
        ],
        "archivos": [
            {
                "id": adjunto.id,
                "nombre_archivo": adjunto.nombre_archivo,
                "url": url_for('base_tickets.servir_archivo', nombre_archivo=adjunto.nombre_archivo, _external=True)
            }
            for adjunto in ticket.archivos
        ]
    }
