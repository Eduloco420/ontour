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
    if not request.is_json:
        return jsonify({'message': 'Content-type must be JSON'}), 400
    
    data = request.get_json()
    
    if 'mail' not in data or 'password' not in data:
        return jsonify({'message': 'Missing mail or password'}), 400
    
    mail = data['mail']
    password = data['password']

    _user = User(0, mail, password, "")
    authenticated_user = AuthService.login_user(_user)

    if authenticated_user:
        encoded_token = Security.generate_token(authenticated_user)
        return jsonify({'success': True, 'token': encoded_token, 'user': authenticated_user.to_dict()})
    else:
        return jsonify({'message': 'Unauthorized'}), 401


############

class AuthService():

    @classmethod
    def login_user(cls, user):
        try:
            cursor = conexion.connection.cursor()
            authenticated_user = None
            
            cursor.execute('SELECT id, mail, password, rol FROM user WHERE mail = %s AND password = %s', (user.mail, user.password))
            row = cursor.fetchone()

            if row:
                authenticated_user = User(int(row[0]), row[1], row[2], row[3])
            cursor.close()

            return authenticated_user

        except Exception as ex:
            print(f"Error during login: {str(ex)}")
            return None  # Si ocurre un error, devuelve None


@main.route('/validar', methods=['POST'])
def validar():
    has_access = Security.verify_token(request.headers)
    if has_access:
        return jsonify({'message': "SUCCESS", 'success': True})
    else:
        response = jsonify({'message': 'Unauthorized', 'success': False})
        return response, 401

    
@main.route('/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'No se proporcionó un token'}), 401

    token = auth_header.split(" ")[1]

    try:
        # Agregar el token a la lista negra
        Security.blacklist_token(token)
        return jsonify({'message': 'Sesión cerrada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
