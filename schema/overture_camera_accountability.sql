-- Overture Camera Accountability Schema
-- Public-source civic oversight for ALPR, traffic cameras, public safety camera contracts, and policy accountability.

create table if not exists jurisdictions (
  id bigserial primary key,
  name text not null,
  state text,
  country text default 'USA',
  jurisdiction_type text,
  website_url text,
  public_records_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists agencies (
  id bigserial primary key,
  jurisdiction_id bigint references jurisdictions(id) on delete set null,
  name text not null,
  agency_type text,
  website_url text,
  public_records_contact text,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists legislators (
  id bigserial primary key,
  name text not null,
  state text,
  chamber text,
  district text,
  party text,
  official_url text,
  campaign_url text,
  contact_url text,
  committees text[],
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists camera_assets (
  id bigserial primary key,
  source_label text not null,
  jurisdiction_id bigint references jurisdictions(id) on delete set null,
  agency_id bigint references agencies(id) on delete set null,
  vendor text,
  camera_type text not null,
  public_source_url text not null,
  latitude numeric(10,7),
  longitude numeric(10,7),
  location_description text,
  confidence_level text not null default 'unverified',
  capability_notes text,
  privacy_notes text,
  last_verified date,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint camera_type_check check (camera_type in ('traffic_camera','alpr','cctv','public_safety_camera','unknown')),
  constraint confidence_check check (confidence_level in ('unverified','source_pointer','verified_public_source','official_record'))
);

create table if not exists contracts (
  id bigserial primary key,
  jurisdiction_id bigint references jurisdictions(id) on delete set null,
  agency_id bigint references agencies(id) on delete set null,
  vendor text not null,
  contract_title text,
  contract_url text,
  start_date date,
  end_date date,
  renewal_date date,
  price_amount numeric(12,2),
  funding_source text,
  retention_policy text,
  audit_policy text,
  sharing_policy text,
  warrant_policy text,
  breach_policy text,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public_records_requests (
  id bigserial primary key,
  jurisdiction_id bigint references jurisdictions(id) on delete set null,
  agency_id bigint references agencies(id) on delete set null,
  request_title text not null,
  request_text text not null,
  submitted_date date,
  due_date date,
  status text not null default 'draft',
  response_url text,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint request_status_check check (status in ('draft','submitted','acknowledged','fulfilled','partial','denied','appealed','closed'))
);

create table if not exists source_notes (
  id bigserial primary key,
  source_title text not null,
  source_url text not null,
  source_type text,
  summary text,
  entities text[],
  reliability text not null default 'unknown',
  captured_at timestamptz not null default now(),
  notes text,
  constraint reliability_check check (reliability in ('unknown','low','medium','high','official'))
);

create index if not exists idx_camera_assets_vendor on camera_assets(vendor);
create index if not exists idx_camera_assets_type on camera_assets(camera_type);
create index if not exists idx_camera_assets_location on camera_assets(latitude, longitude);
create index if not exists idx_contracts_vendor on contracts(vendor);
create index if not exists idx_public_records_status on public_records_requests(status);
create index if not exists idx_legislators_state_chamber on legislators(state, chamber);

insert into jurisdictions (name, state, country, jurisdiction_type, website_url, public_records_url)
values
  ('Arizona', 'AZ', 'USA', 'state', 'https://az.gov/', 'https://www.azlibrary.gov/arm/accessing-arizona-public-records'),
  ('Tempe', 'AZ', 'USA', 'city', 'https://www.tempe.gov/', 'https://www.tempe.gov/government/city-clerk-s-office/public-records'),
  ('Arizona State University', 'AZ', 'USA', 'campus', 'https://www.asu.edu/', 'https://cfo.asu.edu/records-requests')
on conflict do nothing;
