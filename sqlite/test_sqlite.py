import json
import pytest

from os import path, remove
from .sqlite_driver import SqliteDriver
from backend.exceptions import InvalidInputError, NoResultError

class TestSqlite:
    @pytest.fixture
    def database(self):
        db = SqliteDriver("test.db")
        db.create_tables("create.sql")
        yield db
        if path.exists("test.db"):
            remove("test.db")

    def test_get_notifications(self, database):
        database.insert_from_csv("Notifications", "test_input/notifications.csv", ";")
        notifications = database.get_notifications()
        with open("test_output/notifications.json", encoding="utf-8") as notifications_results:
            expected_result = json.load(notifications_results)
            assert notifications == expected_result

    def test_add_notification(self, database):
        database.add_notification(
            {
                "notification_title": "test_notification",
                "notification_description": ""
            }
        )
        notifications = database.get_notifications()
        assert notifications == [
            {
                "notification_id": 1,
                "notification_title": "test_notification",
                "notification_description": ""
            }
        ]

    def test_edit_notification(self, database):
        database.insert_from_csv("Notifications", "test_input/notifications.csv", ";")
        database.edit_notification(0, {"notification_title" : "edited title"})
        notifications = database.get_notifications()
        assert notifications[0]["notification_title"] == "edited title"
    
    def test_delete_notification(self, database):
        database.insert_from_csv("Notifications", "test_input/notifications.csv", ";")
        database.delete_notification(0)
        notifications = database.get_notifications()
        assert len(notifications) == 3 and notifications[0]["notification_id"] != 0

    def test_wrong_notification_fields(self, database):
        with pytest.raises(InvalidInputError):
            database.add_notification(
                {
                    "notification_title": "wrong_notification",
                    "notification_description": "",
                    "illegal_field": "value"
                }
            )

    def test_get_seasons(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        seasons = database.get_seasons()
        with open("test_output/seasons.json", encoding="utf-8") as seasons_results:
            expected_result = json.load(seasons_results)
            assert seasons == expected_result
    
    def test_add_season(self, database):
        database.add_season(
            {
                "season_title": "test",
                "season_start_date": "19990101",
                "season_end_date": "19990110"
            }
        )
        seasons = database.get_seasons()
        assert seasons[0] == {
            "season_id": 1,
            "season_title": "test",
            "season_start_date": "19990101",
            "season_end_date": "19990110"
        }
    
    def test_edit_season(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.edit_season(1, {"season_title" : "edited season"})
        seasons = database.get_seasons()
        assert seasons[1]["season_title"] == "edited season"
    
    def test_delete_season(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.delete_season(1)
        seasons = database.get_seasons()
        assert len(seasons) == 1 and seasons[0]["season_id"] == 0

    def test_wrong_season_fields(self, database):
        with pytest.raises(InvalidInputError):
            database.add_season(
                {
                    "season_title": "test",
                    "season_start_date": "19990101",
                    "season_end_date": "19990110",
                    "illegal_field": "some value"
                }
            )

    def test_get_season_highscore(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        highscore = database.get_season_highscore(1)
        assert highscore == [
            {
                "team_id": 2,
                "team_name": "Warszawa Unicorns",
                "team_score": 125
            },
            {
                "team_id": 8,
                "team_name": "Lublin Lynx",
                "team_score": 40
            },
            {
                "team_id": 1,
                "team_name": "Łódź Pirates",
                "team_score": 35
            }
        ]

    def test_get_teams(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        teams = database.get_teams()
        with open("test_output/teams.json", encoding="utf-8") as teams_results:
            expected_result = json.load(teams_results)
            assert teams == expected_result
    
    def test_add_team(self, database):
        database.add_team({"team_name": "test team"})
        teams = database.get_teams()
        assert teams == [{"team_id": 1, "team_name": "test team"}]
    
    def test_edit_team(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.edit_team(0, {"team_name": "edited name"})
        teams = database.get_teams()
        assert teams[0]["team_name"] == "edited name"
    
    def test_delete_team(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.delete_team(0)
        teams = database.get_teams()
        assert len(teams) == 8 and teams[0]["team_id"] != 0

    def test_wrong_team_data(self, database):
        with pytest.raises(InvalidInputError):
            database.add_team({"team_name": "test team", "illegal_field": ""})

    def test_get_matches(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        matches = database.get_matches()
        with open("test_output/matches.json", encoding="utf-8") as matches_results:
            expected_result = json.load(matches_results)
            assert matches == expected_result

    def test_get_match(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        match = database.get_match(0)
        assert match == {
            "match_id": 0,
            "match_date": "20220312",
            "match_start_time": "113000",
            "match_end_time": "123000",
            "team_a_name": "Poznań Capricorns",
            "team_b_name": "Łódź Pirates",
            "team_a_points": 50,
            "team_b_points": 100
        }

    def test_get_season_matches(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        matches = database.get_season_matches(1)
        assert matches == [
            {
                "match_id": 4,
                "match_date": "20220720",
                "match_start_time": "143000",
                "match_end_time": "153000",
                "team_a_name": "Łódź Pirates",
                "team_b_name": "Warszawa Unicorns",
                "team_a_points": 35,
                "team_b_points": 65
            },
            {
                "match_id": 5,
                "match_date": "20220810",
                "match_start_time": "090500",
                "match_end_time": "112000",
                "team_a_name": "Warszawa Unicorns",
                "team_b_name": "Lublin Lynx",
                "team_a_points": 60,
                "team_b_points": 40
            }
        ]

    def test_add_match(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.add_match(1, {
            "match_date": "20220720",
            "match_start_time": "143000",
            "match_end_time": "153000",
            "team_a_id": 0,
            "team_b_id": 1,
            "team_a_points": 35,
            "team_b_points": 65
        })
        matches = database.get_season_matches(1)
        assert matches == [
            {
                "match_id": 1,
                "match_date": "20220720",
                "match_start_time": "143000",
                "match_end_time": "153000",
                "team_a_name": "Poznań Capricorns",
                "team_b_name": "Łódź Pirates",
                "team_a_points": 35,
                "team_b_points": 65
            }
        ]
    
    def test_wrong_match_fields(self, database):
        with pytest.raises(InvalidInputError):
            database.add_match(1, {
                "match_date": "20220720",
                "match_start_time": "143000",
                "match_end_time": "153000",
                "team_a_id": 0,
                "team_b_id": 1,
                "team_a_points": 35,
                "team_b_points": 65,
                "illegal_field": ""
            })

    def test_edit_match(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.edit_match(0, {"team_a_points" : 200})
        match = database.get_match(0)
        assert match["team_a_points"] == 200
    
    def test_get_empty_match(self, database):
        match = database.get_match(0)
        assert match == {}

    def test_delete_match(self, database):
        database.insert_from_csv("Seasons", "test_input/seasons.csv", ";")
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.delete_match(0)
        matches = database.get_matches()
        assert matches[0]["match_id"] != 0
    
    def test_get_players(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        players = database.get_players()
        with open("test_output/players.json", encoding="utf-8") as players_results:
            expected_result = json.load(players_results)
            assert players == expected_result
    
    def test_get_player(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        player = database.get_player(1)
        assert player["player_id"] == 1

    def test_add_player(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.add_player({
            "player_name": "Test Name",
            "player_gender": "Male",
            "player_team": 0
        })
        player = database.get_player(1)
        assert player == {
            "player_id": 1,
            "player_name": "Test Name",
            "player_gender": "Male",
            "player_team": "Poznań Capricorns"
        }
    
    def test_wrong_player_fields(self, database):
        with pytest.raises(InvalidInputError):
            database.add_player({
                "player_name": "Test Name",
                "player_gender": "Male",
                "player_team": 0,
                "illegal_field": ""
            })

    def test_edit_player(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.edit_player(1, {"player_name" : "Edited Name"})
        match = database.get_player(1)
        assert match["player_name"] == "Edited Name"
    
    def test_get_empty_player(self, database):
        with pytest.raises(NoResultError):
            database.get_player(0)

    def test_delete_player(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.delete_player(1)
        with pytest.raises(NoResultError):
            database.get_player(1)
    
    def test_wrong_gender(self, database):
        with pytest.raises(InvalidInputError):
            database.add_player({
                "player_name": "Test Name",
                "player_gender": "some gender",
                "player_team": 0
            })

    def test_get_match_players(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")

        players = database.get_match_players(0)
        with open("test_output/match_players.json", encoding="utf-8") as players_results:
            expected_result = json.load(players_results)
            assert players == expected_result

    def test_add_match_player(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")

        database.add_match_player(0, 0)
        players = database.get_match_players(0)
        assert players == [
            {"match_player_id": 1, "match_player": 0, "match_id": 0, "player_active": True}
        ]

    def test_add_duplicate_player(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")

        database.add_match_player(0, 0)
        with pytest.raises(InvalidInputError):
            database.add_match_player(0, 0)

    def test_delete_match_player(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")

        database.delete_match_player(0, 0)
        players = database.get_match_players(0)
        assert 0 not in [ player["match_player"] for player in players ]

    def test_get_substitutions(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")
        database.insert_from_csv("Substitutions", "test_input/substitutions.csv", ";")

        substitutions = database.get_substitutions()
        with open("test_output/substitutions.json", encoding="utf-8") as substitutions_results:
            expected_result = json.load(substitutions_results)
            assert substitutions == expected_result
    
    def test_get_match_substitutions(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")
        database.insert_from_csv("Substitutions", "test_input/substitutions.csv", ";")

        substitutions = database.get_match_substitutions(0)
        with open("test_output/substitutions.json", encoding="utf-8") as substitutions_results:
            expected_result = json.load(substitutions_results)
            assert substitutions == list(filter(lambda result: result["substitution_match"] == 0, expected_result))
    
    def test_add_substitution(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")
        database.add_substitution(0, {"substitution_time": "121000", "substitution_match": 0,
                                      "substituted_player": 0, "substituting_player": 3})

        substitutions = database.get_match_substitutions(0)
        assert substitutions == [
            {"substitution_id": 1, "substitution_time": "121000", "substitution_match": 0,
             "substituted_player": 0, "substituting_player": 3, "substituted_player_name": "Maciej Kleban",
             "substituting_player_name": "Jakub Grzesiak"}
        ]

    def test_edit_substitution(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")
        database.add_substitution(0, {"substitution_time": "121000", "substitution_match": 0,
                                      "substituted_player": 1, "substituting_player": 2})
        database.edit_substitution(1, {"substitution_time": "121000", "substitution_match": 0,
                                       "substituted_player": 2, "substituting_player": 1})
        substitutions = database.get_match_substitutions(0)
        assert substitutions == [
            {"substitution_id": 1, "substitution_time": "121000", "substitution_match": 0,
             "substituted_player": 2, "substituting_player": 1, "substituted_player_name": "Kinga Banasik",
             "substituting_player_name": "Krzysztof Herbot"}
        ]

    def test_substitute_inactive_player(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")
        database.add_substitution(0, {"substitution_time": "121000", "substitution_match": 0,
                                      "substituted_player": 0, "substituting_player": 3})
        with pytest.raises(InvalidInputError):
            database.substitute_player(0, 0, 7)

    def test_substitute_actived_player(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")
        database.add_substitution(0, {"substitution_time": "121000", "substitution_match": 0,
                                      "substituted_player": 0, "substituting_player": 3})
        with pytest.raises(InvalidInputError):
            database.substitute_player(0, 3, 3)

    def test_substitute_nonexistent_player(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")

        with pytest.raises(InvalidInputError):
            database.substitute_player(0, 10, 3)

    def test_substitute_different_teams(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")

        with pytest.raises(InvalidInputError):
            database.substitute_player(0, 0, 1)

    def test_add_match_player_gender_rule(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")

        with pytest.raises(InvalidInputError):
            database.add_match_player(0, 3)

    def test_substitute_gender_rule(self, database):
        database.insert_from_csv("Teams", "test_input/teams.csv", ";")
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.insert_from_csv("Match_Players", "test_input/match_players.csv", ";")

        with pytest.raises(InvalidInputError):
            database.substitute_player(0, 6, 3)

    def test_add_event(self, database):
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        expected_result = {
            "match_id": 0, "event_player_1": 0, "event_player_2": 1,
            "event_type": "shots", "event_value": 1
        }
        res = database.add_event(expected_result)
        expected_result["event_id"] = 1
        assert res == expected_result
    
    def test_get_event(self, database):
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        expected_result = database.add_event({
            "match_id": 0, "event_player_1": 0, "event_player_2": 1,
            "event_type": "shots", "event_value": 1
        })
        res = database.get_event(1)
        assert res == expected_result
    
    def test_get_events(self, database):
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        event_1 = database.add_event({
            "match_id": 0, "event_player_1": 0, "event_player_2": 1,
            "event_type": "shots", "event_value": 1
        })
        event_2 = database.add_event({
            "match_id": 0, "event_player_1": 0, "event_player_2": None,
            "event_type": "red card", "event_value": 1
        })

        events = database.get_events()
        assert events == [event_1, event_2]

    def test_get_match_events(self, database):
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        event_1 = database.add_event({
            "match_id": 0, "event_player_1": 0, "event_player_2": 1,
            "event_type": "shots", "event_value": 1
        })
        database.add_event({
            "match_id": 1, "event_player_1": 0, "event_player_2": None,
            "event_type": "red card", "event_value": 1
        })

        events = database.get_match_events(0)
        assert events == [event_1]

    def test_delete_match(self, database):
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        event_1 = database.add_event({
            "match_id": 0, "event_player_1": 0, "event_player_2": 1,
            "event_type": "shots", "event_value": 1
        })
        assert event_1 == database.get_event(1)
        database.delete_event(1)
        events = database.get_events()
        assert len(events) == 0

    def test_edit_match(self, database):
        database.insert_from_csv("Players", "test_input/players.csv", ";")
        database.insert_from_csv("Matches", "test_input/matches.csv", ";")
        database.add_event({
            "match_id": 0, "event_player_1": 0, "event_player_2": 1,
            "event_type": "shots", "event_value": 1
        })
        event_1 = database.edit_event(1, {"event_type": "misses"})
        assert event_1 == {
            "event_id": 1,
            "match_id": 0,
            "event_player_1": 0,
            "event_player_2": 1,
            "event_type": "misses",
            "event_value": 1
        }
