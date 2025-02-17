from flask import Blueprint, session, jsonify, request
from services.roles_queries import RolesQueries
from services.proyecto_queries import ProyectosQueries

mis_proyectos = Blueprint('mis_proyectos', __name__)

@mis_proyectos.route('/mis_proyectos/acceso', methods=['GET'])
def acceso_mis_proyectos():
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    if not RolesQueries.tiene_permiso(usuario_id, 'Acceso Mis Proyectos'):
        return jsonify({"error": "Acceso denegado a Mis Proyectos"}), 403

    proyectos = ProyectosQueries.obtener_proyectos(usuario_id)

    if not proyectos:
        return jsonify({
            "message": "Bienvenido a tus proyectos, pero no tienes proyectos asociados.",
            "proyectos": [],
            "opciones": [{"nombre": "Listar proyectos", "endpoint": "/mis_proyectos/listar"}]
        }), 200

    proyectos_json = [
        {"id": proyecto.id, "nombre": proyecto.nombre, "descripcion": proyecto.descripcion}
        for proyecto in proyectos
    ]
    return jsonify({
        "message": "Bienvenido a tus proyectos",
        "proyectos": proyectos_json,
        "opciones": [{"nombre": "Filtrar proyectos", "endpoint": "/mis_proyectos/listar"}]
    }), 200

# ////////////////////////////////////////////////////
# ////////////////////////////////////////////////////
# ////////////////////////////////////////////////////


@mis_proyectos.route('/mis_proyectos/listar', methods=['GET'])
def listar_proyectos():
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    if not RolesQueries.tiene_permiso(usuario_id, 'Acceso Mis Proyectos'):
        return jsonify({"error": "Acceso denegado a Mis Proyectos"}), 403

    nombre = request.args.get('nombre')
    proyectos = ProyectosQueries.obtener_proyectos(usuario_id=usuario_id, nombre=nombre)

    if not nombre and not proyectos:
        proyectos = ProyectosQueries.obtener_todos_proyectos()

    if not proyectos:
        return jsonify({"message": "No se encontraron proyectos"}), 404

    proyectos_json = [
        {"id": proyecto.id, "nombre": proyecto.nombre, "descripcion": proyecto.descripcion}
        for proyecto in proyectos
    ]
    return jsonify(proyectos_json), 200
## para probar en postman se debe filtrar por nombre del proyecto en params

# ////////////////////////////////////////////////////
# ////////////////////////////////////////////////////
# ////////////////////////////////////////////////////

    
@mis_proyectos.route('/mis_proyectos/resumen_tickets', methods=['GET'])
def resumen_tickets():
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    if not RolesQueries.tiene_permiso(usuario_id, 'Acceso Mis Proyectos'):
        return jsonify({"error": "Acceso denegado a Mis Proyectos"}), 403

    try:
        resumen = ProyectosQueries.obtener_resumen_tickets(usuario_id)
        if not resumen:
            return jsonify({"message": "No se encontraron tickets asociados a los proyectos"}), 404

        resumen_json = [
            {
                "proyecto_id": item.fk_proyecto,
                "proyecto_nombre": item.proyecto_nombre,
                "abiertos": item.abiertos,
                "pendientes": item.pendientes,
                "atendidos": item.atendidos,
                "cerrados": item.cerrados,
                "devueltos": item.devueltos,
            } for item in resumen
        ]
        return jsonify({"resumen": resumen_json}), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener el resumen de tickets: {str(e)}"}), 500
    
