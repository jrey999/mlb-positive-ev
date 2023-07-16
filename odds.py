from odds.datamodels import Game, DB
from odds.funcs import get_markets


data, cursor = get_markets(), DB.cursor()
for game in data:

    game = Game(game)
    odds = game.odds
    cursor.execute(
        """
        INSERT INTO
            game
        (
            game_id, away, home, game_date
        )
            VALUES
        (
            ?, ?, ?, ?
        )
            ON CONFLICT(game_id)
            DO UPDATE SET
        game_date = EXCLUDED.game_date;
        """,
        game.game
    )
    money_line = [tuple(value for key, value in _.items() if key != "market") for _ in odds if _["market"] == "money_line"]
    cursor.executemany(
        """
        INSERT INTO
            money_line
        (
            game_id, sportsbook, team, price, updated
        )
            VALUES
        (
            ?, ?, ?, ?, ?
        )
            ON CONFLICT(game_id, sportsbook, team, price)
            DO NOTHING;
        """,
        money_line
    )
    spreads = [tuple(value for key, value in _.items() if key != "market") for _ in odds if _["market"] == "spread"]
    cursor.executemany(
        """
        INSERT INTO
            spread
        (
            game_id, sportsbook, team,
            price, point, updated
        )
            VALUES
        (
            ?, ?, ?, ?, ?, ?
        )
            ON CONFLICT(game_id, sportsbook, team, price, point)
            DO NOTHING;
        """,
        spreads
    )
    totals = [tuple(value for key, value in _.items() if key != "market") for _ in odds if _["market"] == "total"]
    cursor.executemany(
        """
        INSERT INTO
            total
        (
            game_id, sportsbook, over_under,
            price, point, updated
        )
            VALUES
        (
            ?, ?, ?, ?, ?, ?
        )
            ON CONFLICT(game_id, sportsbook, over_under, price, point)
            DO NOTHING;
        """,
        totals
    )
DB.commit()