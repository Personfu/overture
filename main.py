#!/usr/bin/env python3
"""
Overture: public-source civic accountability pipeline.

This script builds source-backed reports about legislators, ALPR/Flock deployments,
traffic-enforcement camera policy, road-data privatization, public-records requests,
and camera-governance questions.

Safety boundary: this is a documentation and civic-records tool. It does not bypass,
scan, attack, disable, spam, harass, or interfere with cameras, courts, vendors,
agencies, legislators, or public systems.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import textwrap
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Iterable, Sequence

try:
    import psycopg2  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    psycopg2 = None

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
DATA = ROOT / "data"
BUILD = ROOT / "build"
SCHEMA = ROOT / "schema" / "overture_camera_accountability.sql"
SOURCE_JSON = DATA / "arizona-camera-accountability-sources.json"

SUPPORTED_CLAIM = "supported"
NEEDS_RECORDS = "needs_public_records"
NEEDS_VERIFICATION = "needs_location_verification"
UNSUPPORTED = "unsupported_or_overstated"


@dataclass(frozen=True)
class Source:
    id: str
    title: str
    url: str
    publisher: str
    source_type: str
    relevance: str
    reliability: str = "public_source"
    notes: str = ""


@dataclass(frozen=True)
class Claim:
    id: str
    claim: str
    status: str
    source_ids: list[str]
    caveat: str = ""
    action: str = ""


@dataclass(frozen=True)
class ActionTarget:
    name: str
    level: str
    url: str
    ask: str
    category: str = "policy"


@dataclass(frozen=True)
class CameraPointer:
    label: str
    url: str
    latitude: float | None = None
    longitude: float | None = None
    jurisdiction: str = "unknown"
    camera_type: str = "unknown"
    confidence: str = "source_pointer"
    verification_questions: list[str] = field(default_factory=list)


SOURCES: list[Source] = [
    Source(
        id="deflock",
        title="DeFlock public camera source map",
        url="https://deflock.org/",
        publisher="DeFlock",
        source_type="public_map",
        relevance="Crowd/source map for public camera and ALPR visibility. Use as source pointer, then verify with official records.",
    ),
    Source(
        id="osm_asu_tempe",
        title="OpenStreetMap ASU / Tempe camera node",
        url="https://www.openstreetmap.org/node/13613353701#map=19/33.420348/-111.931079",
        publisher="OpenStreetMap",
        source_type="public_map_node",
        relevance="Public map pointer near ASU / Tempe that should be verified with ownership and contract records.",
        notes="Do not treat an OSM point as final proof of vendor, capability, ownership, or retention policy.",
    ),
    Source(
        id="traffic_england_notice",
        title="Traffic England closure notice supplied to FLLC",
        url="https://www.trafficengland.com/",
        publisher="Traffic England / National Highways context",
        source_type="closure_notice",
        relevance="User-supplied notice says Traffic England closes 2026-06-30 and redirects public road information to navigation apps, National Highways, downloadable data, live incidents, and NTIS professional access.",
        reliability="needs_archive_capture",
        notes="Archive the notice if visible in browser. Search engines did not reliably surface the exact notice text.",
    ),
    Source(
        id="national_highways",
        title="National Highways travel updates",
        url="https://nationalhighways.co.uk/travel-updates/",
        publisher="National Highways",
        source_type="official_road_info",
        relevance="Official England road information fallback after Traffic England changes.",
    ),
    Source(
        id="az511",
        title="AZ511 traveler information",
        url="https://www.az511.gov/",
        publisher="Arizona Department of Transportation / AZ511",
        source_type="official_road_info",
        relevance="Arizona public-road data, traveler information, incidents, restrictions, and camera visibility where available.",
    ),
    Source(
        id="adot",
        title="Arizona Department of Transportation",
        url="https://azdot.gov/",
        publisher="ADOT",
        source_type="official_agency",
        relevance="State transportation agency context for AZ road information and public highway operations.",
    ),
    Source(
        id="eff_alpr",
        title="EFF: Automated License Plate Readers",
        url="https://www.eff.org/pages/automated-license-plate-readers-alpr",
        publisher="Electronic Frontier Foundation",
        source_type="civil_liberties_research",
        relevance="ALPR privacy, retention, and data-sharing concerns.",
    ),
    Source(
        id="aclu_alpr",
        title="ACLU: Automatic License Plate Readers",
        url="https://www.aclu.org/issues/privacy-technology/location-tracking/automatic-license-plate-readers",
        publisher="ACLU",
        source_type="civil_liberties_research",
        relevance="Civil-liberties overview and oversight framing for ALPR systems.",
    ),
    Source(
        id="car_driver_alpr",
        title="Car and Driver: What Are Automated License Plate Readers and Why Are People Worried?",
        url="https://www.caranddriver.com/news/a70792616/automated-license-plate-reader-explainer/",
        publisher="Car and Driver",
        source_type="journalism_explainer",
        relevance="Explains ALPR capabilities, Flock adoption, vehicle attributes, data-sharing concerns, and city pushback.",
    ),
    Source(
        id="wsj_backlash",
        title="The Nationwide Backlash Against Cameras Watching Your Car",
        url="https://www.wsj.com/us-news/the-nationwide-backlash-against-cameras-watching-your-car-401a656a",
        publisher="Wall Street Journal",
        source_type="journalism",
        relevance="National backlash, DeFlock context, contract cancellations/rejections, and privacy concerns.",
    ),
    Source(
        id="guardian_flock",
        title="Why some cities are shutting down Flock cameras amid privacy concerns",
        url="https://www.theguardian.com/us-news/ng-interactive/2026/apr/06/flock-cameras-privacy-concerns",
        publisher="The Guardian",
        source_type="journalism",
        relevance="City shutdowns, privacy concerns, data sharing controversy, and security criticism.",
    ),
    Source(
        id="axios_shaker",
        title="Shaker Heights rewrites contract with Flock",
        url="https://www.axios.com/local/cleveland/2026/06/24/shaker-heights-flock-contract-amended",
        publisher="Axios Cleveland",
        source_type="local_journalism",
        relevance="Example of a city adding warrant and notice requirements for outside disclosure after public-records revelations.",
    ),
    Source(
        id="business_insider_false_hits",
        title="AI cameras are everywhere — and people are paying the price for their mistakes",
        url="https://www.businessinsider.com/flock-safety-alpr-cameras-misreads-2026-3",
        publisher="Business Insider",
        source_type="investigative_journalism",
        relevance="Misread plates, false stops/arrests, accuracy questions, and contract reconsideration context.",
    ),
    Source(
        id="az_leg_roster",
        title="Arizona Legislature member roster",
        url="https://www.azleg.gov/memberroster/",
        publisher="Arizona Legislature",
        source_type="official_roster",
        relevance="Official roster for state-level outreach and legislative accountability.",
    ),
    Source(
        id="stacey_travers_official",
        title="Rep. Stacey Travers official Arizona Legislature page",
        url="https://www.azleg.gov/house-member/?legislature=57&session=130&legislator=2340",
        publisher="Arizona Legislature",
        source_type="official_legislator_page",
        relevance="Official legislator page referenced by the Arizona campaign.",
    ),
    Source(
        id="lauren_kuby_official",
        title="Sen. Lauren Kuby official Arizona Legislature page",
        url="https://www.azleg.gov/senate-member/?legislature=57&legislator=2390",
        publisher="Arizona Legislature",
        source_type="official_legislator_page",
        relevance="Official legislator page referenced by the Arizona campaign.",
    ),
    Source(
        id="az_v_evans",
        title="Arizona v. Evans background: erroneous warrant after traffic violations",
        url="https://supreme.justia.com/cases/federal/us/514/1/",
        publisher="Justia / U.S. Supreme Court record",
        source_type="case_law",
        relevance="Shows how court database or warrant errors can produce real-world consequences after traffic-case failure-to-appear context.",
    ),
]

CLAIMS: list[Claim] = [
    Claim(
        id="alpr_location_records",
        claim="ALPR systems can create searchable vehicle-location records because they associate plate scans with time and place.",
        status=SUPPORTED_CLAIM,
        source_ids=["eff_alpr", "aclu_alpr", "car_driver_alpr"],
        action="Demand retention, audit, access, and sharing policy before deployment.",
    ),
    Claim(
        id="flock_not_ordinary_camera",
        claim="Flock-style ALPR systems should not be described as ordinary safety cameras because their core value is searchable vehicle intelligence.",
        status=SUPPORTED_CLAIM,
        source_ids=["car_driver_alpr", "wsj_backlash", "guardian_flock"],
        action="Separate traffic cameras, CCTV, and ALPR records in every public map and contract review.",
    ),
    Claim(
        id="traffic_england_public_to_private_warning",
        claim="The Traffic England closure notice is a warning that public-road information can move away from public portals and toward private or professional channels.",
        status=NEEDS_RECORDS,
        source_ids=["traffic_england_notice", "national_highways"],
        caveat="Archive the closure notice and cite National Highways sources for continuity. Do not claim motive unless documented.",
        action="Capture screenshots, archive URLs, and track what public data remains accessible after closure.",
    ),
    Claim(
        id="federal_sharing_concerns",
        claim="Some communities have raised concerns that ALPR data can be shared or accessed outside the local jurisdiction without adequate controls.",
        status=SUPPORTED_CLAIM,
        source_ids=["axios_shaker", "guardian_flock", "car_driver_alpr"],
        action="Demand outside-disclosure warrant rules and written notice to the local owner before sharing.",
    ),
    Claim(
        id="misread_false_stop_risk",
        claim="ALPR misreads and false positives can create serious consequences if officers rely on them without verification.",
        status=SUPPORTED_CLAIM,
        source_ids=["business_insider_false_hits"],
        action="Demand confidence thresholds, secondary verification, false-hit logs, and public reporting.",
    ),
    Claim(
        id="face_tracking_audio_claim",
        claim="A specific ASU/Tempe Flock or ALPR camera performs face tracking, audio capture, or driver identity collection.",
        status=UNSUPPORTED,
        source_ids=["osm_asu_tempe"],
        caveat="Do not state this as fact without the contract, vendor model, technical sheet, policy, and official record. Phrase it as a verification question.",
        action="Request model numbers, data fields, analytics features, and vendor policy through public records.",
    ),
    Claim(
        id="speed_camera_warrant_pipeline",
        claim="Traffic or photo-enforcement cases can escalate when people fail to respond or appear, and court/warrant database errors can create real consequences.",
        status=SUPPORTED_CLAIM,
        source_ids=["az_v_evans"],
        caveat="This is a court-process risk claim, not legal advice and not proof that every camera ticket creates a warrant.",
        action="Request local court policy for photo enforcement, service, default judgments, failure-to-appear, license suspension, warrants, and error correction.",
    ),
]

TARGETS: list[ActionTarget] = [
    ActionTarget(
        name="Arizona Legislature member roster",
        level="state",
        url="https://www.azleg.gov/memberroster/",
        category="legislative_roster",
        ask="Identify representatives and ask for statewide ALPR transparency, retention limits, public camera registries, and warrant rules.",
    ),
    ActionTarget(
        name="Rep. Stacey Travers",
        level="state_house",
        url="https://www.azleg.gov/house-member/?legislature=57&session=130&legislator=2340",
        ask="Ask whether Arizona should require public ALPR camera registries, warrant-based outside disclosure, annual reporting, and retention limits.",
    ),
    ActionTarget(
        name="Sen. Lauren Kuby",
        level="state_senate",
        url="https://www.azleg.gov/senate-member/?legislature=57&legislator=2390",
        ask="Ask whether Arizona should prohibit secret ALPR data sharing and require public contract disclosure.",
    ),
    ActionTarget(
        name="Tempe City Council / Clerk",
        level="city",
        url="https://www.tempe.gov/government/city-clerk-s-office/public-records",
        ask="Request contracts, camera locations, retention policy, audit logs, access rules, and sharing partners for ALPR/public safety cameras.",
    ),
    ActionTarget(
        name="Arizona State University records",
        level="campus",
        url="https://cfo.asu.edu/records-requests",
        ask="Request procurement, location, vendor, retention, and access-policy records for campus ALPR/public safety cameras.",
    ),
]

CAMERA_POINTERS: list[CameraPointer] = [
    CameraPointer(
        label="ASU / Tempe public map pointer",
        url="https://www.openstreetmap.org/node/13613353701#map=19/33.420348/-111.931079",
        latitude=33.420348,
        longitude=-111.931079,
        jurisdiction="Tempe / ASU area",
        camera_type="unknown",
        confidence="source_pointer",
        verification_questions=[
            "Who owns the device?",
            "Is it ALPR, CCTV, traffic monitoring, parking enforcement, or another sensor?",
            "What contract or procurement record authorizes it?",
            "What data fields are collected?",
            "What retention period applies?",
            "Can outside agencies search or request the data?",
            "Is a warrant required for external disclosure?",
        ],
    )
]


def ensure_dirs() -> None:
    for path in (DOCS, DATA, BUILD, ROOT / "schema"):
        path.mkdir(parents=True, exist_ok=True)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def md_table(rows: Iterable[Sequence[Any]], headers: Sequence[str]) -> str:
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |")
    return "\n".join(output)


def source_lookup() -> dict[str, Source]:
    return {source.id: source for source in SOURCES}


def export_sources() -> Path:
    ensure_dirs()
    payload = {
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "sources": [asdict(source) for source in SOURCES],
        "claims": [asdict(claim) for claim in CLAIMS],
        "targets": [asdict(target) for target in TARGETS],
        "camera_pointers": [asdict(pointer) for pointer in CAMERA_POINTERS],
    }
    path = BUILD / "overture-source-ledger.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_csv() -> list[Path]:
    ensure_dirs()
    paths: list[Path] = []
    for name, rows in {
        "sources.csv": [asdict(x) for x in SOURCES],
        "claims.csv": [asdict(x) for x in CLAIMS],
        "targets.csv": [asdict(x) for x in TARGETS],
        "camera_pointers.csv": [asdict(x) for x in CAMERA_POINTERS],
    }.items():
        path = BUILD / name
        if not rows:
            continue
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        paths.append(path)
    return paths


def verify_claims(strict: bool = False) -> int:
    lookup = source_lookup()
    errors = 0
    for claim in CLAIMS:
        missing = [sid for sid in claim.source_ids if sid not in lookup]
        if missing:
            print(f"[FAIL] {claim.id}: missing source IDs {missing}")
            errors += 1
        elif claim.status == UNSUPPORTED:
            print(f"[HOLD] {claim.id}: unsupported as fact; keep as verification question")
        elif claim.status in (NEEDS_RECORDS, NEEDS_VERIFICATION):
            print(f"[VERIFY] {claim.id}: source-backed direction, needs records/location verification")
        else:
            print(f"[OK] {claim.id}: supported by {', '.join(claim.source_ids)}")
    if strict and any(c.status == UNSUPPORTED for c in CLAIMS):
        print("[STRICT] Unsupported claims exist by design. Do not publish them as facts.")
    return errors


def build_exposure_report() -> Path:
    ensure_dirs()
    lookup = source_lookup()
    supported = [c for c in CLAIMS if c.status == SUPPORTED_CLAIM]
    needs = [c for c in CLAIMS if c.status in (NEEDS_RECORDS, NEEDS_VERIFICATION)]
    held = [c for c in CLAIMS if c.status == UNSUPPORTED]

    report = f"""# Arizona ALPR Exposure Report

