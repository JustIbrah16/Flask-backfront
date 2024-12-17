from flask import Blueprint, session, jsonify, request
from services.roles_queries import RolesQueries
from services.tickets_queries import TicketsQueries
from services.proyecto_queries import ProyectosQueries
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

    return jsonify({"message": "Bienvenido a base de tickets"}), 200

@base_tickets.route('/tickets/nuevo', methods=['POST'])
def crear_ticket():
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 401
    
    data = request.form
    titulo = data.get('titulo')
    comentario = data.get('comentario')
    fk_proyecto = data.get('proyecto_id')

    if not titulo or not fk_proyecto:
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    proyecto = ProyectosQueries.obtener_proyectos(usuario_id, proyecto_id=fk_proyecto)
    if not proyecto:
        return jsonify({"error": "El proyecto no existe o no está asociado a la compañia"}), 403
    proyecto = proyecto[0]
    
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
        fk_proyecto=fk_proyecto,  
        usuario_id=usuario_id,
        archivos=archivos_adjuntos 
    )

    return jsonify({ 
        "message": "Ticket creado exitosamente", 
        "ticket_id": ticket.id 
    }), 201   

