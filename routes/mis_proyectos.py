from flask import Blueprint, session, jsonify
from services.roles_queries import RolesQueries

mis_proyectos = Blueprint('mis_proyectos', __name__)

@mis_proyectos.route('/mis_proyectos', methods=['GET'])
def acceso_mis_proyectos():
    usuario_id = session.get('user_id')
    if not RolesQueries.tiene_permiso(usuario_id, 'Acceso Mis Proyectos'):
        return jsonify({"error": "Acceso denegado"}), 403
    return jsonify({"message": "Bienvenido a Mis proyectos"}), 200
