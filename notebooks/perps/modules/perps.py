import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
from typing import List


class FundingPeriod:
    def __init__(
        self,
        start: dt.datetime,
        end: dt.datetime,
        payment: float,
        rate: float,
        spot_twap: float,
        perp_twap: float,
    ):
        self.start = start
        self.end = end
        self.payment = payment
        self.rate = rate
        self.spot_twap = spot_twap
        self.perp_twap = perp_twap

    def __str__(self):
        return f"FundingPeriod({self.start} - {self.end}):\n\tpayment={self.payment}\n\trate={self.rate}\n\tspot(TWAP)={self.spot_twap}\n\tperp(TWAP)={self.perp_twap}\n"


def create_schedule(
    start_date: dt.datetime, 
    end_date: dt.datetime, 
    time_step: dt.timedelta, 
    include_end_date: bool =False, ax=None
    ) -> List[dt.datetime]:
    if end_date < start_date:
        raise ValueError("end date cannot be lower than start date")

    schedule = np.array([start_date])
    while True:
        next_date = schedule[-1] + time_step
        if next_date >= end_date:
            break
        schedule = np.append(schedule, next_date)

    if include_end_date:
        schedule = np.append(schedule, end_date)

    return schedule


def twap(curve, curve_schedule: List[dt.datetime], start: dt.datetime, end: dt.datetime, weight_multiplier_increment: int = 0):
    if end <= start:
        raise ValueError("end must be after start")

    if curve is None:
        raise ValueError("curve must be specified")

    if curve_schedule is None:
        raise ValueError("curve schedule must be specified")

    indices = np.transpose(
        np.argwhere(np.logical_and(curve_schedule >= start, curve_schedule < end))
    )[0]
    if len(indices) == 0:
        if min(curve_schedule) > start:
            # schedule starts later
            return None
        # the last value before or at start still prevails
        return curve(
            curve_schedule[np.transpose(np.argwhere(curve_schedule <= start))[0][-1]]
        )

    prev_value = curve(curve_schedule[indices[0]].timestamp())
    if indices[0] == 0:
        # move start to first available observation
        start = curve_schedule[indices[0]]
    else:
        # use last known value
        prev_value = curve(curve_schedule[indices[0] - 1].timestamp())

    schedule_points_in_range = curve_schedule[indices]
    prev_time = start.timestamp()
    sum_product = 0
    sum_weight = 0
    weight_multiplier = 1
    for p in schedule_points_in_range[1:]:
        t = p.timestamp()
        w = (t-prev_time)*weight_multiplier
        sum_product += prev_value * w
        sum_weight += w
        weight_multiplier += weight_multiplier_increment
        prev_value = curve(t)
        prev_time = t
    t = end.timestamp()
    w = (t-prev_time)*weight_multiplier
    sum_product += prev_value * w
    sum_weight += w
    return sum_product / sum_weight

def compute_premium_index(impact_bid_curve, impact_ask_curve, price_index_curve, price_index_curve_schedule: List[dt.datetime], start: dt.datetime, end: dt.datetime, weight_multiplier_increment: int = 0):
    if end <= start:
        raise ValueError("end must be after start")

    if price_index_curve is None:
        raise ValueError("price_index_curve must be specified")

    if impact_bid_curve is None:
        raise ValueError("impact_bid_curve must be specified")

    if impact_ask_curve is None:
        raise ValueError("impact_ask_curve must be specified")

    if price_index_curve_schedule is None:
        raise ValueError("price_index_curve_schedule schedule must be specified")

    indices = np.transpose(
        np.argwhere(np.logical_and(price_index_curve_schedule >= start, price_index_curve_schedule < end))
    )[0]
    if len(indices) == 0:
        if min(price_index_curve_schedule) > start:
            # schedule starts later
            return None
        # the last value before or at start still prevails
        return premium_index_at_point(impact_bid_curve, impact_ask_curve, price_index_curve, price_index_curve_schedule[np.transpose(np.argwhere(price_index_curve_schedule <= start))[0][-1]]) 


    prev_value = premium_index_at_point(impact_bid_curve, impact_ask_curve, price_index_curve, price_index_curve_schedule[indices[0]].timestamp())
    if indices[0] == 0:
        # move start to first available observation
        start = price_index_curve_schedule[indices[0]]
    else:
        # use last known value
        prev_value = premium_index_at_point(impact_bid_curve, impact_ask_curve, price_index_curve, price_index_curve_schedule[indices[0] - 1].timestamp())

    schedule_points_in_range = price_index_curve_schedule[indices]
    prev_time = start.timestamp()
    sum_product = 0
    sum_weight = 0
    weight_multiplier = 1
    for p in schedule_points_in_range[1:]:
        t = p.timestamp()
        w = (t-prev_time)*weight_multiplier
        sum_product += prev_value * w
        sum_weight += w
        weight_multiplier += weight_multiplier_increment
        prev_value = premium_index_at_point(impact_bid_curve, impact_ask_curve, price_index_curve, t)
        prev_time = t
    t = end.timestamp()
    w = (t-prev_time)*weight_multiplier
    sum_product += prev_value * w
    sum_weight += w
    return sum_product / sum_weight

