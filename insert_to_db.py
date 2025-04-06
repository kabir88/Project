# import json
# import time
# import psycopg2
# from nba_api.stats.static import players
# from nba_api.stats.endpoints import CommonPlayerInfo, PlayerGameLog
# from psycopg2.extras import execute_values


# # DB connection
# conn = psycopg2.connect(
#     host="localhost",
#     port=5432,
#     user="nba_app",
#     password="pass1234",
#     dbname="nba_dashboard"
# )
# cur = conn.cursor()


# def fetch_active_players():
#     return players.get_active_players()


# def fetch_player_details(player_id):
#     try:
#         info = CommonPlayerInfo(player_id=player_id).get_normalized_dict()["CommonPlayerInfo"][0]
#         return {
#             "id": str(info["person_id"]),
#             "first_name": info["first_name"],
#             "last_name": info["last_name"],
#             "team": info["team_name"],
#             "position": info["position"],
#             "height": info["height"],
#             "weight": info["weight"],
#             "experience": info["experience"]
#         }
#     except Exception as e:
#         print(f"Error fetching details for player {player_id}: {e}")
#         return None


# def insert_player_info(player):
#     cur.execute("""
#         INSERT INTO nba_players (id, first_name, last_name, team, position, height, weight, experience)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         ON CONFLICT (id) DO UPDATE SET
#             first_name = EXCLUDED.first_name,
#             last_name = EXCLUDED.last_name,
#             team = EXCLUDED.team,
#             position = EXCLUDED.position,
#             height = EXCLUDED.height,
#             weight = EXCLUDED.weight,
#             experience = EXCLUDED.experience;
#     """, (
#         player["id"], player["first_name"], player["last_name"], player["team"],
#         player["position"], player["height"], player["weight"], player["experience"]
#     ))
#     conn.commit()


# def fetch_player_game_stats(player_id, season="2023-24"):
#     try:
#         logs = PlayerGameLog(player_id=player_id, season=season).get_normalized_dict()["PlayerGameLog"]
#         return logs
#     except Exception as e:
#         print(f"Error fetching game stats for player {player_id}: {e}")
#         return []


# def insert_game_stats(player_id, game_stats, season):
#     if not game_stats:
#         return
#     values = []
#     for game in game_stats:
#         values.append((
#             player_id,
#             game.get("Game_ID"),
#             game.get("GAME_DATE"),
#             game.get("MATCHUP"),
#             game.get("MIN"),
#             game.get("FGM"), game.get("FGA"),
#             game.get("FG3M"), game.get("FG3A"),
#             game.get("FTM"), game.get("FTA"),
#             game.get("OREB"), game.get("DREB"),
#             game.get("REB"), game.get("AST"),
#             game.get("STL"), game.get("BLK"),
#             game.get("TOV"), game.get("PF"),
#             game.get("PTS"), game.get("PLUS_MINUS"),
#             season
#         ))
#     execute_values(cur, """
#         INSERT INTO nba_player_stats (
#             player_id, game_id, game_date, matchup, min,
#             fgm, fga, fg3m, fg3a, ftm, fta, oreb, dreb,
#             reb, ast, stl, blk, tov, pf, pts, plus_minus, season
#         )
#         VALUES %s
#         ON CONFLICT DO NOTHING;
#     """, values)
#     conn.commit()


# def run_pipeline(season="2023-24", limit=50):
#     all_players = fetch_active_players()
#     for i, p in enumerate(all_players[:limit]):
#         print(f"Processing {p['full_name']} ({i + 1}/{limit})")
#         details = fetch_player_details(p["id"])
#         if details:
#             insert_player_info(details)
#             time.sleep(0.6)
#             stats = fetch_player_game_stats(p["id"], season=season)
#             insert_game_stats(p["id"], stats, season)
#             time.sleep(0.6)

#     print("✅ All players processed and data inserted.")


# if __name__ == "__main__":
#     run_pipeline(season="2023-24", limit=100)  # Change limit as needed
#     cur.close()
#     conn.close()


import psycopg2
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from datetime import datetime
import json

# Database config
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="nba_app",
    password="pass1234",
    dbname="nba_dashboard"
)
cur = conn.cursor()

# Fetch all active players
active_players = players.get_active_players()

for p in active_players[:50]:  # limit for testing
    player_id = p['id']
    
    try:
        # Fetch game stats for the player
        game_log = playergamelog.PlayerGameLog(player_id=player_id, season='2023-24')
        data = game_log.get_normalized_dict()
        
        # Loop through each game and insert game stats
        for game in data.get('gamelogs', []):
            game_date = datetime.strptime(game['GAME_DATE'], '%b %d, %Y').date()  # Convert string to date
            points = game['PTS']
            assists = game['AST']
            rebounds = game['REB']
            steals = game['STL']
            blocks = game['BLK']
            minutes = game['MIN']
            field_goals_made = game['FGM']
            field_goal_attempts = game['FGA']
            three_pointers_made = game['3PM']
            three_point_attempts = game['3PA']
            free_throws_made = game['FTM']
            free_throw_attempts = game['FTA']
            turnovers = game['TO']
            personal_fouls = game['PF']

            # Insert the stats into the player_stats table
            cur.execute("""
                INSERT INTO player_stats (
                    player_id, season, game_date, points, assists, rebounds, steals, blocks, minutes,
                    field_goals_made, field_goal_attempts, three_pointers_made, three_point_attempts,
                    free_throws_made, free_throw_attempts, turnovers, personal_fouls
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (player_id, game_date) DO NOTHING;
            """, (player_id, '2023-24', game_date, points, assists, rebounds, steals, blocks, minutes,
                  field_goals_made, field_goal_attempts, three_pointers_made, three_point_attempts,
                  free_throws_made, free_throw_attempts, turnovers, personal_fouls))

        print(f"Processed stats for {p['full_name']}")

    except Exception as e:
        print(f"Error fetching stats for player {player_id}: {e}")

# Commit and close connection
conn.commit()
cur.close()
conn.close()
print("Game stats inserted successfully.")
