import matplotlib.pyplot as plt
import datetime as dt
import modules.curves as curves
import modules.perps as perps
import modules.plots as plots
import ipywidgets as widgets
import glob


class UI:
    def __init__(
        self, curve_folder_path: str, start_date: dt.datetime, end_date: dt.datetime
    ):
        self.curve_folder_path = curve_folder_path
        self.start_date = start_date
        self.end_date = end_date
        self.spot_curve = curves.create_simple_curve(start_date, end_date, 0, 0)
        self.perp_curve = curves.create_simple_curve(start_date, end_date, 0, 0)

    def display_funding_periods(
        self,
        start_date,
        end_date,
        funding_schedule_minutes,
        spot_sampling_minutes,
        perp_sampling_minutes,
        interest_rate=0,
        clamp_lower_bound=0,
        clamp_upper_bound=0,
        show_funding_payment=False,
        show_funding_rate=False,
        show_spot_twap=False,
        show_perp_twap=False,
        show_spot_step=False,
        show_perp_step=False,
        show_spot_points=False,
        show_perp_points=False,
        zoom=None,
    ):
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
            self.spot_curve,
            self.perp_curve,
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
            self.spot_curve,
            self.perp_curve,
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

    def display_curves(
        self,
        start_date: dt.datetime,
        end_date: dt.datetime,
        use_spot_curve_1: bool,
        use_spot_curve_2: bool,
        spot_curve_1_path: str,
        spot_curve_1_scaling: float,
        spot_curve_1_horizontal_shift: float,
        spot_curve_1_vertical_shift: float,
        spot_curve_2_starting_value: float,
        spot_curve_2_relative_change: float,
        use_perp_curve_1: bool,
        use_perp_curve_2: bool,
        perp_curve_1_path: str,
        perp_curve_1_scaling: float,
        perp_curve_1_horizontal_shift: float,
        perp_curve_1_vertical_shift: float,
        perp_curve_2_starting_value: float,
        perp_curve_2_relative_change: float,
    ):
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
            spot_curve_1 = curves.create_curve_from_file(
                spot_curve_1_path,
                scaling=spot_curve_1_scaling,
                horizontal_shift=spot_curve_1_horizontal_shift,
                vertical_shift=spot_curve_1_vertical_shift,
            )

        if use_perp_curve_1:
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

        self.spot_curve = spot_resulting_curve
        self.perp_curve = perp_resulting_curve

        return plots.plot_curve_difference(
            ax[2], perp_resulting_curve, spot_resulting_curve, start_date, end_date
        )

    def get_spot_curve(self):
        return self.spot_curve

    def get_perp_curve(self):
        return self.perp_curve

    def get_curve_elements(self):
        slider_style = {"description_width": "120px"}

        spot_base_cb = widgets.Checkbox(value=True, description="Spot: use base curve")
        spot_base_path = widgets.Select(
            options=sorted(glob.glob("{}/*".format("./data/")))
        )

        spot_slider_mult = widgets.FloatSlider(
            value=1,
            min=0,
            max=10,
            step=0.1,
            description="base: scaling",
            style=slider_style,
        )
        spot_slider_h_shift = widgets.FloatSlider(
            value=0,
            min=-5e5,
            max=5e5,
            step=0.1,
            description="base: h. shift",
            style=slider_style,
        )
        spot_slider_v_shift = widgets.FloatSlider(
            value=0,
            min=-1e4,
            max=4e4,
            step=0.1,
            description="base: v. shift",
            style=slider_style,
        )

        spot_super_cb = widgets.Checkbox(
            value=True, description="Spot: add curve to base"
        )

        spot_slider_super_value = widgets.FloatSlider(
            value=0,
            min=-1e4,
            max=4e4,
            step=0.1,
            description="initial value",
            style=slider_style,
        )

        spot_slider_super_change = widgets.FloatSlider(
            value=0,
            min=-10,
            max=10,
            step=0.1,
            description="change over period",
            readout_format=".1%",
            style=slider_style,
        )

        spot_column = widgets.VBox(
            [
                spot_base_cb,
                spot_base_path,
                spot_slider_mult,
                spot_slider_h_shift,
                spot_slider_v_shift,
                spot_super_cb,
                spot_slider_super_value,
                spot_slider_super_change,
            ]
        )

        perp_base_cb = widgets.Checkbox(value=True, description="Perps: use base curve")

        perp_base_path = widgets.Select(
            options=sorted(glob.glob("{}/*".format("./data/")))
        )

        perp_slider_mult = widgets.FloatSlider(
            value=1,
            min=0,
            max=10,
            step=0.1,
            description="base: scaling",
            style=slider_style,
        )

        perp_slider_h_shift = widgets.FloatSlider(
            value=0,
            min=-5e5,
            max=5e5,
            step=0.1,
            description="base: h. shift",
            style=slider_style,
        )

        perp_slider_v_shift = widgets.FloatSlider(
            value=0,
            min=-1e4,
            max=1e4,
            step=0.1,
            description="base: v. shift",
            style=slider_style,
        )

        perp_super_cb = widgets.Checkbox(
            value=True, description="Perp: add curve to base"
        )

        perp_slider_super_value = widgets.FloatSlider(
            value=0,
            min=-1e4,
            max=1e4,
            step=0.1,
            description="initial value",
            style=slider_style,
        )

        perp_slider_super_change = widgets.FloatSlider(
            value=0,
            min=-10,
            max=10,
            step=0.1,
            description="change over period",
            readout_format=".1%",
            style=slider_style,
        )

        perp_column = widgets.VBox(
            [
                perp_base_cb,
                perp_base_path,
                perp_slider_mult,
                perp_slider_h_shift,
                perp_slider_v_shift,
                perp_super_cb,
                perp_slider_super_value,
                perp_slider_super_change,
            ]
        )

        controls = widgets.HBox([spot_column, perp_column])

        output = widgets.interactive_output(
            self.display_curves,
            {
                "start_date": widgets.fixed(self.start_date),
                "end_date": widgets.fixed(self.end_date),
                "use_spot_curve_1": spot_base_cb,
                "use_spot_curve_2": spot_super_cb,
                "spot_curve_1_path": spot_base_path,
                "spot_curve_1_scaling": spot_slider_mult,
                "spot_curve_1_horizontal_shift": spot_slider_h_shift,
                "spot_curve_1_vertical_shift": spot_slider_v_shift,
                "spot_curve_2_starting_value": spot_slider_super_value,
                "spot_curve_2_relative_change": spot_slider_super_change,
                "use_perp_curve_1": perp_base_cb,
                "use_perp_curve_2": perp_super_cb,
                "perp_curve_1_path": perp_base_path,
                "perp_curve_1_scaling": perp_slider_mult,
                "perp_curve_1_horizontal_shift": perp_slider_h_shift,
                "perp_curve_1_vertical_shift": perp_slider_v_shift,
                "perp_curve_2_starting_value": perp_slider_super_value,
                "perp_curve_2_relative_change": perp_slider_super_change,
            },
        )

        return controls, output

    def get_funding_elements(self):
        cb1 = widgets.Checkbox(value=True, description="show payment", indent=False)
        cb2 = widgets.Checkbox(value=False, description="show rate", indent=False)
        cb3 = widgets.Checkbox(value=True, description="show spot TWAP", indent=False)
        cb4 = widgets.Checkbox(value=True, description="show perp TWAP", indent=False)
        cb5 = widgets.Checkbox(value=False, description="show spot steps", indent=False)
        cb6 = widgets.Checkbox(value=False, description="show perp steps", indent=False)
        cb7 = widgets.Checkbox(
            value=False, description="show spot points", indent=False
        )
        cb8 = widgets.Checkbox(
            value=False, description="show perp points", indent=False
        )

        slider_layout = widgets.Layout(width="600px", height="40px")

        slider1 = widgets.IntSlider(
            value=1500,
            min=1,
            max=44e3,
            step=1,
            description="funding payment frequency (minutes)",
            style={"description_width": "250px"},
            layout=slider_layout,
        )
        slider2 = widgets.IntSlider(
            value=1500,
            min=1,
            max=44e3,
            step=1,
            description="spot sampling frequency (minutes)",
            style={"description_width": "250px"},
            layout=slider_layout,
        )
        slider3 = widgets.IntSlider(
            value=1500,
            min=1,
            max=44e3,
            step=1,
            description="perp smapling frequency (minutes)",
            style={"description_width": "250px"},
            layout=slider_layout,
        )

        frequency_sliders = widgets.HBox(
            [slider1, slider2, slider3], layout=widgets.Layout(width="90%")
        )
        checkboxes = widgets.HBox(
            [cb1, cb2, cb3, cb4, cb5, cb6, cb7, cb8], layout=widgets.Layout(width="93%")
        )

        box_interest_rate = widgets.FloatText(
            value=0, description="Interest rate:", style={"description_width": "200px"}
        )
        box_lower_bound = widgets.FloatText(
            value=0,
            description="clamp lower bound:",
            style={"description_width": "200px"},
        )
        box_upper_bound = widgets.FloatText(
            value=0,
            description="clamp upper bound:",
            style={"description_width": "200px"},
        )
        clamp_inputs = widgets.HBox(
            [box_interest_rate, box_lower_bound, box_upper_bound]
        )

        zoom_slider = widgets.FloatRangeSlider(
            value=[0, 1],
            min=0,
            max=1,
            step=0.1,
            description="display x-axis portion",
            disabled=False,
            readout_format=".0%",
            style={"description_width": "200px"},
            layout=widgets.Layout(width="50%"),
        )
        controls = widgets.VBox(
            [frequency_sliders, checkboxes, clamp_inputs, zoom_slider]
        )

        output = widgets.interactive_output(
            self.display_funding_periods,
            {
                "start_date": widgets.fixed(self.start_date),
                "end_date": widgets.fixed(self.end_date),
                "funding_schedule_minutes": slider1,
                "spot_sampling_minutes": slider2,
                "perp_sampling_minutes": slider3,
                "interest_rate": box_interest_rate,
                "clamp_lower_bound": box_lower_bound,
                "clamp_upper_bound": box_upper_bound,
                "show_funding_payment": cb1,
                "show_funding_rate": cb2,
                "show_spot_twap": cb3,
                "show_perp_twap": cb4,
                "show_spot_step": cb5,
                "show_perp_step": cb6,
                "show_spot_points": cb7,
                "show_perp_points": cb8,
                "zoom": zoom_slider,
            },
        )

        return controls, output
