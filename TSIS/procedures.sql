
-- 1. Add a new phone to an existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Wrong phone type "%". Use home, work or mobile.', p_type;
    END IF;

    SELECT id INTO v_id FROM contacts WHERE first_name = p_contact_name LIMIT 1;
    IF v_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    IF EXISTS (SELECT 1 FROM phones WHERE contact_id = v_id AND phone = p_phone) THEN
        RAISE EXCEPTION 'Contact "%" already has the phone %.', p_contact_name, p_phone;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type);
END;
$$;

-- 2. Move a contact to another group (creates the group if needed)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    UPDATE contacts SET group_id = v_group_id WHERE first_name = p_contact_name;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;
END;
$$;

-- 3. Extended search: name, email and ALL phones
-- (the Practice 8 version is replaced, because the result columns changed)
DROP FUNCTION IF EXISTS search_contacts(TEXT);
DROP FUNCTION IF EXISTS search_contacts(VARCHAR);

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id         INTEGER,
    first_name VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phones     TEXT
)
LANGUAGE sql AS $$
    SELECT c.id,
           c.first_name::VARCHAR,
           c.email::VARCHAR,
           c.birthday,
           g.name::VARCHAR,
           COALESCE(string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id), '-')::TEXT
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.id IN (
        SELECT c2.id
        FROM contacts c2
        LEFT JOIN phones p2 ON p2.contact_id = c2.id
        WHERE c2.first_name ILIKE '%' || p_query || '%'
           OR c2.email      ILIKE '%' || p_query || '%'
           OR p2.phone      ILIKE '%' || p_query || '%'
    )
    GROUP BY c.id, c.first_name, c.email, c.birthday, g.name
    ORDER BY c.first_name;
$$;