-- Отзовик / first-party review publication gate
-- READ-ONLY inspection. Do not execute as a migration.
-- Purpose: inspect the real Supabase schema before any moderation/publication mutation.
-- Expected project: otzovik (rzhlcszqtuhkhfibygnk)

-- 1) Confirm review-related tables in public/private schemas.
select table_schema, table_name
from information_schema.tables
where table_schema in ('public','private')
  and (
    table_name ilike '%review%'
    or table_name ilike '%submission%'
    or table_name ilike '%moder%'
  )
order by table_schema, table_name;

-- 2) Inspect columns and nullability for the private intake and public review records.
select table_schema, table_name, ordinal_position, column_name,
       data_type, is_nullable, column_default
from information_schema.columns
where table_schema in ('public','private')
  and table_name in ('own_review_submissions','reviews')
order by table_schema, table_name, ordinal_position;

-- 3) Inspect constraints/indexes that can affect publication and idempotency.
select n.nspname as schema_name,
       c.relname as table_name,
       con.conname as constraint_name,
       pg_get_constraintdef(con.oid) as constraint_definition
from pg_constraint con
join pg_class c on c.oid = con.conrelid
join pg_namespace n on n.oid = c.relnamespace
where n.nspname in ('public','private')
  and c.relname in ('own_review_submissions','reviews')
order by n.nspname, c.relname, con.conname;

select schemaname, tablename, indexname, indexdef
from pg_indexes
where schemaname in ('public','private')
  and tablename in ('own_review_submissions','reviews')
order by schemaname, tablename, indexname;

-- 4) Inspect grants (do not broaden them).
select grantee, table_schema, table_name, privilege_type
from information_schema.role_table_grants
where table_schema in ('public','private')
  and table_name in ('own_review_submissions','reviews')
order by table_schema, table_name, grantee, privilege_type;

-- 5) Inspect existing publication/moderation functions before creating anything new.
select n.nspname as schema_name,
       p.proname as function_name,
       pg_get_function_identity_arguments(p.oid) as arguments,
       pg_get_function_result(p.oid) as result_type,
       p.prosecdef as security_definer
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where n.nspname in ('public','private')
  and (
    p.proname ilike '%review%'
    or p.proname ilike '%moder%'
    or p.proname ilike '%publish%'
  )
order by n.nspname, p.proname;

-- Gate rule:
-- No INSERT/UPDATE/DELETE is included here.
-- After inspection, implement the smallest auditable publication operation only
-- if the actual schema matches OWN_REVIEW_MODERATION_SPEC.md and the owner
-- explicitly authorizes the production mutation.
