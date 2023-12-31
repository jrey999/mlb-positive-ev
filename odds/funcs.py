import requests, json, pytz, datetime, dotenv, os


dotenv.load_dotenv()
config = {key: value for key, value in os.environ.items()}
HOST, APIKEY = "https://api.the-odds-api.com", config.get("API_KEY")
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

def get_odds_info(game_id: str, book_maker_odds: dict) -> dict:

    return {
        "game_id": game_id,
        "sportsbook": book_maker_odds["key"],
        #"update": book_maker_odds["last_update"]
    }

def fmt_odds(odds_info: dict, line: list[dict]) -> list[dict]:

    return [
        {
            "game_id": odds_info["game_id"],           # game_id
            "sportsbook": odds_info["sportsbook"],     # sportsbook
            "market": "money_line",       # market
            "team": get_team(line["outcomes"][0]["name"]),     # team
            "price": line["outcomes"][0]["price"],    # price
            "updated": iso_to_dt(line["last_update"]),    # updated
        },
        {
            "game_id": odds_info["game_id"],           # game_id
            "sportsbook": odds_info["sportsbook"],     # sportsbook
            "market": "money_line",       # market
            "team": get_team(line["outcomes"][1]["name"]),     # team
            "price": line["outcomes"][1]["price"],    # price
            "updated": iso_to_dt(line["last_update"]),    # updated
        }

    ] if line["key"] == "h2h" else [

        {
            "game_id": odds_info["game_id"],           # game_id
            "sportsbook": odds_info["sportsbook"],     # sportsbook
            "market": "spread",                         # spread
            "team": get_team(line["outcomes"][0]["name"]),                  # team
            "price": line["outcomes"][0]["price"],     # price
            "point": line["outcomes"][0]["point"],                          # point
            "updated": iso_to_dt(line["last_update"]),              # updated
        },
        {
           "game_id": odds_info["game_id"],           # game_id
            "sportsbook": odds_info["sportsbook"],     # sportsbook
            "market": "spread",                         # spread
            "team": get_team(line["outcomes"][1]["name"]),                  # team
            "price": line["outcomes"][1]["price"],     # price
            "point": line["outcomes"][1]["point"],                          # point
            "updated": iso_to_dt(line["last_update"]),              # updated
        }
    ] if line["key"] == "spreads" else [
        {
            "game_id": odds_info["game_id"],           # game_id
            "sportsbook": odds_info["sportsbook"],     # sportsbook
            "market": "total",                         # market
            "name": line["outcomes"][0]["name"],        # name
            "price": line["outcomes"][0]["price"],     # price
            "point": line["outcomes"][0]["point"],      # point
            "updated": iso_to_dt(line["last_update"]),              # updated
        },
        {
            "game_id": odds_info["game_id"],           # game_id
            "sportsbook": odds_info["sportsbook"],     # sportsbook
            "market": "total",                         # market
            "name": line["outcomes"][1]["name"],        # name
            "price": line["outcomes"][1]["price"],     # price
            "point": line["outcomes"][1]["point"],      # point
            "updated": iso_to_dt(line["last_update"]),              # updated
        }
    ] if line["key"] == "totals" else []
