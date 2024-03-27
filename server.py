from datetime import datetime
from flask import jsonify, Flask, request
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, create_refresh_token, get_jwt_identity, get_jwt

from sqlite.sqlite_driver import SqliteDriver
from backend.exceptions import DatabaseUnavailableError, InvalidInputError, InvalidQueryError, NoResultError

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
db = SqliteDriver("database.db")

JWT_EXPIRY_SEC = 300

def throws_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseUnavailableError as err:
            print(err)
            return jsonify({"msg": "Database unavailable."}), 500
        except InvalidInputError as err:
            return jsonify({"msg": str(err)}), 401
        except InvalidQueryError as err:
            print(err)
            return jsonify({"msg": "Backend error. Check logs."}), 503
        except NoResultError as err:
            return jsonify({"msg": str(err)}), 404
    wrapper.__name__ = func.__name__
    return wrapper

@app.before_first_request
@throws_exception
def setup_database():
    db.create_tables("sqlite/create.sql")
    db.add_mock_data("mock_data")

@app.route("/api/register", methods=["POST"])
@throws_exception
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    repeat_password = request.json.get("repeat_password", None)
    if password != repeat_password:
        return jsonify({"msg": "Passwords do not match."}), 401
    
    db.add_user(username, password)

    generated_at = datetime.now()
    response = {
        "access_token": create_access_token(identity=username,
                                            additional_claims={"generated": generated_at.strftime("%H:%M:%S")}),
        "refresh_token": create_refresh_token(identity=username)
    }
    return jsonify(response), 201

@app.route("/api/login", methods=["POST"])
@throws_exception
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not db.user_exists(username, password):
        return jsonify({"msg": "Invalid login or password."}), 401
    
    generated_at = datetime.now()
    response = {
        "access_token": create_access_token(identity=username,
                                            additional_claims={"generated_at": generated_at.strftime("%m/%d/%y %H:%M:%S")}),
        "refresh_token": create_refresh_token(identity=username)
    }
    return jsonify(response), 200

@app.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
@throws_exception
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify({"token": new_token}), 200

def jwt_token_valid(user, claims):
    if "generated_at" in claims:
        try:
            last_generated_at = datetime.strptime(claims["generated_at"], "%m/%d/%y %H:%M:%S")
            if (datetime.now() - last_generated_at).seconds < JWT_EXPIRY_SEC and db.login_exists(user):
                return True
        except ValueError:
            return False
    return False

@app.route("/api/seasons", methods=["GET", "POST"])
@throws_exception
def seasons():
    if request.method == "POST":
        db.add_season(request.json)
    return db.get_seasons()

@app.route("/api/season/<season_id>", methods=["PUT", "DELETE"])
@throws_exception
def season(season_id):
    if request.method == "PUT":
        db.edit_season(season_id, request.json)
        return db.get_seasons()
    db.delete_season(season_id)
    return jsonify({"msg": "Season deleted."}), 204

@app.route("/api/seasons/<season_id>/matches", methods=["GET", "POST"])
@throws_exception
def season_matches(season_id):
    if request.method == "POST":
        db.add_match(season_id, request.json)
    return db.get_season_matches(season_id)

@app.route("/api/seasons/<season_id>/highscore", methods=["GET"])
@throws_exception
def season_highscore(season_id):
    return db.get_season_highscore(season_id)

@app.route("/api/notifications", methods=["GET", "POST"])
@throws_exception
def notifications():
    if request.method == "POST":
        db.add_notifiaction(request.json)
    return db.get_notifiactions()

@app.route("/api/notifications/<notification_id>", methods=["PUT", "DELETE"])
@throws_exception
def notification(notification_id):
    if request.method == "PUT":
        db.edit_notifiaction(notification_id, request.json)
        return db.get_notifiactions()
    db.delete_notifiaction(notification_id)
    return jsonify({"msg": "Notifiaction deleted"}), 204

@app.route("/api/matches/", methods=["GET", "POST"])
@throws_exception
def matches():
  if request.method == "POST":
      return db.add_match(request.json), 201
  return db.get_matches(), 200

@app.route("/api/matches/<match_id>", methods=["GET", "PUT", "DELETE"])
@throws_exception
def match(match_id):
    if request.method == "PUT":
        if db.edit_match(match_id, request.json):
            return db.get_match(match_id), 200
        return {"msg": "Unable to edit match"}, 401
    elif request.method == "DELETE":
        if db.delete_match(match_id):
            return {"msg": "Match deleted."}, 201
        return {"msg": "Unable to delete match"}, 404
    return db.get_match(match_id)

@app.route("/api/matches/<match_id>/players", methods=["GET", "POST"])
@throws_exception
def match_players(match_id):
    if request.method == "POST":
        if "player_id" not in request.json:
            raise InvalidInputError("Player ID not provided.")
        db.add_match_player(match_id, request.json["player_id"])
    return db.get_match_players(match_id)

@app.route("/api/teams/", methods=["GET", "POST"])
@throws_exception
def teams():
    if request.method == "POST":
        db.add_team(request.json)
    return db.get_teams()

@app.route("/api/teams/<team_id>", methods=["PUT", "DELETE"])
@throws_exception
def team(team_id):
    if request.method == "PUT":
        db.edit_team(team_id, request.json)
        return db.get_teams()
    db.delete_team(team_id)
    return jsonify({"msg": "Team deleted."}), 204

@app.route("/api/substitutions", methods=["GET", "POST"])
@throws_exception
def substitutions():
    if request.method == "POST":
        db.add_substitution(request.json)
    return db.get_substitutions()

@app.route("/api/substitutions/<substitution_id>", methods=["GET", "PUT"])
@throws_exception
def substitution(substitution_id):
    if request.method == "PUT":
        db.edit_substitution(substitution_id, request.json)
    return db.get_substitution(substitution_id, request.json), 200

@app.route("/api/players", methods=["GET", "POST"])
@throws_exception
def players():
    if request.method == "POST":
        db.add_player(request.json)
    return db.get_players()

@app.route("/api/players/<player_id>", methods=["GET", "PUT", "DELETE"])
@throws_exception
def player(player_id):
    if request.method == "DELETE":
        db.delete_player(player_id)
        return jsonify({"msg": "Player deleted."}), 204
    if request.method == "PUT":
        db.edit_player(player_id, request.json)
    return db.get_player(player_id)

@app.route("/api/events", methods=["GET", "POST"])
@throws_exception
def events():
    if request.method == "POST":
        return db.add_event(request.json)
    return db.get_events(request.json)

@app.route("/api/events/<event_id>", methods=["GET", "PUT", "DELETE"])
@throws_exception
def event(event_id):
    if request.method == "PUT":
        return db.edit_event(event_id, request.json)
    if request.method == "DELETE":
        db.delete_event(event_id)
        return jsonify({"msg": "Event deleted."}), 204
    return db.get_event(event_id)

@app.route("/api/matches/<match_id>/events", methods=["GET"])
@throws_exception
def match_events(match_id):
    return db.get_match_events(match_id)
