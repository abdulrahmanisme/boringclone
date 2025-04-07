-- Enable necessary extensions
create extension if not exists "uuid-ossp";

-- Create enum types
create type submission_status as enum ('pending', 'in_progress', 'completed', 'failed');
create type submission_type as enum ('api', 'selenium');

-- Create startups table
create table if not exists startups (
    id bigint primary key generated always as identity,
    name varchar(255) not null,
    website text not null,
    description text not null,
    tagline text,
    founded_year integer,
    logo_url text,
    twitter_handle varchar(255),
    linkedin_url text,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Create platforms table
create table if not exists platforms (
    id bigint primary key generated always as identity,
    name varchar(255) not null unique,
    url text not null,
    submission_type submission_type not null,
    submission_endpoint text,
    api_key_required boolean default false,
    is_active boolean default true,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Create submissions table
create table if not exists submissions (
    id bigint primary key generated always as identity,
    startup_id bigint references startups(id) on delete cascade,
    platform_id bigint references platforms(id) on delete cascade,
    status submission_status default 'pending',
    error_message text,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Create indexes
create index if not exists idx_submissions_startup_id on submissions(startup_id);
create index if not exists idx_submissions_platform_id on submissions(platform_id);
create index if not exists idx_submissions_status on submissions(status);
create index if not exists idx_platforms_submission_type on platforms(submission_type);
create index if not exists idx_startups_name on startups(name);

-- Create updated_at trigger function
create or replace function update_updated_at_column()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

-- Create triggers for updated_at
create trigger update_startups_updated_at
    before update on startups
    for each row
    execute function update_updated_at_column();

create trigger update_platforms_updated_at
    before update on platforms
    for each row
    execute function update_updated_at_column();

create trigger update_submissions_updated_at
    before update on submissions
    for each row
    execute function update_updated_at_column();

-- Create storage bucket for startup logos
insert into storage.buckets (id, name)
values ('startup-logos', 'startup-logos')
on conflict (id) do nothing;

-- Set up storage policies
create policy "Public Access"
    on storage.objects for select
    using ( bucket_id = 'startup-logos' );

create policy "Authenticated Users Can Upload"
    on storage.objects for insert
    with check ( bucket_id = 'startup-logos' AND auth.role() = 'authenticated' ); 