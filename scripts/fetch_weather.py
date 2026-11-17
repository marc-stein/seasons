"""Fetch daily weather for the calendar's center and merge it into data/weather.csv.

Source: Open-Meteo (free, no key). Recent days come from the forecast API's
past_days window; on the first run, older days are backfilled from the archive API.
Values are kept in °F and inches; the page shows °C and mm alongside.
Standard library only, so it runs on a bare GitHub Actions runner.
"""
import csv
import datetime as dt
import json
import pathlib
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAL = json.loads((ROOT / "data" / "calendar.json").read_text())
LAT, LON = CAL["center"]["lat"], CAL["center"]["lon"]
CSV = ROOT / "data" / "weather.csv"
FIELDS = ["date", "high_f", "low_f", "precip_in", "snow_in"]
BACKFILL_FROM = dt.date(2026, 2, 4)  # start of the first season we keep

DAILY = "temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum"
COMMON = {
    "latitude": LAT,
    "longitude": LON,
    "daily": DAILY,
    "temperature_unit": "fahrenheit",
    "precipitation_unit": "inch",
    "timezone": "America/New_York",
}


def get(url, params):
    with urllib.request.urlopen(url + "?" + urllib.parse.urlencode(params), timeout=60) as r:
        return json.load(r)


def rows_from(payload):
    d, units = payload["daily"], payload.get("daily_units", {})
    snow_factor = 1 / 2.54 if units.get("snowfall_sum") == "cm" else 1.0
    out = {}
    for i, day in enumerate(d["time"]):
        vals = [d["temperature_2m_max"][i], d["temperature_2m_min"][i],
                d["precipitation_sum"][i], d["snowfall_sum"][i]]
        if any(v is None for v in vals):
            continue
        hi, lo, pr, sn = vals
        out[day] = {"date": day, "high_f": round(hi, 1), "low_f": round(lo, 1),
                    "precip_in": round(pr, 2), "snow_in": round(sn * snow_factor, 2)}
    return out


def main():
    have = {}
    if CSV.exists():
        with CSV.open() as f:
            have = {r["date"]: r for r in csv.DictReader(f)}

    today = dt.date.today()
    new = {}
    if not have:
        end = today - dt.timedelta(days=6)
        if end > BACKFILL_FROM:
            new.update(rows_from(get("https://archive-api.open-meteo.com/v1/archive",
                                     {**COMMON, "start_date": BACKFILL_FROM.isoformat(),
                                      "end_date": end.isoformat()})))
    # Recent days, including yesterday; today is skipped because it is not complete.
    recent = rows_from(get("https://api.open-meteo.com/v1/forecast",
                           {**COMMON, "past_days": 14, "forecast_days": 1}))
    new.update({k: v for k, v in recent.items() if k < today.isoformat()})

    have.update(new)
    with CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for k in sorted(have):
            w.writerow({x: have[k][x] for x in FIELDS})
    print(f"weather.csv now has {len(have)} days ({len(new)} fetched this run)")


if __name__ == "__main__":
    main()
