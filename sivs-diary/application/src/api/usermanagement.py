from flask import Blueprint, request
from src.support.db_handler import DBHandler

user_management_blueprint = Blueprint('users', __name__)
db_handler = DBHandler()
db_handler.connect()

@user_management_blueprint.route('/api/authorize', methods=['POST'])
def login():
    """
    Stellt einen Login Endpunkt zur Verfügung (Prüft Benutzernamen und Password), bei Erfolg übergibt diese Methode
    einen Homelink auf das Tagebuch des Benutzers zurück.
    :return:
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    result = db_handler.checkPassword(username=username,password=password)
    return result

@user_management_blueprint.route('/api/createuser', methods=['POST'])
def create_account():
    """
    Stellt einen Endpunkt zur Verfügung um einen Benutzer zu erstellen
    :return:
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    secret_question = data.get('secretQuestion')
    secret_answer = data.get('secretAnswer')
    result = db_handler.insertUser(username=username,password=password,secret_question=secret_question,
                          secret_answer=secret_answer)
    return result

@user_management_blueprint.route('/api/resetpassword', methods=['POST'])
def reset_password():
    """
    Stellt einen Endpunkt zur Verfügung um ein Passwort zurückzusetzen.
    Bei richtiger Geheimantwort, wird der Username neu gesetzt
    :return:
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    secret_answer = data.get('secret_answer')
    result = db_handler.resetPassword(username=username,password=password,secret_answer=secret_answer)
    return result

@user_management_blueprint.route('/api/resetpassword', methods=['GET'])
def initiate_reset_password():
    """
    Stellt einen Endpunkt zur Verfügung um ein Passwort zurückzusetzen.
    Geheimfrage des Benutzers wird übermittelt
    :return:
    """
    username = request.args.get('username')
    result = db_handler.getSecretQuestion(username=username)
    return result