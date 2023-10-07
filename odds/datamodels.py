from odds.funcs import get_team, fmt_odds, iso_to_dt, get_markets, DATE
from sqlalchemy import create_engine, Column, Integer, REAL, Numeric, String, DateTime, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from json import dump, load


engine = create_engine("sqlite:///db.sqlite3")
Base = declarative_base()
class Game(Base):

    __tablename__ = "game"

    game_id = Column("game_id", String, primary_key=True)
    away = Column("away", String)
    home = Column("home", String)
    game_date = Column("game_date", DateTime)

    def __init__(self, game_and_odds: dict) -> None:

        self.game_id = game_and_odds["id"]
        self.away = get_team(game_and_odds["away_team"])
        self.home = get_team(game_and_odds["home_team"])
        self.game_date = iso_to_dt(game_and_odds["commence_time"])

class MoneyLine(Base):

    __tablename__ = "money_line"

    game_id = Column("game_id", String)
    sportsbook = Column("sportsbook", String) 
    team = Column("team", String)
    price = Column("price", REAL)
    updated = Column("updated", DateTime)

    __table_args__ = (
        PrimaryKeyConstraint('game_id', 'sportsbook', 'team', 'price'),
        ForeignKeyConstraint(['game_id'], ['game.game_id'], ondelete='CASCADE', onupdate='NO ACTION'),
    )

    def __init__(self, data: dict) -> None:

        self.game_id = data["game_id"]
        self.sportsbook = data["sportsbook"]
        self.team = data["team"]
        self.price = data["price"]
        self.updated = iso_to_dt(data["updated"])

class Spread(Base):

    __tablename__ = "spread"

    game_id = Column("game_id", String)
    sportsbook = Column("sportsbook", String) 
    team = Column("team", String)
    price = Column("price", REAL)
    point = Column("point", Numeric)
    updated = Column("updated", DateTime)

    __table_args__ = (
        PrimaryKeyConstraint('game_id', 'sportsbook', 'team', 'price', 'point'),
        ForeignKeyConstraint(['game_id'], ['game.game_id'], ondelete='CASCADE', onupdate='NO ACTION'),
    )

    def __init__(self, data: dict) -> None:

        self.game_id = data["game_id"]
        self.sportsbook = data["sportsbook"]
        self.team = data["team"]
        self.price = data["price"]
        self.point = data["point"]
        self.updated = iso_to_dt(data["updated"])

class Total(Base):

    __tablename__ = "total"

    game_id = Column("game_id", String)
    sportsbook = Column("sportsbook", String)
    over_under = Column("over_under", String)
    price = Column("price", REAL)
    point = Column("point", Numeric)
    updated = Column("updated", DateTime)

    __table_args__ = (
        PrimaryKeyConstraint("game_id", "sportsbook", "over_under", "price", "point"),
        ForeignKeyConstraint(['game_id'], ['game.game_id'], ondelete='CASCADE', onupdate='NO ACTION')
    )

    def __init__(self, data: dict) -> None:

        self.game_id = data["game_id"]
        self.sportsbook = data["sportsbook"]
        self.over_under = data["name"]
        self.price = data["price"]
        self.point = data["point"]
        self.updated = iso_to_dt(data["updated"])

Base.metadata.create_all(engine)

def dump_objects() -> list:

    markets, odds, games = get_markets(), [], []
    for market in markets:

        games.append(market)
        for bookmaker in market["bookmakers"]:
            sportsbook = bookmaker["key"]
            for line in bookmaker["markets"]:
                odds.append(fmt_odds({"game_id": market["id"], "sportsbook": sportsbook}, line))
                
    dump(games, open(f"mlb-positive-ev/data/raw/games-{DATE}.json", "w"), indent=0)
    dump(odds, open(f"mlb-positive-ev/data/raw/odds-{DATE}.json", "w"), indent=0)
    

def write_objects() -> None:
    Session = sessionmaker(bind=engine)
    session = Session()
    games, odds = load(open(f"mlb-positive-ev/data/raw/games-{DATE}.json", "r")), load(open(f"mlb-positive-ev/data/raw/odds-{DATE}.json", "r"))
    data = [Game(_) for _ in games]
    data += [MoneyLine(_) if _["market"] == "money_line" else Spread(_) if _["market"] == "spread" else Total(_) for _ in odds]
    with Session() as session:
        for _ in data:
            session.merge(_)
        session.commit()
    session.close()