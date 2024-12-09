from flask import Blueprint, request, jsonify
# Models
from user import User
# Security
from Security import Security

# Errors
from CustomException import CustomException

from app import conexion

main = Blueprint('auth_blueprint', __name__)

def login():
    mail = request.json['mail']
    password = request.json['password']

    _user = User(0, mail, password, "")
    authenticated_user = AuthService.login_user(_user)

    if (authenticated_user != None):
        encoded_token = Security.generate_token(authenticated_user)
        return jsonify({'success': True, 'token': encoded_token})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


############

class AuthService():

    @classmethod
    def login_user(cls, user):
        try:
            sql = conexion.connection.cursor()
            authenticated_user = None
            with sql as cursor:
                cursor.execute('SELECT id, mail, password, rol FROM user WHERE mail = %s AND password = %s', (user.mail, user.password))
                
                row = cursor.fetchone()
                if row != None:
                    authenticated_user = User(int(row[0]), row[1], row[2], row[3])
                    print(row[3])
            cursor.close()
            return authenticated_user
        except CustomException as ex:
            raise CustomException(ex)

@main.route('/')
def validar():
    has_access = Security.verify_token(request.headers)
    if has_access:
        return jsonify({'message': "SUCCESS", 'success': True})
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401