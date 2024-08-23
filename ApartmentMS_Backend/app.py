from flask import Flask
from flask_cors import CORS
from config import Config
from routes import setup_routes
from database import db, check_database_exists, check_tables, check_connection, insert_data

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)
setup_routes(app)

with app.app_context():
    check_connection()
    check_database_exists()
    check_tables()
    insert_data()

if __name__ == '__main__':
    app.run(debug=False)
