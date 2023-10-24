import matplotlib.pyplot as plt
import datetime as dt
import modules.curves as curves
import modules.perps as perps
import modules.plots as plots
from typing import Optional, List, Any


def spot_perp_difference(
    start_date: dt.datetime,
    end_date: dt.datetime,
    use_spot_curve_1: bool = False,
    use_spot_curve_2: bool = False,
    spot_curve_1_path: str = "",
    spot_curve_1_scaling: float = 1,
    spot_curve_1_horizontal_shift: float = 0,
    spot_curve_1_vertical_shift: float = 0,
    spot_curve_2_starting_value: float = 0,
    spot_curve_2_relative_change: float = 0,
    use_perp_curve_1: bool = False,
    use_perp_curve_2: bool = False,
    perp_curve_1_path: str = "",
    perp_curve_1_scaling: float = 1,
    perp_curve_1_horizontal_shift: float = 0,
    perp_curve_1_vertical_shift: float = 0,
    perp_curve_2_starting_value: float = 0,
    perp_curve_2_relative_change: float = 0,
    show: bool = False,
    plot_save_path: Optional[str] = None,
):
    if not show:
        plt.ioff()
        plt.clf()
    else:
        plt.ion()

    _, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].set_title("spot price")
    ax[1].set_title("perp price")
    ax[2].set_title("price difference")

    spot_curve_1 = None
    spot_curve_2 = None
    perp_curve_1 = None
    perp_curve_2 = None
    spot_resulting_curve = None
    perp_resulting_curve = None

    if use_spot_curve_1:
        if spot_curve_1_path == "":
            raise ValueError(
                "'spot_curve_1_path' must be specified when 'use_spot_curve_1'==True"
            )
        spot_curve_1 = curves.create_curve_from_file(
            spot_curve_1_path,
            scaling=spot_curve_1_scaling,
            horizontal_shift=spot_curve_1_horizontal_shift,
            vertical_shift=spot_curve_1_vertical_shift,
        )

    if use_perp_curve_1:
        if perp_curve_1_path == "":
            raise ValueError(
                "'perp_curve_1_path' must be specified when 'use_perp_curve_1'==True"
            )
        perp_curve_1 = curves.create_curve_from_file(
            perp_curve_1_path,
            scaling=perp_curve_1_scaling,
            horizontal_shift=perp_curve_1_horizontal_shift,
            vertical_shift=perp_curve_1_vertical_shift,
        )

    if use_spot_curve_2:
        spot_curve_2 = curves.create_simple_curve(
            start_date,
            end_date,
            spot_curve_2_starting_value,
            spot_curve_2_relative_change,
        )

    if use_perp_curve_2:
        perp_curve_2 = curves.create_simple_curve(
            start_date,
            end_date,
            perp_curve_2_starting_value,
            perp_curve_2_relative_change,
        )

    if spot_curve_1 != None or spot_curve_2 != None:
        spot_resulting_curve = curves.create_superimposed_curve(
            spot_curve_1,
            spot_curve_2,
            ax=ax[0],
            start_date=start_date,
            end_date=end_date,
            add_labels=False,
        )
    else:
        spot_resulting_curve = curves.create_simple_curve(
            start_date, end_date, 0, 0, ax=ax[0]
        )

    if perp_curve_1 != None or perp_curve_2 != None:
        perp_resulting_curve = curves.create_superimposed_curve(
            perp_curve_1,
            perp_curve_2,
            ax=ax[1],
            start_date=start_date,
            end_date=end_date,
            add_labels=False,
        )
    else:
        perp_resulting_curve = curves.create_simple_curve(
            start_date, end_date, 0, 0, ax=ax[1]
        )

    plots.plot_curve_difference(
        ax[2], perp_resulting_curve, spot_resulting_curve, start_date, end_date
    )
    if not plot_save_path is None:
        plt.savefig(plot_save_path)

    if show:
        plt.show()
    return spot_resulting_curve, perp_resulting_curve


def funding_periods(
    start_date: dt.datetime,
    end_date: dt.datetime,
    spot_curve: Any,
    perp_curve: Any,
    funding_schedule_minutes: int,
    spot_sampling_minutes: int,
    perp_sampling_minutes: int,
    interest_rate: float = 0,
    clamp_lower_bound: float = 0,
    clamp_upper_bound: float = 0,
    show_funding_payment: bool = False,
    show_funding_rate: bool = False,
    show_spot_twap: bool = False,
    show_perp_twap: bool = False,
    show_spot_step: bool = False,
    show_perp_step: bool = False,
    show_spot_points: bool = False,
    show_perp_points: bool = False,
    zoom: Optional[List] = None,
    show: bool = False,
    plot_save_path: Optional[str] = None,
):
    if not show:
        plt.ioff()
        plt.clf()
    else:
        plt.ion()

    _, ax = plt.subplots(1, 1, figsize=(15, 5))

    funding_schedule = perps.create_schedule(
        start_date,
        end_date,
        dt.timedelta(minutes=funding_schedule_minutes),
        False,
        ax,
    )
    spot_sampling_schedule = perps.create_schedule(
        start_date, end_date, dt.timedelta(minutes=spot_sampling_minutes)
    )
    perp_sampling_schedule = perps.create_schedule(
        start_date, end_date, dt.timedelta(minutes=perp_sampling_minutes)
    )

    funding_periods = perps.compute_funding_periods(
        funding_schedule,
        spot_sampling_schedule,
        perp_sampling_schedule,
        spot_curve,
        perp_curve,
        interest_rate,
        clamp_lower_bound,
        clamp_upper_bound,
    )

    x_limit_left = None
    x_limit_right = None
    if zoom != None and (zoom[0] != 0 or zoom[1] != 1):
        if zoom[0] == zoom[1]:
            if zoom[0] > 0.01:
                zoom = (zoom[1] - 0.01, zoom[1])
            else:
                zoom = (zoom[0], zoom[0] + 0.01)

        s = start_date.timestamp()
        e = end_date.timestamp()
        start = s + zoom[0] * (e - s)
        end = s + zoom[1] * (e - s)
        x_limit_left = dt.datetime.fromtimestamp(start)
        x_limit_right = dt.datetime.fromtimestamp(end)

    plots.plot_funding_periods(
        ax,
        funding_periods,
        spot_sampling_schedule,
        perp_sampling_schedule,
        spot_curve,
        perp_curve,
        x_limit_left=x_limit_left,
        x_limit_right=x_limit_right,
        show_spot_points=show_spot_points,
        show_perp_points=show_perp_points,
        show_spot_step=show_spot_step,
        show_perp_step=show_perp_step,
        show_spot_twap=show_spot_twap,
        show_perp_twap=show_perp_twap,
        show_funding_payment=show_funding_payment,
        show_funding_rate=show_funding_rate,
    )

    if not plot_save_path is None:
        plt.savefig(plot_save_path)
