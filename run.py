#run.py
from app import create_app
import os

env = os.getenv('FLASK_ENV', 'development')
app = create_app(env=env)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
