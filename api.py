# Import dependency
from flask import Flask, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"
    

user_arg = reqparse.RequestParser()
user_arg.add_argument('name', type=str, required=True, help="Name can not be blank")
user_arg.add_argument('email', type=str, required=True, help="Email can not be blank")

userFields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'email' : fields.String,
}

class Users(Resource):
    @marshal_with(userFields)
    # Get all users
    def get(self):
        users = UserModel.query.all()
        return users
    

    # Add user
    @marshal_with(userFields)
    def post(self):
        args = user_arg.parse_args()

        name = args.get("name")
        email = args.get("email")

        # Check existing user
        ex_user = UserModel.query.filter(
            or_(
                UserModel.name == name,
                UserModel.email == email
            )
        ).first()
        if ex_user:
            abort(404, description="User alrady exist")

        # Add user to database
        user = UserModel(name=args["name"],email=args["email"])
        db.session.add(user)
        db.session.commit()

        # Get all user and return
        users = UserModel.query.all()
        return users, 201
    

class User(Resource):
    # Get user by id
    @marshal_with(userFields)
    def get(self, id):
        # Get existing user
        user = UserModel.query.filter_by(id=id).first()

        # if not found, return not found message
        if not user:
            abort(404, description="User not found")
        # return user data
        return user
    
    
    # Update user
    @marshal_with(userFields)
    def patch(self, id):
        args = user_arg.parse_args()

        # Get existing user
        user = UserModel.query.filter_by(id=id).first()

        # if not found, return not found message
        if not user:
            abort(404, description="User not found")
        
        # Set user date
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()

        # return user data
        return user
    

    # Delete user by id
    @marshal_with(userFields)
    def delete(self, id):
        # Get existing user
        user = UserModel.query.filter_by(id=id).first()

        # if not found, return not found message
        if not user:
            abort(404, description="User not found")
        
        # Delete user
        db.session.delete(user)
        db.session.commit()

        # Get all user and return
        users = UserModel.query.all()
        return users
    

# Add route
api.add_resource(Users, "/api/users/")
api.add_resource(User, "/api/users/<int:id>")


# Error handler
@app.errorhandler(404)
def handle_404(e):
    return jsonify(error=str(e)), 404


# Add route
@app.route("/")
def home():
    return "<h1>Flask REST API</h1>"


if __name__ == "__main__":
    app.run(debug=True)