def premium_index_at_point(impact_bid_curve, impact_ask_curve, price_index_curve, point):
    # Premium Index (P) = [ Max(0, Impact Bid Price - Price Index ) - Max(0, Price Index - Impact Ask Price)] / Price Index
    price_index_at_point = price_index_curve(points)
    if price_index_at_point is None:
        return None
    return (max(0,impact_bid_curve(point)-price_index_at_point) - max(0,price_index_at_point-impact_ask_curve(points))) / price_index_at_point

def compute_funding_rate_from_premium_index(
    average_previum_index: float,
    interest_rate: float,
    delta_t: float,
    clamp_lower_bound: float,
    clamp_upper_bound: float,
) -> float:
    # Funding Rate (F) = Average Premium Index (P) + clamp (interest rate - Premium Index (P), 0.05%, -0.05%)
    return average_previum_index +  min(
            clamp_upper_bound,
            max(
                clamp_lower_bound,
                (1 + delta_t * interest_rate) - average_previum_index,
            ))

def compute_funding_payment(
    perp_twap: float,
    spot_twap: float,
    interest_rate: float,
    delta_t: float,
    clamp_lower_bound: float,
    clamp_upper_bound: float,
) -> float:
    funding_payment = perp_twap - spot_twap
    if clamp_lower_bound != 0 or clamp_upper_bound != 0:
        x = (1 + delta_t * interest_rate) * spot_twap - perp_twap
        funding_payment += min(
            clamp_upper_bound * spot_twap,
            max(
                clamp_lower_bound * spot_twap,
                (1 + delta_t * interest_rate) * spot_twap - perp_twap,
            ),
        )
    return funding_payment


def summarise(start, end, funding_periods, spot_curve, perp_curve):
    if len(funding_periods) == 0:
        return None

    # start = funding_periods[0].start
    # end = funding_periods[-1].end

    spot_rate_of_return = spot_curve(end) / spot_curve(start) - 1

    sum_funding_payments = sum([x.payment for x in funding_periods])
    perp_rate_of_return = (perp_curve(end) - sum_funding_payments) / perp_curve(
        start
    ) - 1

    return spot_rate_of_return, perp_rate_of_return, sum_funding_payments


def compute_funding_periods(
    funding_schedule,
    spot_sampling_schedule,
    perp_sampling_schedule,
    spot_curve,
    perp_curve,
    interest_rate=0,
    clamp_lower_bound=0,
    clamp_upper_bound=0,
):
    funding_periods = []
    for i in range(0, len(funding_schedule) - 1):
        start = funding_schedule[i]
        end = funding_schedule[i + 1]
        spot_twap = twap(spot_curve, spot_sampling_schedule, start, end)
        perp_twap = twap(perp_curve, perp_sampling_schedule, start, end)

        if spot_twap is None or perp_twap is None:
            continue

        delta_t = relativedelta(end, start).days / 365.25
        funding_payment = compute_funding_payment(
            perp_twap,
            spot_twap,
            interest_rate,
            delta_t,
            clamp_lower_bound,
            clamp_upper_bound,
        )
        funding_rate = funding_payment / spot_twap
        funding_periods.append(
            FundingPeriod(
                start, end, funding_payment, funding_rate, spot_twap, perp_twap
            )
        )
    return funding_periods
