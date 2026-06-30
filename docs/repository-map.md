# Repository Map

## Purpose

This file explains how the Overture repository is organized and how each file supports the civic-accountability workflow.

## Top-level files

### `README.md`

The front door for the project. It explains the mission, original attribution, consumer promise, quick start, current research lanes, claim discipline, and major file paths.

### `ATTRIBUTION.md`

Credits Emma Landis for the original civic-legislator project concept and PostgreSQL/OpenStates direction. Keep this file visible as the fork grows.

### `requirements.txt`

Python dependencies used by the local tooling:

- `python-dotenv`
- `psycopg2-binary`
- `PyYAML`

### `main.py`

The main local pipeline. It stores the source ledger, claims, action targets, and camera pointers as Python dataclasses, then exports reports and structured files.

Important objects:

- `Source` — public source metadata.
- `Claim` — public claim, status, source IDs, caveat, and action.
- `ActionTarget` — public body, legislator, campus, or agency to contact.
- `CameraPointer` — public map or location lead requiring verification.

Important commands:

```bash
python main.py all
python main.py verify
python main.py report
python main.py records
python main.py linkedin
python main.py sources
python main.py csv
python main.py init-db
python main.py seed-db
```

## `docs/`

### `docs/consumer-guide.md`

Plain-English guide for residents and nontechnical readers. Explains how to read the project, how to ask civic questions, and how to use generated reports.

### `docs/legislation-impact-framework.md`

The policy-to-impact model. It maps authority, funding, procurement, implementation, data collection, access, retention, sharing, use, correction, reporting, and renewal.

### `docs/evidence-standards.md`

Evidence rules for public statements. Defines supported statements, records-needed statements, location-verification leads, and unsupported statements.

### `docs/arizona-alpr-brief.md`

Arizona camera-accountability field brief. Explains ALPR/Flock concerns, public-records questions, Arizona research lanes, road-data continuity, and minimum ordinance language.

### `docs/az511-road-data-history.md`

Public-road data continuity notes. Used to frame AZ511, ADOT, Traffic England, National Highways, navigation providers, downloadable data, and public access to road information.

### `docs/public-records-toolkit.md`

Public-records and public-comment templates. Use this when asking an agency for contracts, camera lists, retention rules, audit logs, sharing rules, access policies, and renewal dates.

### `docs/speed-camera-court-pipeline.md`

Photo-enforcement and court-process research notes. Focuses on service, notice, default, hearing, license, warrant, and correction questions.

### `docs/linkedin-campaign-post.md`

Short public-facing campaign language for outreach.

## `data/`

### `data/arizona-camera-accountability-sources.json`

Structured source map. This should stay aligned with the source objects in `main.py` where possible.

## `schema/`

### `schema/overture_camera_accountability.sql`

PostgreSQL schema for civic source notes, camera assets, public records, legislation impact, and action tracking.

The database path is optional. The repository still works as a local documentation pipeline without PostgreSQL.

## `build/`

Generated local output. This directory is created when the pipeline runs.

Expected outputs:

- `overture-source-ledger.json`
- `sources.csv`
- `claims.csv`
- `targets.csv`
- `camera_pointers.csv`
- `arizona-alpr-exposure-report.md`
- `public-records-bundle.md`
- `linkedin-post.md`

Generated outputs should be reviewed before public use.

## Suggested contribution workflow

1. Add or update sources in `main.py`.
2. Add or update claims in `main.py`.
3. Keep each claim tied to source IDs.
4. Run `python main.py verify`.
5. Run `python main.py all`.
6. Review generated files in `build/`.
7. Update docs when the public explanation changes.
8. Keep unsupported statements out of public-facing summaries.

## Documentation standard

Every major issue should eventually have:

- short consumer summary
- source table
- supported claims
- unresolved questions
- public-records request
- legislation-impact map
- responsible public body
- renewal or review date
- public comment script
- correction notes
