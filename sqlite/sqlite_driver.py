from csv import reader
import sqlite3

from backend.exceptions import DatabaseUnavailableError, InvalidInputError, InvalidQueryError, NoResultError

NOTIFICATION_FIELDS = ["notification_id", "notification_title", "notification_description"]
MATCH_FIELDS = ["match_id", "match_date", "match_start_time", "match_end_time",
                "match_season", "team_a_id", "team_b_id", "team_a_points", "team_b_points"]
SEASON_FIELDS = ["season_id", "season_title", "season_start_date", "season_end_date"]
TEAM_FIELDS = ["team_id", "team_name"]
PLAYER_FIELDS = ["player_id", "player_name", "player_gender", "player_team"]
SUBSTITUTION_FIELDS = ["substitution_id", "substitution_match", "substitution_time",
                       "substituted_player", "substituting_player"]
EVENT_FIELDS = ["event_id", "match_id", "event_player_1", "event_player_2", "event_type", "event_value"]
MAX_GENDER_PLAYERS = 4

class SqliteContext:
    def __init__(self, dbpath : str) -> None:
        self.dbpath = dbpath
    
    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.dbpath)
            if not self.conn:
                raise DatabaseUnavailableError("Unable to connect to db, check connection")
            self.cursor = self.conn.cursor()
            return [self.conn, self.cursor]
        except sqlite3.Error as error:
            raise DatabaseUnavailableError(f"Unable to connect to db, error: {error}")
    
    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.conn.close()

