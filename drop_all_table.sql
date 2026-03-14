DO $$
DECLARE
    r RECORD;
BEGIN
    -- пройтись по всем таблицам в схеме public
    FOR r IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        -- динамически выполнить DROP TABLE
        EXECUTE format('DROP TABLE IF EXISTS %I CASCADE;', r.tablename);
    END LOOP;
END $$;
