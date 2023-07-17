from dotenv import dotenv_values
import requests, json, pytz, datetime


config = {key: value for key, value in dotenv_values(".env").items()}
HOST, APIKEY = "https://api.the-odds-api.com", config.get("api_key")
SPORTS = f"/v4/sports/?apiKey={APIKEY}"
MARKETS="/v4/sports/baseball_mlb/odds/?apiKey={}&regions=us&markets=h2h,spreads,totals"

def get_markets() -> list[dict]:
    
    data = requests.get(HOST + MARKETS.format(APIKEY)).json()
    json.dump(data, open("meta/sampledata/data.json", "w"), indent=0)
    return data

def get_team(long_name: str) -> str:

    return json.load(open("meta/teammap.json", "r")).get(long_name)

def utc_aware(dt_object: datetime.datetime) -> datetime.datetime:
    "takes in a datetime object and returns the datetime object UTC aware"
    return pytz.timezone("UTC").localize(dt_object)

def iso_to_dt(iso_fmt_time: str) -> datetime.datetime:
    """takes in an iso formatted str rep of a timestamp and returns a timestamp"""
    date, time = iso_fmt_time.split("Z")[0].split(".")[0].split("T")
    year, month, day = date.split("-")
    hour, minute, sec = time.split(":")
    return utc_aware(datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(sec)))

def utc_now() -> datetime.datetime:

    return utc_aware(datetime.datetime.now())

def fmt_odds(line: dict, game_id: str, sportsbook) -> tuple:

    return [
        {
            "game_id": game_id,           # game_id
            "sportsbook": sportsbook,     # sportsbook
            "market": "money_line",       # market
            "team": get_team(line["outcomes"][0]["name"]),     # team
            "price": line["outcomes"][0]["price"],    # price
            "updated": line["last_update"],    # updated
        },
        {
            "game_id": game_id,           # game_id
            "sportsbook": sportsbook,     # sportsbook
            "market": "money_line",       # market
            "team": get_team(line["outcomes"][1]["name"]),     # team
            "price": line["outcomes"][1]["price"],    # price
            "updated": line["last_update"],    # updated
        }

    ] if line["key"] == "h2h" else [

        {
            "game_id": game_id,                         # game_id
            "sportsbook": sportsbook,                   # sportsbook
            "market": "spread",                         # spread
            "team": get_team(line["outcomes"][0]["name"]),                  # team
            "price": line["outcomes"][0]["price"],     # price
            "point": line["outcomes"][0]["point"],                          # point
            "updated": line["last_update"],              # updated
        },
        {
            "game_id": game_id,                         # game_id
            "sportsbook": sportsbook,                   # sportsbook
            "market": "spread",                         # spread
            "team": get_team(line["outcomes"][1]["name"]),                  # team
            "price": line["outcomes"][1]["price"],     # price
            "point": line["outcomes"][1]["point"],                          # point
            "updated": line["last_update"],              # updated
        }
    ] if line["key"] == "spreads" else [
        {
            "game_id": game_id,                         # game_id
            "sportsbook": sportsbook,                   # sportsbook
            "market": "total",                         # market
            "name": line["outcomes"][0]["name"],        # name
            "price": line["outcomes"][0]["price"],     # price
            "point": line["outcomes"][0]["point"],      # point
            "updated": line["last_update"],              # updated
        },
        {
            "game_id": game_id,                         # game_id
            "sportsbook": sportsbook,                   # sportsbook
            "market": "total",                         # market
            "name": line["outcomes"][1]["name"],        # name
            "price": line["outcomes"][1]["price"],     # price
            "point": line["outcomes"][1]["point"],      # point
            "updated": line["last_update"],              # updated
        }
    ] if line["key"] == "totals" else []