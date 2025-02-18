from functools import wraps
from flask import session, jsonify
from services.roles_queries import RolesQueries

def requiere_permiso(permiso):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            usuario_id = session.get('user_id')
            if not usuario_id:
                return jsonify({"error": "Usuario no autenticado"}), 401

            if not RolesQueries.tiene_permiso(usuario_id, permiso):
                return jsonify({"error": "Acceso denegado"}), 403

            kwargs['current_user_id'] = usuario_id  
            return f(*args, **kwargs)  
        return wrapper
    return decorator

