# Seasons Log

A small tool for keeping a seasonal calendar from observation, centered on Towson, Maryland.

The year is split into 24 periods of about 15 days, each split into three sub-periods of about 5 days. Each period shows its typical weather (1991–2020 normals), this year's actual weather, and what was observed. Names start as plain-English placeholders. Our own names go in as observation earns them.

## What's in here

| Path | What it is |
| --- | --- |
| `index.html` | The whole app: one page, no build step |
| `data/calendar.json` | The 24 periods and 72 sub-periods, with dates and normals (°F, inches; the page shows °C and mm too) |
| `data/names.json` | Our own names for periods and sub-periods |
| `data/weather.csv` | Daily actual weather for Towson, filled in automatically |
| `log/entries.json` | Observations, one record each |
| `log/summaries.json` | "What this stretch was like," one per period per season |
| `scripts/fetch_weather.py` | Pulls daily weather from Open-Meteo |
| `.github/workflows/weather.yml` | Runs that script every morning and commits the result |

Everything is plain text, so the record stays readable even without the app.

**Season years.** A season runs from February 4 to February 3. "2026–27" means February 4, 2026 to February 3, 2027.

**Normals.** These are NOAA's 1991–2020 monthly normals for BWI (station USW00093721), about 26 km (16 mi) from Towson. They are spread into periods by interpolation, so treat them as rough.

## Using it

- **New observation:** pick a lens (light, air, sound, smell, living things, human life), optionally mark first / full / last / not yet, and write a sentence.
- **Clicking a period** shows its weather, sub-periods, observations from this season, and the same period in earlier seasons.
- **When a period ends,** write a sentence or two under "What this stretch was like."
- **Naming a period** you think has earned it: type the name in "Our name." It replaces the placeholder on the calendar.

Every save is a git commit, so the history of the log is kept automatically.
