import numpy as np
import pandas as pd
import scipy.interpolate as interp
import datetime as dt
import modules.plots as plots


class SimpleCurveBetweenDates:
    def __init__(
        self,
        start_date: dt.datetime,
        end_date: dt.datetime,
        start_value: float,
        relatove_change_over_period: float = 0,
    ):
        self.start = start_date.timestamp()
        self.end = end_date.timestamp()
        self.a = start_value * relatove_change_over_period / (self.end - self.start)
        self.b = start_value

        curve_at_start = self.evaluate(self.start)
        curve_at_end = self.evaluate(self.end)

        self.min = min(curve_at_start, curve_at_end)
        self.max = max(curve_at_start, curve_at_end)

    def __call__(self, xs):
        if type(xs) is dt.datetime:
            xs = xs.timestamp()
        if np.isscalar(xs):
            return self.evaluate(xs)
        return np.array([self.evaluate(x) for x in xs])

    def evaluate(self, x):
        return self.a * (x - self.start) + self.b


class FlatExtensionCurve:
    def __init__(self, base_curve):
        self.base_curve = base_curve
        self.x_min = base_curve.x[0]
        self.x_max = base_curve.x[-1]
        ys = base_curve(base_curve.x)
        self.min = min(ys)
        self.max = max(ys)

    def __call__(self, xs):
        if type(xs) is dt.datetime:
            xs = xs.timestamp()
        if np.isscalar(xs):
            return self.evaluate(xs)
        return np.array([self.evaluate(x) for x in xs])

    def evaluate(self, x):
        if x < self.x_min:
            x = self.x_min
        if x > self.x_max:
            x = self.x_max
        return self.base_curve(x)


class TransformedCurve:
    def __init__(
        self, curve, base_curve_scaling_factor=1, horizontal_shift=0, vertical_shift=0
    ):
        self.curve = curve
        self.vertical_shift = vertical_shift
        self.scaling_factor = base_curve_scaling_factor
        self.horizontal_shift = horizontal_shift

    def __call__(self, xs):
        if np.isscalar(xs):
            return self.evaluate(xs)
        return np.array([self.evaluate(x) for x in xs])

    def evaluate(self, x):
        return (
            self.scaling_factor * self.curve(x - self.horizontal_shift)
            + self.vertical_shift
        )


class SuperimposedCurve:
    def __init__(self, curve_1, curve_2):
        if curve_1 == None and curve_2 == None:
            raise ValueError("at least one curve must be specified")
        self.curve_1 = curve_1
        self.curve_2 = curve_2

    def __call__(self, xs):
        if type(xs) is dt.datetime:
            xs = xs.timestamp()
        if np.isscalar(xs):
            return self.evaluate(xs)
        return np.array([self.evaluate(x) for x in xs])

    def evaluate(self, x):
        ret = 0
        if self.curve_1 != None:
            ret += self.curve_1(x)
        if self.curve_2 != None:
            ret += self.curve_2(x)
        return ret


def create_curve_from_file(
    dir, scaling=1, horizontal_shift=0, vertical_shift=0, ax=None
):
    col_vol = "volume"
    col_date = "date"
    col_price = "price"

    df = pd.read_csv(dir)

    if col_vol in df:
        df = df[df[col_vol] > df[col_vol].quantile(0.05)]

    timestamps = df[col_date]
    prices = df[col_price]
    cs = interp.Akima1DInterpolator(timestamps, prices)
    xs = np.arange(timestamps.min(), timestamps.max(), 120)
    if ax != None:
        ax.plot(timestamps, prices, "o", label="data point")
        ax.plot(xs, cs(xs), label="interpolation")
        ax.legend(loc="upper center", ncol=2)
        plots.format_axis(ax)

    return TransformedCurve(
        FlatExtensionCurve(cs), scaling, horizontal_shift, vertical_shift
    )


def create_simple_curve(
    start_date: dt.datetime,
    end_date: dt.datetime,
    start_value: float,
    relative_change_over_period: float,
    ax=None,
    add_labels=False,
):
    curve = SimpleCurveBetweenDates(
        start_date, end_date, start_value, relative_change_over_period
    )

    if ax != None:
        plots.plot_curve(curve, ax, start_date, end_date, add_labels)

    return curve


def create_superimposed_curve(
    curve_1,
    curve_2,
    ax=None,
    start_date: dt.datetime = None,
    end_date: dt.datetime = None,
    add_labels=False,
):
    curve = SuperimposedCurve(curve_1, curve_2)

    if ax != None:
        if start_date == None or end_date == None:
            raise ValueError(
                "start and end date must be speficied if the ax object is suplied"
            )
        plots.plot_curve(curve, ax, start_date, end_date, add_labels)

    return curve
