from sqlalchemy import desc
from typing_extensions import List

from src.db.engine_session import SessionLocal
from src.db.models.mexc.TickerTimeseries import (
    TickerTimeseries as TickerTimeseriesModel,
)
from src.services.mexc.types_ import TickerAnalyticsDataPoint


def get_ticker_timeseries(symbol: str, steps: int) -> List[TickerAnalyticsDataPoint]:
    with SessionLocal() as session:
        rows = (
            session.query(TickerTimeseriesModel)
            .filter(TickerTimeseriesModel.symbol == symbol)
            .order_by(desc(TickerTimeseriesModel.timestamp))
            .limit(steps)
            .all()
        )
        return [
            {
                "symbol": row.symbol,
                "timestamp": row.timestamp,
                "last_price": row.last_price,
                "fair_price": row.fair_price,
                "index_price": row.index_price,
                "funding_rate": row.funding_rate,
                #
                "index_fair_delta_div_index": row.index_fair_delta_div_index,
                "fair_last_delta_div_fair": row.fair_last_delta_div_fair,
                #
                "last_fair_delta_div_avg": row.last_fair_delta_div_avg,
            }
            for row in rows
        ]


def add_ticker_update(ticker_data_point: TickerAnalyticsDataPoint):
    # add row to db
    with SessionLocal() as session:
        row = TickerTimeseriesModel(
            symbol=ticker_data_point["symbol"],
            timestamp=ticker_data_point["timestamp"],
            last_price=ticker_data_point["last_price"],
            fair_price=ticker_data_point["fair_price"],
            index_price=ticker_data_point["index_price"],
            funding_rate=ticker_data_point["funding_rate"],
            #
            index_fair_delta_div_index=ticker_data_point["index_fair_delta_div_index"],
            fair_last_delta_div_fair=ticker_data_point["fair_last_delta_div_fair"],
            #
            last_fair_delta_div_avg=ticker_data_point["last_fair_delta_div_avg"],
        )
        session.add(row)
        session.commit()
