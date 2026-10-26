-- Snabbmatte: konton och molnsparning.
-- Klistra in allt i Supabase → SQL Editor → New query och tryck Run.
-- Skriptet går att köra flera gånger.

-- Profiler: ett användarnamn per konto, unikt oavsett stora och små bokstäver.
create table if not exists public.profiles (
  id uuid primary key references auth.users on delete cascade,
  username text not null check (username ~ '^[A-Za-z0-9ÅÄÖåäö_.-]{3,20}$'),
  created_at timestamptz not null default now()
);
create unique index if not exists profiles_username_lower on public.profiles (lower(username));
alter table public.profiles enable row level security;
drop policy if exists "Läsa egen profil" on public.profiles;
create policy "Läsa egen profil" on public.profiles for select using (auth.uid() = id);

-- Profilen skapas automatiskt med användarnamnet som valdes vid registreringen.
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profiles (id, username) values (new.id, new.raw_user_meta_data ->> 'username');
  return new;
end;
$$;
revoke execute on function public.handle_new_user() from public, anon, authenticated;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- Appen frågar om ett namn är ledigt utan att kunna läsa andras profiler.
create or replace function public.username_available(name text) returns boolean
language sql security definer set search_path = '' stable as $$
  select not exists (select 1 from public.profiles where lower(username) = lower(name));
$$;
revoke all on function public.username_available(text) from public;
grant execute on function public.username_available(text) to anon, authenticated;

-- Framsteg: hela spelläget som JSON, en rad per konto.
create table if not exists public.progress (
  user_id uuid primary key references auth.users on delete cascade,
  data jsonb not null,
  updated_at timestamptz not null default now()
);
alter table public.progress enable row level security;
drop policy if exists "Egna framsteg" on public.progress;
create policy "Egna framsteg" on public.progress for all
  using (auth.uid() = user_id) with check (auth.uid() = user_id);