Generated: {dt.datetime.now(dt.UTC).isoformat()}

## Executive point

Arizona should not normalize private ALPR grids without public proof. Flock-style systems and other ALPR deployments can create searchable vehicle-location records. The civic issue is not one camera. The issue is retention, sharing, auditability, warrant rules, error handling, contract renewals, and whether public-road intelligence becomes private infrastructure.

## Supported claims

{md_table([(c.claim, ', '.join(c.source_ids), c.action) for c in supported], ['Claim', 'Sources', 'Action'])}

## Claims that need public records before stronger language

{md_table([(c.claim, c.caveat, c.action) for c in needs], ['Claim', 'Caveat', 'Next action'])}

## Claims to hold until verified

{md_table([(c.claim, c.caveat, c.action) for c in held], ['Claim', 'Why held', 'Verification path'])}

## Camera pointer review

{md_table([(p.label, p.jurisdiction, p.url, p.confidence, '; '.join(p.verification_questions)) for p in CAMERA_POINTERS], ['Pointer', 'Jurisdiction', 'URL', 'Confidence', 'Questions'])}

## Public-records targets

{md_table([(t.name, t.level, t.url, t.ask) for t in TARGETS], ['Target', 'Level', 'URL', 'Ask'])}

## Source details

{md_table([(s.id, s.title, s.publisher, s.url, s.relevance) for s in SOURCES], ['ID', 'Title', 'Publisher', 'URL', 'Relevance'])}

