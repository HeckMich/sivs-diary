from flask import render_template, Blueprint, request
from src.support.db_handler import DBHandler

db_handler = DBHandler()
db_handler.connect()

views_blueprint = Blueprint('views', __name__)

#Views.py stellt lediglich die Webpages zur Verfügung. Diese befinden sich im Static Folder
@views_blueprint.route('/', methods=['GET'])
def view_login():
    return render_template('index.html')

@views_blueprint.route('/pages/diary.html', methods=['GET'])
def view_diary():
    search_parameter = request.args.get('searchparameter')
    return render_template('/pages/diary.html', search_parameter=search_parameter)

@views_blueprint.route('/pages/create_account.html', methods=['GET'])
def view_create_account():
    return render_template('/pages/create_account.html')
