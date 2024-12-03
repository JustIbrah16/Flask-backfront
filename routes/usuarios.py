from flask import Blueprint, request, jsonify
from services.usuarios_queries import Usuarios

usuarios = Blueprint('usuarios', __name__)