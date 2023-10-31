import numpy as np
import datetime as dt
import modules.perps as perps
import matplotlib.dates as mdates
from matplotlib.patches import Patch


def plot_curve(curve, ax, start_date, end_date, add_labels):
    xs = np.arange(start_date.timestamp(), end_date.timestamp(), 120)
    ax.plot(xs, curve(xs), label="simple curve")

    format_axis(ax)

    if add_labels:
        start = start_date.timestamp()
        end = end_date.timestamp()
        ax.text(
            start,
            curve(start),
            f"{curve(start):,.0f}",
            ha="center",
            bbox=dict(facecolor="orange", alpha=0.5),
        )
        ax.text(
            end,
            curve(end),
            f"{curve(end):,.0f}",
            ha="center",
            bbox=dict(facecolor="orange", alpha=0.5),
        )


def plot_curve_difference(
    ax, perp_curve, spot_curve, start_date, end_date, relative_difference=False
):
    xs = np.arange(start_date.timestamp(), end_date.timestamp(), 120)
    ys = []
    label = ""
    if relative_difference:
        ys = [(perp_curve(x) - spot_curve(x)) / spot_curve(x) for x in xs]
        label = r"$\frac{perp - spot}{spot}$"
    else:
        ys = [(perp_curve(x) - spot_curve(x)) for x in xs]
        label = "perp - spot"
    ax.plot(xs, ys, "-", label=label)
    format_x_axis_timestamp_to_date(ax)


def format_axis(ax):
    format_x_axis_timestamp_to_date(ax)
    format_y_axis_in_thousands(ax)


def format_x_axis_timestamp_to_date(ax):
    ax.set_xticks(ax.get_xticks().tolist()[1:-1])  # needed to suppress the warning
    ax.set_xticklabels(
        [dt.datetime.fromtimestamp(x).strftime("%B %d") for x in ax.get_xticks()]
    )


def format_y_axis_in_thousands(ax):
    ax.set_yticks(ax.get_yticks().tolist()[1:-1])  # needed to suppress the warning
    ax.set_yticklabels(["{:,.0f}".format(x) for x in ax.get_yticks()])


def add_labels(dates, values, labels, ax, min_date=None, max_date=None):
    for i in range(len(dates)):
        d = dates[i]
        if (min_date == None or d >= min_date) and (max_date == None or d <= max_date):
            ax.text(
                d,
                values[i],
                f"{labels[i]:0.2%}",
                ha="center",
                bbox=dict(facecolor="orange", alpha=0.5),
            )


def plot_funding_periods(
    ax,
    start_date,
    end_date,
    funding_periods,
    spot_sampling_schedule,
    perp_sampling_schedule,
    spot_curve,
    perp_curve,
    x_limit_left=None,
    x_limit_right=None,
    show_spot_points=False,
    show_perp_points=False,
    show_spot_step=False,
    show_perp_step=False,
    show_spot_twap=False,
    show_perp_twap=False,
    show_funding_payment=False,
    show_funding_rate=False,
):
    funding_periods_for_chart = funding_periods
    extra_point = funding_periods[-1]
    funding_periods_for_chart.append(
        perps.FundingPeriod(
            extra_point.end,
            extra_point.end,
            extra_point.payment,
            extra_point.rate,
            extra_point.spot_twap,
            extra_point.perp_twap,
        )
    )

    spot_points = spot_curve([x.timestamp() for x in spot_sampling_schedule])
    perp_points = perp_curve([x.timestamp() for x in perp_sampling_schedule])

    if show_spot_points:
        ax.plot(
            spot_sampling_schedule,
            spot_points,
            "x",
            color="green",
            label="spot: sampled points",
        )
    if show_spot_step:
        ax.step(
            spot_sampling_schedule,
            spot_points,
            "--",
            where="post",
            color="green",
            label="spot: observed",
        )
    if show_spot_twap:
        ax.step(
            [x.start for x in funding_periods_for_chart],
            [x.spot_twap for x in funding_periods_for_chart],
            where="post",
            color="green",
            label="spot: TWAP",
            linewidth="3",
        )

    if show_perp_points:
        ax.plot(
            perp_sampling_schedule,
            perp_points,
            "*",
            color="purple",
            label="perp: sampled points",
        )
    if show_perp_step:
        ax.step(
            perp_sampling_schedule,
            perp_points,
            "--",
            where="post",
            color="purple",
            label="perp: observed",
        )
    if show_perp_twap:
        ax.step(
            [x.start for x in funding_periods_for_chart],
            [x.perp_twap for x in funding_periods_for_chart],
            where="post",
            color="purple",
            label="perp: TWAP",
        )
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%B %d"))
    ax.set_yticks(ax.get_yticks().tolist()[1:-1])  # needed to suppress the warning
    ax.set_yticklabels(["{:,.0f}".format(x) for x in ax.get_yticks()])

    additional_handles = []
    additional_labels = []
    if show_funding_payment:
        ax2 = ax.twinx()
        colour = "cadetblue"
        ax2.axhline(y=0, alpha=0.25, color=colour, lw=0.6)
        ax2.bar(
            [x.end for x in funding_periods],
            [x.payment for x in funding_periods],
            color=colour,
            width=0.3,
            alpha=0.8,
            label="funding payment",
        )
        ax2.set_ylabel("funding payment", color=colour)

        additional_handles.append(Patch(facecolor=colour))
        additional_labels.append("funding payment")

        if show_funding_rate:
            add_labels(
                [x.end for x in funding_periods],
                [x.payment for x in funding_periods],
                [x.rate for x in funding_periods],
                ax2,
                x_limit_left,
                x_limit_right,
            )
            additional_handles.append(
                Patch(facecolor="orange", edgecolor="b", alpha=0.5)
            )
            additional_labels.append("funding rate")

    if not show_funding_payment and show_funding_rate:
        ax2 = ax.twinx()
        colour = "orange"
        ax2.axhline(y=0, alpha=0.25, color=colour, lw=0.6)
        ax2.bar(
            [x.end for x in funding_periods],
            [x.rate for x in funding_periods],
            color=colour,
            width=0.3,
            alpha=0.8,
            label="funding rate",
        )
        ax2.set_ylabel("funding rate", color=colour)

        additional_handles.append(Patch(facecolor=colour))
        additional_labels.append("funding rate")

    y_min, y_max = ax.get_ylim()
    ax.vlines(
        x=[x.end for x in funding_periods_for_chart],
        ymin=y_min,
        ymax=y_max,
        colors="black",
        label="funding periods",
    )
    handles, labels = ax.get_legend_handles_labels()
    handles.extend(additional_handles)
    labels.extend(additional_labels)

    ax.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=5)

    x_min, x_max = ax.get_xlim()

    if x_limit_left != None:
        left = mdates.date2num(x_limit_left)
        if left != x_min:
            ax.set_xlim(left=max(x_min, left))

    if x_limit_right != None:
        right = mdates.date2num(x_limit_right)
        if right != x_max:
            ax.set_xlim(right=min(x_max, right))

    spot_rr, perp_rr, sum_funding_payments = perps.summarise(
        start_date, end_date,
        funding_periods, spot_curve, perp_curve
    )
    txt = f"metrics for position of size 1:\n  {'sum of payments':<19} = {sum_funding_payments:,.0f}\n  {'perp rate of return':<21} = {perp_rr:0.3%}\n  {'spot rate of return':<21} = {spot_rr:0.3%}"
    ax.get_figure().text(
        x=0,
        y=1,
        s=txt,
    )
