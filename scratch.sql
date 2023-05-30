SELECT * FROM levelupapi_gametype;
SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;
SELECT * FROM levelupapi_game;
SELECT * FROM levelupapi_event;

SELECT
                gmr.id AS gamer_id,
                (u.first_name || ' ' || u.last_name) AS full_name,
                e.id AS event_id,
                e.description,
                e.date,
                e.time,
                g.title
            FROM levelupapi_gamer gmr
            LEFT JOIN auth_user u ON gmr.user_id=u.id
            LEFT JOIN levelupapi_event e ON gmr.id=e.organizer_id
            LEFT JOIN levelupapi_game g ON e.game_id=g.id