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

OK_STATUS_CODE = 200
CREATED_STATUS_CODE = 201
DELETED_STATUS_CODE = 204

NOT_FOUND_STATUS_CODE = 404
EXISTANT_RECORD_STATUS_CODE = 409


# This is our Team model for database player table construction
class TeamModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    owner = db.Column(db.String(50), nullable=False)
    year_formed = db.Column(db.Integer, nullable=False)
    num_players = db.Column(db.Integer, nullable=False, default=0)
    num_staff = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Team(name = {name}, owner = {owner}, num_players = {num_players})"

# This is our Player model for database player table construction
class PlayerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    team = db.Column(db.String(70), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return f"Player(name = {name}, player_id = {id}, team = {team}, position = {position})"

# This is our Staff model for database player table construction
class StaffModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    team = db.Column(db.String(70), db.ForeignKey('team_model.name'), nullable=False)
    position = db.Column(db.String(40), nullable=False)
    years_on_team = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Staff(name = {name}, id = {id}, team = {team}, position = {position}, years_on_team = {years_on_team})"

# This request parser tells us what arguments are required in any player data given
#   This specific one is for put, if you are writing an update method where 
#   you dont need all of these arguments, you should write another parser 
#   for that method below
team_put_args = reqparse.RequestParser()
team_put_args.add_argument(
    "name", type=str, help="Name of the Team is required", required=True)
team_put_args.add_argument(
    "owner", type=str, help="Owner of the team is required", required=True)
team_put_args.add_argument(
    "year_formed", type=int, help="The year the team was formed is required", required=True)

team_patch_args = reqparse.RequestParser()
team_patch_args.add_argument(
    "name", type=str, help="Name of the team")
team_patch_args.add_argument(
    "owner", type=str, help="Owner of the team")

# This dict is used as our benchmark for how marshal_with will format our team records
team_resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "owner": fields.String,
    "year_formed": fields.Integer,
    "num_players": fields.Integer,
    "num_staff": fields.Integer

}

# This request parser tells us what arguments are required in any player data given
#   This specific one is for put, if you are writing an update method where 
#   you dont need all of these arguments, you should write another parser 
#   for that method below
players_put_args = reqparse.RequestParser()
players_put_args.add_argument(
    "name", type=str, help="Name of the player is required", required=True)
players_put_args.add_argument(
    "team", type=str, help="Team of the player (if the player is a free agent put 'Free Agent')", required=True)
players_put_args.add_argument(
    "age", type=int, help="Age of the player is required", required=True)
players_put_args.add_argument(
    "height", type=int, help="Height of the player is required", required=True)
players_put_args.add_argument(
    "weight", type=str, help="Weight of the player is required", required=True)
players_put_args.add_argument(
    "position", type=str, help="Position of the player is required", required=True)

players_patch_args = reqparse.RequestParser()
players_patch_args.add_argument(
    "name", type=str, help="Name of the player")
players_patch_args.add_argument(
    "team", type=str, help="Team of the player (if the player is a free agent put 'Free Agent')")
players_patch_args.add_argument(
    "age", type=int, help="Age of the player")
players_patch_args.add_argument(
    "height", type=int, help="Height of the player")
players_patch_args.add_argument(
    "weight", type=str, help="Weight of the player")
players_patch_args.add_argument(
    "position", type=str, help="Position of the player")

# This dict is used as our benchmark for how marshal_with will format our player records
player_resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "team": fields.String,
    "age": fields.Integer,
    "height": fields.Integer,
    "weight": fields.Integer,
    "position": fields.String
}

# This request parser tells us what arguments are required in any player data given
#   This specific one is for put, if you are writing an update method where 
#   you dont need all of these arguments, you should write another parser 
#   for that method below
staff_put_args = reqparse.RequestParser()
staff_put_args.add_argument(
    "name", type=str, help="Name of the staff member is required", required=True)
staff_put_args.add_argument(
    "team", type=str, help="Team of the staff member is required", required=True)
staff_put_args.add_argument(
    "position", type=str, help="Position of the staff member is required", required=True)
staff_put_args.add_argument(
    "years_on_team", type=int, help="The number of years the staff member has been on the team is required", required=True)

staff_patch_args = reqparse.RequestParser()
staff_patch_args.add_argument(
    "name", type=str, help="Name of the staff member", required=False)
staff_patch_args.add_argument(
    "team", type=str, help="Team of the staff member", required=False)
staff_patch_args.add_argument(
    "position", type=str, help="Position of the staff member", required=False)
staff_patch_args.add_argument(
    "years_on_team", type=int, help="The number of years the staff member has been on the team", required=False)

