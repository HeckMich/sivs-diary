from flask import Flask
from flask_cors import CORS
import sys
#Setzen von ENV-Pfaden
folder_path = '/home/ubuntu/sivs/sivs-diary/application/'
if folder_path not in sys.path:
    sys.path.append(folder_path)

from src.api.diary import diary_blueprint
from src.api.usermanagement import user_management_blueprint
from src.pages.views import views_blueprint


app = Flask(__name__,template_folder="./frontend/",static_folder="./frontend/static/")
#Setzt die CORS Header auf * (Übungszwecke!)
CORS(app, resources={r"/api/*": {"origins": "*"}})
#Registriert die Blueprint
#Dieser Blueprint ist für das Usermanagement zuständig (Erstellung, Login, PW-Reset)
app.register_blueprint(user_management_blueprint)
#Dieser Blueprint ist für die Tagebucheinträge zuständig (Erstellung, Auflisten, Löschen)
app.register_blueprint(diary_blueprint)
#Dieser Blueprint ist für die Bereitstellung von HTML-Seiten zuständig
app.register_blueprint(views_blueprint)

# Define routes and configurations here
if __name__ == "__main__":
    app.run(debug=True,port=9090, host='0.0.0.0')