from data.funcs import get_team, fmt_odds, iso_to_dt
import sqlite3


DB = sqlite3.connect("db.sqlite3")
class Game:

    def __init__(self, game_and_odds: dict) -> None:
        
        self.data = game_and_odds["bookmakers"]
        self.game = (
            game_and_odds["id"], #id
            get_team(game_and_odds["away_team"]), #away
            get_team(game_and_odds["home_team"]), #home
            iso_to_dt(game_and_odds["commence_time"]), #game_date
        )

    @property
    def odds(self) -> list[tuple]:
        
        return sum([fmt_odds(line, self.game[0], book["key"]) for book in self.data for line in book["markets"]], [])