# This dict is used as our benchmark for how marshal_with will format our player records
staff_resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "team": fields.String,
    "position": fields.String,
    "years_on_team": fields.Integer
}

# The Team resource we are accessing
class Team(Resource):

    @marshal_with(team_resource_fields)
    def get(self, team_id):
        team_record = TeamModel.query.filter_by(id=team_id).first()
        if team_record is None:
            abort(404, message="Team with given ID does not exist...")
        return team_record, OK_STATUS_CODE

    @marshal_with(team_resource_fields)
    def put(self, team_id):
        args = team_put_args.parse_args()
        team_record = TeamModel.query.filter_by(id=team_id).first()
        if team_record:
            abort(EXISTANT_RECORD_STATUS_CODE, message="Team with given team ID already exists")
        team = TeamModel(id=team_id, 
                         name=args['name'],
                         owner=args['owner'],
                         year_formed=args['year_formed'])
        db.session.add(team)
        db.session.commit()
        return team, CREATED_STATUS_CODE

    @marshal_with(team_resource_fields)
    def patch(self, team_id):
        args = team_patch_args.parse_args()
        team_record = TeamModel.query.filter_by(id=team_id).first()
        if team_record is None:
            abort(NOT_FOUND_STATUS_CODE, message="Team with given ID does not exist...")
        if args['name'] is not None:
            # If the name of the team has changed
            #   find all of its players and staff and update the team they play/work for with the new name
            #   then update the name of the team to the new name
            player_records = PlayerModel.query.filter_by(team=team_record.name).all()
            staff_records = StaffModel.query.filter_by(team=team_record.name).all()
            team_record.name = args['name']

            for i in range(len(player_records)):
                player_records[i].team = args['name']
            
            for i in range(len(staff_records)):
                staff_records[i].team = args['name']

        if args['owner'] is not None:
            team_record.owner = args['owner']

        db.session.commit()
        return team_record, CREATED_STATUS_CODE

    def delete(self, team_id):
        team_record = TeamModel.query.filter_by(id=team_id).first()

        # If team does not exist
        if team_record is None:
            abort(NOT_FOUND_STATUS_CODE, message="Team with given ID does not exist")
        
        # Find all the players on the former team and make them free agents
        player_records = PlayerModel.query.filter_by(team=team_record.name).all()
        for i in range(len(player_records)):
            player_records[i].team = "Free Agent"

        # Find all the staff on the former team and delete them
        staff_records = StaffModel.query.filter_by(team=team_record.name).all()
        for i in range(len(staff_records)):
            db.session.delete(staff_records[i])

        db.session.delete(team_record)
        db.session.commit()
        return "", DELETED_STATUS_CODE
    
# The Player resource we are accessing
class Player(Resource):

    # Works perfectly in tandem with team resource, per team player count, and free agency
    @marshal_with(player_resource_fields)
    def get(self, player_id):
        player_record = PlayerModel.query.filter_by(id=player_id).first()
        if not player_record:
            abort(404, message="Player with given ID does not exist...")
        return player_record, 200

    # Works perfectly in tandem with team resource, per team player count, and free agency
    @marshal_with(player_resource_fields)
    def put(self, player_id):
        args = players_put_args.parse_args()
        player_record = PlayerModel.query.filter_by(id=player_id).first()

        # If their is an existing player record
        if player_record:
            abort(EXISTANT_RECORD_STATUS_CODE, message="Player with given ID already exists...")

        team_record = TeamModel.query.filter_by(name=args['team']).first()

        # If the player isnt a free agent and the team doesnt exist
        if args['team'] != "Free Agent" and team_record is None:
            abort(NOT_FOUND_STATUS_CODE, message="Player cannot play for a team that doesnt exist...")

        # If the player isnt a free agent but the team exists
        if args['team'] != "Free Agent":
            team_record.num_players += 1

        player = PlayerModel(
            id=player_id,
            name=args['name'],
            team=args['team'],
            age=args['age'],
            height=args['height'],
            weight=args['weight'],
            position=args['position']
        )

        db.session.add(player)
        db.session.commit()
        return player, CREATED_STATUS_CODE

    # Works perfectly in tandem with team resource, per team player count, and free agency
    @marshal_with(player_resource_fields)
    def patch(self, player_id):
        player_record = PlayerModel.query.filter_by(id=player_id).first()
        if player_record is None:
            abort(NOT_FOUND_STATUS_CODE, message="Player with given ID does not exist")
        args = players_patch_args.parse_args()
        if args['name'] is not None:
            player_record.name = args['name']
        if args['team'] is not None:
            # Find the records for the old and new teams
            old_team_record = TeamModel.query.filter_by(name=player_record.team).first()
            new_team_record = TeamModel.query.filter_by(name=args['team']).first()

            # Check if new team exists
            #   If the player's new team is 'Free Agent', 
            #   both of these statements will be skipped
            if new_team_record is None and args['team'] != "Free Agent":
                abort(NOT_FOUND_STATUS_CODE, message="Player cannot play for a team that doesnt exist...")
            elif new_team_record:
                # Add player to new team
                new_team_record.num_players += 1

            # Subtract player from old team if the player was not a free agent
            if old_team_record:
                old_team_record.num_players -= 1

            # Set players team to new team
            player_record.team = args['team']
        if args['age'] is not None:
            player_record.age = args['age']
        if args['height'] is not None:
            player_record.height = args['height']
        if args['weight'] is not None:
            player_record.weight = args['weight']
        if args['position'] is not None:
            player_record.position = args['position']
        db.session.commit()
        return player_record, OK_STATUS_CODE

    # Works perfectly in tandem with team resource, per team player count, and free agency
    def delete(self, player_id):
        player_record = PlayerModel.query.filter_by(id=player_id).first()
        if player_record is None:
            abort(NOT_FOUND_STATUS_CODE, message="Player with the given ID does not exist...")

        team_record = TeamModel.query.filter_by(name=player_record.team).first()

        # If the player is not a free agent
        if team_record:
            team_record.num_players -= 1

        db.session.delete(player_record)
        db.session.commit()
        return "", DELETED_STATUS_CODE

