import modules.perps as perps
import modules.curves as curves
import datetime as dt
import numpy as np
import pytest


def test_payment_schedule():
    start = dt.datetime(2023, 5, 1)
    end = dt.datetime(2023, 6, 1)
    timestep = dt.timedelta(days=27)

    with pytest.raises(ValueError):
        perps.create_schedule(end, start, timestep)

    schedule = perps.create_schedule(start, start, timestep)
    assert len(schedule) == 1
    assert schedule[0] == start

    schedule = perps.create_schedule(start, end, timestep)
    assert len(schedule) == 2
    assert schedule[0] == start
    assert schedule[1] != end

    schedule = perps.create_schedule(start, end, timestep, include_end_date=True)
    assert len(schedule) == 3
    assert schedule[0] == start
    assert schedule[1] != end
    assert schedule[2] == end


def test_twap():
    delta = 1e-3

    start = dt.datetime(2023, 5, 1)
    end = dt.datetime(2023, 5, 30)

    const = 0.5
    curve = lambda x: const
    curve_schedule = np.array([start, end])

    with pytest.raises(ValueError):
        perps.twap(None, None, end, start)
        perps.twap(None, curve_schedule, start, end)
        perps.twap(curve, None, start, end)

    twap = perps.twap(curve, curve_schedule, start, end)
    assert twap == const

    start_value = 3.21
    relative_change_over_period = -0.6
    curve = curves.SimpleCurveBetweenDates(
        start, end, start_value, relative_change_over_period
    )
    twap = perps.twap(curve, curve_schedule, start, end)
    assert twap == start_value

    curve_schedule = np.array(
        [
            dt.datetime.fromtimestamp(x)
            for x in np.linspace(start.timestamp(), end.timestamp(), 10000)
        ]
    )

    twap = perps.twap(curve, curve_schedule, start, end)
    expected = (start_value + start_value * (1 + relative_change_over_period)) / 2
    assert abs(expected - twap) < delta

    # moving start before first point in the curve schedule shouldn't affect TWAP
    twap = perps.twap(curve, curve_schedule, start - dt.timedelta(days=20), end)
    assert abs(expected - twap) < 100 * delta

    # moving end after last point in the curve schedule should change TWAP (last point gets carried over)
    twap = perps.twap(curve, curve_schedule, start, end + dt.timedelta(days=20))
    assert expected > twap + delta

    # moving start into the schedule should change TWAP
    twap = perps.twap(curve, curve_schedule, start + dt.timedelta(days=20), end)
    assert expected > twap + 100 * delta

    # single point schedule should work fine
    point = start + dt.timedelta(days=10)
    twap = perps.twap(curve, np.array([point]), start, end)
    expected = curve(point)
    assert abs(twap - expected) < delta

    # schedule starting after end should result in nil value
    twap = perps.twap(
        curve,
        np.array([end + dt.timedelta(days=10), end + dt.timedelta(days=20)]),
        start,
        end,
    )
    assert twap is None

    # schedule ending before start date should result in constant last value
    schedule_start = start - dt.timedelta(days=20)
    schedule_end = start - dt.timedelta(days=10)
    twap = perps.twap(curve, np.array([schedule_start, schedule_end]), start, end)
    expected = curve(schedule_end)
    assert abs(twap - expected) < delta


def test_compute_funding_payment():
    delta = 1e-6

    value1 = 123.456
    value2 = 78.91
    interest_rate = 0.15

    assert (
        perps.compute_funding_payment(value1, value2, interest_rate, 1, 0, 0)
        == value1 - value2
    )
    assert (
        perps.compute_funding_payment(value2, value1, interest_rate, 1, 0, 0)
        == value2 - value1
    )
    assert (
        perps.compute_funding_payment(value2, value1, interest_rate, 1, 0, 0)
        == value2 - value1
    )
    assert perps.compute_funding_payment(value1, value1, interest_rate, 1, 0, 0) == 0

    delta_t = 0.5

    expected = 0
    actual = perps.compute_funding_payment(value1, value2, 0, delta_t, -1000, 1000)
    assert abs(actual - expected) < delta

    expected = value1
    actual = perps.compute_funding_payment(
        value1, value2, interest_rate, delta_t, 1, 1000
    )
    assert abs(actual - expected) < delta

    lb = 2
    expected = value1 - value2 + lb * value2
    actual = perps.compute_funding_payment(
        value1, value2, interest_rate, delta_t, lb, 1000
    )
    assert abs(actual - expected) < delta

    ub = 0.21
    expected = value2 - value1 + ub * value1
    actual = perps.compute_funding_payment(
        value2, value1, interest_rate, delta_t, -1000, ub
    )
    assert abs(actual - expected) < delta


def test_payment_summarize():
    start = dt.datetime(2019, 1, 1)
    end = dt.datetime(2019, 7, 7)
    spot_start = 100
    spot_end = 150
    perp_start = 110
    perp_end = 95

    spot_curve = (
        lambda x: spot_start if x == start else (spot_end if x == end else None)
    )
    perp_curve = (
        lambda x: perp_start if x == start else (perp_end if x == end else None)
    )

    funding_periods = np.array([])
    assert None == perps.summarise(start, end, funding_periods, spot_curve, perp_curve)

    payment1 = 123.4
    payment2 = -567.8
    payment3 = 910.11
    fp1 = perps.FundingPeriod(start, dt.datetime(2019, 2, 2), payment1, -1, -1, -1)
    fp2 = perps.FundingPeriod(
        dt.datetime(2019, 2, 2), dt.datetime(2019, 3, 3), payment2, -1, -1, -1
    )
    fp3 = perps.FundingPeriod(dt.datetime(2019, 6, 6), end, payment3, -1, -1, -1)

    spot_rate_of_return, perp_rate_of_return, sum_funding_payments = perps.summarise(
        start, end, np.array([fp1, fp2, fp3]), spot_curve, perp_curve
    )

    assert payment1 + payment2 + payment3 == sum_funding_payments
    assert spot_rate_of_return == spot_end / spot_start - 1
    assert perp_rate_of_return == (perp_end - sum_funding_payments) / perp_start - 1
