from odds.datamodels import Game, MoneyLine, Spread, Total, engine
from sqlalchemy.orm import sessionmaker
from odds.funcs import get_markets, get_odds_info, fmt_odds


Session = sessionmaker(bind=engine)
session = Session()
markets, data = get_markets(), []
for market in markets:

    data.append(Game(market))
    for bookmaker in market["bookmakers"]:
        sportsbook = bookmaker["key"]
        for line in bookmaker["markets"]:
            odds = fmt_odds({"game_id": market["id"], "sportsbook": sportsbook}, line)
            for _ in odds:
                data.append(MoneyLine(_) if _["market"] == "money_line" else Spread(_) if _["market"] == "spread" else Total(_))

with Session() as session:
    for _ in data:
        session.merge(_)
    session.commit()
session.close()