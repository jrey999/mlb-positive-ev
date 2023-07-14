CREATE TABLE IF NOT EXISTS
    money_line
        (
            game_id text NOT null,
            sportsbook text NOT null,
            team VARCHAR(3) NOT null,
            price real,
            updated timestamptz NOT null,
                PRIMARY KEY(game_id, sportsbook, team, price),
                    FOREIGN KEY(game_id) REFERENCES game(game_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );