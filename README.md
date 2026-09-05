# Voyager - Mission to the stars

A personal portfolio project exploring a simple question: **what would it actually take to reach another world, using real data and real physics?**

Pick a real exoplanet, plan a journey to it, and see how relativily - time dilation from speed, and ooptionally from passing near a real black hole - would affect or reshape the trip.

Built to bring together everything studied so far in a BSc Hons Computing Systems course: Python, databases, mathematics, and client-side web development, applied to one coherent, real-world-flavoured problem rather than four separate exercises.

---

## The idea

This is a space mission planner - real exoplanet data, real astrophysics formulas (special and general relativity), and an interactive simulation, tied together into a single site.

---

### Architecture

The project is split into two clean stages:

```
NASA's public data → MySQL → exported to JSON → client-side website
```

**Why this shape, specifically:**
- The site itself is pure HTML/CSS/JS - no live backend server, no framework needed. It just reads static JSON files.
- All the real "data engineering" work (fetching, cleaning, storing) happens offline, ahead of time, using Python and MySQL.
- This keeps the frontend within reach of skills already learned, while the backend/database work is genuine, not a toy exercise.
- Its also a deliberate stepping stone: if a live backend is learned later within the course (e.g. Flask), upgrading this project means replacing `fetch(`data.json`)` with `fetch(`https://api/...`)` - same shape of data, same frontend code, just a different source. Nothing here will need to be thrown away to do that.

---

## Data pipeline

### Exoplanets
- **Source:** NASA's Exoplanet Archive, queried via its public TAP API (no API key required)
- **Table used:** `pscomppars` (composite parameters - one row per confirmed planet), not `ps` (which has one row per *published study*, and returned 39,000 + duplicate-heavy rows before this was caught and fixed)
- **Fields pulled:** name, distance (parsecs, converted to light-years), planet radius, host star temperature
- **Storage:** MySQL, `exoplanets` table, upserted (`UNIQUE constraint on name + `ON DUPLICATE KEY UPDATE` via modern `AS new_row` syntax) so re-runnung the fetch never creatd duplicates, even updates the data if the data in NASA's side is updated
- **Missind data:** some planets lack radius/star temperature measurements - these are kept as `NULL` rather than excluded, since the data is still useful for browsing even if a specific feature (like habitability scoring) can't use it. Filtering happens later, only where it's actually needed.
- **Result:** 6228 real confirmed exoplanets

### Black holes
-No equivalent large public API exists for black holes the way it does for exoplanets
- well-measured ones are a small, hand-curated list, not a queryable database.
- **13 real blackholes** compiled from public astronomical sources (Wikipedia's blackhole catalogs, NASA, and recent published research on Gaia's discoveries), spanning distances from ~1560 to 26000 light-years.
- Same storage/export pattern as exoplanets, for consistency - stored in MySQL, then exported to JSON - even though the data was manually researched rather than fetched from a live source.
- A couple of contested cases (e.g. 2MASS J052515658+4359220) were left out, since follow-up observations cast doubt on their status as a genuine black holes.

### Scripts
| sCRIPT | PURPOSE |
|---|---|
| `fetch_and_store.py` | pulls exoplanet data from NASA, upserts into MySQL |
| `store_black_holes,py` | Stores the curated black hole list into MyAQL |
| `export_to_json.py` | exports the `exoplanets` table to `exoplanets.json` |
| `export_black_holes.py` | Exports the `exoplanets` table to `exoplanets.json` |

Credentials are kept out of code entirely, loaded from a `.env` file (excluded from Git via `.gitignore`).

---

## The Physics

- **Journey time:** distance / speed
- **Special relativity (speed-based time dilation):**  t_ship = t_earth × √(1 − v²/c²)
- **General reletivity ( gravitational time dilation near black hole):** t_far = t_near / √(1 − 2GM/rc²)
- **Schwarzchild radius** (event horizon size): r_s = 2GM/c²
- **Escape velocity:** v = √(2GM/r)
- **Wormholes** are included only as a clearly-labelled *speculative* toggle - real predicted math falling out of general reletivity, but not something confirmed to exist or be traversable.

All formulas use real constants and produce real, checkable numbers - not placeholder/ fake maths.

---

## Website

Three pages, kept deliberately minimal :
- `index.html` - the concept pitch (Skeleton)
- `about.html` - how it's built, and the physics involved
- `mission.html` - everything else: choose a destination, plan a journey, optionally route past a black hole, launch, and see the mission report - all on one page

### Built so far
- Destination picker reading the real 'exoplanets.json` (6,228 planets)
- Live search-as-you-type filtering by name
- *(In progress)* Click-to-select a destination


### Planned 
- Journey speed calculator (real km/s input, converted to fraction of light speed)
- Special relativity time dilation calculator
- Black hole route selection - only black holes real-world *closer than* the selected destination are offered, and mustiple can be chosen but only in increaing distance order (reflecting passing them in physical sequence en route)
- Full mission simulation with an animated cockpit view (starfield warp effect, black hole visuals growing in the windshield)
- Mission summary/report, generated only after the simulation actually runs

---

## Design decisions worth nothing

- **No live backend (yet).** Exoplanet/black hole data doesnot change minute-to-minute, so a static JSON export is a legitimate, modern approach (the same idea behind the "JAMstack"), not a lesser substitute for a real backend.
- **The black hole route only ever afects crew time, never Earth time.** Earth-frame travel time is purely distance / speed; gravitational time dilation slowa the *crew's* clock for that same fixed trip duration - it doesn't add extra distance or extra Earth-measured time.
-Visuals stay 2D for now.** A 3D version (Three.js) is a possible future stretch goal, not a requirement for the project to be complete.
- **All combined-relativity effects (speed + gravity together) are a simplified, illustrative model**, not a fully rigorous merged calculation - worth being upfront, since combining special and general relativity accurately is genuinely complex physics beyond this project's scope.

---

## Tech stack

-**Python** - `requests`, `mysql-connector-python`, `python-dotenv`
- **MySQL** - local database, two tables (`exoplanets`, `black_holes`)
-**HTML / CSS / JavaScript** - no frameworks, no build tools
- **Data sources** - NASA Exoplanet Archive (TAP API), public astronomical sources for blackhole data

---

## Author

Krishal Acharya - BSc Hons Computing Systems, Ulster University London