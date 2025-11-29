import logging
from flask import Blueprint, request
from src.support.db_handler import DBHandler

logger = logging.getLogger(__name__)

user_management_blueprint = Blueprint('users', __name__)

try:
    db_handler = DBHandler()
    db_handler.connect()
    logger.info("Database connection established for User Management Blueprint.")
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")


@user_management_blueprint.route('/api/authorize', methods=['POST'])
def login():
    """
    Stellt einen Login Endpunkt zur Verfügung (Prüft Benutzernamen und Password), bei Erfolg übergibt diese Methode
    einen Homelink auf das Tagebuch des Benutzers zurück.
    :return:
    """
    data = request.get_json()
    password = data.get('password')
    username = data.get('username')
    logger.info(f"Login attempt received for user: {username} and {password}")
    try:

        result = db_handler.checkPassword(username=username, password=password)

        logger.info(f"Login operation completed for {username}. Result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error during login for user {username}: {e}")
        return {"error": "Login failed due to server error"}, 500


@user_management_blueprint.route('/api/createuser', methods=['POST'])
def create_account():
    """
    Stellt einen Endpunkt zur Verfügung um einen Benutzer zu erstellen
    :return:
    """
    data = request.get_json()
    username = data.get('username')

    logger.info(f"Request to create new user account: {username}")

    try:
        password = data.get('password')
        secret_question = data.get('secretQuestion')
        secret_answer = data.get('secretAnswer')

        result = db_handler.insertUser(username=username, password=password,
                                       secret_question=secret_question, secret_answer=secret_answer)

        return result
    except Exception as e:
        logger.error(f"Error creating user {username}: {e}")
        return {"error": "User creation failed"}, 500


@user_management_blueprint.route('/api/resetpassword', methods=['POST'])
def reset_password():
    """
    Stellt einen Endpunkt zur Verfügung um ein Passwort zurückzusetzen.
    Bei richtiger Geheimantwort, wird der Username neu gesetzt
    :return:
    """
    data = request.get_json()
    username = data.get('username')

    logger.info(f"Password reset attempt for user: {username}")

    try:
        password = data.get('password')
        secret_answer = data.get('secret_answer')

        result = db_handler.resetPassword(username=username, password=password, secret_answer=secret_answer)

        logger.info(f"Password reset result for {username}: {result}")
        return result
    except Exception as e:
        logger.error(f"Error resetting password for {username}: {e}")
        return {"error": "Password reset failed"}, 500


@user_management_blueprint.route('/api/resetpassword', methods=['GET'])
def initiate_reset_password():
    """
    Stellt einen Endpunkt zur Verfügung um ein Passwort zurückzusetzen.
    Geheimfrage des Benutzers wird übermittelt
    :return:
    """
    username = request.args.get('username')

    logger.info(f"Fetching secret question for user: {username}")

    try:
        result = db_handler.getSecretQuestion(username=username)
        logger.info(
            f"Secret question retrieved for {username}: {bool(result)}")  # Logging bool to avoid logging sensitive data if result contains it
        return result
    except Exception as e:
        logger.error(f"Error fetching secret question for {username}: {e}")
        return {"error": "Could not fetch secret question"}, 500