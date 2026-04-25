-- 1. Upsert
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook c WHERE c.name = p_name) THEN
        UPDATE phonebook c
        SET phone = p_phone
        WHERE c.name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


-- 2. Bulk insert
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        
        IF p_phones[i] ~ '^[0-9]+$' THEN
            CALL upsert_contact(p_names[i], p_phones[i]);
        ELSE
            RAISE NOTICE 'Invalid: % - %', p_names[i], p_phones[i];
        END IF;

    END LOOP;
END;
$$;


-- 3. Delete
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook c
    WHERE c.name = p_value OR c.phone = p_value;
END;
$$;