import math

from typing_extensions import List, Optional

from src.services.bingx.notifications.historic.types_ import (
    NotifTriggerParams,
    NotifWithPriority,
)
from src.services.bingx.types_ import TickerAnalyticsDataPoint

notif_name_to_priority = {
    "fair_trade-0_05-3_ticks": 1,
    "fair_trade-0_5-3_ticks": 1,
    "fair_trade-1_3-3_ticks": 1,
    "fair_trade-5-3_ticks": 2,
    "fair_trade-10-3_ticks": 2,
}

notif_name_to_chats = {
    "fair_last-0_05-3_ticks": [],
    "fair_last-0_5-3_ticks": [],
    "fair_last-1_3-3_ticks": ["all", "prior"],
    "fair_last-5-3_ticks": ["all", "prior"],
    "fair_last-10-3_ticks": ["all", "prior"],
}


subnotifs: List[NotifTriggerParams] = [
    {"notif_name": "10-3_ticks", "threshold": 0.1},
    {"notif_name": "5-3_ticks", "threshold": 0.05},
    {"notif_name": "1_3-3_ticks", "threshold": 0.013},
    # {"notif_name": "0_5-3_ticks", "threshold": 0.005},
    # {"notif_name": "0_05-3_ticks", "threshold": 0.0005},
]  # in precedence order (only one (the first met) will be fired)


def notif_name_template(subnotif_name: str):
    return f"fair_trade-{subnotif_name}"


def should_fire(
    notif_params: NotifTriggerParams, data_points: List[TickerAnalyticsDataPoint]
) -> bool:
    return all(
        [
            data_point["fair_trade_delta_div_fair"] > notif_params["threshold"]
            for data_point in data_points
        ]
    )


def get_notif_to_fire(
    data_points: List[TickerAnalyticsDataPoint],
) -> Optional[NotifWithPriority]:
    data_points_to_analyze = data_points[-3:]
    # chose which subnotif to fire if any
    for subnotif in subnotifs:
        if should_fire(subnotif, data_points_to_analyze):
            notif_to_fire_name = notif_name_template(subnotif["notif_name"])
            notif_to_fire: NotifWithPriority = {
                "name": notif_to_fire_name,
                "priority": notif_name_to_priority[notif_to_fire_name],
                "last_value": data_points_to_analyze[-1]["fair_trade_delta_div_fair"],
                "chats": notif_name_to_chats[notif_to_fire_name],
            }
            return notif_to_fire
