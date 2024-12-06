from flask import Blueprint, request, jsonify, session
from services.usuarios_queries import User_queries
from services.roles_queries import RolesQueries

usuarios = Blueprint('usuarios', __name__)

@usuarios.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    usuario = User_queries.login(username, password)
    if usuario:
        session['user_id'] = usuario.id  
        session['username'] = usuario.nombre
        return jsonify({
            "message": f"Bienvenido, {usuario.nombre}!",
            "redirect": "/inicio"
        }), 200
    return jsonify({"error": "Datos incorrectas"}), 401

@usuarios.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  
    session.pop('username', None)
    return jsonify({"message": "Sesión cerrada correctamente"}), 200

@usuarios.route('/inicio', methods=['GET'])
def inicio():
    if not session.get('user_id'):
        return jsonify({"error": "Usuario no autenticado"}), 401

    opciones = [
        {"nombre": "Mis Proyectos", "endpoint": "/mis_proyectos/acceso"},
        {"nombre": "Base de Tickets", "endpoint": "/base_tickets"}
    ]
    return jsonify({"message": "Bienvenido al Reddesk", "opciones": opciones}), 200

