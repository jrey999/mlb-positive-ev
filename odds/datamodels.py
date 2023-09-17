from odds.funcs import get_team, fmt_odds, iso_to_dt
from sqlalchemy import create_engine, Column, Integer, REAL, Numeric, String, DateTime, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


engine = create_engine("sqlite:///db.sqlite3")
Base = declarative_base()
class Game(Base):

    __tablename__ = "game"

    game_id = Column(String, primary_key=True)
    away = Column(String)
    home = Column(String)
    game_date = Column(DateTime)

    def __init__(self, game_and_odds: dict) -> None:

        self.game_id = game_and_odds["id"]
        self.away = get_team(game_and_odds["away_team"])
        self.home = get_team(game_and_odds["home_team"])
        self.game_date = iso_to_dt(game_and_odds["commence_time"])

class MoneyLine(Base):

    __tablename__ = "money_line"

    game_id = Column(String)
    sportsbook = Column(String) 
    team = Column(String)
    price = Column(REAL)
    updated = Column(DateTime)

    __table_args__ = (
        PrimaryKeyConstraint('game_id', 'sportsbook', 'team', 'price'),
        ForeignKeyConstraint(['game_id'], ['game.game_id'], ondelete='CASCADE', onupdate='NO ACTION'),
    )

    def __init__(self, data: dict) -> None:

        self.game_id = data["game_id"]
        self.sportsbook = data["sportsbook"]
        self.team = data["team"]
        self.price = data["price"]
        self.updated = data["updated"]

class Spread(Base):

    __tablename__ = "spread"

    game_id = Column(String)
    sportsbook = Column(String) 
    team = Column(String)
    price = Column(REAL)
    point = Column(Numeric)
    updated = Column(DateTime)

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
        self.updated = data["updated"]

class Total(Base):

    __tablename__ = "total"

    game_id = Column(String)
    sportsbook = Column(String)
    over_under = Column(String)
    price = Column(REAL)
    point = Column(Numeric)
    updated = Column(DateTime)

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
        self.updated = data["updated"]

Base.metadata.create_all(engine)