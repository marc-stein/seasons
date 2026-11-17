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

## Setup (one time)

1. **Make a repository** on GitHub, for example `seasons-log`, and push these files to it:
   ```
   cd seasons-log
   git init -b main
   git add .
   git commit -m "Start the seasons log"
   git remote add origin https://github.com/YOUR-NAME/seasons-log.git
   git push -u origin main
   ```
   The browser's drag-and-drop upload can skip the hidden `.github` folder, which is why command-line git is the safer route.
2. **Turn on the page.** In the repository, go to Settings → Pages → Build and deployment, set Source to "Deploy from a branch," and pick `main` and `/ (root)`. The page appears at `https://YOUR-NAME.github.io/seasons-log/` within a minute or two.
   - On a free GitHub account, Pages only works for **public** repositories, which would make the log public. To keep it private, either use a paid plan or skip Pages and run it locally (step 5).
3. **Start the weather job.** Go to Actions → Daily weather → Run workflow. The first run backfills from February 4, 2026. After that it runs every morning on its own.
   - If the run can't push, set Settings → Actions → General → Workflow permissions to "Read and write."
4. **Let the page save.** Create a fine-grained personal access token: GitHub → Settings → Developer settings → Fine-grained tokens. Limit it to this one repository, with **Contents: Read and write** and nothing else. Then open the page, click Settings, and paste it in. The token is stored only in that browser.
5. **Running it locally instead of on Pages.** From the repository folder, run `python3 -m http.server 8000` and open `http://localhost:8000`. With the token set, saves still go straight to GitHub. Run `git pull` now and then to keep the local copy current.

## Using it

- **New observation:** pick a lens (light, air, sound, smell, living things, human life), optionally mark first / full / last / not yet, and write a sentence.
- **Clicking a period** shows its weather, sub-periods, observations from this season, and the same period in earlier seasons.
- **When a period ends,** write a sentence or two under "What this stretch was like."
- **Naming a period** you think has earned it: type the name in "Our name." It replaces the placeholder on the calendar.

Every save is a git commit, so the history of the log is kept automatically.
