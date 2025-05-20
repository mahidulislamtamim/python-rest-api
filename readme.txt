py -m venv .venv
source .venv/Scripts/activate

pip insatll flask
pip insatll flask_restful
pip insatll flask_sqlalchemy
pip freeze > requirements.txt

For install all dependency
    pip install -r requirements.txt

py create_db.py

py api.py


