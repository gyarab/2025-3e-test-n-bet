create or replace function chybova_hlaska(
    chyba_id integer,
    code integer,
    c_op integer,
    req json,
    logy json,
    cas timestamp with time zone default current_timestamp,
    detaily jsonb default '{}'::jsonb
)
returns table(
    stav integer,
    odpoved json,
    hlavicky json
) as $$
begin
    stav := chyba_id; 
    odpoved := json_build_object(
        'message', 'Došlo k chybě',
        'detaily', detaily,
        'request', req
    );
    hlavicky := json_build_object(
        'X-Operation', c_op,
        'X-Code', code
    );

    return next;
end;
$$ language plpgsql security definer;
