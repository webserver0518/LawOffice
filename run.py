#run.py
from app import create_app
import os

env = os.getenv('FLASK_ENV', 'development')
app = create_app(env=env)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
