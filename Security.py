from decouple import config
import datetime
import jwt
import pytz


class Security():

   
    tz = pytz.timezone("America/Santiago")

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
                encoded_token = authorization.split(" ")[1]  # Asegúrate de obtener solo el token
                decoded_token = jwt.decode(encoded_token, "JWT_KEY", algorithms=['HS256'])
                print(decoded_token)  # Esto te ayudará a ver el contenido del token
                return True
            except jwt.ExpiredSignatureError:
                return False  # El token ha expirado
            except jwt.InvalidTokenError:
                return False  # El token no es válido
        return False  # Si no se encuentra la cabecera 'Authorization'
    