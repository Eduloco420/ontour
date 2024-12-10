from decouple import config
import datetime
import jwt
import pytz


class Security():

   
    tz = pytz.timezone("America/Santiago")

    blacklisted_tokens = set()

    @classmethod
    def generate_token(cls, authenticated_user):
        payload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=10),
            'mail': authenticated_user.mail,
            'rol': authenticated_user.rol
        }
        return jwt.encode(payload, "JWT_KEY", algorithm="HS256")
    
    


    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers:
            authorization = headers['Authorization']
            try:
                # Obtener token
                encoded_token = authorization.split(" ")[1]

                # Verificar si el token está en la lista negra
                if encoded_token in cls.blacklisted_tokens:
                    print("Token en lista negra")
                    return False
                
                # Decodificar el token para validarlo
                decoded_token = jwt.decode(encoded_token, "JWT_KEY", algorithms=['HS256'])
                print(decoded_token)  # Para depuración, muestra el contenido del token
                return True
            except jwt.ExpiredSignatureError:
                print("Token expirado")
                return False  # El token ha expirado
            except jwt.InvalidTokenError:
                print("Token inválido")
                return False  # El token no es válido
        return False  # Si no se encuentra la cabecera 'Authorization'

    @classmethod
    def blacklist_token(cls, token):
            cls.blacklisted_tokens.add(token)
            print(f"Token agregado a la lista negra: {token}")