## Public message

Public safety should not become private mass tracking. If a city, campus, HOA, or agency wants ALPR, residents deserve the contract, camera map, retention rules, audit logs, sharing partners, warrant policy, misuse penalties, and annual public review.
"""
    path = BUILD / "arizona-alpr-exposure-report.md"
    path.write_text(report, encoding="utf-8")
    return path


def build_public_records_bundle() -> Path:
    ensure_dirs()
    body = """# Public Records Bundle: ALPR / Flock / Camera Accountability

## Request template

Subject: Public records request: ALPR, Flock, public-safety camera, traffic-enforcement camera, and road-data records

Hello,

I am requesting public records related to automated license plate readers, Flock Safety systems, speed/photo-enforcement cameras, traffic cameras, public-safety cameras, and vendor-operated road or camera data systems used by your agency.

Please provide:

1. Contracts, purchase orders, invoices, amendments, renewals, and statements of work.
2. Camera locations, device IDs, installation dates, device models, and device purposes.
3. Data fields collected by each system.
4. Retention settings and retention-policy documents.
5. Search policies, access policies, user roles, and administrator roles.
6. Audit logs for searches, alerts, exports, outside requests, and administrative access.
7. Hotlist sources and procedures for hotlist entry/removal.
8. Data-sharing agreements with other agencies, vendors, federal entities, private entities, campuses, HOAs, or regional networks.
9. Warrant, subpoena, court-order, emergency-request, and informal-request procedures.
10. Misuse investigations, complaints, policy violations, false-hit reviews, and corrective actions.
11. Vendor security reviews, breach notices, cyber incident reports, penetration-test summaries, or access-control reviews.
12. Records showing whether data can be sold, licensed, analyzed, exported, trained on, or used beyond the original public-safety purpose.
13. For photo/speed enforcement: service-of-process policy, default judgment policy, failure-to-appear policy, license-suspension policy, warrant policy, judge/pro-tem review process, and error-correction process.

