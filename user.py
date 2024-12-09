class User():
    def __init__(self, id, mail, password, rol) -> None:
        self.id = id
        self.mail = mail
        self.password = password
        self.rol = rol

    # Método para convertir el objeto User a un formato que pueda ser convertido a JSON
    def to_dict(self):
        return {
            'id': self.id,
            'mail': self.mail,
            'rol': self.rol
        }
