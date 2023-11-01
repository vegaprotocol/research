import datetime as dt
import modules.curves as curves
import ipywidgets as widgets
import modules.figures as figs
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
        start_date: dt.datetime,
        end_date: dt.datetime,
        funding_payment_frequency: dt.time,
        spot_sampling_frequency: dt.time,
        perp_sampling_frequency: dt.time,
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
        zoom=None,
    ):
        figs.funding_periods(
            start_date=start_date,
            end_date=end_date,
            spot_curve=self.spot_curve,
            perp_curve=self.perp_curve,
            funding_payment_frequency=dt.datetime.combine(
                dt.date.min, funding_payment_frequency
            )
            - dt.datetime.min,
            spot_sampling_frequency=dt.datetime.combine(
                dt.date.min, spot_sampling_frequency
            )
            - dt.datetime.min,
            perp_sampling_frequency=dt.datetime.combine(
                dt.date.min, perp_sampling_frequency
            )
            - dt.datetime.min,
            interest_rate=interest_rate,
            clamp_lower_bound=clamp_lower_bound,
            clamp_upper_bound=clamp_upper_bound,
            show_funding_payment=show_funding_payment,
            show_funding_rate=show_funding_rate,
            show_spot_twap=show_spot_twap,
            show_perp_twap=show_perp_twap,
            show_spot_step=show_spot_step,
            show_perp_step=show_perp_step,
            show_spot_points=show_spot_points,
            show_perp_points=show_perp_points,
            zoom=zoom,
            show=True,
            plot_save_path=None,
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
        self.spot_curve, self.perp_curve = figs.spot_perp_difference(
            start_date=start_date,
            end_date=end_date,
            use_spot_curve_1=use_spot_curve_1,
            use_spot_curve_2=use_spot_curve_2,
            spot_curve_1_path=spot_curve_1_path,
            spot_curve_1_scaling=spot_curve_1_scaling,
            spot_curve_1_horizontal_shift=spot_curve_1_horizontal_shift,
            spot_curve_1_vertical_shift=spot_curve_1_vertical_shift,
            spot_curve_2_starting_value=spot_curve_2_starting_value,
            spot_curve_2_relative_change=spot_curve_2_relative_change,
            use_perp_curve_1=use_perp_curve_1,
            use_perp_curve_2=use_perp_curve_2,
            perp_curve_1_path=perp_curve_1_path,
            perp_curve_1_scaling=perp_curve_1_scaling,
            perp_curve_1_horizontal_shift=perp_curve_1_horizontal_shift,
            perp_curve_1_vertical_shift=perp_curve_1_vertical_shift,
            perp_curve_2_starting_value=perp_curve_2_starting_value,
            perp_curve_2_relative_change=perp_curve_2_relative_change,
            show=True,
            plot_save_path=None,
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

        dp1 = widgets.TimePicker(
            value=dt.time(hour=8, minute=0, second=0),
            step=1,
            description="funding payment frequency",
            style={"description_width": "250px", "width": 400},
        )

        dp2 = widgets.TimePicker(
            value=dt.time(hour=0, minute=5, second=0),
            step=1,
            description="spot sampling frequency",
            style={"description_width": "250px"},
        )

        dp3 = widgets.TimePicker(
            value=dt.time(hour=8, minute=0, second=30),
            step=1,
            description="perp sampling frequency",
            style={"description_width": "250px"},
        )

        frequency_sliders = widgets.HBox(
            [dp1, dp2, dp3], layout=widgets.Layout(width="90%")
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
                "funding_payment_frequency": dp1,
                "spot_sampling_frequency": dp2,
                "perp_sampling_frequency": dp3,
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
