from models.Users import Usuarios
from models.Roles import Roles
from models.Permisos import Permisos
from utils.db import db


class RolesQueries:

    @staticmethod
    def tiene_permiso(usuario_id, permiso):
        usuario = Usuarios.query.filter_by(id=usuario_id).first()
        if usuario and usuario.rol:
            return db.session.query(Roles).join(Roles.permisos).filter(
                Roles.id == usuario.fk_rol,
                Permisos.nombre == permiso
            ).first() is not None
        return False
