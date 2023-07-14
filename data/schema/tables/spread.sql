CREATE TABLE IF NOT EXISTS
    spread
        (
            game_id text NOT null,
            sportsbook text NOT null,
            team VARCHAR(3) NOT null,
            price real,
            point numeric(4, 1),
            updated timestamptz NOT null,
                PRIMARY KEY(game_id, sportsbook, team, price, point),
                    FOREIGN KEY(game_id) REFERENCES game(game_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );