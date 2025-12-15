
CREATE FUNCTION chybova_hlaska(
    chyba_id integer,
    code integer,
    c_op integer,
    req json,
    logy json,
    cas timestamp with time zone default current_timestamp,
    detaily jsonb default '{}'::jsonb
)
RETURNS TABLE(
    stav integer,
    odpoved json,
    headers json
) AS $$
BEGIN
    stav := chyba_id; 
    odpoved := json_build_object(
        'message', 'Došlo k chybě',
        'details', detaily,
        'request', req
    );
    headers := json_build_object(
        'X-Operation', c_op,
        'X-Code', code
    );

    RETURN NEXT;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
