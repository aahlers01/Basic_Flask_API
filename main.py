# Austin Ahlers -- Basic NFL player API

# Below is the code needed to initialize a flask API
from logging import debug
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# This is our model for a database table construction
class PlayerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    team = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return f"Players(name = {name}, team = {team}, position = {position})"

# This request parser tells us what arguments are required in any data given
#   This specific one is for put, if you are writing an update method where 
#   you dont need all of these arguments, you should write another parser 
#   for that method below
players_put_args = reqparse.RequestParser()
players_put_args.add_argument(
    "name", type=str, help="Name of the player is required", required=True)
players_put_args.add_argument(
    "team", type=str, help="Team of the player is required", required=True)
players_put_args.add_argument(
    "age", type=int, help="Age of the player is required", required=True)
players_put_args.add_argument(
    "position", type=str, help="Position of the player is required", required=True)

# This dict is used as our benchmark for how marshal_with will format our records
resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "team": fields.String,
    "age": fields.Integer,
    "position": fields.String
}

# The resource we are accessing
class Player(Resource):

    # The overwriting of the get method in flask with a mw decorator
    @marshal_with(resource_fields)
    def get(self, player_id):
        result = PlayerModel.query.filter_by(id=player_id).first()
        if not result:
            abort(404, message="Player with given ID does not exist")
        return result

    # The overwriting of the put method in flask with a mw decorator
    @marshal_with(resource_fields)
    def put(self, player_id):
        args = players_put_args.parse_args()
        result = PlayerModel.query.filter_by(id=player_id).first()
        if result:
            abort(409, message="Player with given ID already exists...")
        player = PlayerModel(id=player_id,
                             name=args['name'],
                             team=args['team'],
                             age=args['age'],
                             position=args['position'])
        db.session.add(player)
        db.session.commit()
        return player, 201

    """
    def delete(self, player_id):
        abort_if_invalid_player(player_id)
        del players[player_id]
        return "", 204
    """


# Here is where we add all of our resources
#   We must given flask the name of the resource
#   and the path of the resource at the end of the base URI.
#   For this resource we are saying the user must enter player, followed by some player ID
api.add_resource(Player, "/player/<int:player_id>")

# Here is where we run the server
if __name__ == "__main__":
    app.run(debug=True)
