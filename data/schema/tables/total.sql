CREATE TABLE IF NOT EXISTS
    total
        (
            game_id text NOT null,
            sportsbook text NOT null,
            over_under VARCHAR(5) NOT null,
            price real,
            point numeric(4, 1),
            updated timestamptz NOT null,
                PRIMARY KEY(game_id, sportsbook, over_under, price, point),
                    FOREIGN KEY(game_id) REFERENCES game(game_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );