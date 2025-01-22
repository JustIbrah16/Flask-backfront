from models.Users import Usuarios
from models.Roles import rol_permisos
from models.Permisos import Permisos
from utils.db import db


class RolesQueries:

    @staticmethod
    def tiene_permiso(usuario_id, permiso):
        usuario = Usuarios.query.filter_by(id=usuario_id).first()
        if not usuario or not usuario.fk_rol:
            return False
        permiso_existe = db.session.query(Permisos).join(rol_permisos).filter(
                rol_permisos.c.fk_rol == usuario.fk_rol,
                Permisos.nombre == permiso
            ).first() 
        
        return permiso_existe is not None
