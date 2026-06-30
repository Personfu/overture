# Overture

> PostgreSQL civic-data tooling for legislators, voting records, public records, and Arizona camera-governance research.

**Original project by Emma Landis.**

This fork keeps Emma Landis' original civic-legislator data direction as the base: legislators, parties, jurisdictions, chambers, districts, terms, PostgreSQL, and OpenStates-style YAML parsing.

FLLC / PersonFu expanded the fork with Arizona public camera accountability notes, road-data continuity, public-records templates, and traffic-enforcement court-process questions.

## Original data model

- legislators
- parties
- jurisdictions
- chambers
- districts
- terms

## Arizona research lanes

- legislator and policy tracking
- public camera source review
- ASU / Tempe camera-source notes
- AZ511 and ADOT road-information continuity
- Traffic England closure context
- ALPR contract and retention review
- speed/photo-enforcement process review
- public-records request templates

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py all
```

Useful commands:

```bash
python main.py verify
python main.py report
python main.py records
python main.py linkedin
python main.py sources
python main.py csv
```

Optional PostgreSQL workflow:

```bash
export DATABASE_URL='postgresql://USER:PASSWORD@HOST:5432/DBNAME'
python main.py init-db
python main.py seed-db
```

Generated files appear in `build/`.

## Repository map

- `main.py` — source ledger, report generator, claim verifier, public-records bundle, PostgreSQL seeder.
- `docs/arizona-alpr-brief.md` — Arizona camera field brief.
- `docs/az511-road-data-history.md` — AZ511 and road-data continuity notes.
- `docs/public-records-toolkit.md` — public-records and public-comment templates.
- `docs/speed-camera-court-pipeline.md` — photo enforcement and court-process questions.
- `docs/linkedin-campaign-post.md` — short public campaign language.
- `data/arizona-camera-accountability-sources.json` — structured source map.
- `schema/overture_camera_accountability.sql` — PostgreSQL schema.
- `ATTRIBUTION.md` — original project credit.

## Visual reference

Camera reference image for the README / docs:

https://commons.wikimedia.org/wiki/File:Flock_Safety_camera_with_solar_panel.jpg

## FLLC

https://fllc.net
