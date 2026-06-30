# Overture

> Civic-data tooling for legislators, voting records, public records, camera governance, road-data continuity, and legislation-impact mapping.

Overture began from an upstream civic-legislator data project covering legislators, parties, jurisdictions, chambers, districts, terms, PostgreSQL, and OpenStates-style YAML parsing. This fork keeps that foundation visible while expanding the project into a consumer-facing civic accountability system for Arizona camera governance, ALPR/Flock oversight, public-road data continuity, public-records workflows, and legislation consequence mapping.

## What this project is

Overture is a public-source research and documentation pipeline. It helps citizens understand how a law, contract, camera network, data-sharing agreement, or public portal change can affect ordinary life.

The goal is not to tell people what to think. The goal is to make civic infrastructure legible:

- Who wrote or sponsored a rule?
- What system does the rule authorize?
- What data does the system collect?
- Who gets access?
- What happens when the system is wrong?
- What public records prove the claim?
- What can a resident ask, file, cite, or challenge?

Overture treats civic policy as an impact chain. A bill becomes a procurement decision. A procurement decision becomes a vendor contract. A vendor contract becomes a database. A database becomes searches, alerts, audits, errors, sharing, renewals, denials, fines, stops, hearings, and public consequences.

## Consumer promise

A normal resident should be able to open this repository and understand the issue without already knowing PostgreSQL, OpenStates, ALPR, Flock, AZ511, procurement language, or public-records law.

The documentation is organized around plain questions:

1. What is being tracked?
2. Who controls it?
3. What law, contract, or policy allows it?
4. What records prove that?
5. What could go wrong?
6. What can citizens do next?

## Current research lanes

### Arizona camera accountability

Overture tracks public-facing questions around ALPR, Flock-style systems, traffic cameras, public-safety cameras, campus cameras, HOA/private deployments, and road-data portals. The repository separates verified claims from source pointers and unverified capability claims.

### Legislation impact mapping

The project maps legislation and policy through consequence layers:

- statutory authority
- procurement authority
- vendor control
- data collected
- retention and deletion
- sharing and outside access
- warrants, subpoenas, emergency requests, and informal requests
- error handling and false positives
- renewal, audit, reporting, and sunset clauses
- resident remedies

### Public records workflow

Overture includes templates and checklists for requesting contracts, purchase orders, camera maps, retention settings, audit logs, data-sharing agreements, security reviews, and court-process policies.

### Road-data continuity

The project treats public road information as civic infrastructure. AZ511, ADOT, National Highways, Traffic England, downloadable data, private navigation providers, and professional data feeds all raise a basic question: does the public retain direct visibility, or does practical access shift to private systems?

## What Overture does not do

This is a lawful civic documentation project. It does not bypass, scan, attack, disable, spam, harass, intimidate, dox, or interfere with cameras, vendors, agencies, courts, legislators, residents, or public systems.

The project is designed to strengthen public oversight, not to create operational harm.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py all
```

Generated files appear in `build/`.

Useful commands:

```bash
python main.py verify     # classify supported, needs-records, and held claims
python main.py report     # build Arizona ALPR exposure report
python main.py records    # build public-records request bundle
python main.py linkedin   # build short public campaign post
python main.py sources    # export structured source ledger
python main.py csv        # export source, claim, target, and camera-pointer CSVs
```

Optional PostgreSQL workflow:

```bash
export DATABASE_URL='postgresql://USER:PASSWORD@HOST:5432/DBNAME'
python main.py init-db
python main.py seed-db
```

## Repository map

| Path | Purpose | Audience |
| --- | --- | --- |
| `README.md` | Front door, mission, quick start, repo map | Everyone |
| `main.py` | Source ledger, report generator, claim verifier, public-records bundle, PostgreSQL seeder | Developers, civic-data maintainers |
| `ATTRIBUTION.md` | Minimal upstream credit | Everyone |
| `requirements.txt` | Python dependencies | Developers |
| `schema/overture_camera_accountability.sql` | PostgreSQL schema for source notes, camera assets, requests, actions, and legislation impact | Developers, analysts |
| `data/arizona-camera-accountability-sources.json` | Structured source map | Analysts, journalists, maintainers |
| `docs/consumer-guide.md` | Plain-English guide for residents and nontechnical readers | Consumers, citizens, local groups |
| `docs/legislation-impact-framework.md` | How Overture maps a law or policy into real-world consequences | Policy researchers, advocates, journalists |
| `docs/evidence-standards.md` | How public statements are classified, sourced, held, and corrected | Maintainers, contributors |
| `docs/repository-map.md` | Detailed explanation of every major file and output | Developers, reviewers |
| `docs/arizona-alpr-brief.md` | Arizona ALPR and camera accountability field brief | Residents, journalists, public commenters |
| `docs/az511-road-data-history.md` | AZ511 and public-road data continuity notes | Transportation, public-data, privacy readers |
| `docs/public-records-toolkit.md` | Records-request and public-comment templates | Citizens, journalists, watchdogs |
| `docs/speed-camera-court-pipeline.md` | Photo-enforcement and court-process questions | Residents, legal-policy researchers |
| `docs/linkedin-campaign-post.md` | Short public campaign language | Outreach |
| `build/` | Generated reports and exports after running `main.py` | Local output only |

## Claim discipline

Overture uses four claim states:

| Status | Meaning | Publication rule |
| --- | --- | --- |
| `supported` | The claim is backed by cited public sources | Can be used with citation |
| `needs_public_records` | The direction is plausible but requires contracts, policies, or official records | Phrase as a records target, not a conclusion |
| `needs_location_verification` | A location or device pointer needs official confirmation | Use as a lead, not proof |
| `unsupported_or_overstated` | The claim is not proven by available sources | Do not publish as fact |

This distinction matters. A public map point can be a lead. A contract can be proof. A rumor is neither.

## How to use Overture as a resident

1. Read `docs/consumer-guide.md`.
2. Read the current issue brief in `docs/arizona-alpr-brief.md`.
3. Run `python main.py all` to generate fresh local exports.
4. Open `build/arizona-alpr-exposure-report.md`.
5. Use `docs/public-records-toolkit.md` or `build/public-records-bundle.md` to ask an agency for records.
6. Track each answer against the legislation-impact framework.
7. Keep claims separated into supported, needs-records, needs-location-verification, or unsupported.

## How to use Overture as a developer

The current codebase is intentionally small. The pipeline is built around dataclasses in `main.py`:

- `Source` records the public source.
- `Claim` records the public claim, source IDs, caveat, and action.
- `ActionTarget` records the agency, legislator, campus, or public body to contact.
- `CameraPointer` records map leads that need verification.

Run `python main.py verify` before publishing new language. If a claim is not source-backed, keep it framed as a question or public-records target.

## Visual reference

Camera reference image for README / docs:

https://commons.wikimedia.org/wiki/File:Flock_Safety_camera_with_solar_panel.jpg

## FLLC

https://fllc.net