# The Staff resource we are accessing
class Staff(Resource):

    # Works perfectly in tandem with team resource, per team staff member count
    @marshal_with(staff_resource_fields)
    def get(self, staff_id):
        staff_record = StaffModel.query.filter_by(id=staff_id).first()
        if staff_record is None:
            abort(404, message="A Staff Member with the given ID does not exist...")
        return staff_record, 200

    # Works perfectly in tandem with team resource, per team staff member count
    @marshal_with(staff_resource_fields)
    def put(self, staff_id):
        args = staff_put_args.parse_args()
        staff_record = StaffModel.query.filter_by(id=staff_id).first()
        
        if staff_record is not None:
            abort(409, message="Staff Member with given ID already exists...")

        staff = StaffModel(
            id=staff_id,
            name=args['name'],
            team=args['team'],
            position=args['position'],
            years_on_team=args['years_on_team']
        )

        team_record = TeamModel.query.filter_by(name=args['team']).first()
        team_record.num_staff += 1

        db.session.add(staff)
        db.session.commit()
        return staff, 201

    # Works perfectly in tandem with team resource, per team staff member count
    @marshal_with(staff_resource_fields)
    def patch(self, staff_id):
        args = staff_patch_args.parse_args()
        staff_record = StaffModel.query.filter_by(id=staff_id).first()
        if staff_record is None:
            abort(404, message="Staff Member with the given ID does not exist...")
        if args['name'] is not None:
            staff_record.name = args['name']
        if args['team'] is not None:
            # Find the records for the old and new teams
            old_team_record = TeamModel.query.filter_by(name=staff_record.team).first()
            new_team_record = TeamModel.query.filter_by(name=args['team']).first()

            # Check if new team exists or if it is a nonexistant team
            if new_team_record is None:
                abort(404, message="Staff member cannot work for a team that doesnt exist...")
            
            # Add staff member to new team
            new_team_record.num_staff += 1

            # Subtract staff member from old team
            old_team_record.num_staff -= 1

            # Set staff member's team to new team
            staff_record.team = args['team']
        if args['position'] is not None:
            staff_record.position = args['position']
        if args['years_on_team'] is not None:
            staff_record.years_on_team = args['years_on_team']

        db.session.commit()
        return staff_record, 200

    # Works perfectly in tandem with team resource, per team staff member count
    def delete(self, staff_id):
        staff_record = StaffModel.query.filter_by(id=staff_id).first()
        if staff_record is None:
            abort(404, message="A staff member with the given ID does not exist...")

        # Subtract the staff member from their former team
        team_record = TeamModel.query.filter_by(name=staff_record.team).first()
        team_record.num_staff -= 1
        
        db.session.delete(staff_record)
        db.session.commit()

        return "", 204

# Comment and uncomment this line as needed in order to add additional resources
# db.create_all()

# Here is where we add all of our resources
#   We must give flask the name of the resource
#   and the path of the resource at the end of the base URI.
#   For this resource we are saying the user must enter player, followed by some player ID
api.add_resource(Team, "/team/<int:team_id>")
api.add_resource(Player, "/player/<int:player_id>")
api.add_resource(Staff, "/staff/<int:staff_id>")


# Here is where we run the server
if __name__ == "__main__":
    app.run(debug=True)
