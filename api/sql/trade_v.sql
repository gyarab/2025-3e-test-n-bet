create or replace view trade_v as
select
    json_strip_nulls(
        json_build_object(
            'trade_id', a.id,
            'trade_time', a.time,
            'trade_price', a.price,
            'trade_quantity', a.quantity,
            'trade_profit', a.profit,
            'backtest_id', a.backtest_id
        )
    ) as jdata
from backtests_trade a;
