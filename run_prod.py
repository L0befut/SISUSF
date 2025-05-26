# run_prod.py

from waitress import serve
from sisusf_app.app import app

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
