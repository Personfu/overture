# Overture: Arizona Public Safety Camera Accountability

Overture is an FLLC civic-intelligence project for lawful, public-source oversight of public safety camera systems, automated license plate readers (ALPR), speed/photo-enforcement systems, road information systems, and the legislators or agencies that control the policy environment around them.

The project began as a legislator and voting-record organizer. It now expands into an operational accountability layer for Arizona and the United States: who buys surveillance systems, who votes for them, who audits them, where public cameras are visible, when road data becomes privatized, what traffic/court escalation looks like, and what residents can do before public safety becomes private mass tracking.

## Original project credit

Overture is built from an original forked civic-legislator data project by **Emma Landis**. Credit to Emma Landis for the original repository concept, legislator-organizing scope, and early PostgreSQL/OpenStates direction. FLLC's later work expands that base into Arizona ALPR, public safety camera, road-data, public-records, and camera-governance accountability.

## Position

Arizona should not normalize private ALPR grids without public proof, public policy, and public accountability.

Flock-style ALPR systems are not ordinary traffic cameras. ALPR networks can scan plates, log time and place, compare vehicles against hotlists, retain data, and allow searches across a wider network depending on contract and configuration. The civic risk is not one pole-mounted camera. The risk is persistent movement intelligence operated through vendor platforms, weak procurement review, unclear retention settings, silent data sharing, false-hit consequences, and court-process escalation when automated systems are tied to enforcement.

This repository does not publish instructions for bypassing, damaging, disabling, harassing, or interfering with cameras, courts, agencies, vendors, legislators, or public systems. It is for exposure through documentation: public records, source mapping, policy review, contract analysis, public comment, legal/civic pressure, and sourced reporting.

## Core Arizona message

> Arizona should not normalize private ALPR grids. We are the Wild West, not a private location-tracking test range.
>
> If a city, campus, HOA, or agency wants Flock or any ALPR network, residents should demand the contract, camera map, retention policy, audit logs, sharing partners, warrant rules, misuse penalties, false-hit reporting, court-process safeguards, and annual public vote.
>
> Public safety should not become private mass tracking.

## Why this matters now

The UK Traffic England closure notice supplied to FLLC says public road information is shifting away from the Traffic England website and toward navigation providers, National Highways sources, and professional data channels. That is a warning for the United States: once public-road intelligence moves into private systems, public oversight can become weaker.

Arizona already has public traveler-information infrastructure through AZ511, ADOT camera views, traffic alerts, signs, road restrictions, and incident data. That public-information model should not be replaced by opaque private tracking platforms.

## Project scope

Overture tracks six connected systems:

1. **Legislators and policy power**
   - Arizona House and Senate members
   - committee assignments
   - public safety, transportation, procurement, privacy, and technology policy
   - public contact and campaign links

2. **ALPR and Flock oversight**
   - public camera sightings
   - city/campus/HOA procurement records
   - contracts and renewal dates
   - retention settings
   - sharing agreements
   - audit logs and public-records request results

3. **Public safety camera operations**
   - traffic cameras
   - ALPR cameras
   - city-owned public safety cameras
   - campus public safety cameras
   - private cameras used for public safety purposes
   - source confidence and governance notes

4. **Speed/photo-enforcement court process**
   - citation workflow
   - vendor review
   - service rules
   - hearing/default process
   - failure-to-appear process
   - license consequences
   - court-order/warrant consequences
   - error-correction and database hygiene

5. **Road information and public data continuity**
   - AZ511 and ADOT public road information
   - National Highways / Traffic England closure context
   - Google Maps, Waze, TomTom, and similar public-facing navigation layers
   - risks when public data moves to private interfaces

6. **Constituent action**
   - public comment
   - public-records requests
   - city council questions
   - campus governance questions
   - HOA questions
   - contract-redline demands
   - lawful outreach to legislators

## Arizona starter targets

The project starts with Arizona, Tempe, ASU, and public state-level legislative context.

Examples and source links:

- DeFlock source map: https://deflock.org/
- ASU / Tempe OpenStreetMap example: https://www.openstreetmap.org/node/13613353701#map=19/33.420348/-111.931079
- Arizona Legislature member roster: https://www.azleg.gov/memberroster/
- Rep. Stacey Travers: https://www.azleg.gov/house-member/?legislature=57&session=130&legislator=2340
- Stacey Travers campaign site: https://www.traversforaz.com/
- Sen. Lauren Kuby: https://www.azleg.gov/senate-member/?legislature=57&legislator=2390
- Lauren Kuby campaign site: https://www.kubyforsenate.com/
- AZ511: https://www.az511.gov/
- ADOT: https://azdot.gov/

OpenStreetMap contributors who have helped surface public camera visibility deserve credit. Examples referenced by the campaign include:

- RickDalton: https://www.openstreetmap.org/user/RickDalton
- g_uy: https://www.openstreetmap.org/user/g_uy
- pidogs: https://www.openstreetmap.org/user/pidogs

## What to demand before any ALPR system stays up

Every city, campus, HOA, and agency should publish:

- the full contract
- camera locations
- vendor and reseller names
- funding source
- installation date
- renewal date
- retention period
- hotlist sources
- access roles
- search policy
- audit logs
- outside-agency sharing partners
- warrant policy
- misuse penalties
- false-hit review process
- breach notification policy
- public complaint path
- annual performance report
- annual public vote or renewal hearing

## What to demand before any speed/photo-enforcement system stays up

Every city, court, and vendor should publish:

- photo-enforcement contract
- device calibration policy
- violation review workflow
- judge/pro-tem or hearing officer review process
- service-of-process policy
- default policy
- failure-to-appear policy
- license consequence policy
- court-order or warrant policy
- collections policy
- dismissal/error statistics
- vendor fee schedule
- error-correction process
- annual public performance report

## Main pipeline

Install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Generate the exposure packet:

```bash
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

## Lawful action plan

Do this:

1. Find the agency or property owner.
2. Capture public source links only.
3. Submit a public-records request for the contract, policy, audit logs, and sharing agreements.
4. Attend the public meeting before renewal.
5. Ask for a written response from city council, campus leadership, HOA boards, and state legislators.
6. Publish a source-backed summary.
7. Ask for a moratorium, sunset clause, warrant rule, retention limit, false-hit reporting, court-process safeguards, and public registry.

Do not do this:

- do not damage cameras
- do not bypass camera systems
- do not harass public employees
- do not spam or mail-bomb anyone
- do not publish private personal data
- do not make unsupported claims as fact
- do not impersonate agencies or vendors

## Repository map

- `main.py` — exposure-report pipeline, source ledger, claim verifier, public-records bundle generator, optional PostgreSQL seeder.
- `docs/arizona-alpr-brief.md` — field brief for Arizona ALPR and public safety camera oversight.
- `docs/az511-road-data-history.md` — AZ511, Traffic England, and public-road data continuity notes.
- `docs/public-records-toolkit.md` — lawful public-records and public-comment templates.
- `docs/speed-camera-court-pipeline.md` — photo enforcement, speed camera, default, failure-to-appear, and court-process accountability questions.
- `docs/linkedin-campaign-post.md` — short public campaign post and CTA.
- `data/arizona-camera-accountability-sources.json` — structured source map for Arizona camera and policy research.
- `schema/overture_camera_accountability.sql` — PostgreSQL schema for camera, contract, legislator, source, and public-records tracking.
- `requirements.txt` — Python dependencies.

## FLLC connection

FLLC tracks cybersecurity, public-source intelligence, camera governance, consumer safety, public accountability, and the data systems that affect ordinary residents.

Subscribe and follow the wider work at https://fllc.net.