If any portion is withheld, please cite the specific exemption and release all segregable non-exempt material.

Thank you,

[NAME]
[CONTACT]

## Meeting questions

- What problem justifies the system?
- What less invasive alternatives were considered?
- What data is collected?
- Who owns the data?
- Who can search it?
- How long is it retained?
- What outside agencies can access it?
- Is a warrant required?
- What happens after a false hit?
- How are errors corrected?
- What happens if a camera ticket escalates to default, license suspension, or warrant status?
- When does the contract expire?
- Will there be an annual public vote?

## Contract redlines

- public camera registry
- maximum retention limit
- no sale of resident data
- no unrelated secondary use
- no outside disclosure without warrant or court order
- written notice before vendor disclosure
- role-based access
- case-number requirement
- audit logs
- independent audit
- false-hit review
- misuse penalties
- breach notice
- annual public report
- sunset clause
"""
    path = BUILD / "public-records-bundle.md"
    path.write_text(body, encoding="utf-8")
    return path


def build_linkedin_post() -> Path:
    ensure_dirs()
    post = """Arizona should not normalize private ALPR grids. We are the Wild West, not a private location-tracking test range.

England's Traffic England closure is the warning: public-road information can move away from public portals and toward private/professional channels.

Flock-style systems are not ordinary cameras. They can create searchable vehicle-location records. That means public contracts, retention limits, audit logs, sharing partners, warrant policy, and annual review are non-negotiable.

