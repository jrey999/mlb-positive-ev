# **mlb-positive-ev**
Find profitable MLB bets by comparing sportsbook odds.

**Overview**
This project identifies situations where sportsbook odds deviate enough to provide positive expected value bets for upcoming MLB games. It calculates implied probability averages across books and highlights opportunities against the market.

The output is a Markdown table with matchups, dates, odds, and expected values for betting consideration. Useful for baseball fans, bettors, and anyone interested in sports analytics.

**Usage**

Clone the repo
```bash
git clone https://github.com/jrey999/mlb-positive-ev.git && cd mlb-positive-ev
```

Create and instantiate a virtual environment
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
```bash
pip install --upgrade pip -r requirements.txt
```

Collect data
```bash
./shell/schema.sh
```
```bash
python odds.py
```

Generate Positive EV Report
```bash
./shell/queries.sh
````
Reports are output ![HERE](/data/reports)