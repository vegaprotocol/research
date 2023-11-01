import modules.perps as perps
import modules.curves as curves
import scipy.interpolate as interp
import datetime as dt
import numpy as np
import pytest


def test_simple_curve():
    start = dt.datetime(year=dt.MINYEAR + 100, month=1, day=1)
    end = dt.datetime(year=dt.MAXYEAR - 100, month=1, day=1)
    start_value = 123.45
    curve1 = curves.SimpleCurveBetweenDates(start, end, start_value, 0)
    assert curve1(start - dt.timedelta(weeks=10)) == start_value
    assert curve1(start) == start_value
    assert curve1(start + dt.timedelta(weeks=500)) == start_value
    assert curve1(end) == start_value
    assert curve1(end + dt.timedelta(weeks=10)) == start_value

    relative_change_over_period = -0.567
    curve2 = curves.SimpleCurveBetweenDates(
        start, end, start_value, relative_change_over_period
    )

    assert curve2(start) == start_value
    assert abs(curve2(end) - start_value * (1 + relative_change_over_period)) < 1e-3


def test_flat_extension_curve():
    points = np.array([1, 2, 3])
    values = np.array([1, 9, 4])

    curve = interp.interp1d(points, values)

    assert curve(points[0]) == values[0]
    with pytest.raises(ValueError):
        curve(points[0] - 1)

    flat_extension = curves.FlatExtensionCurve(curve)

    assert flat_extension(points[0] - 1000) == curve(points[0])
    assert flat_extension(points[0]) == curve(points[0])
    assert flat_extension(points[1] + 0.5) == curve(points[1] + 0.5)
    assert flat_extension(points[2]) == curve(points[2])
    assert flat_extension(points[2] + 1000) == curve(points[2])


def test_transformed_curve():
    xs = [-100, -1.3, 0, 2, 3.14, 3e6]

    base_curve = lambda x: 2 * x + 3

    transformerd_curve = curves.TransformedCurve(base_curve)
    for x in xs:
        assert base_curve(x) == transformerd_curve(x)

    scaling = 6.789
    transformerd_curve = curves.TransformedCurve(
        base_curve, base_curve_scaling_factor=scaling
    )
    for x in xs:
        assert scaling * base_curve(x) == transformerd_curve(x)

    h_shift = -2.345
    transformerd_curve = curves.TransformedCurve(base_curve, horizontal_shift=h_shift)
    for x in xs:
        assert base_curve(x - h_shift) == transformerd_curve(x)

    v_shift = 0.123
    transformerd_curve = curves.TransformedCurve(base_curve, vertical_shift=v_shift)
    for x in xs:
        assert base_curve(x) + v_shift == transformerd_curve(x)

    scaling = -0.123
    h_shift = 0.891
    v_shift = -4.567

    transformerd_curve = curves.TransformedCurve(
        base_curve,
        base_curve_scaling_factor=scaling,
        horizontal_shift=h_shift,
        vertical_shift=v_shift,
    )
    for x in xs:
        assert scaling * base_curve(x - h_shift) + v_shift == transformerd_curve(x)


def test_superimposed_curve():
    with pytest.raises(ValueError):
        curves.SuperimposedCurve(None, None)

    xs = [-100, -1.3, 0, 2, 3.14, 3e6]

    curve_1 = lambda x: 1.23 * x
    curve_2 = lambda x: -456 * x

    test_curve = curves.SuperimposedCurve(None, curve_2)
    for x in xs:
        assert curve_2(x) == test_curve(x)

    test_curve = curves.SuperimposedCurve(curve_1, None)
    for x in xs:
        assert curve_1(x) == test_curve(x)

    test_curve_1 = curves.SuperimposedCurve(curve_1, curve_2)
    test_curve_2 = curves.SuperimposedCurve(curve_2, curve_1)
    for x in xs:
        assert curve_1(x) + curve_2(x) == test_curve_1(x)
        assert test_curve_1(x) == test_curve_2(x)
