-- =========================
-- ADD PHONE
-- =========================
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    c_id INTEGER;
BEGIN
    -- найти контакт
    SELECT id INTO c_id
    FROM contacts
    WHERE name = p_contact_name;

    -- если не найден
    IF c_id IS NULL THEN
        RAISE NOTICE 'Contact not found';
        RETURN;
    END IF;

    -- добавить телефон
    INSERT INTO phones(contact_id, phone, type)
    VALUES (c_id, p_phone, p_type);

END;
$$;


-- =========================
-- MOVE TO GROUP
-- =========================
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    c_id INTEGER;
    g_id INTEGER;
BEGIN
    -- найти или создать группу
    SELECT id INTO g_id FROM groups WHERE name = p_group_name;

    IF g_id IS NULL THEN
        INSERT INTO groups(name)
        VALUES (p_group_name)
        RETURNING id INTO g_id;
    END IF;

    -- найти контакт
    SELECT id INTO c_id FROM contacts WHERE name = p_contact_name;

    IF c_id IS NULL THEN
        RAISE NOTICE 'Contact not found';
        RETURN;
    END IF;

    -- обновить группу
    UPDATE contacts
    SET group_id = g_id
    WHERE id = c_id;

END;
$$;


-- =========================
-- SEARCH CONTACTS
-- =========================
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(name VARCHAR, phone VARCHAR, email VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.name, p.phone, c.email
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;


-- =========================
-- DELETE CONTACT
-- =========================
CREATE OR REPLACE PROCEDURE delete_contact(p_name VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_name;
END;
$$;