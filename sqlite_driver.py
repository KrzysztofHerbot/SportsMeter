from csv import reader
import sqlite3

class SqliteDriver:
    def __init__(self, dbpath : str) -> None:
        self.dbpath = dbpath

    def get_handle(self):
        conn = None
        try:
            conn = sqlite3.connect(self.dbpath, check_same_thread=False)
        except sqlite3.Error as error:
            print(f"Sqlite error in get_connection: {error}")
        return [conn, conn.cursor()]
    
    def create_tables(self):
        conn, cur = self.get_handle()
        if conn:
            with open("mock_data/create.sql") as create_script:
                cur.executescript(create_script.read())
            conn.commit()
            cur.close()
            conn.close()
        
    def insert_from_csv(self, table : str, filepath : str, delimiter : str):
        conn, cur = self.get_handle()
        if conn:
            try:
                with open(filepath, encoding="utf-8") as csv_file:
                    content = reader(csv_file, delimiter=delimiter)
                    header = next(content)

                    for row in content:
                        cur.execute(
                            f"INSERT OR REPLACE INTO {table} ({','.join(header)}) VALUES ({','.join(row)});"
                        )
                conn.commit()
            except sqlite3.Error as error:
                print(f"Sqlite error while adding data from file {filepath} : {error}")
    
    def add_mock_data(self):
        self.insert_from_csv("Seasons", "mock_data/seasons.csv", ";")
        self.insert_from_csv("Teams", "mock_data/teams.csv", ";")
        self.insert_from_csv("Matches", "mock_data/matches.csv", ";")
        self.insert_from_csv("Events", "mock_data/events.csv", ";")

    def get_seasons(self):
        conn, cur = self.get_handle()
        rows = []
        if conn:
            cur.execute("SELECT * FROM Seasons")
            rows = [
                {
                    "season_id": entry[0],
                    "season_title": entry[1],
                    "season_start_date": entry[2],
                    "season_end_date": entry[3]
                } for entry in cur.fetchall()
            ]
            cur.close()
            conn.close()
        return rows

    def get_season_matches(self, season_id : int):
        conn, cur = self.get_handle()
        rows = []
        if conn:
            cur.execute(f"SELECT " 
                        f"m.match_id, m.match_date, m.match_start_time, m.match_end_time, t1.team_name,"
                        f"t2.team_name, m.team_a_points, m.team_b_points "
                        f"FROM Matches m, Teams t1, Teams t2 "
                        f"WHERE m.match_season = {season_id} AND m.team_a_id = t1.team_id "
                        f"AND m.team_b_id = t2.team_id")
            rows = [{
                "match_id": entry[0],
                "match_date": entry[1],
                "match_start_time": entry[2],
                "match_end_time": entry[3],
                "team_a_name": entry[4],
                "team_b_name": entry[5],
                "team_a_points": entry[6],
                "team_b_points": entry[7]} for entry in cur.fetchall()]
            cur.close()
            conn.close()
        return rows

    def get_season_highscore(self, season_id : int):
        conn, cur = self.get_handle()
        rows = []
        if conn:
            cur.execute((f"SELECT team_id, team_name, SUM(points) AS highscore FROM ("
                         f"SELECT t.team_id AS team_id, t.team_name as team_name, m.team_a_points as points "
                         f"FROM Matches m, Teams t WHERE m.match_season = {season_id} AND t.team_id = m.team_a_id"
                         f" UNION ALL "
                         f"SELECT t.team_id AS team_id, t.team_name as team_name, m.team_b_points as points "
                         f"FROM Matches m, Teams t WHERE m.match_season = {season_id} AND t.team_id = m.team_b_id"
                         f") GROUP BY team_name ORDER BY highscore DESC"))
            rows = [{"team_id": entry[0], "team_name": entry[1], "team_score": entry[2]} for entry in cur.fetchall()]
            cur.close()
            conn.close()
        return rows
    
    def get_match(self, match_id : int):
        conn, cur = self.get_handle()
        result = {}
        if conn:
            cur.execute(f"SELECT " 
                        f"m.match_id, m.match_date, m.match_start_time, m.match_end_time, t1.team_name,"
                        f"t2.team_name, m.team_a_points, m.team_b_points "
                        f"FROM Matches m, Teams t1, Teams t2 "
                        f"WHERE m.match_id = {match_id} AND m.team_a_id = t1.team_id AND m.team_b_id = t2.team_id")
            row = cur.fetchall()
            if len(row) > 0:
                result = {
                    "match_id": row[0][0],
                    "match_date": row[0][1],
                    "match_start_time": row[0][2],
                    "match_end_time": row[0][3],
                    "team_a_name": row[0][4],
                    "team_b_name": row[0][5],
                    "team_a_points": row[0][6],
                    "team_b_points": row[0][7]
                    }
            cur.close()
            conn.close()
        return result
    
    def edit_match(self, match_id : int, new_data : dict):
        conn, cur = self.get_handle()
        if conn:
            cur.execute(f"UPDATE Matches SET match_title = '{new_data['match_title']}' WHERE match_id = {match_id}")
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False
    
    def delete_match(self, match_id : int):
        conn, cur = self.get_handle()
        if conn:
            cur.execute(f"DELETE FROM Matches WHERE match_id = {match_id}")
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False
    
    def add_match(self, season_id : int, match_data : dict):
        conn, cur = self.get_handle()
        if conn:
            cur.execute(
                f"INSERT INTO Matches (season_id, match_title) "
                f"VALUES ({season_id}, '{match_data['match_title']}')"
            )
            conn.commit()
            cur.close()
            conn.close()
            return True
        return False
    
    def get_events(self):
        conn, cur = self.get_handle()
        rows = []
        if conn:
            cur.execute("SELECT event_id, event_title, event_description FROM Events")
            rows = [
                {
                    "event_id": entry[0],
                    "event_title": entry[1],
                    "event_description": entry[2]
                } for entry in cur.fetchall()
            ]
            cur.close()
            conn.close()
        return rows
