CREATE OR REPLACE FUNCTION vrat_trade(
    request json,
    logy    json DEFAULT '{}'::json,
    cas     timestamp with time zone DEFAULT current_timestamp,
    stav    OUT integer,
    odpoved OUT json
)
AS $$
DECLARE
    _req json := request;
    _odpoved json;
    _err integer := 0;
BEGIN
    -- získání všech záznamů z pohledu trade_v
    SELECT json_agg(jdata)
    INTO _odpoved
    FROM trade_v;

    -- pokud není žádný záznam, použij chybovou hlášku
    IF _odpoved IS NULL THEN
        SELECT ch.stav, ch.odpoved
        INTO stav, odpoved
        FROM chybova_hlaska(1, 0, 99, _req, logy, cas) AS ch;
        RETURN;
    END IF;

    -- normální případ, vrací data
    SELECT ch.stav, COALESCE(_odpoved, '[]'::json)
    INTO stav, odpoved
    FROM chybova_hlaska(_err, 0, 99, _req, logy, cas) AS ch;

EXCEPTION
    WHEN others THEN
        -- pokud nastane neočekávaná chyba, vrátí chybovou hlášku s detailem
        SELECT ch.stav, ch.odpoved
        INTO stav, odpoved
        FROM chybova_hlaska(
            27, 0, 99, _req, logy, cas,
            json_build_object('message', SQLERRM)::jsonb
        ) AS ch;
END;
$$
LANGUAGE plpgsql
SECURITY DEFINER;
	