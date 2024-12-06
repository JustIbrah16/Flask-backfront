from flask import Blueprint, session, jsonify
from services.roles_queries import RolesQueries

base_tickets = Blueprint('base_tickets', __name__)

@base_tickets.route('/base_tickets', methods=['GET'])
def acceso_base_tickets():
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    if not RolesQueries.tiene_permiso(usuario_id, 'Acceso Base de Tickets'):
        return jsonify({"error": "Acceso denegado a Base de Tickets"}), 403

    return jsonify({"message": "Bienvenido a base de tickets"}), 200
