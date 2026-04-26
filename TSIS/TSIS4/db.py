import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


# =========================
# PLAYER
# =========================
def get_or_create_player(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    result = cur.fetchone()

    if result:
        player_id = result[0]
    else:
        cur.execute(
            "INSERT INTO players(username) VALUES (%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()

    return player_id


# =========================
# SAVE GAME
# =========================
def save_game(player_id, score, level):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO game_sessions(player_id, score, level_reached) VALUES (%s, %s, %s)",
        (player_id, score, level)
    )

    conn.commit()
    cur.close()
    conn.close()


# =========================
# TOP 10
# =========================
def get_top_scores():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        ORDER BY g.score DESC
        LIMIT 10
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


# =========================
# PERSONAL BEST
# =========================
def get_personal_best(player_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(score) FROM game_sessions
        WHERE player_id = %s
    """, (player_id,))

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return result if result else 0