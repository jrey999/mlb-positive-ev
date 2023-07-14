CREATE TABLE IF NOT EXISTS
    game
        (
            game_id text NOT null,
            away text NOT null,
            home text NOT null,
            game_date timestamptz NOT null,
                PRIMARY KEY(game_id)
        );