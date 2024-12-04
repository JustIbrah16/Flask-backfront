from models.Users import Usuarios
class User_queries:

    @staticmethod
    def login(username, password):
        usuario = Usuarios.query.filter_by(nombre=username).first()
        if usuario and usuario.password == password:  
            return usuario
        return None

