import os
import mimetypes
from datetime import datetime
from models.proyectos import Proyectos
from utils.decorador import requiere_permiso
from utils.respuesta_json import serializar_tickets
from services.tickets_queries import TicketsQueries
from flask import Blueprint, session, jsonify, request, send_from_directory

base_tickets = Blueprint('base_tickets', __name__)

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

@base_tickets.route('/base_tickets', methods=['GET'])
@requiere_permiso('Acceso Base de Tickets')
def acceso_base_tickets():

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

    tickets_json = serializar_tickets(tickets)

    
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



@base_tickets.route('/tickets/nuevo', methods=['POST'])
@requiere_permiso('Crear Tickets')
def crear_ticket():

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
    
    total_zise = 0
    for archivo in archivos:
        archivo.seek(0, os.SEEK_END)
        total_zise += archivo.tell()
        archivo.seek(0)

    if total_zise > 10 * 1024 * 1024:
        return jsonify({"error": "El tamaño total de los archivos adjuntos no puede superar los 10MB"}), 400
    
    for archvo in archivos:
        archivo_ruta = os.path.join(UPLOAD_FOLDER, archvo.filename)
        archvo.seek(0)
        archvo.save(archivo_ruta)
        archivos_adjuntos.append({"nombre_archivo": archvo.filename, "ruta_archivo": archivo_ruta})

    ticket = TicketsQueries.crear_ticket(
        titulo=titulo,
        comentario=comentario,
        fk_proyecto=proyecto.id,  
        usuario_id=session.get('user_id'),
        archivos=archivos_adjuntos,
        categoria=categoria,
        fecha_estimada=fecha_estimada
    )

    return jsonify({
        "message": "Ticket creado exitosamente",
        "ticket_id": ticket.id
    }), 201



@base_tickets.route('/api/archivos/<nombre_archivo>', methods=['GET'])
def servir_archivo(nombre_archivo):
    archivo_ruta = os.path.join(UPLOAD_FOLDER, nombre_archivo)
    if not os.path.exists(archivo_ruta):
        return jsonify({"error": "Archivo no encontrado"}), 404
    
    mimetype, _ = mimetypes.guess_type(archivo_ruta)
    if not mimetype:
        mimetype = 'application/octet-stream'
    
    return send_from_directory(UPLOAD_FOLDER, nombre_archivo, as_attachment=False, mimetype=mimetype)




@base_tickets.route('/base_tickets/filtrar', methods=['GET'])
@requiere_permiso('Acceso Base de Tickets')
def filtrar_tickets():
    filtros = {
        "titulo" : request.args.get('titulo'),
        "nombre_proyecto" : request.args.get('nombre_proyecto'),
        "nombre_usuario" : request.args.get('nombre_usuario'),
        "estado" : request.args.get('estado'),
        "categoria" : request.args.get('categoria'),
        "fecha_creacion" : request.args.get('fecha_creacion'),
        "fecha_estimada" : request.args.get('fecha_estimada'),
        "causal_cierre" : request.args.get('causal_cierre'),
        "comentario_cierre" : request.args.get('comentario_cierre')
    }

    tickets = TicketsQueries.filtrar_tickets(**filtros)

    if isinstance(tickets, tuple):
        return jsonify({"error": tickets[0]}), tickets[1]

    if not tickets:
        return jsonify({"message": "No se encontraron tickets"}), 404

    return jsonify({
        "message": "Filtrado exitoso",
        "tickets": serializar_tickets(tickets)
    }), 200



@base_tickets.route('/tickets/<int:ticket_id>/estado', methods=['PUT'])
@requiere_permiso('Actualizar Estado Ticket')
def actualizar_estado_ticket(ticket_id):
    data = request.json
    nuevo_estado = data.get('estado', '').lower().strip()
    causal_cierre = data.get('causal_cierre')
    comentario_cierre = data.get('comentario_cierre')
    usuario_id = session.get('user_id')

    estados_validos = ['abierto', 'pendiente', 'atendido', 'devuelto', 'cerrado']
    if nuevo_estado not in estados_validos:
        return jsonify({"error": f"Estado inválido. Opciones: {', '.join(estados_validos)}"}), 400

    ticket, mensaje, codigo = TicketsQueries.actualizar_estado(ticket_id, nuevo_estado, causal_cierre, comentario_cierre, usuario_id)
    
    if not ticket:
        return jsonify({"error": mensaje}), codigo

    return jsonify({"message": mensaje, "ticket_id": ticket.id, "nuevo_estado": ticket.estado}), codigo


@base_tickets.route('/tickets/<int:ticket_id>/cerrar', methods=['PUT'])
@requiere_permiso('Actualizar Estado Ticket')
def cerrar_ticket(ticket_id):
    data = request.json
    usuario_id = session.get('user_id')

    ticket, mensaje, codigo = TicketsQueries.actualizar_estado(
        ticket_id, 'cerrado', data.get('causal_cierre'), data.get('comentario_cierre'), usuario_id
    )

    if not ticket:
        return jsonify({"error": mensaje}), codigo

    return jsonify({
        "message": mensaje,
        "ticket_id": ticket.id,
        "nuevo_estado": ticket.estado,
        "causal_cierre": ticket.causal_cierre,
        "comentario_cierre": ticket.comentario_cierre,
        "usuario_cierre": ticket.usuario_cierre.nombre if ticket.usuario_cierre else "Usuario no encontrado"
    }), codigo
    

@base_tickets.route('/tickets/<int:ticket_id>/comentarios', methods=['POST'])
@requiere_permiso('Comentar Ticket')
def agregar_comentario(ticket_id):
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 401    

    comentario_texto = request.json.get('comentario')
    if not comentario_texto:
        return jsonify({"error": "El campo 'comentario' es requerido"}), 400

    comentario = TicketsQueries.agregar_comentario(ticket_id, comentario_texto, usuario_id)

    return jsonify({
        "message": "Comentario agregado exitosamente",
        "comentario": {
            "id": comentario.id,
            "comentario": comentario.comentario,
            "fecha_creacion": comentario.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
            "usuario": comentario.usuario.nombre
        }
    }), 201