ASU/Tempe example: https://www.openstreetmap.org/node/13613353701#map=19/33.420348/-111.931079
Source map: https://deflock.org/

Ask your city, campus, HOA, police department, and state legislators for the contract, camera map, retention policy, audit logs, sharing partners, warrant rules, and renewal vote.

Public safety should not become private mass tracking.
"""
    path = BUILD / "linkedin-post.md"
    path.write_text(post, encoding="utf-8")
    return path


def db_url_from_env() -> str | None:
    direct = os.getenv("DATABASE_URL")
    if direct:
        return direct
    host = os.getenv("DB_HOST")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT", "5432")
    if not all([host, name, user, password]):
        return None
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


def connect_db():
    if psycopg2 is None:
        raise RuntimeError("psycopg2 is not installed. Run: pip install -r requirements.txt")
    url = db_url_from_env()
    if not url:
        raise RuntimeError("Set DATABASE_URL or DB_HOST/DB_NAME/DB_USER/DB_PASSWORD/DB_PORT.")
    return psycopg2.connect(url)


def init_db() -> None:
    if not SCHEMA.exists():
        raise FileNotFoundError(f"Missing schema file: {SCHEMA}")
    conn = connect_db()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(SCHEMA.read_text(encoding="utf-8"))
        print("[OK] database schema applied")
    finally:
        conn.close()


def seed_db() -> None:
    conn = connect_db()
    try:
        with conn, conn.cursor() as cur:
            for source in SOURCES:
                cur.execute(
                    """
                    insert into source_notes (source_title, source_url, source_type, summary, reliability, notes)
                    values (%s, %s, %s, %s, %s, %s)
                    """,
                    (source.title, source.url, source.source_type, source.relevance, "official" if source.source_type.startswith("official") else "high", source.notes),
                )
            for pointer in CAMERA_POINTERS:
                cur.execute(
                    """
                    insert into camera_assets (source_label, vendor, camera_type, public_source_url, latitude, longitude, location_description, confidence_level, capability_notes, privacy_notes, last_verified)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        pointer.label,
                        None,
                        pointer.camera_type if pointer.camera_type in {"traffic_camera", "alpr", "cctv", "public_safety_camera", "unknown"} else "unknown",
                        pointer.url,
                        pointer.latitude,
                        pointer.longitude,
                        pointer.jurisdiction,
                        pointer.confidence,
                        " ; ".join(pointer.verification_questions),
                        "Public map pointer only. Verify ownership, vendor, capability, and policy before publication.",
                        dt.date.today(),
                    ),
                )
        print("[OK] database seeded with sources and camera pointers")
    finally:
        conn.close()


def run_all() -> None:
    paths = [export_sources(), *write_csv(), build_exposure_report(), build_public_records_bundle(), build_linkedin_post()]
    print("Generated:")
    for path in paths:
        print(f"- {path.relative_to(ROOT)}")
    verify_claims()


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Overture civic-accountability pipeline")
    parser.add_argument(
        "command",
        choices=["all", "report", "records", "linkedin", "sources", "csv", "verify", "init-db", "seed-db"],
        help="Pipeline command to run.",
    )
    parser.add_argument("--strict", action="store_true", help="Strict claim verification mode.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    ensure_dirs()
    try:
        if args.command == "all":
            run_all()
        elif args.command == "report":
            print(build_exposure_report())
        elif args.command == "records":
            print(build_public_records_bundle())
        elif args.command == "linkedin":
            print(build_linkedin_post())
        elif args.command == "sources":
            print(export_sources())
        elif args.command == "csv":
            for path in write_csv():
                print(path)
        elif args.command == "verify":
            return verify_claims(strict=args.strict)
        elif args.command == "init-db":
            init_db()
        elif args.command == "seed-db":
            seed_db()
        return 0
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
