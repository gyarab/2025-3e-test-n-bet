create or replace function vrat_trade(
    request in json,
    logy    in json default '{}'::json,
    cas     timestamp with time zone default current_timestamp,
    stav    out integer,
    odpoved out json,
    hlavicky out json
)
as $$
declare
    _req json := request;
    _odpoved json;
    _err integer := 0;
begin

    select json_agg(jdata) 
    into _odpoved
    from trade_v;

    if _odpoved is null then
        select ch.stav, ch.odpoved, ch.hlavicky
        into stav, odpoved, hlavicky
        from chybova_hlaska(1, 0, 99, _req, logy, cas) ch;  
        return;
    end if;

    select ch.stav, coalesce(_odpoved, '[]'::json), ch.hlavicky
    into stav, odpoved, hlavicky
    from chybova_hlaska(_err, 0, 99, _req, logy, cas) ch;

exception
    when others then
        select ch.stav, ch.odpoved, ch.hlavicky
        into stav, odpoved, hlavicky
        from chybova_hlaska(27, 0, 99, _req, logy, cas, 
            json_build_object('message', SQLERRM)::jsonb) ch;
end;
$$ language plpgsql security definer;
