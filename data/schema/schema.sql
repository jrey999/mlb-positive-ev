CREATE TABLE IF NOT EXISTS
    game
        (
            game_id text NOT null,
            away text NOT null,
            home text NOT null,
            game_date timestamptz NOT null,
                PRIMARY KEY(game_id)
        );

CREATE TABLE IF NOT EXISTS
    money_line
        (
            game_id text NOT null,
            sportsbook text NOT null,
            team VARCHAR(3) NOT null,
            price integer,
            updated timestamptz NOT null,
                PRIMARY KEY(game_id, sportsbook, team, price),
                    FOREIGN KEY(game_id) REFERENCES game(game_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );

CREATE TABLE IF NOT EXISTS
    spread
        (
            game_id text NOT null,
            sportsbook text NOT null,
            team VARCHAR(3) NOT null,
            price integer,
            point numeric(4, 1),
            updated timestamptz NOT null,
                PRIMARY KEY(game_id, sportsbook, team, price, point),
                    FOREIGN KEY(game_id) REFERENCES game(game_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );

CREATE TABLE IF NOT EXISTS
    total
        (
            game_id text NOT null,
            sportsbook text NOT null,
            over_under VARCHAR(5) NOT null,
            price integer,
            point numeric(4, 1),
            updated timestamptz NOT null,
                PRIMARY KEY(game_id, sportsbook, team, price, point),
                    FOREIGN KEY(game_id) REFERENCES game(game_id)
                    ON DELETE CASCADE ON UPDATE NO ACTION
        );