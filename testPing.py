from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3306/hotel_db'  # replace with your database URI
db = SQLAlchemy(app)

@app.route('/')
def test_connection():
    try:
        db.engine.execute('SELECT 1')
        return 'Connection to database successful!'
    except Exception as e:
        return f'Error connecting to database: {e}'

if __name__ == '__main__':
    app.run(debug=True)