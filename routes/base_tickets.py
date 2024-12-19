from flask import Blueprint, session, jsonify, request, send_from_directory, url_for
from services.roles_queries import RolesQueries
from services.tickets_queries import TicketsQueries
from services.proyecto_queries import ProyectosQueries
from models.Tickets import Tickets
from models.proyectos import Proyectos
import os


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

    tickets = Tickets.query.all()

    if not tickets:
        return jsonify({"message": "No se encontraron tickets"}), 404

    tickets_json = [
        {
            "id": ticket.id,
            "titulo": ticket.titulo,
            "comentario": ticket.comentario,
            "proyecto": ticket.proyecto.nombre,
            "usuario": ticket.usuario.nombre,
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
        "message": "Bienvenido a base de tickets",
        "tickets": tickets_json
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

    if not titulo or not nombre_proyecto:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    proyecto = Proyectos.query.filter_by(nombre=nombre_proyecto).first()

    if not proyecto:
        return jsonify({"error": f"No se encontró un proyecto con el nombre '{nombre_proyecto}'"}), 404

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
        archivos=archivos_adjuntos
    )

    return jsonify({
        "message": "Ticket creado exitosamente",
        "ticket_id": ticket.id
    }), 201


# para probar en postman:
# Selecciona la opción form-data en body.
# Incluye los siguientes campos:
# titulo (Texto): El título del ticket.
# comentario (Texto, opcional): El comentario del ticket.
# nombre_proyecto (Texto): El nombre del proyecto(ej: Bancoomeva).
# archivos (Archivo, opcional): hasta 10 mb

# @base_tickets.route('/archivos/<path:nombre_archivo>', methods=['GET'])
# def servir_archivo(nombre_archivo):
#     try:
#         ruta_completa = os.path.join(UPLOAD_FOLDER, nombre_archivo)
#         if not os.path.exists(ruta_completa):
#             return jsonify({"error": "Archivo no encontrado"}), 404
#         return send_from_directory(UPLOAD_FOLDER, nombre_archivo, as_attachment=False)
#     except Exception as e:
#         return jsonify({"error": f"Error al servir el archivo: {str(e)}"}), 500
