# Overture Consumer Guide

## Purpose

Overture helps residents understand how public policy becomes real-world civic infrastructure. A bill, city vote, agency policy, procurement decision, or vendor contract can affect what data is collected, who controls it, how long it is kept, and what remedies residents have when a system creates harm or confusion.

This guide is written for nontechnical readers: residents, students, journalists, neighborhood groups, public commenters, and local watchdogs.

## The basic chain

```text
Law or policy
  -> agency authority
  -> budget or procurement
  -> vendor contract
  -> public system
  -> data collection
  -> access, retention, audit, sharing, and renewal rules
  -> resident impact
```

Overture focuses on the middle of that chain. Public debate often stops at broad claims such as safety, convenience, efficiency, or modernization. The project asks for the documents that show how the system actually works.

## Questions residents can ask

### What is being collected?

Ask for the exact data fields. For public camera and road-data systems, this can include timestamps, locations, images, device identifiers, alert records, search records, audit records, export records, and account-access records.

### Who controls the system?

Identify the public body or private contractor that controls procurement, data access, renewal, policy, audits, and public reporting.

### What records prove the claim?

A public map point is a lead. A vendor page is context. A signed contract, ordinance, policy, audit, or official records response is stronger evidence.

### What happens when the system is wrong?

Ask for error-review policies, correction procedures, complaint channels, audit rules, and public reporting. A system that has no correction path is not fully accountable.

### When does the public get another vote?

Ask for renewal dates, sunset clauses, public hearing dates, annual reports, and contract-extension rules.

## How to read this repository

Start with these files:

1. `README.md` for the project overview.
2. `docs/arizona-alpr-brief.md` for the Arizona camera-accountability brief.
3. `docs/legislation-impact-framework.md` for the policy-to-impact model.
4. `docs/claim-standards.md` for source and claim rules.
5. `docs/public-records-toolkit.md` for request templates.
6. `docs/repository-map.md` for file-by-file orientation.

## How to use the generated reports

Run:

```bash
python main.py all
```

Then read the files created in `build/`:

- `arizona-alpr-exposure-report.md`
- `public-records-bundle.md`
- `overture-source-ledger.json`
- `sources.csv`
- `claims.csv`
- `targets.csv`
- `camera_pointers.csv`

The generated reports are working drafts. Review source links and claim status before publishing or sending anything.

## A simple public-comment script

```text
Please publish the control documents for this system: the contract, device list, data fields, retention policy, access policy, audit policy, outside-access rules, correction process, renewal date, and annual reporting process.

If the system is limited, accountable, and publicly justified, those documents should be easy for residents to review.
```

## Claim discipline

Use careful language.

Good language:

- “This source points to a system that needs verification.”
- “This claim needs public records before stronger wording.”
- “The contract should answer the retention and access questions.”
- “The current source supports a general risk, not a site-specific conclusion.”

Bad language:

- “This specific device has a capability” without a model sheet or official record.
- “This agency has a secret policy” without records.
- “Every camera is the same kind of system.”
- “A lead is proof.”

Overture is strongest when it separates facts, leads, questions, and advocacy.