class SqliteDriver:
    def __init__(self, dbpath : str) -> None:
        self.dbpath = dbpath
    
    def create_tables(self, script_path : str):
        with SqliteContext(self.dbpath) as [conn, cur]:
            with open(script_path) as create_script:
                cur.executescript(create_script.read())
            conn.commit()
        
    def insert_from_csv(self, table : str, filepath : str, delimiter : str):
        try:
            with SqliteContext(self.dbpath) as [conn, cur]:
                with open(filepath, encoding="utf-8") as csv_file:
                    content = reader(csv_file, delimiter=delimiter)
                    header = next(content)

                    for row in content:
                        cur.execute(
                            f"INSERT OR REPLACE INTO {table} ({','.join(header)}) VALUES ({','.join(row)});"
                        )
                    conn.commit()
        except sqlite3.Error as error:
            raise InvalidQueryError(f"Sqlite error while adding data from file {filepath} : {error}")
    
    def add_mock_data(self, data_directory : str):
        self.insert_from_csv("Seasons", f"{data_directory}/seasons.csv", ";")
        self.insert_from_csv("Teams", f"{data_directory}/teams.csv", ";")
        self.insert_from_csv("Matches", f"{data_directory}/matches.csv", ";")
        self.insert_from_csv("Notifications", f"{data_directory}/notifications.csv", ";")
        self.insert_from_csv("Players", f"{data_directory}/players.csv", ";")
        self.insert_from_csv("Match_Players", f"{data_directory}/match_players.csv", ";")
    
    def get_insert_query(self, table : str, data : dict):
        insert_query = f"INSERT INTO {table} ("
        for key in data:
            insert_query += f"{key}, "
        insert_query = insert_query[:-2] + ") VALUES ("
        for value in data.values():
            if value is None:
                insert_query += "NULL, "
            else:
                insert_query += f"'{value}', " if type(value) == str else f"{value}, "
        insert_query = insert_query[:-2] + ")"
        return insert_query
    
    def get_update_query(self, table : str, data : dict, target_name : str, target_value):
        update_query = f"UPDATE {table} SET "
        for key in data:
            update_query += f"{key} = "
            if data[key] is None:
                update_query += "NULL, "
            else:
                update_query += f"'{data[key]}', " if type(data[key]) == str else f"{data[key]}, "
        update_query = update_query[:-2] + f" WHERE {target_name} = {target_value}"
        return update_query
    
    def input_valid(self, allowed_fields : list, input_data : dict):
        for key in input_data:
            if key not in allowed_fields:
                raise InvalidInputError(f"Illegal field in input data: {key}")
        return True

    def get_notifications(self):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute("SELECT notification_id, notification_title, notification_description FROM Notifications")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching notifications: {error}")
            rows = [
                {
                    "notification_id": entry[0],
                    "notification_title": entry[1],
                    "notification_description": entry[2]
                } for entry in cur.fetchall()
            ]
        return rows

    def add_notification(self, notification_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(NOTIFICATION_FIELDS, notification_data):
                try:
                    cur.execute(self.get_insert_query("Notifications", notification_data))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while adding notification: {error}")
                return True 
        return False

    def edit_notification(self, notification_id : int, notification_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(NOTIFICATION_FIELDS, notification_data):
                if "notification_id" in notification_data:
                    del notification_data["notification_id"]
                try:
                    cur.execute(self.get_update_query("Notifications", notification_data,
                                                      "notification_id", notification_id))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while editing notification: {error}")
                return True
        return False
    
    def delete_notification(self, notification_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Notifications WHERE notification_id = {notification_id}")
                conn.commit()
                return True
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting notification: {error}")

    def get_seasons(self):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute("SELECT * FROM Seasons")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching seasons: {error}")
            rows = [
                {
                    "season_id": entry[0],
                    "season_title": entry[1],
                    "season_start_date": entry[2],
                    "season_end_date": entry[3]
                } for entry in cur.fetchall()
            ]
        return rows

    def add_season(self, season_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(SEASON_FIELDS, season_data):
                try:
                    cur.execute(self.get_insert_query("Seasons", season_data))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while adding new season: {error}")
                return True
        return False

    def edit_season(self, season_id, season_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(SEASON_FIELDS, season_data):
                if "season_id" in season_data:
                    del season_data["season_id"]
                try:
                    cur.execute(self.get_update_query("Seasons", season_data, "season_id", season_id))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while editing season: {error}")
                return True
        return False
    
    def delete_season(self, season_id):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Seasons WHERE season_id = {season_id}")
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting season: {error}")
            return True

    def get_season_highscore(self, season_id : int):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute((f"SELECT team_id, team_name, SUM(points) AS highscore FROM ("
                            f"SELECT t.team_id AS team_id, t.team_name as team_name, m.team_a_points as points "
                            f"FROM Matches m, Teams t WHERE m.match_season = {season_id} AND t.team_id = m.team_a_id"
                            f" UNION ALL "
                            f"SELECT t.team_id AS team_id, t.team_name as team_name, m.team_b_points as points "
                            f"FROM Matches m, Teams t WHERE m.match_season = {season_id} AND t.team_id = m.team_b_id"
                            f") GROUP BY team_name ORDER BY highscore DESC"))
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while getting season highscore: {error}")
            rows = [{"team_id": entry[0], "team_name": entry[1], "team_score": entry[2]} for entry in cur.fetchall()]
        return rows

    def get_teams(self):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute("SELECT team_id, team_name FROM Teams")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while getting teams: {error}")
            rows = [
                {
                    "team_id": entry[0],
                    "team_name": entry[1]
                } for entry in cur.fetchall()
            ]
        return rows
    
    def add_team(self, team_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(TEAM_FIELDS, team_data):
                try:
                    cur.execute(self.get_insert_query("Teams", team_data))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while adding new team: {error}")
                return True
        return False
    
    def edit_team(self, team_id : int, team_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(TEAM_FIELDS, team_data):
                if "team_id" in team_data:
                    del team_data["team_id"]
                try:
                    cur.execute(self.get_update_query("Teams", team_data, "team_id", team_id))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while editing team: {error}")
                return True
        return False
    
    def delete_team(self, team_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Teams WHERE team_id = {team_id}")
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting team: {error}")
            return True

    def get_matches(self):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute("SELECT * FROM Matches")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while getting matches: {error}")
            rows = [
                {
                    "match_id": entry[0],
                    "match_date": entry[1],
                    "match_start_time": entry[2],
                    "match_end_time": entry[3],
                    "match_season": entry[4],
                    "team_a_id": entry[5],
                    "team_b_id": entry[6],
                    "team_a_points": entry[7],
                    "team_b_points": entry[8]
                } for entry in cur.fetchall()
            ]
        return rows

    def get_match(self, match_id : int):
        result = {}
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT " 
                            f"m.match_id, m.match_date, m.match_start_time, m.match_end_time, m.team_a_id,"
                            f"t1.team_name, m.team_b_id, t2.team_name, m.team_a_points, m.team_b_points "
                            f"FROM Matches m, Teams t1, Teams t2 "
                            f"WHERE m.match_id = {match_id} AND m.team_a_id = t1.team_id AND m.team_b_id = t2.team_id")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while getting a match: {error}")
            row = cur.fetchall()
            if len(row) > 0:
                result = {
                    "match_id": row[0][0],
                    "match_date": row[0][1],
                    "match_start_time": row[0][2],
                    "match_end_time": row[0][3],
                    "team_a_id": row[0][4],
                    "team_a_name": row[0][5],
                    "team_b_id": row[0][6],
                    "team_b_name": row[0][7],
                    "team_a_points": row[0][8],
                    "team_b_points": row[0][9]
                    }
        return result

    def get_season_matches(self, season_id : int):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT " 
                            f"m.match_id, m.match_date, m.match_start_time, m.match_end_time, t1.team_name,"
                            f"t2.team_name, m.team_a_points, m.team_b_points "
                            f"FROM Matches m, Teams t1, Teams t2 "
                            f"WHERE m.match_season = {season_id} AND m.team_a_id = t1.team_id "
                            f"AND m.team_b_id = t2.team_id")
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while getting season matches: {error}")
            rows = [{
                "match_id": entry[0],
                "match_date": entry[1],
                "match_start_time": entry[2],
                "match_end_time": entry[3],
                "team_a_name": entry[4],
                "team_b_name": entry[5],
                "team_a_points": entry[6],
                "team_b_points": entry[7]} for entry in cur.fetchall()]
        return rows

    def add_match(self, match_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(MATCH_FIELDS, match_data):
                if "match_id" in match_data:
                    del match_data["match_id"]
                try:
                    cur.execute(self.get_insert_query("Matches", match_data))
                    conn.commit()
                    cur.execute("SELECT match_id FROM Matches ORDER BY match_id LIMIT 1")
                    res = cur.fetchall()
                    if len(res) > 0:
                        return self.get_match(res[0][0])
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while adding new match: {error}")
        return {}
    
    def edit_match(self, match_id : int, match_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(MATCH_FIELDS, match_data):
                if "match_id" in match_data:
                    del match_data["match_id"]
                try:
                    cur.execute(self.get_update_query("Matches", match_data, "match_id", match_id))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while editing match: {error}")
                return True
        return False
    
    def delete_match(self, match_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Matches WHERE match_id = {match_id}")
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting match: {error}")
            return True

    def get_players(self):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute("SELECT p.player_id, p.player_name, p.player_gender, t.team_name FROM Players p,"
                            " Teams t WHERE p.player_team = t.team_id")
                rows = [{
                    "player_id": entry[0],
                    "player_name": entry[1],
                    "player_gender": entry[2],
                    "player_team": entry[3]
                    } for entry in cur.fetchall()
                ]
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching players: {error}")
        return rows

    def get_player(self, player_id : int):
        response = {}
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT p.player_id, p.player_name, p.player_gender, t.team_name FROM Players p, "
                            f"Teams t WHERE p.player_team = t.team_id AND p.player_id = {player_id}")
                row = cur.fetchall()
                response = {
                    "player_id": row[0][0],
                    "player_name": row[0][1],
                    "player_gender": row[0][2],
                    "player_team": row[0][3]
                }
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching player: {error}")
            except IndexError:
                raise NoResultError(f"Player {player_id} does not exist.")
        return response

    def add_player(self, player_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(PLAYER_FIELDS, player_data):
                if "player_gender" in player_data:
                    if player_data["player_gender"] not in ["Male", "Female", "Nonbinary"]:
                        raise InvalidInputError("Not allowed gender provided.")
                try:
                    cur.execute(self.get_insert_query("Players", player_data))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while adding new player: {error}")
                return True
        return False
    
    def edit_player(self, player_id : int, player_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            if self.input_valid(PLAYER_FIELDS, player_data):
                if "player_id" in player_data:
                    del player_data["player_id"]
                if "gender" in player_data:
                    if player_data["gender"] not in ["Male", "Female", "Nonbinary"]:
                        raise InvalidInputError("Not allowed gender provided.")
                try:
                    cur.execute(self.get_update_query("Players", player_data, "player_id", player_id))
                    conn.commit()
                except sqlite3.Error as error:
                    raise InvalidQueryError(f"Error while editing player: {error}")
                return True
        return False

    def delete_player(self, player_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Players WHERE player_id = {player_id}")
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting player: {error}")
            return True
    
    def get_substitutions(self):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute("SELECT s.*, p1.player_name, p2.player_name FROM Substitutions s, Players p1, Players p2"
                            " WHERE s.substituted_player = p1.player_id AND s.substituting_player = p2.player_id")
                rows = [{
                    "substitution_id": entry[0],
                    "substitution_time": entry[1],
                    "substitution_match": entry[2],
                    "substituted_player": entry[3],
                    "substituting_player": entry[4],
                    "substituted_player_name": entry[5],
                    "substituting_player_name": entry[6]   
                } for entry in cur.fetchall()]
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching substitutions: {error}")
        return rows
    
    def get_match_substitutions(self, match_id : int):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT s.*, p1.player_name, p2.player_name FROM Substitutions s, Players p1, Players p2"
                            f" WHERE s.substituted_player = p1.player_id AND s.substituting_player = p2.player_id"
                            f" AND s.substitution_match = {match_id}")
                rows = [{
                    "substitution_id": entry[0],
                    "substitution_time": entry[1],
                    "substitution_match": entry[2],
                    "substituted_player": entry[3],
                    "substituting_player": entry[4],
                    "substituted_player_name": entry[5],
                    "substituting_player_name": entry[6]   
                } for entry in cur.fetchall()]
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching substitutions for match {match_id}: {error}")
        return rows
        
    def get_substitution(self, substitution_id : int):
        result = {}
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT s.*, p1.player_name, p2.player_name FROM Substitutions s, Players p1, Players p2"
                            f" WHERE s.substituted_player = p1.player_id AND s.substituting_player = p2.player_id"
                            f" AND s.substitution_id = {substitution_id}")
                row = cur.fetchall()
                result = {
                    "substitution_id": row[0][0],
                    "substitution_time": row[0][1],
                    "substitution_match": row[0][2],
                    "substituted_player": row[0][3],
                    "substituting_player": row[0][4],
                    "substituted_player_name": row[0][5],
                    "substituting_player_name": row[0][6]   
                }
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching substitution: {error}")
            except IndexError:
                raise NoResultError(f"Unable to find substitution with id {substitution_id}.")
        return result
    
    def get_match_players(self, match_id : int):
        rows = []
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT * FROM Match_Players WHERE match_id = {match_id}")
                rows = [{
                    "match_player_id": entry[0],
                    "match_player": entry[1],
                    "match_id": entry[2],
                    "player_active": True if entry[3] == 1 else False
                } for entry in cur.fetchall()]
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching players for match {match_id} : {error}")
        return rows
    
    def check_gender_ratio(self, match_id : int, player_id : int, old_player_id = None):
        player_data = self.get_player(player_id)
        gender_ratio = {"Male": 0, "Female": 0, "Nonbinary": 0}

        if old_player_id is not None:
            old_player = self.get_player(old_player_id)
            gender_ratio[old_player["player_gender"]] -= 1
        gender_ratio[player_data["player_gender"]] += 1

        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT p.player_gender FROM Match_Players mp, Players p WHERE mp.match_id"
                            f" = {match_id} AND mp.match_player_id = p.player_id AND mp.player_active = 1")
                for row in cur.fetchall():
                    gender_ratio[row[0]] += 1
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching gender ratio: {error}")
        
        if any(gender > MAX_GENDER_PLAYERS for gender in gender_ratio.values()):
            raise InvalidInputError("Gender rule broken!")
        
    def check_players_same_team(self, old_player : int, new_player : int):
        old_player_data = self.get_player(old_player)
        new_player_data = self.get_player(new_player)
        if old_player_data["player_team"] != new_player_data["player_team"]:
            raise InvalidInputError("Players are not in the same team!")
        return True
    
    def substitute_player(self, match_id : int, old_player : int, new_player : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                self.check_players_same_team(old_player, new_player)
                players = self.get_match_players(match_id)
                old_player_detected = False
                new_player_detected = False
                for player in players:
                    if player["match_player"] == old_player:
                        if player["player_active"] == False:
                            raise InvalidInputError("Substituted player is inactive!")
                        old_player_detected = True
                    if player["match_player"] == new_player:
                        if player["player_active"] == True:
                            raise InvalidInputError("Substituting player is already active!")
                        new_player_detected = True

                if not old_player_detected:
                    raise InvalidInputError(f"Player {old_player} does not play in this match!")
                cur.execute(f"UPDATE Match_Players SET player_active = 0 WHERE "
                            f"match_id = {match_id} AND match_player = {old_player}")
                
                if not new_player_detected:
                    self.check_gender_ratio(match_id, new_player, old_player)
                    cur.execute(f"INSERT INTO Match_Players(match_player, match_id, player_active)"
                                f"VALUES ({new_player}, {match_id}, 1)")
                else:
                    cur.execute(f"UPDATE Match_Players SET player_active = 1 WHERE "
                                f"match_id = {match_id} AND match_player = {new_player}")
                    
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while changing match {match_id} players: {error}")
    
    def add_substitution(self, match_id : int, substitution_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                self.substitute_player(match_id, substitution_data["substituted_player"],
                                       substitution_data["substituting_player"])
                substitution_data["substitution_match"] = match_id
                cur.execute(self.get_insert_query("Substitutions", substitution_data))
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while adding new player: {error}")
        return True
    
    def edit_substitution(self, substitution_id : int, substitution_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                if "substitution_id" in substitution_data:
                    del substitution_data["substitution_id"]
                self.substitute_player(substitution_data["substitution_match"],
                                       substitution_data["substituted_player"],
                                       substitution_data["substituting_player"])
                cur.execute(self.get_update_query("Substitutions", substitution_data,
                                                  "substitution_id", substitution_id))
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while editing substitution: {error}")
        return True
    
    def add_match_player(self, match_id : int, player_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                self.check_gender_ratio(match_id, player_id)
                players = self.get_match_players(match_id)
                if any(player["match_player"] == player_id for player in players):
                    raise InvalidInputError(f"Player {player_id} is already in the match!")
                cur.execute(self.get_insert_query("Match_Players",
                                                  {"match_player": player_id, "match_id": match_id, "player_active": 1}
                                                  ))
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while adding match player: {error}")
        return True

    def delete_match_player(self, match_id : int, player_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Match_Players WHERE match_id = {match_id} AND match_player = {player_id}")
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting player {player_id}: {error}")
        return True

    def user_exists(self, user_login : str, user_password : str):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT * FROM Users WHERE user_login = '{user_login}' "
                            f"AND user_password = '{user_password}'")
                rows = cur.fetchall()
                if len(rows) > 0:
                    return True
                else:
                    return False
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching user : {error}")
            
    def login_exists(self, login : str):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT * FROM Users WHERE user_login = '{login}'")
                rows = cur.fetchall()
                if len(rows) > 0:
                    return True
                else:
                    return False
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching login : {error}")

    def add_user(self, user_login : str, user_password : str):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                if self.user_exists(user_login, user_password):
                    raise InvalidInputError(f"User {user_login} already exists!")
                cur.execute(self.get_insert_query("Users", {"user_login": user_login, "user_password": user_password}))
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while adding new user : {error}")

    def edit_user(self, user_id : int, user_data : dict):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(self.get_update_query("Users", user_data, "user_id", user_id))
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while editing user {user_id} : {error}")

    def delete_user(self, user_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Users WHERE user_id = {user_id}")
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting user {user_id}: {error}")

    def get_events(self):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute("SELECT * FROM Events")
                response = [
                    {
                        "event_id": row[0],
                        "match_id": row[1],
                        "event_player_1": row[2],
                        "event_player_2": row[3],
                        "event_type": row[4],
                        "event_value": row[5]
                    } for row in cur.fetchall()
                ]
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching events: {error}")
            return response
    
    def get_event(self, event_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT * FROM Events WHERE event_id = {event_id}")
                row = cur.fetchall()
                response = {
                    "event_id": row[0][0],
                    "match_id": row[0][1],
                    "event_player_1": row[0][2],
                    "event_player_2": row[0][3],
                    "event_type": row[0][4],
                    "event_value": row[0][5]
                }
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching event {event_id}: {error}")
            return response
    
    def get_match_events(self, match_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"SELECT * FROM Events WHERE match_id = {match_id}")
                response = [
                    {
                        "event_id": row[0],
                        "match_id": row[1],
                        "event_player_1": row[2],
                        "event_player_2": row[3],
                        "event_type": row[4],
                        "event_value": row[5]
                    } for row in cur.fetchall()
                ]
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while fetching match {match_id} events: {error}")
            return response

    def add_event(self, event_data : dict):
        self.input_valid(EVENT_FIELDS, event_data)
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(self.get_insert_query("Events", event_data))
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while adding event: {error}")
            
            cur.execute("SELECT * FROM Events ORDER BY event_id DESC LIMIT 1")
            res = cur.fetchall()
            row = {
                "event_id": res[0][0],
                "match_id": res[0][1],
                "event_player_1": res[0][2],
                "event_player_2": res[0][3],
                "event_type": res[0][4],
                "event_value": res[0][5]
            }
            return row

    def delete_event(self, event_id : int):
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(f"DELETE FROM Events WHERE event_id = {event_id}")
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while deleting event {event_id}: {error}")
    
    def edit_event(self, event_id : int, event_data : dict):
        self.input_valid(EVENT_FIELDS, event_data)
        if "event_id" in event_data:
            del event_data["event_id"]
        with SqliteContext(self.dbpath) as [conn, cur]:
            try:
                cur.execute(self.get_update_query("Events", event_data, "event_id", event_id))
                conn.commit()
            except sqlite3.Error as error:
                raise InvalidQueryError(f"Error while editing event {event_id}: {error}")
        return self.get_event(event_id)
