-- 2. Insert a new user; if the name already exists, update the phone
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE first_name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO contacts(first_name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

-- 3. Insert many users from lists; invalid data is collected and returned
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names  TEXT[],
    p_phones TEXT[],
    INOUT bad_data TEXT[] DEFAULT '{}'
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    bad_data := '{}';
    FOR i IN 1 .. COALESCE(array_length(p_names, 1), 0) LOOP
        -- valid phone: 87011112233 or +77011112233
        IF p_phones[i] ~ '^(\+7|8)[0-9]{10}$' THEN
            BEGIN
                CALL upsert_contact(p_names[i], p_phones[i]);
            EXCEPTION WHEN OTHERS THEN
                -- e.g. this phone already belongs to another contact
                bad_data := bad_data || (p_names[i] || ': ' || p_phones[i]);
            END;
        ELSE
            bad_data := bad_data || (p_names[i] || ': ' || p_phones[i]);
        END IF;
    END LOOP;
END;
$$;

-- 5. Delete data by username or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts WHERE first_name = p_value OR phone = p_value;
END;
$$;