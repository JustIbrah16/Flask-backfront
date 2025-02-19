from functools import wraps
from flask import session, jsonify
from services.roles_queries import RolesQueries

def requiere_permiso(permiso):
    def decorador(func):
        @wraps(func)
        def funcion_decorador(*args, **kwargs):
            usuario_id = session.get('user_id')
            if not usuario_id:
                return jsonify({"error": "Usuario no autenticado"}), 401

            if not RolesQueries.tiene_permiso(usuario_id, permiso):
                return jsonify({"error": f"No tiene permisos para {permiso}"}), 403

            return func(*args, **kwargs)
        return funcion_decorador
    return decorador
