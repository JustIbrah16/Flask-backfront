from flask import Blueprint, session, jsonify, request, send_from_directory, url_for
from services.roles_queries import RolesQueries
from services.tickets_queries import TicketsQueries
from services.proyecto_queries import ProyectosQueries
from models.Tickets import Tickets
from models.proyectos import Proyectos
from models.Users import Usuarios
from utils.db import db
import os
from datetime import datetime, timedelta


base_tickets = Blueprint('base_tickets', __name__)

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

@base_tickets.route('/base_tickets', methods=['GET'])
def acceso_base_tickets():
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    if not RolesQueries.tiene_permiso(usuario_id, 'Acceso Base de Tickets'):
        return jsonify({"error": "Acceso denegado a Base de Tickets"}), 403

    tickets = TicketsQueries.obtener_tickets()

    if not tickets: 
        return jsonify({
            "message": "No se encontraron tickets",
            "opciones": [
                {
                    "endpoint": "/base_tickets/filtrar",
                    "nombre": "Filtrar Tickets"
                }
            ]
        }), 404

    tickets_json = [
    {
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
    for ticket in tickets
]

    
    return jsonify({
        "message": "Bienvenido a Base de Tickets",
        "tickets": tickets_json,
        "opciones": [
            {
                "endpoint": "/base_tickets/filtrar",
                "nombre": "Filtrar Tickets"
            }
        ]
    }), 200





@base_tickets.route('/api/archivos/<nombre_archivo>', methods=['GET'])
def servir_archivo(nombre_archivo):
    try:
        return send_from_directory(UPLOAD_FOLDER, nombre_archivo, as_attachment=False)
    except FileNotFoundError:
        return jsonify({"error": "Archivo no encontrado"}), 404




@base_tickets.route('/tickets/nuevo', methods=['POST'])
def crear_ticket():
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    if not RolesQueries.tiene_permiso(usuario_id, 'Crear Tickets'):
        return jsonify({"error": "No tiene permisos para crear tickets"}), 403

    data = request.form
    titulo = data.get('titulo')
    comentario = data.get('comentario')
    nombre_proyecto = data.get('nombre_proyecto')
    categoria = data.get('categoria')
    fecha_estimada = data.get('fecha_estimada')  

    if not titulo or not nombre_proyecto:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    proyecto = Proyectos.query.filter_by(nombre=nombre_proyecto).first()
    if not proyecto:
        return jsonify({"error": f"No se encontró un proyecto con el nombre '{nombre_proyecto}'"}), 404
    
    try:
        fecha_estimada = datetime.strptime(fecha_estimada,'%Y-%m-%d') if fecha_estimada else None
    except ValueError:
        return jsonify({"error": "Formato de fecha estimada invalido. Use Año/Mes/Dia"}), 400

    archivos_adjuntos = []
    archivos = request.files.getlist('archivos')
    total_size = sum(archivo.content_length for archivo in archivos)

    if total_size > 10 * 1024 * 1024:  
        return jsonify({"error": "El tamaño máximo total es de 10MB"}), 400

    for archivo in archivos:
        archivo_ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(archivo_ruta)
        archivos_adjuntos.append({"nombre_archivo": archivo.filename, "ruta_archivo": archivo_ruta})

    ticket = TicketsQueries.crear_ticket(
        titulo=titulo,
        comentario=comentario,
        fk_proyecto=proyecto.id,  
        usuario_id=usuario_id,
        archivos=archivos_adjuntos,
        categoria=categoria,
        fecha_estimada=fecha_estimada
    )

    return jsonify({
        "message": "Ticket creado exitosamente",
        "ticket_id": ticket.id
    }), 201




@base_tickets.route('/base_tickets/filtrar', methods=['GET'])
def filtrar_tickets():
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    if not RolesQueries.tiene_permiso(usuario_id, 'Acceso Base de Tickets'):
        return jsonify({"error": "Acceso denegado a Base de Tickets"}), 403

    titulo = request.args.get('titulo')
    nombre_proyecto = request.args.get('nombre_proyecto')
    nombre_usuario = request.args.get('nombre_usuario')
    estado = request.args.get('estado')
    categoria = request.args.get('categoria')
    fecha_creacion = request.args.get('fecha_creacion')
    fecha_estimada = request.args.get('fecha_estimada')
    causal_cierre = request.args.get('causal_cierre')
    comentario_cierre = request.args.get('comentario_cierre')

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
            return jsonify({"error": "Formato de fecha de creación inválido. Use Año-Mes-Día"}), 400
    if fecha_estimada:
        try:
            fecha_estimada = datetime.strptime(fecha_estimada, '%Y-%m-%d')
            query = query.filter(Tickets.fecha_estimada == fecha_estimada)
        except ValueError:
            return jsonify({"error": "Formato de fecha estimada inválido. Use Año-Mes-Día"}), 400

    tickets = query.all()

    if not tickets:
        return jsonify({"message": "No se encontraron tickets"}), 404

    tickets_json = [
        {
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
        for ticket in tickets
    ]

    return jsonify({
        "message": "Filtrado exitoso",
        "tickets": tickets_json
    }), 200





@base_tickets.route('/tickets/<int:ticket_id>/estado', methods=['PUT'])
def actualizar_estado_ticket(ticket_id):
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 403

    if not RolesQueries.tiene_permiso(usuario_id, 'Actualizar Estado Ticket'):
        return jsonify({"error": "No tiene permisos para actualizar el estado del ticket"}), 403

    data = request.json
    nuevo_estado = data.get('estado')

    if not nuevo_estado:
        return jsonify({"error": "El campo 'estado' es requerido"}), 400

    nuevo_estado = nuevo_estado.lower().strip()
    estados_validos = ['abierto', 'pendiente', 'atendido', 'devuelto', 'cerrado']
    if nuevo_estado not in estados_validos:
        return jsonify({"error": f"Estado inválido. Opciones permitidas: {', '.join(estados_validos)}"}), 400

    try:
        ticket = Tickets.query.get(ticket_id)
        if not ticket:
            return jsonify({"error": "Ticket no encontrado"}), 404

        if ticket.estado == nuevo_estado:
            return jsonify({
                "message": "El estado del ticket ya es el especificado",
                "ticket_id": ticket.id,
                "estado_actual": ticket.estado
            })

        if nuevo_estado == 'cerrado':
            causal_cierre = data.get('causal_cierre')
            comentario_cierre = data.get('comentario_cierre')

            if not causal_cierre:
                return jsonify({"error": "El campo 'causal_cierre' es requerido para cerrar el ticket"}), 400
            if not comentario_cierre:
                return jsonify({"error": "El campo 'comentario_cierre' es requerido para cerrar el ticket"}), 400

            ticket.causal_cierre = causal_cierre
            ticket.comentario_cierre = comentario_cierre
            ticket.fk_usuario_cierre = usuario_id

        ticket.estado = nuevo_estado
        db.session.commit()

        return jsonify({
            "message": "Estado del ticket actualizado exitosamente",
            "ticket_id": ticket.id,
            "nuevo_estado": ticket.estado
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar el estado del ticket: {str(e)}"}), 500




@base_tickets.route('/tickets/<int:ticket_id>/cerrar', methods=['PUT'])
def cerrar_ticket(ticket_id):
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    if not RolesQueries.tiene_permiso(usuario_id, 'Actualizar Estado Ticket'):
        return jsonify({"error": "No tiene permisos para cerrar tickets"}), 403

    data = request.json
    causal_cierre = data.get('causal_cierre')
    comentario_cierre = data.get('comentario_cierre')

    if not causal_cierre:
        return jsonify({"error": "El campo 'causal_cierre' es requerido"}), 400

    if not comentario_cierre:
        return jsonify({"error": "El campo 'comentario_cierre' es requerido"}), 400

    try:
        ticket = Tickets.query.get(ticket_id)
        if not ticket:
            return jsonify({"error": "Ticket no encontrado"}), 404

        if ticket.estado == 'cerrado':
            return jsonify({
                "message": "El ticket ya está cerrado",
                "ticket_id": ticket.id
            }), 400

        ticket.estado = 'cerrado'
        ticket.causal_cierre = causal_cierre
        ticket.comentario_cierre = comentario_cierre
        ticket.fk_usuario_cierre = usuario_id
        
        db.session.commit()

        return jsonify({
            "message": "El ticket ha sido cerrado exitosamente",
            "ticket_id": ticket.id,
            "nuevo_estado": ticket.estado,
            "causal_cierre": ticket.causal_cierre,
            "comentario_cierre": ticket.comentario_cierre,
            "usuario_cierre": ticket.usuario_cierre.nombre if ticket.usuario_cierre else "Usuario no encontrado"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al cerrar el ticket: {str(e)}"}), 500
    



@base_tickets.route('/tickets/<int:ticket_id>/comentarios', methods=['POST'])
def agregar_comentario(ticket_id):
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 401    
    
    data = request.json
    comentario_texto = data.get('comentario')
    
    if not comentario_texto:
        return jsonify({"error": "El campo 'comentario' es requerido"}), 400
    
    ticket = Tickets.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket no encontrado"}), 404
    
    nuevocomentario = TicketsQueries.agregar_comentario(    
        comentario=comentario_texto,
        ticket_id=ticket_id,
        usuario_id=usuario_id
    )

    db.session.add(nuevocomentario)
    db.session.commit()

    return jsonify({
        "message": "Comentario agregado exitosamente",
        "comentario": {
            "id": nuevocomentario.id,
            "comentario": nuevocomentario.comentario,
            "fecha_creacion": nuevocomentario.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
            "usuario": nuevocomentario.usuario.nombre
        }
    }), 201


